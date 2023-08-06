#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from silx.gui import qt
import signal
from typing import Union
from tomwer.gui import icons
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomwer.gui.reconstruction.saaxis.saaxis import SAAxisWindow as _SAAxisWindow
from tomwer.core.process.reconstruction.axis.axis import AxisProcess, NoAxisUrl
from tomwer.core.process.reconstruction.saaxis.saaxis import SAAxisProcess
from tomwer.synctools.axis import QAxisRP
from tomwer.synctools.saaxis import QSAAxisParams
import logging
import time


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


class SAAxisThread(qt.QThread):
    """
    Thread to call nabu and reconstruct one slice with several cor value
    """

    def init(self, scan, configuration):
        self.scan = scan
        self._configuration = configuration

    def run(self) -> None:
        process = SAAxisProcess(process_id=None)
        process.set_properties(self._configuration)
        t0 = time.time()
        process.process(self.scan)
        print("execution time is {}".format(time.time() - t0))


class SAAxisWindow(_SAAxisWindow):
    def __init__(self, parent=None):
        self._scan = None
        super().__init__(parent)
        # thread for computing cors
        self._processingThread = SAAxisThread()
        self._processingThread.finished.connect(self._threadedProcessEnded)
        self.sigStartSinogramLoad.connect(self._callbackStartLoadSinogram)
        self.sigEndSinogramLoad.connect(self._callbackEndLoadSinogram)
        # processing for the cor estimation
        self._cor_estimation_process = AxisProcess(self.getQAxisRP())

        # hide the validate button
        self._saaxisControl._applyBut.hide()
        self.hideAutoFocusButton()

    def _launchReconstructions(self):
        if self._processingThread.isRunning():
            _logger.error(
                "a calculation is already launch. You must wait for "
                "it to end prior to launch a new one"
            )
        else:
            qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
            self._processingThread.init(
                configuration=self.getConfiguration(), scan=self.getScan()
            )
            self._processingThread.start()

    def _threadedProcessEnded(self):
        saaxis_params = self._processingThread.scan.saaxis_params
        if saaxis_params is None:
            scores = None
        else:
            scores = saaxis_params.scores
        scan = self.getScan()
        assert scan is not None, "scan should have been set"
        self.setCorScores(
            scores, img_width=scan.dim_1, score_method=self.getScoreMethod()
        )
        if scan.saaxis_params.autofocus is not None:
            self.setCurrentCorValue(scan.saaxis_params.autofocus)
        self.showResults()
        qt.QApplication.restoreOverrideCursor()

    def _callbackStartLoadSinogram(self):
        print(
            "start loading sinogram for {}. Can take some time".format(self.getScan())
        )

    def _callbackEndLoadSinogram(self):
        print("sinogram loaded for {} loaded.".format(self.getScan()))

    def close(self) -> None:
        self._stopProcessingThread()
        super().close()

    def _stopProcessingThread(self):
        if self._processingThread:
            self._processingThread.terminate()
            self._processingThread.wait(500)
            self._processingThread = None

    def stop(self):
        self._stopProcessingThread()
        super().stop()

    def _computeEstimatedCor(self) -> Union[float, None]:
        scan = self.getScan()
        if scan is None:
            return
        _logger.info("{} - start cor estimation for".format(scan))
        qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
        try:
            self._cor_estimation_process.compute(scan=scan, wait=True)
        except NoAxisUrl:
            qt.QApplication.restoreOverrideCursor()
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Warning)
            text = (
                "Unable to find url to compute the axis, please select them "
                "from the `axis input` tab"
            )
            msg.setText(text)
            msg.exec_()
            return None
        else:
            self.setEstimatedCorPosition(
                value=scan.axis_params.relative_cor_value,
            )
            qt.QApplication.restoreOverrideCursor()
            self.getAutomaticCorWindow().hide()
            return scan.axis_params.relative_cor_value


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "scan_path",
        help="For EDF acquisition: provide folder path, for HDF5 / nexus"
        "provide the master file",
        default=None,
    )
    parser.add_argument(
        "--entry", help="For Nexus files: entry in the master file", default=None
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Set logging system in debug mode",
    )

    options = parser.parse_args(argv[1:])

    if options.debug:
        logging.root.setLevel(logging.DEBUG)

    global app  # QApplication must be global to avoid seg fault on quit
    app = qt.QApplication.instance() or qt.QApplication([])
    splash = getMainSplashScreen()
    qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
    qt.QApplication.processEvents()

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler

    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    if options.scan_path is not None:
        if os.path.isdir(options.scan_path):
            options.scan_path = options.scan_path.rstrip(os.path.sep)
            scan = ScanFactory.create_scan_object(scan_path=options.scan_path)
        else:
            if not os.path.isfile(options.scan_path):
                raise ValueError(
                    "scan path should be a folder containing an"
                    " EDF acquisition or an hdf5 - nexus "
                    "compliant file"
                )
            if options.entry is None:
                raise ValueError("entry in the master file should be specify")
            scan = HDF5TomoScan(scan=options.scan_path, entry=options.entry)
    else:
        scan = ScanFactory.mock_scan()
    # define the process_index is any tomwer_processes_existing
    if options.debug:
        _logger.setLevel(logging.DEBUG)

    window = SAAxisWindow()
    # window.setAttribute(qt.Qt.WA_DeleteOnClose)
    window.setWindowTitle("saaxis")
    window.setWindowIcon(icons.getQIcon("tomwer"))
    if scan.axis_params is None:
        scan.axis_params = QAxisRP()
    if scan.saaxis_params is None:
        scan.saaxis_params = QSAAxisParams()
    window.setScan(scan)
    splash.finish(window)
    window.show()
    qt.QApplication.restoreOverrideCursor()
    app.aboutToQuit.connect(window.stop)
    app.exec_()


def getinputinfo():
    return "tomwer saaxis [scanDir]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.quit()


if __name__ == "__main__":
    main(sys.argv)
