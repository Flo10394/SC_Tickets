from GUI import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread

from selenium import webdriver
import time
import httplib2
import smtplib
import ssl
import winsound
import getpass
import os
from datetime import datetime

class ProcessThread(QThread):

    signalizing = QtCore.pyqtSignal(object)

    def __init__(self):
        QThread.__init__(self)
        self.smtp_server = 0
        self.smtp_port = 0
        self.mail = 0
        self.password = 0
        self.browser = 0

    def config(self, smtp_server, smtp_port, mail, password, gegnerList, receiverList):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.mail = mail
        self.password = password
        self.Gegnerlist = gegnerList
        self.receiverList = receiverList

    # run method gets called when we start the thread
    def run(self):
        self.Process()

    def Process(self):
        self.signalizing.emit("process started")

        ## Browser Config ####################################################
        url = 'https://heimspiele-scfreiburg.reservix.de/'
        GegnerList = self.Gegnerlist

        info = "Searching for Tickets against: "
        for i in range(len(GegnerList)):
            if(i != len(GegnerList)-1):
                info = info + GegnerList[i] + ", "
            else:
                info = info + GegnerList[i]
        self.signalizing.emit(info)

        Zustand = [0] * len(GegnerList)

        #if self.hide:
         #   options = webdriver.FirefoxOptions()
          #  options.add_argument('-headless')
           # self.browser = webdriver.Firefox(options=options)
        #else:
        self.browser = webdriver.Firefox()
        ######################################################################

        ## Process Config ####################################################
        GegnerNum = -1
        DurchlaufNum = 0
        ######################################################################

        while (1):
            listi = []
            self.browser.get(url)
            time.sleep(5)
            GegnerNum += 1
            if (GegnerNum > len(GegnerList) - 1):
                GegnerNum = 0
                DurchlaufNum += 1
                info = "Durchlauf " + str(DurchlaufNum)
                self.signalizing.emit(info)
            Gegner = GegnerList[GegnerNum]
            try:
                el = self.browser.find_element_by_partial_link_text("SC Freiburg - %s" % (Gegner))
                el.click()
                time.sleep(5)
            except:
                continue

            try:
                el2 = self.browser.find_element_by_class_name("button-teaser")
            except:
                if (Zustand[GegnerNum] == 1):
                    Zustand[GegnerNum] = 0
                    beepForTickets(0)
                    SUBJECT = "Tickets fuer %s weg" % (Gegner)
                    TEXT = "Nord"
                    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                    message = message.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
                    message = message.replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE")
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                        server.login(self.mail, self.password)
                        for el in self.receiverList:
                            server.sendmail(self.mail, el, message)
                    info = ""
                    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S:  ")
                    info = info + date_time + SUBJECT
                    self.signalizing.emit(info)
                continue

            if (el2.text == "Jetzt Plätze auswählen"):
                time.sleep(5)
                el2.click()
                try:
                    time.sleep(5)
                    el3 = self.browser.find_element_by_class_name("sm2-pricecategory-dropdown")
                    el4 = el3.find_element_by_tag_name("svg")
                    time.sleep(5)
                    el4.click()
                    time.sleep(1)
                    el5 = self.browser.find_elements_by_class_name("name")
                    for i in range(len(el5)):
                        listi.append(el5[i].text)

                    if ("Stehplatz Nord" in listi):
                        # if ("Block L bis M" in listi):
                        if (Zustand[GegnerNum] == 0):
                            Zustand[GegnerNum] = 1
                            beepForTickets(1)
                            SUBJECT = "Tickets fuer %s verfügbar" % (Gegner)
                            TEXT = "Nord verfügbar"
                            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                            message = message.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
                            message = message.replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE")
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                                server.login(self.mail, self.password)
                                for el in self.receiverList:
                                    server.sendmail(self.mail, el, message)
                            info = ""
                            date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S:  ")
                            info = info + date_time + SUBJECT
                            self.signalizing.emit(info)

                    else:
                        if (Zustand[GegnerNum] == 1):
                            Zustand[GegnerNum] = 0
                            SUBJECT = "Tickets für %s weg" % (Gegner)
                            TEXT = "Nord"
                            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                            message = message.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
                            message = message.replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE")
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                                server.login(self.mail, self.password)
                                for el in self.receiverList:
                                    server.sendmail(self.mail, el, message)
                            info = ""
                            date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S:  ")
                            info = info + date_time + SUBJECT
                            self.signalizing.emit(info)
                except:
                    continue

def beepForTickets(status):
    if status:
        for i in range(0, 3):
            frequency = 500  # Set Frequency To 2500 Hertz
            duration = 300  # Set Duration To 1000 ms == 1 second
            winsound.Beep(frequency, duration)
            time.sleep(0.2)
    else:
        frequency = 500  # Set Frequency To 2500 Hertz
        duration = 300  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
        time.sleep(0.2)
        frequency = 500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)

class SC_GUI(Ui_Form):

    def __init__(self):
        super().__init__()
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.mail_server = 0
        self.loggedIn = 0
        self.process_thread = ProcessThread()

    def loginToMailServer(self):
            try:
                self.mail_server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
                self.mail_server.login(self.lineEdit_email.text(), self.lineEdit_password.text())
                self.pushButton_login.setDisabled(1)
                self.lineEdit_email.setDisabled(1)
                self.lineEdit_password.setDisabled(1)
                self.pushButton_logout.setEnabled(1)
                self.textBrowser.append("login successful")
                self.loggedIn = 1
            except:
                self.textBrowser.append("login failed")

    def disableLogoutButton(self):
        self.pushButton_logout.setEnabled(False)
        self.pushButton_login.setEnabled(True)
        self.lineEdit_email.setEnabled(1)
        self.lineEdit_password.setEnabled(1)
        self.textBrowser.append("logout successful")
        self.loggedIn = 0

    def startProcess(self):
        if(self.loggedIn != 1):
            self.textBrowser.append("please login first")
            return

        gegnerlist = []
        if self.lineEdit_Gegner_1.text() != "":
            gegnerlist.append(self.lineEdit_Gegner_1.text())
        if self.lineEdit_Gegner_2.text() != "":
            gegnerlist.append(self.lineEdit_Gegner_2.text())
        if self.lineEdit_Gegner_3.text() != "":
            gegnerlist.append(self.lineEdit_Gegner_3.text())
        if self.lineEdit_Gegner_4.text() != "":
            gegnerlist.append(self.lineEdit_Gegner_4.text())

        receiverList = self.lineEdit_email_receiver.text().split(",")
        info = "Sending emails to: "
        for i in range(len(receiverList)):
            if(i != len(receiverList)-1):
                info = info + receiverList[i] + ", "
            else:
                info = info + receiverList[i]

        self.textBrowser.append(info)

        #hide = self.checkBox_hideBrowser.isChecked()
        self.process_thread.config(self.smtp_server, self.smtp_port, self.lineEdit_email.text(),
                                   self.lineEdit_password.text(), gegnerlist, receiverList)

        self.process_thread.signalizing.connect(self.printToTextBrowser) # Signal for printing to TextBrowser
        self.process_thread.start()
        self.pushButton_stop.setEnabled(1)
        self.pushButton_start.setDisabled(1)

    def stopProcess(self):
        self.textBrowser.append("process closed\n\n")
        self.process_thread.browser.close()
        self.process_thread.terminate()
        self.pushButton_stop.setDisabled(1)
        self.pushButton_start.setEnabled(1)

    def clearTextBrowser(self):
        self.textBrowser.clear()

    def printToTextBrowser(self, data):
        self.textBrowser.append(data)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app_icon = QtGui.QIcon()
    app_icon.addFile('SCF.jpg', QtCore.QSize(1000, 1000))
    app.setWindowIcon(app_icon)
    Form = QtWidgets.QWidget()
    Form.setWindowIcon(QtGui.QIcon("SCF.jpg"))
    ui = SC_GUI()
    ui.setupUi(Form)
    Form.setWindowTitle("SCF Ticket Alarm")
    ui.pushButton_login.clicked.connect(ui.loginToMailServer)
    ui.pushButton_logout.clicked.connect(ui.disableLogoutButton)
    ui.pushButton_start.clicked.connect(ui.startProcess)
    ui.pushButton_stop.clicked.connect(ui.stopProcess)
    ui.pushButton_clear.clicked.connect(ui.clearTextBrowser)
    Form.show()
    sys.exit(app.exec_())

