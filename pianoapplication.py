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
sfid = fs.sfload("regular_piano.sf2")  # Selects the regular piano soundfont
fs.program_select(0, sfid, 0, 0) # Sets the channel, bank, and preset to 0 and loads the piano soundfont

# Lists of all the MIDI key numbers and all the Qt Keys 
midiNaturalList = [48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83]
midiAccidentalList = [49, 51, 54, 56, 58, 61, 63, 66, 68, 70, 73, 75, 78, 80, 82]
naturalKeyList = [Qt.Key_A, Qt.Key_S, Qt.Key_D, Qt.Key_F, Qt.Key_G, Qt.Key_H, Qt.Key_J, Qt.Key_K, Qt.Key_L, Qt.Key_Semicolon, Qt.Key_Apostrophe, Qt.Key_Z, Qt.Key_X, Qt.Key_C, Qt.Key_V, Qt.Key_B, Qt.Key_N, Qt.Key_M, Qt.Key_Comma, Qt.Key_Period, Qt.Key_Backslash]
accidentalKeyList = [Qt.Key_Q, Qt.Key_W, Qt.Key_E, Qt.Key_R, Qt.Key_T, Qt.Key_Y, Qt.Key_U, Qt.Key_I, Qt.Key_O, Qt.Key_P, Qt.Key_BracketLeft, Qt.Key_BracketRight]


class Window(QMainWindow): 
    def __init__(self, sfid): 
        super().__init__() 
        ## Sets the title of the window
        self.setWindowTitle("Piano") 
        ## Sets the size of the window
        self.setFixedSize(1255,720)
        self.keyboard() 
        self.show() 
        self.sfid = sfid
    def keyboard(self): 
            ## Creates a list of Qt buttons for the natural keys, puts the buttons
            ## in a list, resizes them, and associates them with a function (buttonCallbackNatural)
            ## that plays a note when they are pressed
            naturalKeys = []
            for i in range(21):
                naturalKeys.append(QPushButton("", self)) 
                naturalKeys[-1].move(100 + i*50,150)
                naturalKeys[-1].resize(52, 350) 
                naturalKeys[-1].clicked.connect(self.buttonCallbackNatural(i))
            ## Creates a list of Qt buttons for the accidental keys, puts the buttons
            ## in a list, resizes them, and associates them with a function (buttonCallbackNAccidental)
            ## that plays a note when they are pressed
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
            ## Makes the accidental piano keys black and rounded
            for key in accidentalKeys:
                key.setStyleSheet('''QPushButton {
                                        background-color: rgb(55, 55, 55) ;
                                        border-radius: 5px;
                                    }''')        
                
            ## Creates buttons to switch between the different soundfonts, these buttons are connected
            ## to functions that actually switch the soundfont file being used
            nintendoButton = QPushButton("Nintendo", self)
            nintendoButton.clicked.connect(lambda: self.switchToNintendo())
            nintendoButton.move(100,50)

            regularButton = QPushButton("Regular", self)
            regularButton.clicked.connect(lambda: self.switchToRegular())
            regularButton.move(210,50)

            kalimbaButton = QPushButton("Kalimba", self)
            kalimbaButton.clicked.connect(lambda: self.switchToKalimba())
            kalimbaButton.move(320,50)

            drumsButton = QPushButton("Drums", self)
            drumsButton.clicked.connect(lambda: self.switchToDrums())
            drumsButton.move(430,50)

            customButton = QPushButton("Custom", self)
            customButton.clicked.connect(lambda: self.switchToCustom())
            customButton.move(540,50)

            ## Creating the instructions label
            label = QLabel("You can play notes by both either clicking on the keys above or using your keyboard.\n\nTo play the white keys using your keyboard, you can use keys A-L, semicolon, apostrophe, Z-M,\ncomma, period, and backslash.\n\nTo play the black keys, you can use keys Q-P and both the bracket keys",self)
            label.resize(1100, 200) 
            label.move(100,500)
            label.setFont(QFont('Arial', 13)) 

            showHideButton = QPushButton("Show/Hide Instructions", self)
            showHideButton.move(993,50)
            showHideButton.resize(160,30)
            showHideButton.clicked.connect(lambda: self.showHideClick(label))


    ## Checks for keyboard inputs and plays the corresponding notes associated with the keyboard key
    def keyPressEvent(self, keyEvent):
        for i in range(21):
            if keyEvent.key()  == naturalKeyList[i]:
                self.startNoteThread(midiNaturalList[i])
        for i in range(12):
            if keyEvent.key()  == accidentalKeyList[i]:
                self.startNoteThread(midiAccidentalList[i])
                
    ## These functions create threads so multiple keys can be played at once without stopping the program
    ## whenever time.sleep() runs
    def buttonCallbackNatural(self, i):
        return lambda: self.startNoteThread(midiNaturalList[i])
    
    def buttonCallbackAccidental(self, i):
        return lambda: self.startNoteThread(midiAccidentalList[i])
    def startNoteThread(self, key):

        noteThread = threading.Thread(target=self.playsound, args=(key,))
        noteThread.start()

    ## Plays a note with the corresponding key number
    def playsound(self, key): 
        fs.noteon(0, key, 30)
        time.sleep(3.0)
        fs.noteoff(0, key)


    ## These functions unload the current soundfont and load a new one based on the file name
    def switchToNintendo(self):
        fs.sfunload(self.sfid)
        sfid = fs.sfload("nintendo_soundfont.sf2")  
        fs.program_select(0, sfid, 0, 0) 
    def switchToRegular(self):
        fs.sfunload(self.sfid)
        sfid = fs.sfload("regular_piano.sf2")  
        fs.program_select(0, sfid, 0, 0) 
    def switchToDrums(self):
        fs.sfunload(self.sfid)
        sfid = fs.sfload("drums.sf2")  
        fs.program_select(0, sfid, 0, 0) 
    def switchToKalimba(self):
        fs.sfunload(self.sfid)
        sfid = fs.sfload("kalimba.sf2")  
        fs.program_select(0, sfid, 0, 0) 
    def switchToCustom(self):
        fs.sfunload(self.sfid)
        sfid = fs.sfload("custom.sf2")  
        fs.program_select(0, sfid, 0, 0) 
        
    def showHideClick(self, label):
        if label.isVisible():
            label.setHidden(True)
        else:
            label.setHidden(False)

# Creates a window object and runs the app
window = Window(sfid)
app.exec()