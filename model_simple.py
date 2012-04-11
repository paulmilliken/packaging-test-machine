import gtkmvc
import time
import threading
from packageTestMachineDriver import TestingMachine

class MyModel(gtkmvc.ModelMT):

    def __init__(self):
        gtkmvc.ModelMT.__init__(self)
        self.testingMachine = TestingMachine()
        self._setInitialValuesOfVariables()

    def _setInitialValuesOfVariables(self):
        self.nEvents = 0
        self.dataDirectory = '/home/crush/tmp'
        self.squashStroke = 44 # mm
        self.squashSpeed = 22 # mm/min
        self.fastSpeed = 110 # mm/min
        self.upStroke = -5 # mm
        self.downStroke = 5 # mm
        self.acceleration = 1.0 # mm/sec/sec
        self.boxId = 0

    def squash(self, nEventsAtStartOfSquashing):
        self._openFileForWriting()
        self.startSquashTime = time.time()
        self.testingMachine.moveUpDown(self.squashStroke, self.squashSpeed, \
            self.acceleration)
        self._recordTest(nEventsAtStartOfSquashing)
        self.cleanUpAfterSquashTest(nEventsAtStartOfSquashing)
        
    def _cleanUpAfterSquashTest(self, nEventsAtStart):
        self.testingMachine.moveUpDown(-self.squashStroke, self.squashSpeed, \
            self.acceleration)
        self.nEvents += 1

    def _recordTest(self, nEventsAtStartOfSquashing):
        try:
            while (self.testingMachine.isAtTargetPosition()==False and \
                self.nEvents==nEventsAtStartOfSquashing):
                self.writeOneLineOfDataToFile()
        finally:
            self._closeFile()

    def _writeOneLineOfDataToFile(self):
        lineToWriteToFile = '%f.3, %d, %d\n' % \
            (self.testingMachine.getPASIUnits(), \
                self.testingMachine.getAnalogueMillivoltage(0), \
                self.testingMachine.getAnalogueMillivoltage(1), \
                self.testingMachine.getAnalogueMillivoltage(2), \
                self.testingMachine.getAnalogueMillivoltage(3), \
                self.testingMachine.getAnalogueMillivoltage(4), \
                self.testingMachine.getAnalogueMillivoltage(5), \
                time.time() - self.startSquashTime)
        self.fid.write(lineToWriteToFile)

    def _openFileForWriting(self):
        self.fid = open('%s/box%s.csv' % (self.dataDirectory, \
            str(self.boxId)), 'w')
        self._writeHeader()

    def _writeHeader(self):
        self.fid.write('# distance_mm, load_cell_mV, time_seconds\n')

    def _closeFile(self):
        self.fid.close()

    def _tidyUpAfterSquash(self):
        self.testingMachine.stopMotor()
        self.nEvents += 1
        self.closeFile()
        self.testingMachine.moveSIUnits(0,returnToStartPosition())
    
    def _returnToStartPosition(self):
        self.moveUpDown(self.nEvents, -self.stroke)
        print('Box squashed')

    def moveUp(self, nEvents):
        self.testingMachine.moveUpDown(self.upStroke, self.fastSpeed, \
            self.acceleration)

    def moveDown(self, nEvents):
        self.testingMachine.moveUpDown(self.downStroke, self.fastSpeed, \
            self.acceleration)

    def moveDown(self, nEvents):
        self.testingMachine.moveUpDown(self.downStroke, self.fastSpeed, \
            self.acceleration)

    def stop(self, nEvents):
        self.testingMachine.stopMotor()        

#    def checkForHardStop(self, nEventsAtStartOfMove):
#        #wait for move to complete:
#        while(self.nEvents==nEventsAtStartOfMove):
#            self.askSmartMotorForData()
#            self.readDataFromSmartMotor()
#            #time.sleep(0.1)
#            myChar = ''
#            line = self.ser.readline()
#            line = line.strip().split(',')
#            absPosError = abs(int(line[0]))
#            absTargetError = abs(int(line[1])-int(line[2]))
#            if absPosError>50:
#                self.ser.write('OFF ')
#                print('Error: encountered hard stop, absPosError=%d' % \
#                    absPosError)
#                break
#            if absTargetError<10:
#                self.ser.write('X ')
#                print('Move completed')
#                break
#        #stop motor and reset origin:
#        self.ser.write('O=0 ')
#        self.ser.write('PT=0 ')
#
#    def commandMotorToMove(self):
#        self.setVTandPT(self.speed, self.stroke)
#        # now issue commands for smartmotor to descend:
#        self.ser.write('ECHO_OFF ')
#        self.ser.write('EIGN(2) EIGN(3) ZS MP ')
#        self.ser.write('ADT=%.0f ' % self.smartMotorAndJackParameters['ADT'])
#        self.ser.write('O=0 ')
#        self.ser.write('VT=%.0f ' % self.VT)
#        self.ser.write('PT=%.0f ' % self.PT)
#        self.ser.write('G ')

#    def setVTandPT(self, speed, stroke):
#        omega = speed*self.smartMotorAndJackParameters['gearRatio'] # omega in rps
#        self.VT = self.smartMotorAndJackParameters['kMotor']*omega
#        self.PT = self.smartMotorAndJackParameters['pulsesPerRev'] * \
#            self.smartMotorAndJackParameters['gearRatio'] * stroke

#    def recordDataDuringSquashing(self, nEventsAtStart):
#        import time
#        startTime = time.time()
#        while(self.nEvents==nEventsAtStart):
#            askSmartMotorForData()
#            readDataFromSmartMotor()
#            writeDataToFile()
#            checkForCompletionOfSquash()

#    def askSmartMotorForData(self):
#        self.ser.write('PRINT(EA,",",PA,",",PT,",") ')
#        self.ser.write('RINA(V1,0) ')
#        self.ser.write('PRINT(#10) ')

#    def readDataFromSmartMotor(self):
#        line = self.ser.readline()
#        print(line)
#        line = line.strip().split(',')
#        print(line)
#        self.internalMotorPositionError = float(line[0])
#        self.position = float(line[1])/pulsesPerRev/gearRatio
#        self.fractionalPosition = position/self.stroke
#        self.load = float(line[3])
#        self.absTargetError = abs(int(line[2])-int(line[1]))

#    def writeDataToFile(self):
#        try:
##            if self.fid.closed:
#                self.openFileForWriting()
#        except:
#                self.openFileForWriting()
#        self.fid.write('%.3f, %d\n' % (self.position, self.load))
  
#        self.nEvents += 1
#        boxId = 'box'
#        validChars = '_-.%s%s' % (string.ascii_letters, string.digits)
#        for myChar in self.boxId.get_text():
#            if myChar in validChars:
#                boxId += myChar
#        filename = os.path.join(dataDirectory, '%s.csv' % boxId)
#        if os.path.exists(filename):
#            myMessage = 'File %s already exists.  Overwrite?' % filename
#            print(myMessage)
#            myDialog = gtk.MessageDialog(flags = gtk.DIALOG_MODAL, \
#                type = gtk.MESSAGE_QUESTION, buttons = gtk.BUTTONS_YES_NO, \
#                message_format = myMessage)
#            #myDialog.set_title("Overwrite file?")
#            dialogResult = myDialog.run()
#            myDialog.destroy()
#            if dialogResult==gtk.RESPONSE_NO:
#                print('Aborting squashing of box.')
#                return
#        myThread = threading.Thread(target=self.squashBox, \
#            args=(self.nEvents, filename))
#        myThread.start()
#       
#    def on_stopBtn_clicked(self, widget, data=None):
#        self.nEvents += 1
#        print('stop button clicked')
#        self.ser.write('OFF \r')
#    
#    def updatePlot(self, x, y):
#        self.axis.plot(x, y, 'k.')
#        self.canvas.draw_idle()
#
#    def moveUpDown(self, nEvents, stroke, ADT=100, errorLimit=50, \
#        kMotor=32768, gearRatio=40.0, moveSpeed=1.0, pulsesPerRev=4000.0):
#        
#        omega = moveSpeed*gearRatio # omega in rps
#        VT = kMotor*omega
#        #VT = 500000
#        PT = pulsesPerRev*gearRatio*stroke
#        # now issue commands to smartmotor to descend:
#        #self.ser.write('ECHO_OFF ')
#        self.ser.write('EIGN(2) ')
#        self.ser.write('EIGN(3) ')
#        self.ser.write('ZS ')
#        self.ser.write('MP ')
#        self.ser.write('ADT=%.0f ' % ADT)
#        self.ser.write('O=0 ')
#        self.ser.write('VT=%.0f ' % VT)
#        self.ser.write('PT=%.0f ' % PT)
#        self.ser.write('G ')
#        #wait for move to complete:
#        while(self.nEvents==nEvents):
#            self.ser.write('PRINT(EA,",",PA,",",PT,#10) ')
#            #time.sleep(0.1)
#            myChar = ''
#            line = self.ser.readline()
#            line = line.strip().split(',')
#            absPosError = abs(int(line[0]))
#            absTargetError = abs(int(line[1])-int(line[2]))
#            if absPosError>50:
#                self.ser.write('OFF ')
#                print('Error: encountered hard stop, absPosError=%d' % \
#                    absPosError)
#                break
#            if absTargetError<10:
#                self.ser.write('X ')
#                print('Move completed')
#                break
#        #stop motor and reset origin:
#        self.ser.write('O=0 ')
#        self.ser.write('PT=0 ')
#    
#    def squashBox(self, nEvents, filename, ADT=100, errorLimit=50, \
#        kMotor=32768, gearRatio=40.0, speed=22.0/60.0, stroke=44.0, \
#        pulsesPerRev=4000.0):
#        '''issues serial commands to Smart motor to squash box and logs data'''
#        # ADT is acceleration rate
#        # errorLimit in pulses
#        # kMotor is from VT = kMotor*omega (omega in rps)
#        # gearRatio in rev/mm
#        # testspeed in mm/sec
#        # pulsesPerRev is encoder resolution
#        # testStroke in mm
#        
#        #prepare the axes:
#        self.axis.clear()
#        self.axis.set_autoscale_on(False)
#        self.axis.set_xlim([-1,stroke+1.0])
#        self.axis.set_ylim([-10,5010])
#        self.axis.set_xlabel('displacement (mm)')
#        self.axis.set_ylabel('load cell reading (mV)')
#        
#        fid = open(filename, 'w')
#        omega = speed*gearRatio # omega in rps
#        VT = kMotor*omega
#        PT = pulsesPerRev*gearRatio*stroke
#        # now issue commands to smartmotor to descend:
#        self.ser.write('ECHO_OFF ')
#        self.ser.write('EIGN(2) EIGN(3) ZS MP ')
#        self.ser.write('ADT=%.0f ' % ADT)
#        self.ser.write('O=0 ')
#        self.ser.write('VT=%.0f ' % VT)
#        self.ser.write('PT=%.0f ' % PT)
#        self.ser.write('G ')
#        startTime = time.time()
#        while(self.nEvents==nEvents):
#            self.ser.write('PRINT(PA,",",PT,",") ')
#            self.ser.write('RINA(V1,0) ')
#            self.ser.write('PRINT(#10) ')
#            line = self.ser.readline()
#            print(line)
#            line = line.strip().split(',')
#            print(line)
#            position = float(line[0])/pulsesPerRev/gearRatio
#            self.progressbar.set_fraction(position/stroke)
#            load = float(line[2])
#            self.updatePlot(position, load)
#            absTargetError = abs(int(line[1])-int(line[0]))
#            if absTargetError<10:
#                self.ser.write('X ')
#                print('Move completed')
#                endTime = time.time()
#                self.progressbar.set_fraction(1.0)
#                # now return to start position:
#                self.moveUpDown(self.nEvents, -stroke)
#                print('Box squashed')
#                print('Elapsed time is %.3f seconds' % (endTime - startTime))
#                self.progressbar.set_fraction(0.0)
#                break
#            fid.write('%.3f, %d\n' % (position, load))
#        fid.close()
#
#if __name__=='__main__':
#    c = captainsOfCrush()
#    gtk.gdk.threads_init()
##    def captureStationarySignal(self, nEvents, load):
#        nSamples=100
#        self.axis.clear()
#        self.axis.set_autoscale_on(False)
#        self.axis.set_xlim([-1,nSamples+1.0])
#        self.axis.set_ylim([-10,5010])
#        self.axis.set_xlabel('sample number')
#        self.axis.set_ylabel('load cell reading (mV)')
#        filename = os.path.join(dataDirectory,'calibrationLoad%s.csv' % load)
#        fid = open(filename, 'w')
#        # now issue commands to smartmotor to descend:
#        self.ser.write('ECHO_OFF ')
#        self.ser.write('EIGN(2) EIGN(3) ZS MP ')
#        self.ser.write('O=0 ')
#        self.ser.write('PT=0 ')
#        self.ser.write('G ')
#        startTime = time.time()
#        i = 0 # number of measurements
#        millivoltList = []
#        while(self.nEvents==nEvents and i<nSamples):
#            i = i + 1
#            myFraction = float(i)/float(nSamples)
#            self.calibrationProgressbar.set_fraction(myFraction)
#            while gtk.events_pending():
#                gtk.main_iteration()
#            time.sleep(0.01)
#            self.ser.write('RINA(V1,0) ') # print voltage in mV
#            self.ser.write('PRINT(#10) ') # carriage return
#            line = self.ser.readline()
#            line = line.strip()
#            try:
#                millivoltage = int(line)
#                self.updatePlot(i, millivoltage)
#                millivoltList.append(millivoltage)
#            except:
#                break
#            fid.write('%d\n' % millivoltage)
#        fid.close()
#        self.calibrationProgressbar.set_fraction(0.0)
#        self.loadInputWindow.hide()
#        if len(millivoltList)>0:
#            myMessage = 'At load %s, the signal was %.2f millivolts' % (load, \
#                float(sum(millivoltList))/float(len(millivoltList)))
#            myDialog = gtk.MessageDialog(flags = gtk.DIALOG_MODAL, \
#                type = gtk.MESSAGE_INFO, buttons = gtk.BUTTONS_OK, \
#                message_format = myMessage)
#                #myDialog.set_title("Overwrite file?")
#            dialogResult = myDialog.run()
#            myDialog.destroy()
#
#    def applyConstantLoad(self, nEvents, filename):
#        Kp = 10.0 # proportional gain
#        Ki = 10.0 # integral gain
#        self.ser.write('X ')
#        self.ser.write('MV ') # velocity mode
#        self.ser.write('O=0 ') # set origin to here
#        previousTime = float(1e9)
#        intError = 0
#        self.ser.write('TMR(0,%d) ' % previousTime)
#        while (self.nEvents==nEvents):
#            # read timer and calculate deltaT:
#            self.ser.write('RTMR(0) ')
#            line = self.ser.readline()
#            currentTime = int(line)
#            deltaT = previousTime - currentTime
#            previousTime = currentTime
#           
#            # get load cell reading:
#            self.ser.write('RINA(V1,0) ')
#            myVoltage = float(self.ser.read())
#            time.sleep(0.01)
#           
#            error = myVoltage - self.load
#            intError = intError + error * deltaT 
#            speed = int(Kp*error + Ki*intError)
#            self.ser.write('MV ')
#
#    def updatePlot(self, x, y):
#        self.axis.plot(x, y, 'k.')
#        self.canvas.draw_idle()
#    gtk.main()
