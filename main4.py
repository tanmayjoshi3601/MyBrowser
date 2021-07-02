# importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys

# main window
class MainWindow(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # creating a tab widget
        self.tabs = QTabWidget()

        self.setWindowIcon(QIcon('logo2.png'))

        # making document mode true
        self.tabs.setDocumentMode(True)

        # adding action when double clicked
        #self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)


        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)

        # making tabs closeable
        self.tabs.setTabsClosable(True)

        # adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # making tabs as central widget
        self.setCentralWidget(self.tabs)

        # creating a status bar
        self.status = QStatusBar()

        # setting status bar to the main window
        self.setStatusBar(self.status)

        # creating a tool bar for navigation
        navtb = QToolBar("Navigation")

        # adding tool bar tot he main window
        self.addToolBar(navtb)



        # creating back action
        back_key = QAction("Back", self)
        back_key.setIcon(QIcon('back.png'))
        # setting status tip
        back_key.setStatusTip("Back to previous page")

        # adding action to back button
        # making current tab to go back
        back_key.triggered.connect(lambda: self.tabs.currentWidget().back())

        # adding this to the navigation tool bar
        navtb.addAction(back_key)

        # similarly adding next button
        forward_key = QAction("Forward", self)
        forward_key.setIcon(QIcon('forward.png'))
        forward_key.setStatusTip("Forward to next page")
        forward_key.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(forward_key)

        # similarly adding reload button
        reload_key = QAction("Reload", self)
        reload_key.setIcon(QIcon('refresh.png'))
        reload_key.setStatusTip("Reload page")
        reload_key.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_key)

        # creating home action
        home_key = QAction("Home", self)
        home_key.setIcon(QIcon('home.png'))
        home_key.setStatusTip("Go home")

        # adding action to home button
        home_key.triggered.connect(self.navigate_home)
        navtb.addAction(home_key)

        # new tab key
        addtab_key = QAction('Add new Tab', self)
        addtab_key.setIcon(QIcon('add.png'))
        addtab_key.triggered.connect(self.tab_open)
        navtb.addAction(addtab_key)

        # adding a separator
        navtb.addSeparator()

        # creating a line edit widget for URL
        self.urlbar = QLineEdit()

        # adding action to line edit when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # adding line edit to tool bar
        navtb.addWidget(self.urlbar)

        # similarly adding stop action
        stop_key = QAction("Stop", self)
        stop_key.setIcon(QIcon('stop.png'))
        stop_key.setStatusTip("Stop loading current page")
        stop_key.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_key)

        # creating first tab
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        # showing all the components
        self.show()

        # setting window title
        self.setWindowTitle("MyBrowser")

    # method for adding new tab
    def add_new_tab(self, qurl = None, label ="Blank"):

        # if url is blank
        if qurl is None:
            # creating a google url
            qurl = QUrl('http://www.google.com')

        # creating a QWebEngineView object
        browser = QWebEngineView()

        # setting url to browser
        browser.setUrl(qurl)

        # setting tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # adding action to the browser when url is changed
        # update the url
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                self.update_urlbar(qurl, browser))

        # adding action to the browser when loading is finished
        # set the tab title
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                    self.tabs.setTabText(i, browser.page().title()))



    # when double clicked is pressed on tabs
    def tab_open(self):


        # creating a new tab
        self.add_new_tab()

    # wen tab is changed
    def current_tab_changed(self, i):

        # get the curl
        qurl = self.tabs.currentWidget().url()

        # update the url
        self.update_urlbar(qurl, self.tabs.currentWidget())

        # update the title
        self.update_title(self.tabs.currentWidget())

    # when tab is closed
    def close_current_tab(self, i):

        # if there is only one tab
        if self.tabs.count() < 2:
            # do nothing
            return

        # else remove the tab
        self.tabs.removeTab(i)

    # method for updating the title
    def update_title(self, browser):

        # if signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # do nothing
            return

        # get the page title
        title = self.tabs.currentWidget().page().title()

        # set the window title
        self.setWindowTitle("% s - MyBrowser" % title)

    # action to go to home
    def navigate_home(self):

        # go to google
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    # method for navigate to url
    def navigate_to_url(self):

        # get the line edit text
        # convert it to QUrl object
        q = QUrl(self.urlbar.text())

        # if scheme is blank
        if q.scheme() == "":
            # set scheme
            q.setScheme("http")

        # set the url
        self.tabs.currentWidget().setUrl(q)

    # method to update the url
    def update_urlbar(self, q, browser = None):

        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():

            return

        # set text to the url bar
        self.urlbar.setText(q.toString())

        # set cursor position
        self.urlbar.setCursorPosition(0)

# creating a PyQt5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName("My Browser")

# creating MainWindow object
window = MainWindow()

# loop
app.exec_()
