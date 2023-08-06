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
"""
contains gui to select a slice in a volume
"""


__authors__ = [
    "H. Payno",
]

__license__ = "MIT"
__date__ = "25/02/2021"


from silx.gui import qt
from silx.gui.plot import PlotWidget
from tomwer.gui.reconstruction.saaxis.dimensionwidget import DimensionWidget
from tomwer.gui.visualization.dataviewer import ImageStack
from tomwer.gui.utils.vignettes import VignettesQDialog
from contextlib import AbstractContextManager
from tomwer.gui.utils.buttons import PadlockButton
from tomwer.core.process.reconstruction.saaxis import SAAxisProcess
from tomwer.gui import icons
from tomwer.io.utils.h5pyutils import DatasetReader
from tomwer.core.process.reconstruction.saaxis.params import ScoreMethod
from typing import Union
import weakref
import numpy
import logging

_logger = logging.getLogger(__name__)


class _CorScorePlot(PlotWidget):

    sigMouseWheelActive = qt.Signal(object)

    MARKER_COLOR = "#ff292199"

    def __init__(self, parent):
        PlotWidget.__init__(self, parent)
        self._scores = {}
        self.setAxesDisplayed(False)
        self.setMaximumHeight(150)
        self.setMinimumHeight(100)
        # cor marker
        self.addXMarker(
            x=100, legend="cor", text="cor", draggable=False, color=self.MARKER_COLOR
        )
        self.corMarker = self._getMarker("cor")
        self.corMarker.setLineWidth(3)
        # Retrieve PlotWidget's plot area widget
        plotArea = self.getWidgetHandle()
        # Set plot area custom context menu
        plotArea.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        plotArea.customContextMenuRequested.connect(self._contextMenu)
        self.setInteractiveMode("select", zoomOnWheel=False)
        self.setPanWithArrowKeys(False)

    def clear(self):
        super().clear()
        # cor marker
        self.addXMarker(
            x=100, legend="cor", text="cor", draggable=False, color=self.MARKER_COLOR
        )
        self.corMarker = self._getMarker("cor")

    def wheelEvent(self, event):
        self.sigMouseWheelActive.emit(event)

    def onMouseWheel(self, xPixel, yPixel, angleInDegrees):
        pass

    def _contextMenu(self, pos):
        """Handle plot area customContextMenuRequested signal.

        :param QPoint pos: Mouse position relative to plot area
        """
        # avoir reset zoom
        pass


class _CorSelection(qt.QWidget):
    """Widget to select which cor to select"""

    sigSelectionModeChanged = qt.Signal()
    """Signal emitted when selection mode changed"""
    sigAutoFocusLocked = qt.Signal()
    sigAutoFocusUnLocked = qt.Signal()

    sigCorValueSelected = qt.Signal(float)
    """signal emitted when the cor value is selected by the user from
    vignettes"""

    sigScoreMethodChanged = qt.Signal()
    """Signal meit when the score method (std, tv) change"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self._scores = {}
        self._img_width = None
        self._scan = None
        self.setLayout(qt.QGridLayout())
        # score method
        self._scoreMethodLabel = qt.QLabel("score method", self)
        self.layout().addWidget(self._scoreMethodLabel, 0, 0, 1, 1)
        self._scoreMethodCB = qt.QComboBox(self)
        self.layout().addWidget(self._scoreMethodCB, 0, 1, 1, 1)
        for method in ScoreMethod:
            self._scoreMethodCB.addItem(method.value)
        # left spacer
        lspacer = qt.QWidget(self)
        lspacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(lspacer, 0, 2, 2, 1)
        # cor value
        self._currentCorValue = qt.QGroupBox(self)
        self._currentCorValue.setTitle("current cor position")
        self._currentCorValue.setLayout(qt.QFormLayout())
        self.layout().addWidget(self._currentCorValue, 0, 3, 3, 2)
        self._relativeCorValueLE = qt.QLineEdit(self)
        self._relativeCorValueLE.setReadOnly(True)
        self._currentCorValue.layout().addRow("relative:", self._relativeCorValueLE)
        self._absoluteCorValueLE = qt.QLineEdit(self)
        self._absoluteCorValueLE.setReadOnly(True)
        self._currentCorValue.layout().addRow(
            "absolute:",
            self._absoluteCorValueLE,
        )
        # cor selection option
        self._currentcorRB = qt.QRadioButton("current value", self)
        self.layout().addWidget(self._currentcorRB, 0, 5, 1, 1)
        self._autofocusRB = qt.QRadioButton("autofocus", self)
        self._autofocusRB.setToolTip("Take the cor with the best score")
        self.layout().addWidget(self._autofocusRB, 1, 5, 1, 1)
        # lock autofocus button
        self._lockAutofocusButton = PadlockButton(self)
        self._lockAutofocusButton.setToolTip(
            "If autofocus is locked then "
            "the best center of rotation "
            "will be pick automatically"
        )
        self.layout().addWidget(self._lockAutofocusButton, 1, 7, 1, 1)
        rspacer = qt.QWidget(self)
        rspacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(rspacer, 0, 8, 2, 1)

        openVignettePixmap = icons.getQPixmap("vignettes")
        openVignetteIcon = qt.QIcon(openVignettePixmap)
        self._vignetteButton = qt.QPushButton(self)
        self._vignetteButton.setFixedSize(qt.QSize(50, 50))
        self._vignetteButton.setIconSize(qt.QSize(40, 40))
        self._vignetteButton.setIcon(openVignetteIcon)
        self.layout().addWidget(self._vignetteButton, 0, 9, 2, 1)

        # radio button group
        self._buttonGrp = qt.QButtonGroup()
        self._buttonGrp.addButton(self._currentcorRB)
        self._buttonGrp.addButton(self._autofocusRB)

        # set up
        self._currentcorRB.setChecked(True)

        # connect signal / slot
        self._currentcorRB.toggled.connect(self._selectionModeChanged)
        self._autofocusRB.toggled.connect(self._selectionModeChanged)
        self._lockAutofocusButton.toggled.connect(self._lockButtonActive)
        self._vignetteButton.released.connect(self._openVignetteMode)
        self._scoreMethodCB.currentIndexChanged.connect(self._scoreMethodChanged)

        # update widget to fit set up
        self._selectionModeChanged()

    def getCorSelectionMode(self):
        if self._currentcorRB.isChecked():
            return "current value"
        elif self._autofocusRB.isChecked():
            return "autofocus"
        else:
            raise NotImplementedError("")

    def _openVignetteMode(self):
        colormap = None
        if self.parent() and hasattr(self.parent(), "getPlotWidget"):
            master_plot = self.parent().getPlotWidget()
            colormap = master_plot.getColorBarWidget().getColormap()
        dialog = VignettesQDialog(
            value_name="cor position",
            score_name="score",
            value_format="{:.3f}",
            score_format="{:.3f}",
            colormap=colormap,
        )
        dialog.setWindowTitle("saaxis - vignettes")

        # set scores
        dialog.setScores(self._scores, score_method=self.getScoreMethod())

        if dialog.exec_() == qt.QDialog.Accepted:
            cor_selected = dialog.selectedValue()
            if cor_selected is not None:
                self.sigCorValueSelected.emit(cor_selected)
        dialog.setAttribute(qt.Qt.WA_DeleteOnClose)

    def _selectionModeChanged(self, *args, **kwargs):
        self.sigSelectionModeChanged.emit()

    def setValue(self, relative_value):
        if relative_value is None:
            self._relativeCorValueLE.clear()
        else:
            self._relativeCorValueLE.setText("{:.3f}".format(relative_value))
        if relative_value is None or self._img_width is None:
            self._absoluteCorValueLE.clear()
        else:
            absolute_value = relative_value + self._img_width // 2
            self._absoluteCorValueLE.setText("{:.3f}".format(absolute_value))

    def getAutoFocusLockButton(self):
        return self._lockAutofocusButton

    def _scoreMethodChanged(self):
        self.sigScoreMethodChanged.emit()

    def isAutoFocusLock(self):
        return self._lockAutofocusButton.isChecked()

    def isAutoFocusActive(self):
        return self._autofocusRB.isChecked()

    def hideAutoFocusButton(self):
        self._lockAutofocusButton.hide()

    def lockAutoFocus(self, lock):
        self._currentcorRB.setEnabled(not lock)
        if lock and not self._autofocusRB.isChecked():
            self._autofocusRB.setChecked(True)
        self._lockAutofocusButton.setChecked(lock)

    def _lockButtonActive(self, lock):
        self.lockAutoFocus(lock)
        if self._lockAutofocusButton.isChecked():
            self.sigAutoFocusLocked.emit()
        else:
            self.sigAutoFocusUnLocked.emit()

    def setScores(self, scores: dict):
        self._scores = scores

    def setImgWidth(self, width):
        self._img_width = width

    def getScoreMethod(self):
        return ScoreMethod.from_value(self._scoreMethodCB.currentText())

    def setScoreMethod(self, method):
        method_value = ScoreMethod.from_value(method).value
        index = self._scoreMethodCB.findText(method_value)
        self._scoreMethodCB.setCurrentIndex(index)


class PainterRotationCM(AbstractContextManager):
    """
    On enter move the painter to the position and rotate it of provided angle.
    On exits rotate back then translate back to the original position
    """

    def __init__(self, painter, x: float, y: float, angle: float):
        self.painter = painter
        self.x = x
        self.y = y
        self.angle = angle

    def __enter__(self):
        self.painter.translate(self.x, self.y)
        self.painter.rotate(self.angle)
        return self.painter

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.painter.rotate(-self.angle)
        self.painter.translate(-self.x, -self.y)


class _CorLabels(qt.QWidget):
    """
    Display labels for center of rotation
    """

    # TODO: could be used to define the current value displayed by underlying
    # and the one selected in red.

    _LABEL_WIDTH = 60
    """Label width with rotation"""

    MIN_WIDTH_PER_LABEL = 40
    """Label width without rotation"""

    # DEBUG OPTIONS: Deformation is not handled so you should put rotation to 0
    PLOT_TICKS = False

    PLOT_CANVAS_LIM = False

    PLOT_LABEL_RECT = False

    def __init__(self, parent=None, angle: float = 45.0):
        qt.QWidget.__init__(self, parent)
        self._cor_values = tuple()
        self._right_shift = 0
        self._slider_ticks_margin = 0
        self.rotation_angle_degree = angle

    def setCorValues(self, values):
        self._cor_values = numpy.array(values)

    def setRightShift(self, shift: int):
        self._right_shift = shift

    def setSliderTicksMargin(self, margin: int):
        self._slider_ticks_margin = margin

    def getCorSteps(self) -> int:
        """
        Return step for the cor values to be displayed.
        1: display all cor values
        2: display one cor per each 2 values
        :return:
        """
        if len(self._cor_values) == 0:
            return 1
        width = self.width()
        # 1.8: as we are a 45 degree then / 2.0 should be good. Dividing by 1.8
        # instead will increase visibility
        n_cors = self._cor_values.size
        for i in range(1, 9):
            if ((n_cors / i) * self.MIN_WIDTH_PER_LABEL) < width:
                return i
        return 10

    def paintEvent(self, event):
        n_cor_values = len(self._cor_values)
        if n_cor_values == 0:
            return
        elif n_cor_values < 5:
            cor_indexes = numpy.arange(n_cor_values)
        else:
            cor_indexes = numpy.arange(0, self._cor_values.size)[:: self.getCorSteps()]

        from_ = self._slider_ticks_margin
        to_ = self.width() - self._right_shift - self._slider_ticks_margin
        cor_px_positions = numpy.linspace(
            from_, to_, self._cor_values.size, endpoint=True
        )

        painter = qt.QPainter(self)
        # painter.translate(self.rect().topLeft())
        font = qt.QFont("Helvetica", 10)
        painter.setFont(font)

        txt_width = self._LABEL_WIDTH
        txt_height = self.height()

        for i_cor in cor_indexes:
            cor_value = self._cor_values[i_cor]
            cor_px_pos = cor_px_positions[i_cor]
            txt_value = "{:.3f}".format(cor_value)
            # apply rotation to "invert" the painter rotation requested to
            # paint oblique text
            with PainterRotationCM(
                painter=painter,
                x=cor_px_pos + self._slider_ticks_margin / 2.0,
                y=0,
                angle=self.rotation_angle_degree,
            ) as l_painter:
                cor_rect = qt.QRect(0, 0, txt_width, txt_height)
                l_painter.drawText(cor_rect, qt.Qt.AlignLeft, txt_value)

                if self.PLOT_LABEL_RECT:
                    painter.drawRect(cor_rect)

        # print all ticks
        if self.PLOT_TICKS:
            painter.setPen(qt.QPen(qt.QColor(35, 234, 32)))
            tick_positions = numpy.linspace(
                from_, to_, len(self._cor_values), endpoint=True
            )
            for pos in tick_positions:
                cor_rect = qt.QRect(pos, 0, 2, 6)
                painter.drawRect(cor_rect)

        # print canvas
        if self.PLOT_CANVAS_LIM:
            painter.setPen(qt.QPen(qt.QColor(168, 34, 32)))
            x, y = self.width() - 2, self.height() - 2
            cor_rect = qt.QRect(0, 0, x, y)
            painter.drawRect(cor_rect)


class ScorePlot(qt.QWidget):

    sigConfigurationChanged = qt.Signal()
    """signal emitted when the configuration change"""

    _CENTRAL_SLICE_NAME = "central slice"

    def __init__(self, parent=None, dims_colors=("#ffff5a", "#62efff", "#ff5bff")):
        self._dim_colors = dims_colors
        self._cor_values = tuple()
        self._scores = {}
        self.__scan = None

        qt.QWidget.__init__(self, parent)
        # define GUI
        self.setLayout(qt.QGridLayout())
        # main plot
        self._plot = ImageStack(self)
        self._plot.getPlotWidget().setKeepDataAspectRatio(True)
        self._plot._sliderDockWidget.hide()
        self._plot.getPlotWidget().getColorBarWidget().hide()
        self._plot.getPlotWidget().getPositionInfoWidget().hide()
        # hide dock widget
        self._plot._reconsInfoDockWidget.hide()
        self._plot._tableDockWidget.hide()
        self.layout().addWidget(self._plot, 0, 0, 1, 2)
        right_shift = 40  # pixel
        # cor score plot
        self._corScore = _CorScorePlot(self)
        self._corScore.setContentsMargins(15, 10, right_shift + 15, 0)
        self.layout().addWidget(self._corScore, 1, 0, 1, 2)
        # slider
        self._corSlider = _CorSlider(self, orientation=qt.Qt.Horizontal)
        self.layout().addWidget(self._corSlider, 2, 0, 1, 2)
        self._corSlider.setContentsMargins(0, 0, right_shift, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().addWidget(self._corSlider, 3, 0, 1, 2)
        # cor labels
        self._corLabels = _CorLabels(self)
        self._corLabels.setContentsMargins(0, 0, 0, 0)
        self._corLabels.setFixedHeight(60)
        self.layout().addWidget(self._corLabels, 4, 0, 1, 2)
        self._corLabels.setRightShift(right_shift)
        self._corLabels.setSliderTicksMargin(15)
        # cor value
        self._corValueWidget = _CorSelection(self)
        self._corValueWidget.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._corValueWidget, 5, 0, 1, 1)
        # voxel size
        self._voxelSizeW = DimensionWidget(
            title="Voxel size",
            dims_name=("x:", "y:", "z:"),
            dims_colors=self._dim_colors,
        )
        self._voxelSizeW.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._voxelSizeW, 6, 0, 1, 1)
        # volume size W
        self._volumeSizeW = DimensionWidget(
            title="Volume size",
            dims_name=("x:", "y:", "z:"),
            dims_colors=self._dim_colors,
        )
        self._volumeSizeW.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self._volumeSizeW, 6, 0, 1, 1)
        # axis
        self.setContentsMargins(0, 0, 0, 0)
        self._axisLabel = qt.QLabel(parent=self)
        icon = icons.getQIcon("axis")
        self._axisLabel.setPixmap(icon.pixmap(qt.QSize(96, 96)))
        self.layout().addWidget(self._axisLabel, 7, 1, 2, 1)

        # connect signal / slot
        self._corSlider.valueChanged.connect(self._plot.setCurrentUrlIndex)
        self._corSlider.valueChanged.connect(self._sliderReleased)
        self._corSlider.valueChanged.connect(self._updateCorValue)
        self._corScore.sigMouseWheelActive.connect(self._propagateSPWheelEvent)
        self._corValueWidget.sigAutoFocusLocked.connect(self._autoFocusLockChanged)
        self._corValueWidget.sigAutoFocusUnLocked.connect(self._autoFocusLockChanged)
        self._corValueWidget.sigSelectionModeChanged.connect(
            self._corSelectionModeChanged
        )
        self._corValueWidget.sigCorValueSelected.connect(self._corSelectedFromVignettes)
        self._corValueWidget.sigScoreMethodChanged.connect(self._updateScores)

        # set up
        # for now we don't want to use the volume and voxel size
        self._volumeSizeW.hide()
        self._voxelSizeW.hide()
        self._axisLabel.hide()

    def getScoreMethod(self):
        return self._corValueWidget.getScoreMethod()

    def setScoreMethod(self, method):
        self._corValueWidget.setScoreMethod(method)

    def _configurationChanged(self, *args, **kwargs):
        self.sigConfigurationChanged.emit()

    def getPlotWidget(self):
        return self._plot.getPlotWidget()

    def _stopAnimationThread(self):
        self._plot._freeLoadingThreads()
        if self._plot._plot.updateThread.is_alive():
            self._plot._plot.updateThread.stop()

    def close(self):
        self._plot.close()
        self._plot = None
        super().close()

    def getCurrentCorvalue(self):
        cor_idx = self._corSlider.value()
        if cor_idx < len(self._cor_values):
            return self._cor_values[cor_idx]

    def setCurrentCorvalue(self, value):
        self._corSlider.setCorValue(value=value)

    def lockAutoFocus(self, lock):
        self._corValueWidget.lockAutoFocus(lock)

    def isAutoFocusLock(self):
        return self._corValueWidget.isAutoFocusLock()

    def hideAutoFocusButton(self):
        self._corValueWidget.hideAutoFocusButton()

    def isAutoFocusActive(self):
        return self._corValueWidget.isAutoFocusActive()

    def _autoFocusLockChanged(self):
        if self.isAutoFocusLock():
            self._applyAutofocus()
        self._configurationChanged()

    def getCorSelectionMode(self):
        return self._corValueWidget.getCorSelectionMode()

    def _applyAutofocus(self):
        scan = self.__scan() if self.__scan else None
        if scan is None:
            return
        if scan.saaxis_params:
            best_cor = scan.saaxis_params.autofocus
            if best_cor:
                self._corSlider.setCorValue(best_cor)

    def _corSelectionModeChanged(self):
        if self.getCorSelectionMode() == "autofocus":
            self._applyAutofocus()

    def _updateCorValue(self):
        self._corValueWidget.setValue(self.getCurrentCorvalue())

    def _corSelectedFromVignettes(self, value):
        self._corSlider.setCorValue(value)
        # self._corValueWidget.setValue(value)

    def _propagateSPWheelEvent(self, event):
        self._corSlider.wheelEvent(event)

    def _get_closest_cor(self, value):
        """return the closest cor value to value or None if no cor value
        defined"""
        if len(self._cor_values) > 0:
            idx_closest = numpy.argmin(numpy.abs(self._cor_values - value))
            return self._cor_values[idx_closest]
        else:
            return None

    def _markerReleased(self):
        cor_value = self._get_closest_cor(self._corScore.corMarker.getPosition()[0])
        if cor_value in self._cor_values:
            # get the index
            old = self._corSlider.blockSignals(True)
            self._corSlider.setCorValue(cor_value)
            self._corSlider.blockSignals(old)
            cor_idx = numpy.where(self._cor_values == cor_value)[0][0]
            self._plot.setCurrentUrlIndex(cor_idx)

    def _sliderReleased(self):
        cor_idx = self._corSlider.value()
        if cor_idx < len(self._cor_values):
            cor_value = self._cor_values[cor_idx]
            old = self._corScore.corMarker.blockSignals(True)
            self._corScore.corMarker.setPosition(cor_value, 0)
            self._corScore.corMarker.blockSignals(old)

    def setScan(self, scan):
        self.clear()
        self.__scan = weakref.ref(scan)

    def _updateScores(self):
        scan = self.__scan() if self.__scan else None
        if scan is not None:
            scan.saaxis_params.score_method = self.getScoreMethod()
            img_width = scan.dim_1
            # update autofocus
            SAAxisProcess.autofocus(scan)
        else:
            img_width = None
        self.setCorScores(
            scores=self._scores,
            score_method=self.getScoreMethod(),
            img_width=img_width,
            update_only_scores=True,
        )

    def setCorScores(
        self,
        scores: dict,
        score_method: Union[str, ScoreMethod],
        img_width=None,
        update_only_scores=False,
    ):
        """

        :param dict scores: cor value (float) as key and
                            tuple(url: DataUrl, score: float) as value
        """
        score_method = ScoreMethod.from_value(score_method)
        if not update_only_scores:
            self.clear()
            self._scores = scores
            self.setImgWidth(img_width)
        # set image width to deduce absolute position from relative
        self._cor_values = []
        score_list = []
        self._urls = []

        if scores is None or len(scores) == 0:
            return
        for cor_value, cor_info in scores.items():
            url, score = cor_info
            self._cor_values.append(cor_value)
            score_list.append(score.get(score_method))
            self._urls.append(url)
        # insure cor and scores are numpy arrays
        self._cor_values = list(self._cor_values)
        score_list = numpy.array(score_list)
        # set zoom a priori
        if not update_only_scores and len(self._urls) > 0:
            try:
                with DatasetReader(url=self._urls[0]) as dataset:
                    shape = dataset.shape
            except Exception as e:
                _logger.warning(e)
            else:
                self._plot.setResetZoomOnNextIteration(True)

        if not update_only_scores:
            self._plot.setUrls(urls=self._urls)
            self._corSlider.setCorValues(self._cor_values)
            old = self._corSlider.blockSignals(True)
            self._corSlider.setCorValue(self._cor_values[0])
            self._corSlider.blockSignals(old)

        self._corScore.addCurve(
            x=numpy.array(self._cor_values),
            y=score_list,
            baseline=0,
            fill=True,
            color="#0288d190",
        )
        self._corLabels.setCorValues(self._cor_values)
        # update cor marker position according to the slider position
        self._sliderReleased()
        self._corValueWidget.setScores(scores)

        scan = self.__scan() if self.__scan else None
        if scan is not None and self.isAutoFocusActive():
            best_cor = scan.saaxis_params.autofocus
            if best_cor:
                self._corSlider.setCorValue(best_cor)

    def setImgWidth(self, width):
        self._corValueWidget.setImgWidth(width)

    def clear(self):
        self._corSlider.setCorValues(tuple())
        self._corScore.clear()
        self._corLabels.setCorValues(tuple())
        self._plot.getPlotWidget().clear()
        self._corValueWidget.setImgWidth(None)

    def setVoxelSize(self, dim0, dim1, dim2, unit):
        """

        :param float dim0:
        :param float dim1:
        :param float dim2:
        :param Union[str,float] unit:
        """
        self._voxelSizeW.setValues(dim0=dim0, dim1=dim1, dim2=dim2, unit=unit)

    def setVolumeSize(self, dim0, dim1, dim2, unit):
        """

        :param float dim0:
        :param float dim1:
        :param float dim2:
        :param Union[str,float] unit:
        """
        self._volumeSizeW.setValues(dim0=dim0, dim1=dim1, dim2=dim2, unit=unit)

    def getDim0N(self):
        """return the number of elements in dimension 0 according to voxel
        size and volume size"""
        return int(
            numpy.ceil(
                self._volumeSizeW.getDim0Value()[0] / self._voxelSizeW.getDim0Value()[0]
            )
        )

    def getDim1N(self):
        """return the number of elements in dimension 1 according to voxel
        size and volume size"""
        return int(
            numpy.ceil(
                self._volumeSizeW.getDim1Value()[0] / self._voxelSizeW.getDim1Value()[0]
            )
        )

    def getDim2N(self):
        """return the number of elements in dimension 2 according to voxel
        size and volume size"""
        return int(
            numpy.ceil(
                self._volumeSizeW.getDim2Value()[0] / self._voxelSizeW.getDim2Value()[0]
            )
        )


class _CorSlider(qt.QWidget):
    def __init__(self, parent, orientation):
        self._values = None
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._slider = qt.QSlider(self)
        self.layout().addWidget(self._slider)
        self._slider.setMaximum(0)
        self._slider.setOrientation(orientation)
        self._slider.setTickPosition(qt.QSlider.TicksBelow)

        # connect signal / slot
        self.valueChanged = self._slider.valueChanged

    def wheelEvent(self, event) -> None:
        self._slider.wheelEvent(event)

    def setCorValues(self, values):
        self._slider.setRange(0, len(values) - 1)
        self._values = numpy.array(values, dtype=numpy.float32)

    def setCorValue(self, value):
        if value in self._values:
            where = numpy.where(self._values == value)
            if len(where) > 0:
                value = where[0]
                if isinstance(value, numpy.ndarray):
                    value = value[0]
                self._slider.setValue(value)

    def value(self):
        return self._slider.value()


if __name__ == "__main__":
    from silx.image.phantomgenerator import PhantomGenerator
    from silx.io.url import DataUrl
    import tempfile
    import os
    import h5py
    import shutil
    from scipy import stats

    app = qt.QApplication([])
    img_width = 216
    data = PhantomGenerator.get2DPhantomSheppLogan(n=img_width)
    nb_cor = 50
    urls = []
    slices_folder = tempfile.mkdtemp()
    for i in range(nb_cor):
        noise = (
            numpy.random.random(img_width * img_width).reshape(img_width, img_width)
            * 100.0
        )
        file_path = os.path.join(slices_folder, "slice_{}.hdf5".format(i))
        with h5py.File(file_path, mode="a") as h5f:
            h5f["data"] = noise + data
        urls.append(DataUrl(file_path=file_path, data_path="data", scheme="silx"))
    variance = 1
    mu = 0.5
    sigma = numpy.sqrt(variance)
    x = numpy.linspace(mu - 3 * sigma, mu + 3 * sigma, nb_cor)
    scores = stats.norm.pdf(x, mu, sigma)

    cor_values = numpy.linspace(80, 120, nb_cor)
    scores_dict = {}
    for cor, url, score in zip(cor_values, urls, scores):
        scores_dict[cor] = (url, score)

    window1 = ScorePlot()
    window1.setCorScores(scores=scores_dict, score_method="std")
    window1.show()
    from tomwer.core.scan.scanbase import TomwerScanBase
    from tomwer.core.process.reconstruction.saaxis.params import SAAxisParams
    from tomwer.core.process.reconstruction.saaxis.saaxis import SAAxisProcess

    scan = TomwerScanBase()
    scan.saaxis_params = SAAxisParams()
    scan.saaxis_params.scores = scores_dict
    SAAxisProcess.autofocus(scan)
    window1.setScan(scan)
    app.exec_()

    shutil.rmtree(slices_folder)
