# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(660, 550)
        MainWindow.setMinimumSize(QtCore.QSize(660, 550))
        MainWindow.setMaximumSize(QtCore.QSize(660, 550))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.naverIdLabel = QtWidgets.QLabel(self.centralwidget)
        self.naverIdLabel.setGeometry(QtCore.QRect(10, 10, 91, 22))
        self.naverIdLabel.setObjectName("naverIdLabel")
        self.naverPwLabel = QtWidgets.QLabel(self.centralwidget)
        self.naverPwLabel.setGeometry(QtCore.QRect(300, 10, 91, 22))
        self.naverPwLabel.setObjectName("naverPwLabel")
        self.naverPw = QtWidgets.QLineEdit(self.centralwidget)
        self.naverPw.setGeometry(QtCore.QRect(410, 10, 151, 22))
        self.naverPw.setObjectName("naverPw")
        self.naverId = QtWidgets.QLineEdit(self.centralwidget)
        self.naverId.setGeometry(QtCore.QRect(110, 10, 151, 22))
        self.naverId.setObjectName("naverId")
        self.cafeUrlLabel = QtWidgets.QLabel(self.centralwidget)
        self.cafeUrlLabel.setGeometry(QtCore.QRect(10, 40, 92, 22))
        self.cafeUrlLabel.setObjectName("cafeUrlLabel")
        self.cafeUrl = QtWidgets.QLineEdit(self.centralwidget)
        self.cafeUrl.setGeometry(QtCore.QRect(110, 40, 351, 22))
        self.cafeUrl.setObjectName("cafeUrl")
        self.cafeChk = QtWidgets.QPushButton(self.centralwidget)
        self.cafeChk.setGeometry(QtCore.QRect(490, 40, 73, 24))
        self.cafeChk.setObjectName("cafeChk")
        self.boardChkLabel = QtWidgets.QLabel(self.centralwidget)
        self.boardChkLabel.setGeometry(QtCore.QRect(10, 70, 91, 22))
        self.boardChkLabel.setObjectName("boardChkLabel")
        self.boardChk = QtWidgets.QComboBox(self.centralwidget)
        self.boardChk.setGeometry(QtCore.QRect(110, 70, 211, 22))
        self.boardChk.setObjectName("boardChk")
        self.delayChk = QtWidgets.QComboBox(self.centralwidget)
        self.delayChk.setGeometry(QtCore.QRect(430, 70, 71, 22))
        self.delayChk.setObjectName("delayChk")
        self.delayChk.addItem("")
        self.delayChk.addItem("")
        self.delayChk.addItem("")
        self.delayChk.addItem("")
        self.delayChkLabel = QtWidgets.QLabel(self.centralwidget)
        self.delayChkLabel.setGeometry(QtCore.QRect(330, 70, 91, 22))
        self.delayChkLabel.setObjectName("delayChkLabel")
        self.log = QtWidgets.QTextBrowser(self.centralwidget)
        self.log.setGeometry(QtCore.QRect(10, 200, 641, 341))
        self.log.setObjectName("log")
        self.startPause = QtWidgets.QPushButton(self.centralwidget)
        self.startPause.setGeometry(QtCore.QRect(581, 9, 71, 151))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.startPause.setFont(font)
        self.startPause.setObjectName("startPause")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(560, 10, 20, 181))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.delayChk2 = QtWidgets.QLineEdit(self.centralwidget)
        self.delayChk2.setGeometry(QtCore.QRect(510, 70, 51, 22))
        self.delayChk2.setObjectName("delayChk2")
        self.addKeyword = QtWidgets.QLineEdit(self.centralwidget)
        self.addKeyword.setGeometry(QtCore.QRect(110, 100, 301, 21))
        self.addKeyword.setObjectName("addKeyword")
        self.selectDataLabel = QtWidgets.QLabel(self.centralwidget)
        self.selectDataLabel.setGeometry(QtCore.QRect(10, 130, 101, 22))
        self.selectDataLabel.setObjectName("selectDataLabel")
        self.selectData = QtWidgets.QPushButton(self.centralwidget)
        self.selectData.setGeometry(QtCore.QRect(110, 130, 91, 24))
        self.selectData.setObjectName("selectData")
        self.addKeywordLabel = QtWidgets.QLabel(self.centralwidget)
        self.addKeywordLabel.setGeometry(QtCore.QRect(10, 100, 91, 22))
        self.addKeywordLabel.setObjectName("addKeywordLabel")
        self.resetData = QtWidgets.QPushButton(self.centralwidget)
        self.resetData.setGeometry(QtCore.QRect(210, 130, 111, 24))
        self.resetData.setObjectName("resetData")
        self.titleFromLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleFromLabel.setGeometry(QtCore.QRect(330, 130, 81, 22))
        self.titleFromLabel.setObjectName("titleFromLabel")
        self.titleForm = QtWidgets.QLineEdit(self.centralwidget)
        self.titleForm.setGeometry(QtCore.QRect(420, 130, 141, 21))
        self.titleForm.setObjectName("titleForm")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(420, 100, 151, 20))
        self.radioButton.setObjectName("radioButton")
        self.proxyLabel = QtWidgets.QLabel(self.centralwidget)
        self.proxyLabel.setGeometry(QtCore.QRect(10, 160, 92, 22))
        self.proxyLabel.setObjectName("proxyLabel")
        self.proxycombo = QtWidgets.QComboBox(self.centralwidget)
        self.proxycombo.setGeometry(QtCore.QRect(110, 160, 91, 22))
        self.proxycombo.setObjectName("proxycombo")
        self.proxycombo.addItem("")
        self.proxycombo.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.delayChk.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "주식뉴스포스팅"))
        self.naverIdLabel.setText(_translate("MainWindow", "ID"))
        self.naverPwLabel.setText(_translate("MainWindow", "PW"))
        self.cafeUrlLabel.setText(_translate("MainWindow", "네이버 카페 주소"))
        self.cafeChk.setText(_translate("MainWindow", "확인"))
        self.boardChkLabel.setText(_translate("MainWindow", "게시판 선택"))
        self.delayChk.setItemText(0, _translate("MainWindow", "10"))
        self.delayChk.setItemText(1, _translate("MainWindow", "30"))
        self.delayChk.setItemText(2, _translate("MainWindow", "60"))
        self.delayChk.setItemText(3, _translate("MainWindow", "직접입력"))
        self.delayChkLabel.setText(_translate("MainWindow", "크롤링 간격(분)"))
        self.startPause.setText(_translate("MainWindow", "▶"))
        self.selectDataLabel.setText(_translate("MainWindow", "종목 데이터 선택"))
        self.selectData.setText(_translate("MainWindow", ".csv 파일 선택"))
        self.addKeywordLabel.setText(_translate("MainWindow", "키워드 추가"))
        self.resetData.setText(_translate("MainWindow", "종목 데이터 초기화"))
        self.titleFromLabel.setText(_translate("MainWindow", "제목 형식 입력"))
        self.radioButton.setText(_translate("MainWindow", "ipoStock 공모주 뉴스"))
        self.proxyLabel.setText(_translate("MainWindow", "프록시 선택"))
        self.proxycombo.setItemText(0, _translate("MainWindow", "자체 IP 변경"))
        self.proxycombo.setItemText(1, _translate("MainWindow", "IP 리스트 선택"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())