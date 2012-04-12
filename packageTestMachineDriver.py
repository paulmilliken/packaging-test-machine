import serial

class TestingMachine():
    '''The TestMachine class is a driver for a package testing machine that
    uses an Animatics SM23165D motor and a 40 turns-per-mm jack to perform
    compression tests on cardboard boxes'''

    def __init__(self):
        self._setSmartMotorVariables()
        try:
            self._openSerial()
        except:
            print("Can't open serial port")
        finally:
            self._closeSerial()

    def _setSmartMotorVariables(self):
        '''Defines parameters relating to SmartMotor and jack'''
        self._SMAndJackParameters = {'kMotor': 32768.0, 'gearRatio': 40.0, \
            'pulsesPerRev': 4000.0, 'samplingRate': 8000.0}
        # pulsesPerRev is the number of encoder stripes
        # omega = self.speed/60
        # VT = kMotor*omega (omega in rps)
        # gearRatio in rev/mm

    def _positionToPT(self, positionInMillimetres):
        '''conversion to SmartMotor units'''
        PT = self._SMAndJackParameters['pulsesPerRev'] * \
            self._SMAndJackParameters['gearRatio'] * positionInMillimetres
        return(int(PT))
#
#    def _PTToPosition(self, PT):
#        position = PT / _SMAndJackParameters['pulsesPerRev'] / \
#            _SMAndJackParameters['gearRatio']
#        return(position)
#
    def _speedToVT(self, speedInMillimetresPerSec):
        '''conversion to SmartMotor units'''
        VT = self._SMAndJackParameters['kMotor'] * \
            self._SMAndJackParameters['gearRatio'] * speedInMillimetresPerSec
        return(int(VT))
#    
#    def _VTToSpeed(self, VT):
#        speed = VT / _SMAndJackParameters['kMotor'] / \
#            _SMAndJackParameters['gearRatio']
#        return(speed)
#
    def _accelerationToADT(self, accelerationInMillimetresPerSecSquared):
        '''conversion to SmartMotor units'''
        ADT = self._SMAndJackParameters['kMotor'] / \
            self._SMAndJackParameters['samplingRate'] * \
            self._SMAndJackParameters['gearRatio'] * \
            accelerationInMillimetresPerSecSquared
        return(int(ADT))

#    def _ADTToAcceleration(self, ADT):
#        acceleration = ADT / _SMAndJackParameters['kMotor'] * \
#            _SMAndJackParameters['samplingRate'] / \
#            _SMAndJackParameters['gearRatio']
#        return(acceleration)
#
    def _openSerial(self):
        '''opens serial port and sets handle'''
        self.ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, \
            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, timeout=1)
        self.ser.open()
    
    def _closeSerial(self):
        self.ser.close()

#    def turnOffSmartMotor(self):
#        self.ser.write('OFF ')

    def stopMotor(self):
        self.ser.write('X ')

#    def isHardStop(self):
#        '''if EA exceeds some threshold then assume hard stop encountered'''
#        maximumAllowableEA = 10
#        if abs(self.getEA()) > maximumAllowableEA:
#            return(True)
#        else:
#            return(False)
#
#    def isAtTargetPosition(self):
#        '''Checks to see if target position = actual position'''
#        verySmallNumberOfEncoderStripes = 10 # encoder pulses
#        PT = self.getPT()
#        PA = self.getPA()
#        encoderPulsesFromTarget = abs(PT - PA)
#        if (encoderPulsesFromTarget < verySmallNumberOfEncoderStripes):
#            return(True)
#        else:
#            return(False)
#
    def moveUpDown(self, targetPosition, speed, acceleration):
        '''Does unit conversion from SI units and then calls moveSMUnits'''
        PT = self._positionToPT(targetPosition) # positive downwards
        VT = self._speedToVT(speed)
        ADT = self._accelerationToADT(acceleration)
        self._moveSMUnits(PT, VT, ADT)

    def _moveSMUnits(self, PT, VT, ADT):
        '''Commands SmartMotor to move'''
        self.ser.write('ECHO_OFF ')
        self.ser.write('EIGN(2) EIGN(3) ZS MP ')
        self.ser.write('ADT=%.0f ' % self.smartMotorAndJackParameters['ADT'])
        self.ser.write('O=0 ')
        self.ser.write('VT=%.0f ' % self.VT)
        self.ser.write('PT=%.0f ' % self.PT)
        self.ser.write('G ')
        print('Moved motor PT=%d, VT=%d, ADT=%d' % (PT, VT, ADT))
#
#    def getEA(self):
#        '''Gets the position error from SmartMotor's internal PID loop'''
#        self.ser.write('PRINT(EA) ')
#        EA = int(self.ser.readline())
#        return(EA)
#    
#    def getPA(self):
#        '''Gets actual position of SmartMotor'''
#        self.ser.write('PRINT(PA) ')
#        PA = int(self.ser.readline())
#        return(PA)
#   
#    def getPASIUnits(self):
#        PA = self.getPA()
#        position = PTToPosition(PA)
#        return(position)
#
#    def getPT(self):
#        '''Gets target position of SmartMotor'''
#        self.ser.write('PRINT(PT) ')
#        PT = int(self.ser.readline())
#        return(PT)
#    
#    def getPTSIUnits(self):
#        PT = self.getPT()
#        position = PTToPosition(PT)
#        return(position)

    def getAnalogueMillivoltage(self, analogueInputNumber):
        '''Returns analogue input in millivolts'''
        self.ser.write('RINA(V1,%d) ' % int(analogueInputNumber))
        millivoltage = int(self.ser.readline())
        return(millivoltage)

