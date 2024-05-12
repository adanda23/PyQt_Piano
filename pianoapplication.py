from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import time
import fluidsynth
import threading

app = QApplication([])
fs = fluidsynth.Synth()
fs.start(driver = 'dsound')  # use DirectSound driver
sfid = fs.sfload("FluidR3_GM.sf2")  # replace path as needed
fs.program_select(0, sfid, 0, 0)

midiNoteList = [48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83]

#8
class Window(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        self.setWindowTitle("Piano") 
        self.resize(1255,720)
        self.keyboard() 
        self.show() 

    def keyboard(self): 
            naturalKeys = []
            for i in range(21):
                naturalKeys.append(QPushButton("", self)) 
                naturalKeys[-1].move(100 + i*50,150)
                naturalKeys[-1].resize(52, 350) 
                naturalKeys[-1].clicked.connect(self.buttonCallback(i))
            accidentalKeys = []
            for i in range(3):
                accidentalKeys.append(QPushButton("", self)) 
                accidentalKeys.append(QPushButton("", self)) 
                accidentalKeys[-1].move(133 + i*350,150)
                accidentalKeys[-2].move(133 + 50 + i*350,150)
                accidentalKeys[-1].resize(36, 175) 
                accidentalKeys[-2].resize(36, 175) 
            for i in range(3):
                accidentalKeys.append(QPushButton("", self)) 
                accidentalKeys.append(QPushButton("", self)) 
                accidentalKeys.append(QPushButton("", self)) 
                accidentalKeys[-1].move(283 + i*350,150)
                accidentalKeys[-2].move(283 + 50 + i*350,150)
                accidentalKeys[-3].move(283 + 100 + i*350,150)
                accidentalKeys[-1].resize(36, 175) 
                accidentalKeys[-2].resize(36, 175) 
                accidentalKeys[-3].resize(36, 175) 
            for key in accidentalKeys:
                key.setStyleSheet('''QPushButton {
                                        background-color: rgb(55, 55, 55) ;
                                        border-radius: 5px;
                                    }''')



    def buttonCallback(self, i):
        return lambda: self.startNoteThread(midiNoteList[i])

    def startNoteThread(self, key):
        noteThread = threading.Thread(target=self.playsound, args=(key,))
        noteThread.start()

    def playsound(self, key): 
        fs.noteon(0, key, 30)
        time.sleep(3.0)
        fs.noteoff(0, key)


        

window = Window()



app.exec()