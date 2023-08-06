from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
import sys


# This is the main class. This version only provides back and forward button, more coming soon
class MainWindow(QMainWindow):
    def __init__(self,link):
        super(MainWindow, self).__init__()
        self.link = link
        self.showMaximized()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(self.link))
        self.setCentralWidget(self.browser)

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('back',self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        f_btn = QAction('Forward',self)
        f_btn.triggered.connect(self.browser.forward)
        navbar.addAction(f_btn)


# use this function to execute
def execute(Name = None, link=None):
    app = QApplication(sys.argv)
    QApplication.setApplicationName(Name)
    window = MainWindow(link)
    app.exec_()


