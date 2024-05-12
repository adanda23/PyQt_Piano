from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import time
import fluidsynth
import threading

app = QApplication([]) # Initializing Qt 
fs = fluidsynth.Synth() # Initalizing fluidsynth
fs.setting('synth.gain', 10.0 ) # Setting gain to be higher
fs.start(driver = 'dsound')  # use DirectSound driver
sfid = fs.sfload("regular_piano.sf2")  
fs.program_select(0, sfid, 0, 0)

midiNaturalList = [48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83]
midiAccidentalList = [49, 51, 54, 56, 58, 61, 63, 66, 68, 70, 73, 75, 78, 80, 82]

class Window(QMainWindow): 
    def __init__(self, sfid): 
        super().__init__() 
        self.setWindowTitle("Piano") 
        self.setFixedSize(1255,720)
        self.keyboard() 
        self.show() 
        self.sfid = sfid
        
    def keyboard(self): 
            ##    
            naturalKeys = []
            for i in range(21):
                naturalKeys.append(QPushButton("", self)) 
                naturalKeys[-1].move(100 + i*50,150)
                naturalKeys[-1].resize(52, 350) 
                naturalKeys[-1].clicked.connect(self.buttonCallbackNatural(i))
            ##
            accidentalKeys = []
            for i in range(3):
                for j in range(2):
                    accidentalKeys.append(QPushButton("", self))
                    accidentalKeys[-1].move(133 + j*50 + i*350, 150) 
                    accidentalKeys[-1].resize(36, 175) 
                    accidentalKeys[-1].clicked.connect(self.buttonCallbackAccidental(i*5+j))
            for i in range(3):
                for j in range(3):
                    accidentalKeys.append(QPushButton("", self))
                    accidentalKeys[-1].move(283 + j*50 + i*350, 150) 
                    accidentalKeys[-1].resize(36, 175) 
                    accidentalKeys[-1].clicked.connect(self.buttonCallbackAccidental(i*5+j+2))
            for key in accidentalKeys:
                key.setStyleSheet('''QPushButton {
                                        background-color: rgb(55, 55, 55) ;
                                        border-radius: 5px;
                                    }''')        
                
            nintendoButton = QPushButton("Nintendo", self)
            nintendoButton.clicked.connect(lambda: self.switchToNintendo())
            nintendoButton.move(100,50)

            regularButton = QPushButton("Regular", self)
            regularButton.clicked.connect(lambda: self.switchToRegular())
            regularButton.move(210,50)


    def buttonCallbackNatural(self, i):
        return lambda: self.startNoteThread(midiNaturalList[i])

    def buttonCallbackAccidental(self, i):
        return lambda: self.startNoteThread(midiAccidentalList[i])
    
    def startNoteThread(self, key):
        noteThread = threading.Thread(target=self.playsound, args=(key,))
        noteThread.start()

    def playsound(self, key): 
        fs.noteon(0, key, 30)
        time.sleep(3.0)
        fs.noteoff(0, key)

    def switchToNintendo(self):
        fs.sfunload(self.sfid)
        sfid = fs.sfload("nintendo_soundfont.sf2")  
        fs.program_select(0, sfid, 0, 0) 
    def switchToRegular(self):
        fs.sfunload(self.sfid)
        sfid = fs.sfload("regular_piano.sf2")  
        fs.program_select(0, sfid, 0, 0) 
        
        

window = Window(sfid)

app.exec()