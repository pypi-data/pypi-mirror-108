# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "18/02/2021"


from collections.abc import Iterable
from typing import Union
from silx.utils.enum import Enum as _Enum
import numpy


class ReconstructionMode(_Enum):
    VERTICAL = "Vertical"
    TILT_CORRECTION = "Tilt correction"


class ScoreMethod(_Enum):
    STD = "standard deviation"
    TV = "total variation"


class SAAxisParams:
    """Parameters for the semi-automatic axis calculation"""

    _VALID_FILE_FORMAT = ("hdf5", "h5", "hdf", "npy", "npz", "tiff", "jp2k")

    def __init__(self):
        self._research_width = 10  # in pixel
        self._estimated_cor = None
        self._n_reconstruction = 20
        self._slice_indexes = "middle"
        self._nabu_params = {}
        self._dry_run = False
        self._mode = ReconstructionMode.VERTICAL
        self._output_dir = None
        self._score_method = ScoreMethod.TV
        self._scores = None
        self._autofcous = None
        "scores. expected cor value as key and a tuple (score, url) as value"
        self._file_format = "hdf5"
        self._image_width = None

    @property
    def research_width(self):
        return self._research_width

    @research_width.setter
    def research_width(self, research_width):
        self._research_width = research_width

    @property
    def autofocus(self):
        return self._autofcous

    @autofocus.setter
    def autofocus(self, autofocus):
        self._autofcous = autofocus

    @property
    def estimated_cor(self):
        return self._estimated_cor

    @estimated_cor.setter
    def estimated_cor(self, estimated_cor):
        self._estimated_cor = estimated_cor

    @property
    def n_reconstruction(self):
        return self._n_reconstruction

    @n_reconstruction.setter
    def n_reconstruction(self, n):
        self._n_reconstruction = n

    @property
    def cors(self) -> Iterable:
        return self.compute_cors(
            estimated_cor=self.estimated_cor,
            research_width=self.research_width,
            n_reconstruction=self.n_reconstruction,
        )

    @property
    def slice_indexes(self) -> Union[None, int]:
        return self._slice_indexes

    @slice_indexes.setter
    def slice_indexes(self, indexes: Union[None, dict]):
        if isinstance(indexes, str):
            if not indexes == "middle":
                raise ValueError("the only valid indexes values is 'middle'")
        elif not isinstance(indexes, (type(None), dict)):
            raise TypeError(
                "index should be an instance of int or None and "
                "not {}".format(type(indexes))
            )
        self._slice_indexes = indexes

    @property
    def nabu_params(self) -> dict:
        return self._nabu_params

    @nabu_params.setter
    def nabu_params(self, params: dict):
        if not isinstance(params, dict):
            raise TypeError(
                "params should be a dictionary and not {}" "".format(type(params))
            )
        self._nabu_params = params

    @property
    def dry_run(self) -> bool:
        return self._dry_run

    @dry_run.setter
    def dry_run(self, dry_run: bool):
        if not isinstance(dry_run, bool):
            raise ValueError("dry_run should be a bool")
        self._dry_run = dry_run

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        mode = ReconstructionMode.from_value(mode)
        self._mode = mode

    @property
    def output_dir(self) -> Union[str, None]:
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir: Union[str, None]) -> None:
        if not isinstance(output_dir, (str, type(None))):
            raise TypeError("output_dir should be None or a str")
        self._output_dir = output_dir

    @property
    def score_method(self):
        return self._score_method

    @score_method.setter
    def score_method(self, method):
        self._score_method = ScoreMethod.from_value(method)

    @property
    def scores(self) -> Union[dict, None]:
        return self._scores

    @scores.setter
    def scores(self, scores: Union[None, dict]):
        if not isinstance(scores, (type(None), dict)):
            raise TypeError("scores should be None or a dictionary")
        self._scores = scores

    @property
    def image_width(self) -> Union[None, float]:
        return self._image_width

    @image_width.setter
    def image_width(self, width):
        if not isinstance(width, (type(None), float, int)):
            raise TypeError("None, int or float expected. Not {}".format(type(width)))
        else:
            self._image_width = width

    @property
    def file_format(self) -> str:
        return self._file_format

    @file_format.setter
    def file_format(self, format_: str):
        if not isinstance(format_, str):
            raise TypeError("format should be a str")
        if not format_ in self._VALID_FILE_FORMAT:
            raise ValueError(
                "requested format ({}) is invalid. valid ones "
                "are {}".format(format_, self._VALID_FILE_FORMAT)
            )
        self._file_format = format_

    def to_dict(self):
        return {
            "estimated_cor": self.estimated_cor,
            "research_width": self.research_width,
            "n_reconstruction": self.n_reconstruction,
            "slice_indexes": self.slice_indexes or "",
            "nabu_params": self.nabu_params,
            "dry_run": self.dry_run,
            "mode": self.mode.value,
            "output_dir": self.output_dir or "",
            "score_method": self.score_method.value,
        }

    def load_from_dict(self, dict_: dict):
        if not isinstance(dict_, dict):
            raise TypeError("dict_ should be an instance of dict")
        if "research_width" in dict_:
            self.research_width = dict_["research_width"]
        if "estimated_cor" in dict_:
            self.estimated_cor = dict_["estimated_cor"]
        if "n_reconstruction" in dict_:
            self.n_reconstruction = dict_["n_reconstruction"]
        if "slice_indexes" in dict_:
            slice_index = dict_["slice_indexes"]
            if slice_index == "":
                slice_index = None
            self.slice_indexes = slice_index
        if "nabu_params" in dict_:
            self.nabu_params = dict_["nabu_params"]
        if "dry_run" in dict_:
            self.dry_run = bool(dict_["dry_run"])
        if "mode" in dict_:
            self.mode = ReconstructionMode.from_value(dict_["mode"])
        if "output_dir" in dict_:
            output_dir = dict_["output_dir"]
            if output_dir == "":
                output_dir = None
            self.output_dir = output_dir
        if "score_method" in dict_:
            self.score_method = ScoreMethod.from_value(dict_["score_method"])

    @staticmethod
    def from_dict(dict_):
        params = SAAxisParams()
        params.load_from_dict(dict_=dict_)
        return params

    def check_configuration(self):
        """
        Insure all requested information for processing the SAAXis are here.
        :raises: ValueError if some information are missing
        """
        missing_information = []
        if self.cors is None or len(self.cors) == 0:
            missing_information.append("no values for center of rotation provided")
        if self.slice_indexes is None:
            missing_information.append("slice index not provided")
        if len(missing_information) > 0:
            raise ValueError(
                str(
                    "Some informations are missing: {}".format(
                        " ; ".join(missing_information)
                    )
                )
            )

    @staticmethod
    def compute_cors(estimated_cor, research_width, n_reconstruction):
        if estimated_cor is None:
            raise ValueError("No estimated cor provided")
        if estimated_cor == "middle":
            estimated_cor = 0
        if n_reconstruction % 2 == 0:
            n_reconstruction = n_reconstruction + 1
            # insure we have an odd number of cor to insure the estimated
            # one is reconstructed
        return numpy.linspace(
            start=estimated_cor - research_width / 2.0,
            stop=estimated_cor + research_width / 2.0,
            num=n_reconstruction,
        )
