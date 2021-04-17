from PyQt5.QtCore import Qt, QThread, QTimer, QDir, pyqtSignal, QUrl
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QDesktopServices
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import os
import random
# from generator_emp
# from pyqtgraph import ImageItem


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()

        self.answers = {
            "0.mp4": "Dalla Dalla - Itzy",
            "1.mp4": "Gashina - Sunmi",
            "2.mp4": "Heart Shaker - Twice",
            "3.mp4": "Kill This Love - Blackpink",
            "4.mp4": "Psycho - Red Velvet",
            "5.mp4": "Red Flavor - Red Velvet",
            "6.mp4": "What is Love - Twice"
        }
        # Logo up top
        labelImage = QLabel()
        pixmap = QPixmap("logo.png")
        pixmap = pixmap.scaledToWidth(100)
        labelImage.setPixmap(pixmap)
        
        # Text on right of logo
        name_of_app = QLabel('Guess That Song!')
        learn_more = QPushButton("Learn More")
        width = learn_more.fontMetrics().boundingRect('Learn More').width() + 12
        learn_more.setMaximumWidth(width)
        # name_of_app.setIndent(3)
        top_font = QFont("Helvetica", 30, QFont.Bold)
        name_of_app.setFont(top_font)

        # Layout up top
        top_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        right_button_layout = QHBoxLayout()
        right_button_layout.setAlignment(Qt.AlignRight)
        top_layout.addWidget(labelImage)
        right_layout.addWidget(name_of_app)
        right_button_layout.addWidget(learn_more)
        right_layout.addLayout(right_button_layout)
        top_layout.addLayout(right_layout)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
       
        # List of Videos
        self.vidList = [os.path.abspath(os.path.join("videos/", f)) for f in os.listdir("videos/")]
        random.shuffle(self.vidList)
        # Labels for inputs
        self.question = QLabel()
        self.status = QLabel()
        status_font = QFont("Helvetica", 12, QFont.Bold)
        self.status.setFont(status_font)
        self.answer_group = QButtonGroup()
        self.a1 = QRadioButton("a.")
        self.a2 = QRadioButton("b.")
        self.a3 = QRadioButton("c.")
        self.a4 = QRadioButton("d.")

        self.answer_group.addButton(self.a1)
        self.answer_group.addButton(self.a2)
        self.answer_group.addButton(self.a3)
        self.answer_group.addButton(self.a4)
     
        self.submit = QPushButton('Submit')
        width = self.submit.fontMetrics().boundingRect('Submit').width() + 12
        self.submit.setMaximumWidth(width)

        # Frame for email and password forms
        frame1 = QFrame(self.central_widget)
        frame1.setFrameShape(QFrame.StyledPanel)
        frame1.setFrameShadow(QFrame.Raised)
        questionLayout = QVBoxLayout()
        frame1Layout = QVBoxLayout()
        choiceLayout = QVBoxLayout()
        submitLayout = QVBoxLayout()
        statusLayout = QVBoxLayout()
        questionLayout.addWidget(self.question)
        choiceLayout.addWidget(self.a1)
        choiceLayout.addWidget(self.a2)
        choiceLayout.addWidget(self.a3)
        choiceLayout.addWidget(self.a4)
        submitLayout.addWidget(self.submit)
        statusLayout.addWidget(self.status)
        questionLayout.setAlignment(Qt.AlignCenter)
        choiceLayout.setAlignment(Qt.AlignCenter)
        submitLayout.setAlignment(Qt.AlignCenter)
        statusLayout.setAlignment(Qt.AlignCenter)
        frame1Layout.addLayout(questionLayout)
        frame1Layout.addLayout(choiceLayout)
        frame1Layout.addLayout(submitLayout)
        frame1Layout.addLayout(statusLayout)
        frame1Layout.setAlignment(Qt.AlignCenter)

        
        frame1.setLayout(frame1Layout)
        frame1Layout.addStretch()

       
        # Frame for email and nt3 data paths
        frame2 = QFrame(self.central_widget)
        frame2.setFrameShape(QFrame.StyledPanel)
        frame2.setFrameShadow(QFrame.Raised)

        frame2Layout = QVBoxLayout()
        frame2Layout.addWidget(self.videoWidget)
        
        frame2.setLayout(frame2Layout)

        self.progressBar = QProgressBar()
        self.progressBar.setMaximum(len(self.vidList))
        self.progressBar.setValue(0)
        self.submit.clicked.connect(self.check)
        learn_more.clicked.connect(self.learn_more_dialog)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addLayout(top_layout)
        self.layout.addWidget(frame1)
        self.layout.addWidget(frame2)
        self.layout.addWidget(self.progressBar)
        self.setCentralWidget(self.central_widget)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.mediaStatusChanged.connect(self.loop)
 
        self.item = 1
        self.score = 0
        self.play(self.vidList[self.item-1], self.item)

    def play(self, song, item):
        self.question.setText("{}. What song is the figure dancing?".format(item))
        self.answer = self.answers[song.split("/")[-1]]
        self.items = [self.answer]
        while len(self.items) != 4:
            random_ans = self.answers[random.choice(list(self.answers.keys()))]
            if random_ans not in self.items:
                self.items.append(random_ans)
        random.shuffle(self.items)
        self.a1.setText("a. {}".format(self.items[0]))
        self.a2.setText("b. {}".format(self.items[1]))
        self.a3.setText("c. {}".format(self.items[2]))
        self.a4.setText("d. {}".format(self.items[3]))
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(song)))
        self.mediaPlayer.play()
    
    def check(self):
        user_answer = self.answer_group.checkedButton().text()[3:]
        self.item += 1
        self.progressBar.setValue(self.progressBar.value()+1)
        if user_answer == self.answer:
            self.score += 1
            self.status.setStyleSheet("color: green;")
            self.status.setText("Correct!")
        else:
            self.status.setStyleSheet("color: red;")
            self.status.setText("Wrong!")
        if self.item >= len(self.vidList)+1:
            self.submit.setEnabled(False)
            self.status.setStyleSheet("color: black;")
            if self.score >= len(self.vidList) // 2:
                self.status.setText("DONE! Youre score is:{}/{}. Good Job! :D".format(self.score,len(self.vidList)))
            else:
                self.status.setText("DONE! Youre score is:{}/{}. Better luck next time! :(".format(self.score,len(self.vidList)))
        else:
            self.play(self.vidList[self.item-1], self.item)
    
    def loop(self, status):
        if status == 7:
            self.mediaPlayer.play()

    def learn_more_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("<b>AI4U</b><br><br>This is a project by Renzo Benemerito. Learn more in his blogpost <a href='http://renzobenemerito.github.io'>here.</a>")
        msg.setInformativeText("")
        msg.setWindowTitle("Learn More")
        msg.exec()

    def link(self, linkStr):
        QDesktopServices.openUrl(QUrl(linkStr))
