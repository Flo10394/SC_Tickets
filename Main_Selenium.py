from selenium import webdriver
import time
import httplib2
import smtplib, ssl
import winsound
import getpass
import os


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

## Mail Config #######################################################
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "florian.sprich@googlemail.com"  # Enter your address
receiver_email = "florian.sprich@googlemail.com"  # Enter receiver address
password = getpass.getpass(prompt='Password:', stream=None)

with smtplib.SMTP_SSL(smtp_server, port) as server:
    try:
        server.login(sender_email, password)
        print("login successful")
    except Exception as e:
        print("wrong login credentials")
######################################################################

## Browser Config ####################################################
url = 'https://heimspiele-scfreiburg.reservix.de/'
GegnerList = ["TSG 1899 Hoffenheim"]
Zustand = [0]*GegnerList.__len__()
browser = webdriver.Firefox()
######################################################################


## Process Config ####################################################
GegnerNum = -1
DurchlaufNum = 0
######################################################################


while(1):
    listi = []
    browser.get(url)
    time.sleep(5)
    GegnerNum += 1
    if(GegnerNum > len(GegnerList)-1):
        GegnerNum = 0
        DurchlaufNum += 1
        print("Durchlauf %d" %(DurchlaufNum))
    Gegner = GegnerList[GegnerNum]
    try:
        el = browser.find_element_by_partial_link_text("SC Freiburg - %s" %(Gegner))
        el.click()
        time.sleep(5)
    except:
        continue

    try:
        el2 = browser.find_element_by_class_name("button-teaser")
    except:
        if(Zustand[GegnerNum] == 1):
            Zustand[GegnerNum] = 0
            beepForTickets(0)
            SUBJECT = "Tickets fuer %s weg" %(Gegner)
            TEXT = "Nord"
            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            message = message.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
            message = message.replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE")
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
        continue

    if(el2.text == "Jetzt Plätze auswählen"):
        time.sleep(5)
        el2.click()
        try:
            time.sleep(2)
            el3 = browser.find_element_by_class_name("sm2-pricecategory-dropdown")
            el4 = el3.find_element_by_tag_name("svg")
            time.sleep(2)
            el4.click()
            time.sleep(1)
            el5 = browser.find_elements_by_class_name("name")
            for i in range(len(el5)):
                listi.append(el5[i].text)

            if("Stehplatz Nord" in listi):
            #if ("Block L bis M" in listi):
                if(Zustand[GegnerNum] == 0):
                    Zustand[GegnerNum] = 1
                    beepForTickets(1)
                    SUBJECT = "Tickets fuer %s verfügbar" %(Gegner)
                    TEXT = "Nord verfügbar"
                    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                    message = message.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
                    message = message.replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE")
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message)

            else:
                if(Zustand[GegnerNum] == 1):
                    Zustand[GegnerNum] = 0
                    SUBJECT = "Tickets für %s weg" %(Gegner)
                    TEXT = "Nord"
                    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                    message = message.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
                    message = message.replace("Ä", "AE").replace("Ö", "OE").replace("Ü", "UE")
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message)
        except:
            continue
