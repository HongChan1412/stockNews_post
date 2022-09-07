import sys
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore  # QtCore를 명시적으로 보여주기 위해
from ui import Ui_MainWindow
from PyQt5 import QtWidgets
from main import stockNews 
from getData import getData
import time
from PyInstaller.utils.hooks import collect_submodules
from naver import Naver
from logger import __get_logger
logger = __get_logger()

class Worker(QObject):
    # 쓰레드의 커스텀 이벤트
    # 데이터 전달 시 형을 명시해야 함
    threadEvent = QtCore.pyqtSignal(int)
    progress_start = QtCore.pyqtSignal(str)
    progress = QtCore.pyqtSignal(str)
    finished = pyqtSignal()
    quit_process = 0
    def run(self):
        try:
            i = 0
            self.progress_start.emit("작동중")
            posted_title = []
            naver = Naver(self.id, self.pw, self.proxyLIST)
            if naver.login() :
                while 1:
                    try:
                        if naver.is_logged_in() :
                            if self.quit_process == 1 :
                                break
                            res, title, posted_title = stockNews(self.url, self.delay, posted_title, self.keywords, naver, self.stockdata, self.titleform, self.ipo_search)
                            if res == None:
                                text ="포스팅 실패 다시 실행중"
                                self.progress.emit(text)
                            elif res == -1 :
                                text = "포스팅 실패! 글쓰기 권한이 없음! 게시판 새로 선택!"
                                self.progress.emit(text)
                                self.finished.emit()
                                break
                            elif res == -2 :
                                text = "뉴스 가져오기 실패 다시 실행중"
                                self.progress.emit(text)
                            else : 
                                i += 1
                                now =time.localtime()
                                time_ = f"%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)  
                                text = f"{title}\n포스팅 완료!\n현재까지{i}개 포스팅 성공! {time_}"
                                self.progress.emit(text)
                            time.sleep(10)
                        else : naver.login
                    except Exception as e:
                        self.progress.emit(f"※오류발생※\n{e.args}")
                        logger.error(e.args)
                self.finished.emit()
            else :
                text = "로그인 실패! 아이디와 비밀번호 확인"
                self.progress.emit(text)
                naver.driver.quit()
                self.finished.emit()
        except  Exception as e:
            self.progress.emit(f"※오류발생※\n{e.args}")
            logger.error(e.args)
            self.finished.emit()
            naver.driver.quit()
                
class WindowClass(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.run_flag = 0
        self.stockdata = []
        self.url = ""
        self.proxyLIST = ""
        self.delayChk2.setDisabled(True)
        self.startPause.clicked.connect(self.run_click)
        self.delayChk.activated.connect(self.delay_select)
        self.cafeChk.clicked.connect(self.cafe_Pressed)
        self.boardChk.activated.connect(self.menu_select)
        self.selectData.clicked.connect(self.stockdata_select)
        self.resetData.clicked.connect(self.reset_stockdata)
        self.radioButton.clicked.connect(self.ipo_search)
        self.proxycombo.activated.connect(self.selectPROXY)
        self.naverId.setPlaceholderText("네이버ID 입력")
        self.naverPw.setPlaceholderText("네이버PW 입력")
        self.cafeUrl.setPlaceholderText("네이버 카페 url 입력후 확인버튼 클릭후 게시판 선택")
        self.addKeyword.setPlaceholderText("추가할 키워드 있으면 입력")
        self.log.setText("""※유의사항※
키워드 추가: 스페이스바(" ")로 구분함
종목 데이터 선택: 필수로 kospi,kosdaq,konex,k-otc,unlist중 파일 선택 (복수선택 가능)
종목 데이터 선택: 취소할때는 종목 데이터 초기화 버튼 클릭 (다시 종목 데이터 선택 필요)
제목 형식 입력: '(종목) (입력한 제목 형식) : (기사제목)'으로 글 제목이 설정되기 때문에 (입력한 제목 형식)에 들어갈 단어 입력, 빈칸으로두면 기사 제목으로만 포스팅 예)주가 분석,주가 전망 뉴스
ipoStock 공모주 뉴스: 38커뮤니케이션에 올라온 비상장 뉴스를 크롤링해 네이버에 검색후 연관된 뉴스 포스팅 
""")
    def progress_emited(self, text) :
        self.log.append(text)

    def run_click(self) :
        if self.run_flag == 0 :
            if self.delayChk.currentText() == "직접입력":
                self.delay = self.delayChk2.text()
            
            else:
                self.delay = self.delayChk.currentText()
            
            self.id = self.naverId.text()
            self.pw = self.naverPw.text()
            self.keywords = self.addKeyword.text().split(" ")
            self.titleform = self.titleForm.text()
            self.proxyOPT = self.proxycombo.currentText()
            if self.delay == "":
                self.progress_emited("크롤링 간격을 입력해주세요")
                return
            if self.id == "":
                self.progress_emited("ID를 입력해주세요")
                return
            if self.pw == "":
                self.progress_emited("PW를 입력해주세요")
                return
            
            if self.cafeUrl.text() == "":
                self.progress_emited("카페주소를 입력해주세요")
                return
            if self.url == "":
                self.progress_emited("확인버튼을 누른후 게시판을 선택해주세요")
                return
            
            if self.radioButton.isChecked():
                self.progress_emited(f"ID: {self.id}\nPW: {self.pw}\n게시판: {self.text}\n크롤링 간격: {self.delay}분\n")
                pass
            
            else:
                if self.stockdata == []:
                    self.progress_emited("종목 데이터를 입력해주세요")
                    return

                self.progress_emited(f"ID: {self.id}\nPW: {self.pw}\n게시판: {self.text}\n제목 형식: {self.titleform}\n종목 데이터: {self.stockdata}\n크롤링 간격: {self.delay}분\n키워드: {self.keywords}\n프록시 선택:{self.proxyOPT}")
            
            self.thread = QThread()
            self.startPause.setText('■')
            self.worker = Worker()
            self.worker.moveToThread(self.thread)
            self.run_flag = 1
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.progress.connect(self.progress_emited)
            self.thread.start()
            self.thread.finished.connect(
                lambda : self.progress_emited('프로세스 종료 완료.')
            )
            self.thread.finished.connect(self.threadFinished)
            self.worker.id = self.id
            self.worker.pw = self.pw
            self.worker.delay = int(self.delay)
            self.worker.keywords = self.keywords
            self.worker.url = self.url
            self.worker.stockdata = self.stockdata
            self.worker.titleform = self.titleform
            self.worker.ipo_search = self.radioButton.isChecked()
            self.worker.proxyLIST = self.proxyLIST
        else :
            self.worker.quit_process = 1
            self.progress_emited("현재 수행 작업 후 종료됩니다.")
            
    def threadFinished(self) :
        self.run_flag = 0
        self.startPause.setText('▶')

    def cafe_Pressed(self) :
        cafetitle, menutitle, menuid = getData(self.cafeUrl.text())
        self.boardChk.clear()
        for i in range(len(menutitle)) :
            self.boardChk.addItem(menutitle[i])
            
    def menu_select(self) :
        self.text = str(self.boardChk.currentText())
        cafetitle, menutitle, menuid = getData(self.cafeUrl.text())
        for i in range(len(menutitle)) :
            if self.text == menutitle[i] :
                self.url = f"https://cafe.naver.com/ca-fe/cafes/{cafetitle}/menus/{menuid[i]}/articles/write?boardType=L"

    def delay_select(self) :
        self.postdelay = self.delayChk.currentText()
        if self.postdelay == "직접입력":
            self.delayChk2.setEnabled(True)
        else:
            self.delayChk2.setDisabled(True)
            self.delayChk2.clear()
    
    def input_delay(self):
        self.postdelay = self.delayChk2.currentText()

    def ipo_search(self):
        if self.radioButton.isChecked():
            self.titleForm.clear()
            self.titleForm.setDisabled(True)
            self.selectData.setDisabled(True)
            self.resetData.setDisabled(True)
            self.addKeyword.setDisabled(True)
            self.addKeyword.clear()
        else:
            self.titleForm.setDisabled(False)
            self.selectData.setDisabled(False)
            self.resetData.setDisabled(False)
            self.addKeyword.setDisabled(False)
            
    def stockdata_select(self):
        try:
            fname = QtWidgets.QFileDialog.getOpenFileName(self, "종목 데이터 리스트 선택","","Excel Files (*.csv)")
            self.progress_emited(f"종목 데이터 불러오기 완료 >> {fname[0]}")
            self.stockdata.append(fname[0])
        except Exception as e:  
            logger.error(e.args) 
    
    def reset_stockdata(self):
        self.progress_emited("종목 데이터 초기화 완료")
        self.stockdata = []

    def selectPROXY(self):
        try:
            self.proxyOPT = self.proxycombo.currentText()
            if self.proxyOPT == "IP 리스트 선택":
                fname = QtWidgets.QFileDialog.getOpenFileName(self, "IP 리스트 선택","","Text (*.txt)")
                self.proxyLIST = fname[0]
                if not self.proxyLIST:
                    self.proxycombo.setCurrentText("자체 IP 변경")
                else:
                    self.progress_emited(f"IP 리스트 불러오기 완료 >> {fname[0]}")
        except Exception as e:  
            logger.error(e.args)  
    
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    
    sys.exit(app.exec_())
    