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


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "04/06/2021"


from silx.gui import qt
from Orange.widgets.widget import OWWidget, Input, Output
from darfix.gui.magnificationWidget import MagnificationWidget
from darfix.gui.rsmWidget import RSMWidget


class TransformationWidgetOW(OWWidget):
    """
    Widget that computes the background substraction from a dataset
    """

    name = "transformation"
    # icon = "icons/pca.png"
    want_main_area = False

    # Inputs
    class Inputs:
        dataset = Input("dataset", tuple)

    # Outputs
    class Outputs:
        dataset = Output("dataset", tuple)

    def __init__(self):
        super().__init__()

    @Inputs.dataset
    def setDataset(self, dataset):
        if dataset:
            if not dataset[0].dims.ndim:
                msg = qt.QMessageBox()
                msg.setIcon(qt.QMessageBox.Warning)
                msg.setText("This widget has to be used before selecting any region of \
                             interest and after selecting the dimensions")
                msg.exec_()
            else:
                if dataset[0].dims.ndim == 1:
                    self._widget = RSMWidget(parent=self)
                else:
                    self._widget = MagnificationWidget(parent=self)
                self._widget.sigComputed.connect(self._sendSignal)
                self.controlArea.layout().addWidget(self._widget)
                self._widget.setDataset(*dataset)
        else:
            # Emit None
            self.Outputs.dataset.send(dataset)

        self.open()

    def _sendSignal(self):
        """
        Emits the signal with the new dataset.
        """
        self.close()
        self.Outputs.dataset.send(self._widget.getDataset())
