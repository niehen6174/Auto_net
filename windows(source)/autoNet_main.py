from PyQt5.QtWidgets import QApplication ,QMainWindow,QMessageBox,QFileDialog
from os import getcwd
from time import sleep
from sys import exit,argv
from untitled import Ui_Dialog
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from requests import get,ConnectionError,Timeout
from subprocess import Popen,PIPE,STDOUT
import subprocess
import schedule
class MyMainWindow(QMainWindow,Ui_Dialog):
    def __init__(self,parent=None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.show()

        self.read_config()
        self.pushButton.clicked.connect(self.update_config)
        self.pushButton_6.clicked.connect(self.get_dirver)
        self.pushButton_2.clicked.connect(self.ping_net)
    def read_config(self):
        conf = ConfigParser()  #
        conf.read('config.conf', encoding='gbk')  # 读取配置文件 获取一些参数
        self.username = conf.get('infor','username')
        self.passwd = conf.get('infor', 'passwd')
        self.time_inter = int(conf.get('infor', 'time_inter'))
        self.driver_path = conf.get('infor', 'driver_path')
        self.show_lineinfor()
    def show_lineinfor(self): # 显示信息
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setPlaceholderText(str(self.username))
        self.lineEdit_5.setPlaceholderText(str(self.passwd))
        self.lineEdit_3.setPlaceholderText(str(self.time_inter)+" Min")
    def update_config(self): # 读取输入更新配置
        conf = ConfigParser()  #
        conf.read('config.conf', encoding='gbk')  # 读取配置文件 获取一些参数
        input_username = self.lineEdit_4.text()
        input_passwd = self.lineEdit_5.text()
        input_inter = self.lineEdit_3.text()
        wirte = False
        if input_inter != "":
            if not input_inter.isdigit():
                QMessageBox.information(self,"warning","请输入数字")
            else :
                conf.set("infor","time_inter",input_inter)
                self.time_inter = int(input_inter)
                wirte = True
        if input_username != "":
            if not input_username.isdigit():
                QMessageBox.information(self,"warning","请输入学号")
            else :
                conf.set("infor","username",input_username)
                self.username = input_username
                wirte = True
        if input_passwd != "":
                conf.set("infor","passwd",input_passwd)
                self.passwd = input_passwd
                wirte = True
        if wirte:
            print("更新参数")
            conf.write(open('config.conf', "w"))
        if not self.driver_path.endswith("exe"):
            QMessageBox.information(self, "warning", "请选择正确的driver地址")
            return
        if not str(self.time_inter).isdigit():
            QMessageBox.information(self, "warning", "请选择正确的时间间隔（大于3的数字）")
            return
        self.show_lineinfor()
        self.net_monitor()
        self.label.setText(str(self.get_time()) +'\n'"Now Software is woring")
    def get_dirver(self): # 获取驱动地址
        driver_file = QFileDialog.getOpenFileName(self, "选择版本对应的chrome dirver", getcwd())[0]
        #self.driver_path = path.abspath(path.dirname(driver_file)+path.sep+".")
        self.driver_path = driver_file
        conf = ConfigParser()  #
        conf.read('config.conf', encoding='gbk')  # 读取配置文件 获取一些参数
        conf.set("infor", "driver_path", self.driver_path)
        conf.write(open('config.conf', "w"))
        self.show_lineinfor()

    def openChrome(self):

        option = webdriver.ChromeOptions()
        # option.add_argument('disable-infobars')
        # option.add_argument("--headless")
        # option.add_experimental_option('excludeSwitches', ['enable-automation'])
        filename = self.driver_path
        ser = Service(filename)
        driver = webdriver.Chrome(service=ser, options=option)
        return driver

    def get_time(self):
        now = datetime.now()
        ts = now.strftime('%Y-%m-%d %H:%M:%S')
        return ts

    def ping_net(self):
        exit_code = self.popen2('ping www.baidu.com -n 2')  # windows 下检测网络 # linux 下用 "ping -q -c 2 baidu.com"
        if exit_code.find("ms") == -1:
            status_net = False
        else:
            status_net = True
        # try:
        #     request = get("http://www.baidu.com", timeout=3)
        #     print("Connected to the Internet")
        #     status_net = True
        # except (ConnectionError, Timeout) as exception:
        #     print("No internet connection.")
        #     status_net = False
        ts = self.get_time()
        if status_net:
            self.label.setText(str(ts) +'\n'+ "Net is working")
        else:
            self.label.setText(str(ts) +'\n'+ "Net is not working")
        print(status_net)
        return status_net

    # def execute_cmd(self,cmd):
    #     proc = Popen(
    #         cmd,
    #         shell=True,
    #         stdout=PIPE,
    #         stderr=STDOUT,
    #         stdin=PIPE
    #     )
    #     proc.stdin.close()
    #     proc.wait()
    #     result = proc.stdout.read().decode('gbk')  # 注意你电脑cmd的输出编码（中文是gbk）
    #     proc.stdout.close()
    #     return result
    #
    def popen2(self,cmd):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        return process.stdout.read().decode('gbk')
    def checke_net(self):
        status_net = self.ping_net()
        if not status_net:

            for i in range(5):
                write_file = open("recode.txt", "a")
                try:
                    driver = self.openChrome()
                    url = ["http://2.2.2.2/","http://192.168.112.30/index_18.html"]
                    driver.get(url[i%2])
                    sleep(2)
                    driver.find_element(By.XPATH, "//input[@id='username']").send_keys(self.username)
                    driver.find_element(By.XPATH, "//input[@id='password']").send_keys(self.passwd)
                    driver.find_element(By.XPATH, "//button[@id='login-account']").send_keys(Keys.ENTER)
                    sleep(3)
                    driver.quit()
                    ts = self.get_time()

                    if self.ping_net():
                        write_file.write(str(ts) + "Success!! Get net!\n")
                        write_file.close()
                        self.label.setText(str(ts) + '\n' + "Success!!")
                        print("get net")
                        break
                    else:
                        write_file.write(str(ts) + "i Error!! No get net\n")
                        write_file.close()
                        self.label.setText(str(ts) + '\n' + "i Error!! No get net")
                        print("get net")
                    #print(ts, "Success!")

                except:
                    ts = self.get_time()
                    write_file.write(str(ts) +"error!! Can not get net!\n")
                    write_file.close()
                    self.label.setText(str(ts) +'\n'+ "Error!!")
                    #print(ts, "Error!!!,Please Check!!!")

                sleep(30)
            print("即将退出程序...")
        else:
            print("net working")
    def net_monitor(self):
        ts = self.get_time()
        print('do func  time :', ts)
        print(self.time_inter, type(self.time_inter))
        # sched = BlockingScheduler(timezone='Asia/Shanghai')
        # sched.add_job(self.checke_net, 'interval', seconds=self.time_inter*60, id='my_job_id')
        #sched.start()
        schedule.clear()
        schedule.every(self.time_inter).minutes.do(self.checke_net)
        self.checke_net()
        while True:
            schedule.run_pending()
            QApplication.processEvents()

if __name__ == "__main__":


    app = QApplication(argv)
    ui = MyMainWindow()
    exit(app.exec_())