# coding: utf-8
###########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################

"""contain the SAAxisProcess. Half automatic center of rotation calculation
"""

__authors__ = [
    "H.Payno",
]
__license__ = "MIT"
__date__ = "10/02/2021"


from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.process.reconstruction.nabu.nabuslices import (
    interpret_tomwer_configuration,
    _get_file_basename_reconstruction,
    generate_nabu_configfile,
)
from typing import Iterable
from tomwer.core.scan.edfscan import EDFTomoScan
from ..nabu import utils
from ..nabu import settings as nabu_settings
from .params import ScoreMethod
from .params import ReconstructionMode
from .params import SAAxisParams
from tomwer.core.process.baseprocess import SingleProcess, _input_desc, _output_desc
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils import logconfig
from tomwer.core.process.reconstruction.nabu.utils import check_sinogram_half
from processview.core.manager import ProcessManager, DatasetState
from processview.core.superviseprocess import SuperviseProcess
from tomwer.core.process.baseprocess import BaseProcess
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomoscan.io import HDF5File
from silx.io.utils import get_data
import tomwer.version
import numpy
import subprocess
from tomwer.io.utils import format_stderr_stdout
from tomwer.core.progress import Progress
from tomwer.core.process.reconstruction.axis import AxisRP
from typing import Union
import os
import logging
import copy
import h5py
import sys

try:
    from nabu.app.local_reconstruction import LocalReconstruction
except ImportError as e:
    has_nabu = False
else:
    has_nabu = True


_logger = logging.getLogger(__name__)


DEFAULT_RECONS_FOLDER = "saaxis_results"


class _ComputedScore:
    def __init__(self, tv, std):
        self._tv = tv
        self._std = std

    @property
    def total_variation(self):
        return self._tv

    @property
    def std(self):
        return self._std

    def get(self, method: ScoreMethod):
        method = ScoreMethod.from_value(method)
        if method is ScoreMethod.TV:
            return self.total_variation
        elif method is ScoreMethod.STD:
            return self.std
        else:
            raise ValueError("{} is an unrecognized method".format(method))


def compute_score_contrast_std(data: numpy.ndarray):
    """
    Compute a contrast score by simply computing the standard deviation of
    the frame
    :param numpy.ndarray data: frame for which we should compute the score
    :return: score of the frame
    :rtype: float
    """
    if data is None:
        return None
    elif data.ndim != 2:
        raise ValueError("Data is expected to be 2D. Not {}".format(data.ndim))
    else:
        return data.std() * 100


def compute_tv_score(data: numpy.ndarray):
    """
    Compute the data score as image total variation

    :param numpy.ndarray data: frame for which we should compute the score
                                Handle
    :return: score of the frame
    :rtype: float
    """
    if data is None:
        return None
    elif data.ndim != 2:
        raise ValueError("Data is expected to be 2D. Not {}".format(data.ndim))
    else:
        # handle mask if data is a numpy.ma.array gradient might set "--"
        tv = numpy.sum(
            numpy.sqrt(
                numpy.gradient(data, axis=0) ** 2 + numpy.gradient(data, axis=1) ** 2
            )
        )
        if tv > 0:
            # adapt score to:
            #    - get growing score: the higher the score is the better the cor is.
            #      this is the 1 / tv part
            #    - look more "friendly" (10e5 part)
            return (1.0 / tv) * float(10e5)
        else:
            return tv


_METHOD_TO_FCT = {
    ScoreMethod.STD: compute_score_contrast_std,
    ScoreMethod.TV: compute_tv_score,
}


def compute_score(data: numpy.ndarray, method: ScoreMethod) -> float:
    """

    :param numpy.ndarray data: frame for which we should compute the score
    :param str method:
    :return: score of the frame
    :rtype: float
    """
    if not data.ndim == 2:
        raise ValueError("Data is expected to be 2D. Not {}".format(data.ndim))
    method = ScoreMethod.from_value(method)
    fct = _METHOD_TO_FCT.get(method, None)
    if fct is not None:
        return fct(data)
    else:
        raise ValueError("{} is not handled".format(method))


def one_slice_several_cor(scan, configuration: Union[dict, SAAxisParams]) -> tuple:
    """
    Run a slice reconstruction using nabu per Center Of Rotation (cor) provided
    Then for each compute a score (quality) of the center of rotation

    :param TomwerScanBase scan:
    :param dict configuration:
    :return: cor_reconstructions, outs, errs
             cor_reconstructions is a dictionary of cor as key and a tuple
             (url, score) as value
    :rtype: tuple
    """
    if isinstance(configuration, dict):
        configuration = SAAxisParams.from_dict(configuration)
    elif not isinstance(configuration, SAAxisParams):
        raise TypeError(
            "configuration should be a dictionary or an instance of SAAxisParams"
        )
    check_sinogram_half(scan)

    configuration.check_configuration()
    mode = ReconstructionMode.from_value(configuration.mode)
    slice_index = configuration.slice_indexes
    cors = configuration.cors
    nabu_config = configuration.nabu_params
    output_dir = configuration.output_dir
    dry_run = configuration.dry_run
    nabu_output_config = nabu_config.get("output", {})
    file_format = nabu_output_config.get("file_format", "hdf5")
    _logger.info(
        "launch reconstruction of slice {} and cors {}".format(slice_index, cors)
    )
    if mode is ReconstructionMode.VERTICAL:
        if isinstance(slice_index, str):
            if not slice_index == "middle":
                raise ValueError("slice index {} not recognized".format(slice_index))
        elif not len(slice_index) == 1:
            raise ValueError("{} mode only manage one slice".format(mode.value))
        else:
            slice_index = list(slice_index.values())[0]
        advancement = Progress("saaxis - slice {} of {}".format(slice_index, scan))

        _, cor_reconstructions, outs, errs = run_slice_reconstruction(
            scan=scan,
            slice_index=slice_index,
            cor_positions=cors,
            config=nabu_config,
            output_dir=output_dir,
            dry_run=dry_run,
            file_format=file_format,
            advancement=advancement,
        )
    else:
        raise ValueError("{} is not handled for now".format(mode))
    scores = {}

    def load_datasets():
        datasets_ = {}
        for cor, urls in cor_reconstructions.items():
            for url in urls:
                try:
                    data = get_data(url=url)
                except Exception as e:
                    _logger.error(
                        "Fail to compute a score for {}. Reason is {}"
                        "".format(url.path(), str(e))
                    )
                    datasets_[cor] = (url, None)
                else:
                    if data.ndim == 3:
                        if data.shape[0] == 1:
                            data = data.reshape(data.shape[1], data.shape[2])
                        elif data.shape[2] == 1:
                            data = data.reshape(data.shape[0], data.shape[1])
                        else:
                            raise ValueError(
                                "Data is expected to be 2D. Not {}".format(data.ndim)
                            )
                    elif data.ndim == 2:
                        pass
                    else:
                        raise ValueError(
                            "Data is expected to be 2D. Not {}".format(data.ndim)
                        )

                    datasets_[cor] = (url, data)
        return datasets_

    datasets = load_datasets()

    def get_disk_mask_radius(datasets_) -> int:
        """compute the radius to use for the mask"""
        radius = sys.maxsize
        # get min radius
        for cor, (url, data) in datasets_.items():
            assert data.ndim is 2, "data is expected to be 2D"
            min_ = numpy.array(data.shape).min()
            if radius >= min_:
                radius = min_
        return radius // 2

    def apply_roi(data, radius, url) -> numpy.array:
        """compute the square included in the circle of radius and centered
        in the middle of the data"""
        half_width = int(radius / 2 ** 0.5)
        center = numpy.array(data.shape[:]) // 2
        min_x, max_x = center[0] - half_width, center[0] + half_width
        min_y, max_y = center[1] - half_width, center[1] + half_width
        try:
            return data[min_y:max_y, min_x:max_x]
        except Exception:
            _logger.error(
                "Fail to apply roi for {}. Take the entire dataset".format(url.path())
            )
            return data

    mask_disk_radius = get_disk_mask_radius(datasets)
    for cor, (url, data) in datasets.items():
        if data is None:
            score = None
        else:
            assert data.ndim == 2
            data_roi = apply_roi(data=data, radius=mask_disk_radius, url=url)
            score = _ComputedScore(
                tv=compute_score(data=data_roi, method=ScoreMethod.TV),
                std=compute_score(data=data_roi, method=ScoreMethod.STD),
            )
        scores[cor] = (url, score)

    return scores, outs, errs


def run_slice_reconstruction(
    scan: TomwerScanBase,
    cor_positions: Iterable,
    slice_index: int,
    config: dict,
    output_dir=None,
    dry_run: bool = False,
    local: bool = True,
    file_format: str = "hdf5",
    advancement=None,
) -> tuple:
    """
    call nabu for a reconstruction on scan with the given configuration

    :param TomwerScanBase scan: scan to reconstruct
    :param tuple: cor_positions cor position to used for reconstruction
    :param dict config: configuration to run the reconstruction
    :param Union[None,str]: output dir folder. If None then this will be store
                            under the acquisition folder/saaxis_results
    :param bool dry_run: do we want to run dry
    :param bool local: do we want to run a local reconstruction
    :param advancement: optional Progress class to display advancement

    :return: success, recons_urls, outs, errs
             recons_urls is a dict with cor value as key (float) and reconstructed slice url
             as value
    :rtype: dict
    """
    nabu_configurations = interpret_tomwer_configuration(config, scan=None)
    if len(nabu_configurations) == 0:
        raise RuntimeWarning(
            "Unable to get a valid nabu configuration for " "reconstruction."
        )
    elif len(nabu_configurations) > 1:
        _logger.warning(
            "Several configuration found for nabu (you probably "
            "ask for several delta/beta value or several slices). "
            "Picking the first one."
        )
    if output_dir is None:
        output_dir = os.path.join(scan.path, DEFAULT_RECONS_FOLDER)
    if scan.process_file is not None:
        steps_file_basename, _ = os.path.splitext(scan.process_file)
        steps_file_basename = "_".join(
            ("steps_file_basename", "nabu", "sinogram", "save", "step")
        )
        steps_file_basename = steps_file_basename + ".hdf5"
        steps_file = os.path.join(output_dir, steps_file_basename)
    else:
        steps_file = ""

    configs = {}

    for i_cor, cor in enumerate(cor_positions):
        nabu_configuration = copy.deepcopy(nabu_configurations[0][0])
        nabu_configuration["pipeline"] = {
            "save_steps": "sinogram" if i_cor == 0 else "",
            "resume_from_step": "sinogram",
            "steps_file": steps_file,
        }
        # convert cor from tomwer ref to nabu ref
        if scan.dim_1 is not None:
            cor_nabu_ref = cor + scan.dim_1 // 2
        else:
            _logger.warning("enable to get image half width. Set it to 1024")
            cor_nabu_ref = cor + 1024
        # handle reconstruction section
        if "reconstruction" not in nabu_configuration:
            nabu_configuration["reconstruction"] = {}
        nabu_configuration["reconstruction"]["rotation_axis_position"] = str(
            cor_nabu_ref
        )
        # handle output section
        if "output" not in nabu_configuration:
            nabu_configuration["output"] = {}
        nabu_configuration["output"]["location"] = output_dir
        nabu_configuration["output"]["file_format"] = file_format
        # handle resources section
        if local is True:
            resources_method = "local"
        else:
            resources_method = "slurm"
        nabu_configuration["resources"] = utils.get_nabu_resources_desc(
            scan=scan, workers=1, method=resources_method
        )
        configs[cor] = nabu_configuration
    return run_nabu_one_slice_several_config(
        nabu_configs=configs,
        scan=scan,
        local=local,
        slice_index=slice_index,
        dry_run=dry_run,
        file_format=file_format,
        advancement=advancement,
    )


def run_nabu_one_slice_several_config(
    scan,
    nabu_configs,
    dry_run,
    slice_index: Union[int, str],
    local,
    file_format,
    advancement=None,
) -> tuple:
    """
    # TODO: might need something like a context or an option "keep" slice in memory

    :param scan:
    :param nabu_configs: list of nabu configurations to be run
    :param dry_run:
    :param int slice_index: slice index to reconstruct or "middle"
    :param local:
    :param advancement: optional Progress class to display advancement
    :return: tuple with (success, recons_urls (list of output urls),
             tuple of outs, tuples of errs)
    """
    if slice_index == "middle":
        if scan.dim_2 is not None:
            slice_index = scan.dim_2 // 2
        else:
            _logger.warning(
                "scan.dim_2 returns None, unable to deduce middle " "pick 1024"
            )
            slice_index = 1024
    assert isinstance(slice_index, int), "slice_index should be an int"

    def preprocess_config(config, cor: float):
        dataset_params = scan.get_nabu_dataset_info()
        if "dataset" in config:
            dataset_params.update(config["dataset"])
        config["dataset"] = dataset_params

        if local is True:
            resources_method = "local"
        else:
            resources_method = "slurm"
        config["resources"] = utils.get_nabu_resources_desc(
            scan=scan, workers=1, method=resources_method
        )
        # force overwrite results
        if "output" not in config:
            config["output"] = {}
        config["output"].update({"overwrite_results": 1})

        def treateOutputConfig(_config):
            """
            - add or overwrite some parameters of the dictionary
            - create the output directory if does not exist
            """
            pag = False
            db = None
            if "phase" in _config:
                if "method" in _config["phase"] and _config["phase"]["method"] != "":
                    pag = True
                    if "delta_beta" in _config["phase"]:
                        db = round(float(_config["phase"]["delta_beta"]))
            if "output" in config:
                _file_name = _get_file_basename_reconstruction(
                    scan=scan, slice_index=slice_index, pag=pag, db=db
                )
                _config["output"]["file_prefix"] = "cor_{}_{}".format(_file_name, cor)
                if _config["output"]["location"] not in ("", None):
                    # if user specify the location
                    if not os.path.isdir(_config["output"]["location"]):
                        os.makedirs(_config["output"]["location"])
                else:
                    # otherwise default location will be the data root level
                    _config["output"]["location"] = os.sep.join(
                        scan.path, "saaxis_results"
                    )
            if "reconstruction" not in _config:
                _config["reconstruction"] = {}
            _config["reconstruction"]["start_z"] = slice_index
            _config["reconstruction"]["end_z"] = slice_index
            return _config

        config = treateOutputConfig(config)
        # the policy is to save nabu .cfg file at the same location as the
        # force overwrite results

        cfg_folder = os.path.join(
            config["output"]["location"],
            nabu_settings.NABU_CFG_FILE_FOLDER,
        )
        if not os.path.exists(cfg_folder):
            os.makedirs(cfg_folder)

        name = (
            config["output"]["file_prefix"] + nabu_settings.NABU_CONFIG_FILE_EXTENSION
        )
        if not isinstance(scan, EDFTomoScan):
            name = "_".join((scan.entry, name))
        conf_file = os.path.join(cfg_folder, "cor_{}_{}".format(cor, name))
        return config, conf_file

    recons_urls = {}
    outs = []
    errs = []
    if advancement:
        advancement.setMaxAdvancement(len(nabu_configs))
    # TODO: add logger and extra options
    for cor, config in nabu_configs.items():
        config, conf_file = preprocess_config(config, cor)
        # add some tomwer metadata and save the configuration
        # note: for now the section is ignored by nabu but shouldn't stay that way
        with utils.TomwerInfo(config) as config_to_dump:
            generate_nabu_configfile(
                fname=conf_file, config=config_to_dump, options_level="advanced"
            )
        if dry_run:
            continue

        if slice_index is not None and dry_run is False and local:
            if not has_nabu:
                raise ImportError("Fail to import nabu")
            _logger.info(
                "run nabu slice reconstruction for %s with %s" "" % (scan.path, config)
            )

            # need to be executed in his own context
            command = " ".join(
                ("python", "-m", "nabu.resources.cli.reconstruct", conf_file)
            )
            _logger.info('call nabu from "{}"'.format(command))

            process = subprocess.Popen(
                command,
                shell=True,
                cwd=scan.path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            out, err = process.communicate()
            out_str = format_stderr_stdout(out, err)
            outs.append(out)
            errs.append(err)

        urls = utils.get_recons_urls(
            file_prefix=config_to_dump["output"]["file_prefix"],
            location=config_to_dump["output"]["location"],
            slice_index=None,
            scan=scan,
            file_format=file_format,
            start_z=None,
            end_z=None,
        )
        # specific treatment for cor: rename output files
        recons_urls[cor] = urls
        if advancement:
            advancement.increaseAdvancement(1)
    return (
        len(recons_urls) > 0,
        recons_urls,
        tuple(outs),
        tuple(errs),
    )


class SAAxisProcess(SingleProcess, SuperviseProcess):
    """
    Main process to launch several reconstruction of a single slice with
    several Center Of Rotation (cor) values
    """

    inputs = [
        _input_desc(
            name="data", type=TomwerScanBase, handler="pathReceived", doc="scan path"
        ),
    ]
    outputs = [_output_desc(name="data", type=TomwerScanBase, doc="scan path")]

    def __init__(self, process_id=None, dump_process=True):
        SingleProcess.__init__(self)
        SuperviseProcess.__init__(self, process_id=process_id)
        self._dry_run = False
        self._dump_process = dump_process
        self._std_outs = tuple()
        self._std_errs = tuple()

    @property
    def std_outs(self):
        return self._std_outs

    @property
    def std_errs(self):
        return self._std_errs

    def set_dry_run(self, dry_run):
        self._dry_run = dry_run

    @property
    def dry_run(self):
        return self._dry_run

    def set_configuration(self, configuration: dict) -> None:
        return self.set_properties(configuration)

    def set_properties(self, properties):
        if isinstance(properties, SAAxisParams):
            self._settings = properties.to_dict()
        elif isinstance(properties, dict):
            self._settings = properties
        else:
            raise TypeError(
                "properties should be an instance of dict or " "SAAxisParams"
            )

    @staticmethod
    def autofocus(scan):
        scores = scan.saaxis_params.scores
        score_method = scan.saaxis_params.score_method
        best_cor, best_score = None, 0
        for cor, (_, score_cls) in scores.items():
            score = score_cls.get(score_method)
            if score > best_score:
                best_cor, best_score = cor, score
        scan.saaxis_params.autofocus = best_cor
        if scan.axis_params is None:
            scan.axis_params = AxisRP()
        scan.axis_params.frame_width = scan.dim_1
        scan.axis_params.set_relative_value(best_cor)

    def process(self, scan=None):
        if scan is None:
            return None
        if isinstance(scan, TomwerScanBase):
            scan = scan
        elif isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            raise ValueError(
                "input type of {}: {} is not managed" "".format(scan, type(scan))
            )
        # TODO: look and update if there is some nabu reconstruction
        # or axis information to be used back
        configuration = self.get_configuration()
        params = SAAxisParams.from_dict(configuration)
        # insure output dir is created
        if params.output_dir in (None, ""):
            params.output_dir = os.path.join(scan.path, "saaxis_results")
            if not os.path.exists(params.output_dir):
                os.makedirs(params.output_dir)
        # try to find an estimated cor
        #  from a previously computed cor
        if params.estimated_cor is None and scan.axis_params is not None:
            relative_cor = scan.axis_params.relative_cor_value
            if relative_cor is not None and numpy.issubdtype(
                type(relative_cor), numpy.number
            ):
                params.estimated_cor = relative_cor
                _logger.info(
                    "{}: set estimated cor from previously computed cor ({})".format(
                        str(scan), params.estimated_cor
                    )
                )
        #  from scan.estimated_cor_position
        if params.estimated_cor is None and scan.estimated_cor_frm_motor is not None:
            params.estimated_cor = scan.estimated_cor_frm_motor
            _logger.info(
                "{}: set estimated cor from motor position ({})".format(
                    str(scan), params.estimated_cor
                )
            )
        if scan.dim_1 is not None:
            params.image_width = scan.dim_1
        scan.saaxis_params = params
        cors_res, self._std_outs, self._std_errs = one_slice_several_cor(
            scan=scan,
            configuration=self.get_configuration(),
        )
        scan.saaxis_params.scores = cors_res
        self.autofocus(scan=scan)
        self._process_end(scan=scan, cors_res=cors_res)
        return scan

    def _process_end(self, scan, cors_res):
        assert isinstance(scan, TomwerScanBase)
        try:
            extra = {
                logconfig.DOC_TITLE: self._scheme_title,
                logconfig.SCAN_ID: str(scan),
            }
            slice_index = self.get_configuration().get("slice_index", None)

            if cors_res is None:
                info = "fail to compute cor scores of slice {} for scan {}." "".format(
                    slice_index, scan
                )
                _logger.processFailed(info, extra=extra)
                ProcessManager().notify_dataset_state(
                    dataset=scan, process=self, state=DatasetState.FAILED, details=info
                )
            else:
                info = "cor scores of slice {} for scan {} computed." "".format(
                    slice_index, scan
                )
                _logger.processSucceed(info, extra=extra)
                ProcessManager().notify_dataset_state(
                    dataset=scan,
                    process=self,
                    state=DatasetState.WAIT_USER_VALIDATION,
                    details=info,
                )
        except Exception as e:
            _logger.error(e)
        else:
            if self._dump_process:
                SAAxisProcess.process_to_tomwer_processes(
                    scan=scan,
                )

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        return "semi-automatic axis"

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        return tomwer.version.version

    @staticmethod
    def definition():
        """definition of the process"""
        return "Semi automatic center of rotation / axis calculation"

    @staticmethod
    def process_to_tomwer_processes(scan):
        if scan.process_file is not None:
            entry = "entry"
            if isinstance(scan, HDF5TomoScan):
                entry = scan.entry

            cor = None
            if hasattr(scan, "axis_params"):
                cor = scan.axis_params.relative_cor_value

            process_index = scan.pop_process_index()
            with scan.acquire_process_file_lock():
                BaseProcess._register_process(
                    process_file=scan.process_file,
                    entry=entry,
                    results={"center_of_rotation": cor if cor is not None else "-"},
                    configuration=scan.saaxis_params.to_dict(),
                    process_index=process_index,
                    overwrite=True,
                    process=SAAxisProcess,
                )
                SAAxisProcess._extends_results(
                    scan=scan, entry=entry, process_index=process_index
                )

    @staticmethod
    def _extends_results(scan, entry, process_index):
        process_file = scan.process_file
        process_name = "tomwer_process_" + str(process_index)

        def get_process_path():
            return "/".join((entry or "entry", process_name))

        # save it to the file
        with BaseProcess._get_lock(process_file):
            # needs an extra lock for multiprocessing

            with HDF5File(process_file, mode="a") as h5f:
                nx_process = h5f.require_group(get_process_path())
                if "NX_class" not in nx_process.attrs:
                    nx_process.attrs["NX_class"] = "NXprocess"

                results = nx_process.require_group("results")
                for cor, (url, score) in scan.saaxis_params.scores.items():
                    results_cor = results.require_group(str(cor))
                    for method in ScoreMethod:
                        results_cor[method.value] = score.get(method)

                    link_path = os.path.relpath(
                        url.file_path(),
                        os.path.dirname(process_file),
                    )
                    results_cor["reconstructed_slice"] = h5py.ExternalLink(
                        link_path, url.data_path()
                    )
