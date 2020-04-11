from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic, QtCore, Qt
from main import *
import easygui as eg
from Vision_Artificial.tipoDeSuelosCamaraWeb import *
import sys
import glob
import serial


class Window(QMainWindow):

    def __init__(self):
        # start QMainWindow
        QMainWindow.__init__(self)
        # load file
        uic.loadUi("window.ui", self)
        self.SerialPort = "COM3"
        self.vision_artificial = VisionArtificial()
        self.initUI()

    def initUI(self):
        #print(self.serial_ports())
        for puerto in self.serial_ports():
            self.opcionSerial.addItem(puerto)
        for i in range(4):
            self.seleccionarCamara.addItem(str(i))
        # Default Altitude
        #self.onlyInt = QIntValidator()
        #self.LineEdit.setValidator(self.onlyInt)
        self.altitude.setText('25')
        self.url_video.clicked.connect(lambda: self.predic_from_video())
        self.collect.clicked.connect(lambda: WindowPygame(self.opcionSerial.currentText()))
        self.predict_im.clicked.connect(lambda: self.predict_image())
        self.Web_Cam.clicked.connect(lambda: self.predict_webcam())

    # self.consult.clicked.connect(print('consult'))

    def predict_webcam(self):
        self.vision_artificial.predictWebCam(puertoCamara=self.seleccionarCamara.currentText())

    def predic_from_video(self):
        extension = ["*.mp4", "*.avi"]
        imagen_url = eg.fileopenbox(msg="Abrir archivo",
                                    title="Control: fileopenbox",
                                    default='',
                                    filetypes=extension)
        self.vision_artificial.predictWebCam(url_video=imagen_url)

    def predict_image(self):
        self.result.setText('Zona: '+str(self.vision_artificial.predictImage(self.altitude.text())))

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result


# start application
app = QApplication(sys.argv)
# Create object class
_window = Window()
# show window
_window.show()
app.exec_()
