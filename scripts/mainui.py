#Code By Puron and his team
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
import pyttsx3
engine = pyttsx3.init()
engine.say("LinkedIn Automation Software Is Opening")
engine.runAndWait()
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(848, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 850, 650))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../ui/scanner.gif"))
        self.movie = QMovie("../ui/scanner.gif")
        self.label.setMovie(self.movie)
        self.movie.start()
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 500, 131, 51))
        font = QtGui.QFont()
        font.setFamily("ROG Fonts")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setCheckable(True)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setObjectName("Start")
        self.pushButton.clicked.connect(self.fun1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 570, 131, 51))
        font = QtGui.QFont()
        font.setFamily("ROG Fonts")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setObjectName("Exit")
        self.pushButton_2.clicked.connect(self.fun2)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 0, 781, 131))
        font = QtGui.QFont()
        font.setFamily("ROG Fonts")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel {\n"
"color: white;\n"
"border:2 px;\n"
"}")
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setLineWidth(3)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 110, 781, 131))
        font = QtGui.QFont()
        font.setFamily("ROG Fonts")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("QLabel {\n"
"color: white;\n"
"border:2 px;\n"
"}")
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setLineWidth(3)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(410, 50, 781, 131))
        font = QtGui.QFont()
        font.setFamily("ROG Fonts")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("QLabel {\n"
"color: white;\n"
"border:2 px;\n"
"}")
        self.label_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_4.setLineWidth(3)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))
        self.label_2.setText(_translate("MainWindow", "Face Recognition"))
        self.label_3.setText(_translate("MainWindow", "Attendance System"))
        self.label_4.setText(_translate("MainWindow", "&"))



    def fun2(self):
        sys.terminate(all())

    def  fun1(self):
        import cv2
        import numpy as np
        import face_recognition
        import os
        from datetime import datetime
        import pyttsx3
        engine = pyttsx3.init()
        path = "C:/Users/pc/PycharmProjects/face/Picture"
        images = []
        personNames = []
        myList = os.listdir(path)
        print(myList)
        for cu_img in myList:
            current_Img = cv2.imread(f'{path}/{cu_img}')
            images.append(current_Img)
            personNames.append(os.path.splitext(cu_img)[0])
        print(personNames)

        def faceEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def attendance(name):
            with open('Attendance.csv', 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
                if name not in nameList:
                    time_now = datetime.now()
                    tStr = time_now.strftime('%H:%M:%S')
                    dStr = time_now.strftime('%d/%m/%Y')
                    f.writelines(f'\n{name},{tStr},{dStr}')

        encodeListKnown = faceEncodings(images)
        print('All Encodings Complete!!!')

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

            facesCurrentFrame = face_recognition.face_locations(faces)
            encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

            for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)

                if faceDis[matchIndex] < 0.50:
                    name = personNames[matchIndex].upper()

                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    attendance(name)
                    engine.say("Hello" + name + " sir.Your attendence is recorded.Have a great day.")
                    engine.runAndWait()
                else:
                    engine.say("Sir you are a newcomer please complete your registration  to our system")
                    engine.runAndWait()

            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) == 13:
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())