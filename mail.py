import os
import glob
import pyautogui
import socket
import datetime
import yaml 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

yaml_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(yaml_path, 'r') as file:
    data = yaml.safe_load(file)

class EmailSender:
    def __init__(self, dir, instr):
        server_info = data['server_info']
        receiver_info = data['receiver_info']

        self.smtp_host = server_info['SMTP_HOST']
        self.smtp_port = server_info['SMTP_PORT']
        self.from_address = server_info['FROM_ADDRESS']
        self.user_name = server_info['USER_NAME']
        self.password = server_info['PASSWORD']
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.IP = s.getsockname()[0]

        self.to_address = receiver_info['TO_ADDRESS']
        self.cc_address = receiver_info['CC_ADDRESS']
        self.bcc_address = receiver_info['BCC_ADDRESS']
        self.instr = instr

        self.title = 'stopped'
        self.dir = dir

        self.subject = None
        self.body = None
        
    def send_email(self, attachment_path=None):
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        msg = MIMEMultipart()
        msg["Subject"] = self.subject
        msg["From"] = self.from_address
        msg["To"] = self.to_address
        to_list = self.to_address
        if self.cc_address is not None:
            msg["Cc"] = ",".join(self.cc_address)
            to_list += self.cc_address
        if self.bcc_address is not None:
            msg["Bcc"] = ", ".join(self.bcc_address)
            to_list += self.bcc_address
        msg.attach(MIMEText(self.body))

        if attachment_path is not None:
            with open(attachment_path, "rb") as f:
                mb = MIMEApplication(f.read())
                mb.add_header("Content-Disposition", "attachment", filename=attachment_path)
            msg.attach(mb)

        server.starttls()
        server.login(self.user_name, self.password)
        server.sendmail(self.from_address, to_list, msg.as_string())
        server.quit()
        print("-------Send email-------")
        print("Subject: {}".format(self.subject))
        print("To: {}".format(to_list))
        print("Cc: {}".format(self.cc_address))
        print("Bcc: {}".format(self.bcc_address))
        print("Body: {}".format(self.body))
        print("-------------------------")

    def write_subject(self):
        if self.title == 'stopped':
            comment = 'The measurement has been stopped.'
            self.subject = '{}: {} --{}--'.format(self.title, self.instr, comment)

    def write_body(self):
        if self.title == 'stopped':
            massage = 'The measurement has been stopped. \nPlease check the measurement status.'
            IP = self.IP
            time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            latest_file_list = glob.glob(os.path.join(self.dir, '*'))
            if len(latest_file_list) == 0:
                latest_file = 'No files found.'
            else:
                latest_file = max(latest_file_list, key=os.path.getctime)
            
            self.body = '{}\nIP: {}\nTime: {}\nLatest file: {}'.format(massage, IP, time, latest_file)
        
    def run(self, screen_shot=False):
        print('Composing email...')
        self.write_subject()
        self.write_body()
        if screen_shot:
            pic_dir_path = os.path.dirname(__file__) + r"/screenshots"
            os.makedirs(pic_dir_path, exist_ok=True)
            pic_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
            pic_dir_path += "/"
            pic_path = pic_dir_path + pic_name
            pyautogui.screenshot(pic_path)
        self.send_email(attachment_path=pic_path if screen_shot else None)
