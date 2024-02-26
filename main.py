# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
import psutil
import threading
from PySide6.QtCharts import QChart,QChartView,QLineSeries
import time
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None
class NewThread(QThread):
    finishSignal=Signal(str)
    def __init__(self,parent=None):
        super(NewThread,self).__init__(parent)

    if os.path.exists(f'./computer_info.csv'):
        pass
    else:
        with open(r'./computer_info.csv','w') as f:
            pass
    def run(self):
        
        timer=0
        while True:
            timer += 1
            cpu_percent=psutil.cpu_percent(interval=1)
            cpu_info=cpu_percent
            virtual_memory=psutil.virtual_memory()
            memory_percent=virtual_memory.percent
            with open(r'./computer_info.csv','a') as f:
                f.write(f"{timer},{cpu_info},{memory_percent}\n")
            time.sleep(2)
            self.finishSignal.emit("1")

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "嗷呜，我是山里灵活的狗"
        description = "嗷呜，我是山里灵活的狗"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_message.clicked.connect(self.buttonClick)
        widgets.btn_computer.clicked.connect(self.buttonClick)
        widgets.btn_computer.clicked.connect(self.buttonClick)
        widgets.pushButton_show.clicked.connect(self.start_computer_info)
        widgets.pushButton_clear.clicked.connect(self.clear_computer_info)
        widgets.pushButton_file.clicked.connect(self.open_guide_book)
        widgets.pushButton_baidu.clicked.connect(self.open_web)
        widgets.pushButton_picture.clicked.connect(self.change_pic)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        if getattr(sys,'frozen',False):
            absPath=os.path.dirname(os.path.abspath(sys.executable))
        elif __file__:
            absPath=os.path.dirname(os.path.abspath(__file__))
        useCustomTheme = False
        self.useCustomTheme=useCustomTheme
        self.absPath=absPath
        themeFile = "themes\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def start_computer_info(self):
        self.thread1=NewThread()
        self.thread1.finishSignal.connect(self.data_display)
        self.thread1.start()

    def data_display(self,str_):
        with open(r'./computer_info.csv','r') as f:
            reader=f.readlines()
            reader_last = reader[-1].replace('\n','').split(',')
            col=int(reader_last[0])
            cpu=float(reader_last[1])
            memory=float(reader_last[2])

        self.seriesS.append(col,cpu)
        self.seriesL.append(col,memory)
        self.chart=QChart()
        self.chart.setTitle("设备资源图")
        self.chart.addSeries(self.seriesS)
        self.chart.addSeries(self.seriesL)
        self.chart.createDefaultAxes()
        widgets.graphicsView.setChart(self.chart)


    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
        
        if btnName == "btn_computer":
            
            widgets.stackedWidget.setCurrentWidget(widgets.computer_info) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

            self.seriesS=QLineSeries()
            self.seriesL=QLineSeries()
            self.seriesS.setName("cpu")
            self.seriesL.setName("memory")

        
        if btnName == "btn_save":
            # print("Save BTN clicked!")
            QMessageBox.information(self,"提示","山里灵活不在家，下次再试试吧",QMessageBox.Yes)

        if btnName == "btn_message":
            if self.useCustomTheme:
                themeFile=os.path.abspath(os.path.join(self.absPath,"themes\py_dracula_dark.qss"))
                UIFunctions.theme(self,themeFile,True)
                AppFunctions.setThemeHack(self)
                self.useCustomTheme=False
            else:
                themeFile=os.path.abspath(os.path.join(self.absPath,"themes\py_dracula_light.qss"))
                UIFunctions.theme(self,themeFile,True)
                AppFunctions.setThemeHack(self)
                self.useCustomTheme=True
        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)
    def clear_computer_info(self):
        self.seriesS.clear()
    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
    def open_guide_book(self):
        import webbrowser
        webbrowser.open("说明书"+".docx")
    
    def open_web(self):
        import webbrowser
        webbrowser.open('www.baidu.com')
    
    def change_pic(self):
        url_list=[
            "./pic/1.jpg",
            "./pic/2.jpg",
            "./pic/3.jpg",
            "./pic/4.jpg",
            "./pic/5.jpg",
        ]
        import random
        index=random.randint(0,4)
        lb1=widgets.label
        pix=QPixmap(url_list[index]).scaled(lb1.size(),aspectMode=Qt.KeepAspectRatio)
        lb1.setPixmap(pix)
        lb1.repaint()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
