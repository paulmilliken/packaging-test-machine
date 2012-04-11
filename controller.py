import gtkmvc
import pygtk
pygtk.require('2.0')
import gtk
import serial
import time
import threading
import string
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.figure
import matplotlib.axes
import matplotlib.backends.backend_gtkagg
import matplotlib.cm
import matplotlib.pylab
matplotlib.pylab.hold(True)

#import pdb

class MyController(gtkmvc.Controller):
    
    def __init__(self, model, view):
        gtkmvc.Controller.__init__(self, model, view)


######################### register view #################################

    def register_view(self, view):
        self.setDefaultValuesInView()
        self.view.strokeSpinButton.connect('value_changed', \
            self._onStrokeSpinButtonValueChanged)
        self.view.speedSpinButton.connect('value_changed', \
            self._onSpeedSpinButtonValueChanged)
        self.view.squashBtn.connect('clicked', self._onSquashBtnClicked)
        self.view.stopBtn.connect('clicked', self._onStopBtnClicked)
        self.view.upBtn.connect('clicked', self._onUpBtnClicked)
        self.view.downBtn.connect('clicked', self._onDownBtnClicked)
        self.view.dataDirectoryChooserButton.connect('current-folder-changed', \
            self._updateDataDirectory)
        self.view.mainWindow.connect('destroy', self._onMainWindowDestroy)

    def setDefaultValuesInView(self):
        self.view.setDefaultDataDirectory(self.model.dataDirectory)
        self.view.speedSpinButton.set_value(self.model.squashSpeed)
        self.view.strokeSpinButton.set_value(self.model.squashStroke)
        self._setXAxisLimits()
    
    def _onStrokeSpinButtonValueChanged(self, spinButton):
        self.model.stroke = spinButton.get_value_as_int()
        self._setXAxisLimits()

    def _setXAxisLimits(self):
        xAxisLimitPadding = 2 # mm
        self.view.livePlotAxis.set_xlim([-xAxisLimitPadding, (xAxisLimitPadding\
            + self.model.squashStroke)])
        self.view.livePlotCanvas.draw_idle()

    def _onSpeedSpinButtonValueChanged(self, spinButton):
        self.model.speed = spinButton.get_value_as_int()
        print('speed now %d' % self.model.speed)

    def _onSquashBtnClicked(self, button):
        self._squashThreaded(button)

    def _onStopBtnClicked(self, button):
        self._stopThreaded(button)

    def _onUpBtnClicked(self, button):
        self._goUpThreaded(button)

    def _onDownBtnClicked(self, button):
        self._goDownThreaded(button)

    def _updateDataDirectory(self, chooserButton):
        self.model.dataDirectory = chooserButton.get_current_folder()

    def _onMainWindowDestroy(self, window):
        self._stopThreaded(window)
        gtk.main_quit()

################## signal handling #####################################3

    def updatePlot(self, x, y):
        self.view.livePlotAxis.plot(x, y, 'k.')
        self.view.livePlotCanvas.draw_idle()
    
    def _squashThreaded(self, widget, data=None):
        self.model.nEvents +=1
        squashThread = threading.Thread(target=self.model.squash, \
            args=(self.model.nEvents, ))
        squashThread.start()

    def _stopThreaded(self, widget, data=None):
        self.model.nEvents += 1
        stopThread = threading.Thread(target=self.model.stop, \
            args=(self.model.nEvents, ))
        stopThread.start()

    def _goUpThreaded(self, widget, data=None):
        self.model.nEvents += 1
        goUpThread = threading.Thread(target=self.model.moveUp, \
            args=(self.model.nEvents, ))
        goUpThread.start()

    def _goDownThreaded(self, widget, data=None):
        self.model.nEvents += 1
        goDownThread = threading.Thread(target=self.model.moveDown, \
            args=(self.model.nEvents, ))
        goDownThread.start()

