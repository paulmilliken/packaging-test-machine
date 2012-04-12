import gtkmvc
import pygtk
pygtk.require('2.0')
import gtk

class MyView(gtkmvc.View):
    def __init__(self):
        gtkmvc.View.__init__(self)
        self.createMainWindow()
        self.mainWindow.show_all()

    def createMainWindow(self):
        self.mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.mainWindow.set_size_request(960,680) 
        self.createHBoxParent()

    def createHBoxParent(self):
        self.hboxParent = gtk.HBox()
        self.mainWindow.add(self.hboxParent)
        self.addVButtonBoxAllButtons()
        self.addProgressBar()
        self.addVBoxRHS()
        self.addVBoxExtremeRHS()

    def addVButtonBoxAllButtons(self):
        self.vbuttonboxAllButtons = gtk.VButtonBox()
        self.hboxParent.pack_start(self.vbuttonboxAllButtons, expand=False, \
            fill=False)
        self.addButtons()

    def addButtons(self):
        self.addSquashButton()
        self.addStopButton()
        self.addGoUpButton()
        self.addGoDownButton()
        self.addLiveViewButton()

    def addSquashButton(self):
        self.squashBtn = gtk.Button("Squash Box")
        self.vbuttonboxAllButtons.pack_start(self.squashBtn, expand=False, \
            fill=False)

    def addConstantLoadButton(self):
        self.constantLoadBtn = gtk.Button("Apply Constant\nLoad")
        self.vbuttonboxAllButtons.pack_start(self.constantLoadBtn, False, False)
    
    def addCalibrateButton(self):
        self.calibrateBtn = gtk.Button("Load Calibration\nProcedure")
        self.vbuttonboxAllButtons.pack_start(self.calibrateBtn, expand=False, \
            fill=False)

    def addStopButton(self):
        self.stopBtn = gtk.Button(stock=gtk.STOCK_STOP)
        self.vbuttonboxAllButtons.pack_start(self.stopBtn, expand=False, \
            fill=False)

    def addGoUpButton(self):
        self.upBtn = gtk.Button(stock=gtk.STOCK_GO_UP)
        self.vbuttonboxAllButtons.pack_start(self.upBtn, expand=False, \
            fill=False)
        
    def addGoDownButton(self):
        self.downBtn = gtk.Button(stock=gtk.STOCK_GO_DOWN)
        self.vbuttonboxAllButtons.pack_start(self.downBtn, expand=False, \
            fill=False)
    
    def addLiveViewButton(self):
        self.liveViewBtn = gtk.Button("Live view")
        self.vbuttonboxAllButtons.pack_start(self.liveViewBtn, expand=False, \
            fill=False)

    def addProgressBar(self):
        self.progressbar = gtk.ProgressBar()
        self.hboxParent.pack_start(self.progressbar, expand=False, fill=False)
        self.progressbar.set_orientation(gtk.PROGRESS_TOP_TO_BOTTOM)

    def addVBoxRHS(self):
        self.vboxRHSide = gtk.VBox()
        self.hboxParent.pack_start(self.vboxRHSide, expand=True, fill=True)
        self.addHBoxBoxId()
        self.addHBoxSpeed()
        self.addHBoxStroke()
        self.addHBoxDataDirectory()
        self.addLivePlot()

    def addHBoxBoxId(self):
        self.hboxBoxId = gtk.HBox()
        self.vboxRHSide.pack_start(self.hboxBoxId, expand=False, fill=False)
        self.addBoxIdLabel()
        self.addBoxId()

    def addBoxIdLabel(self):
        self.boxIdLabel = gtk.Label()
        self.boxIdLabel.set_text("Box Id:")
        self.hboxBoxId.pack_start(self.boxIdLabel, False, False)

    def addBoxId(self):
        self.boxId = gtk.Entry(64)
        self.hboxBoxId.pack_start(self.boxId, expand=True, fill=True)
       
    def addHBoxSpeed(self):
        self.hboxSpeed = gtk.HBox()
        self.vboxRHSide.pack_start(self.hboxSpeed, expand=False, fill=False)
        self.addSpeedLabel()
        self.addSpeedSpinButton()

    def addSpeedLabel(self):
        self.speedLabel = gtk.Label()
        self.speedLabel.set_text("Crushing speed (mm/min):")
        self.hboxSpeed.pack_start(self.speedLabel, False, False)

    def addSpeedSpinButton(self):
        self.speedAdjustment = gtk.Adjustment(value=22, lower=1, upper=120, \
            step_incr=1, page_incr=10, page_size=0)
        self.speedSpinButton = gtk.SpinButton(self.speedAdjustment)
        self.speedSpinButton.set_digits(0)
        self.speedSpinButton.set_update_policy(gtk.UPDATE_IF_VALID)
        self.hboxSpeed.pack_start(self.speedSpinButton, False, False)
 
    def addHBoxStroke(self):
        self.hboxStroke = gtk.HBox()
        self.vboxRHSide.pack_start(self.hboxStroke, expand=False, fill=False)
        self.addStrokeLabel()
        self.addStrokeSpinButton()

    def addStrokeLabel(self):
        self.strokeLabel = gtk.Label()
        self.strokeLabel.set_text("Crushing stroke (mm/min):")
        self.hboxStroke.pack_start(self.strokeLabel, False, False)

    def addStrokeSpinButton(self):
        self.strokeAdjustment = gtk.Adjustment(value=44, lower=1, upper=88, \
            step_incr=1, page_incr=10, page_size=0)
        self.strokeSpinButton = gtk.SpinButton(self.strokeAdjustment)
        self.strokeSpinButton.set_digits(0)
        self.strokeSpinButton.set_update_policy(gtk.UPDATE_IF_VALID)
        self.hboxStroke.pack_start(self.strokeSpinButton, False, False)
    
    def addHBoxDataDirectory(self):
        self.hboxDataDirectory = gtk.HBox()
        self.vboxRHSide.pack_start(self.hboxDataDirectory, expand=False, \
            fill=False)
        self.addDataDirectoryLabel()
        self.addDataDirectoryChooser()

    def addDataDirectoryLabel(self):
        self.dataDirectoryLabel = gtk.Label()
        self.dataDirectoryLabel.set_text("Data directory:")
        self.hboxDataDirectory.pack_start(self.dataDirectoryLabel, False, False)

    def addDataDirectoryChooser(self):
        self.dataDirectoryChooserButton = \
            gtk.FileChooserButton('Select a directory')
        self.dataDirectoryChooserButton.set_action(\
            gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        self.hboxDataDirectory.pack_start(self.dataDirectoryChooserButton, \
            expand=True, fill=True)
    
    def setDefaultDataDirectory(self, defaultDataDirectory):
        self.dataDirectoryChooserButton.set_current_folder(defaultDataDirectory)
        
    def addLivePlot(self):
        from matplotlib.figure import Figure
        self.livePlotFigure = Figure()
        self.setUpAxes()

    def setUpAxes(self):
        from matplotlib.backends.backend_gtk import FigureCanvasGTK 
        self.livePlotAxis = self.livePlotFigure.add_subplot(111)
        self.livePlotAxis.set_ylim([-10, 5010])
        self.livePlotAxis.set_autoscale_on(False)
        self.livePlotAxis.set_xlabel('Distance (mm)')
        self.livePlotAxis.set_ylabel('Load cell reading (mV)')
        self.livePlotAxis.grid(True)
        self.livePlotCanvas = FigureCanvasGTK(self.livePlotFigure)
        self.vboxRHSide.pack_start(self.livePlotCanvas, expand=True, fill=True)

    def addVBoxExtremeRHS(self):
        self.vboxExtremeRHSide = gtk.VBox()
        self.hboxParent.pack_start(self.vboxExtremeRHSide, expand=False, \
            fill=True)
        self.addLiveAnalogueValues()

    def addLiveAnalogueValues(self):
        '''Adds labels and values for Analogue channels A0 to A5'''
        self.analogueLabels = [gtk.Label(), gtk.Label(), gtk.Label(), gtk.Label(), gtk.Label(), gtk.Label()]
        self.analogueValues = [gtk.Label(), gtk.Label(), gtk.Label(), gtk.Label(), gtk.Label(), gtk.Label()]
        analogueLabelsText = ['A0 (loadcell) mV', 'A1 (LVDT) mV', \
            'A2 (LVDT) mV', 'A3 (LVDT) mV', 'A4 (LVDT) mV', 'A5 (LVDT) mV']
        for i in range(6):
            self.analogueLabels[i].set_text(analogueLabelsText[i])
            self.vboxExtremeRHSide.pack_start(self.analogueLabels[i], False, \
                False)
            self.vboxExtremeRHSide.pack_start(self.analogueValues[i], True, \
                False)




#        self.A0Label = gtk.Label()
#        self.A0Label.set_text("A0 (loadcell) (mV)")
#        self.A0Value = gtk.Label()
#       
#        self.A1Label = gtk.Label()
#        self.A1Label.set_text("A1 (LVDT) (mV)")
#        self.A1Value = gtk.Label()
#
#        self.A2Label = gtk.Label()
#        self.A2Label.set_text("A2 (LVDT) (mV)")
#        self.A2Value = gtk.Label()
#        
#        self.A3Label = gtk.Label()
#        self.A3Label.set_text("A3 (LVDT) (mV)")
#        self.A3Value = gtk.Label()
#        
#        self.A4Label = gtk.Label()
#        self.A4Label.set_text("A4 (LVDT) (mV)")
#        self.A4Value = gtk.Label()
#        
#        self.A5Label = gtk.Label()
#        self.A5Label.set_text("A5 (LVDT) (mV)")
#        self.A5Value = gtk.Label()
#         
#        widgetList = [[self.A0Label, self.A0Value], \
#            [self.A1Label, self.A1Value], \
#            [self.A2Label, self.A2Value], [self.A3Label, self.A3Value], \
#            [self.A4Label, self.A4Value], [self.A5Label, self.A5Value]]
#        for widget in widgetList:
#            self.vboxExtremeRHSide.pack_start(widget[0], False, False)
#            self.vboxExtremeRHSide.pack_start(widget[1], True, False)
#            widget[1].set_text("*.***")
            
if __name__=='__main__':
   v = MyView() 
   gtk.main()
