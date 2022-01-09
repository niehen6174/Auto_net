
#coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import schedule
from time import sleep
from datetime import datetime
from os import popen

# 开启浏览器
User_name = "xxx"
Passwd = "xxx"
Chrome_path =""
Time_inter = 10 # 分钟

def openChrome():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    option.add_argument("--headless")
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    filename = r'/usr/bin/chromedriver'
    ser =Service(Chrome_path)
    driver = webdriver.Chrome(service=ser)
    return driver

# 流程
def get_time():
    now = datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    return ts
def ping_net():
    exit_code = popen('ping www.baidu.com -c 2').read()  # windows 下检测网络 # linux 下用 "ping -q -c 2 baidu.com"
    if exit_code.find("100% packet loss") != -1:
        status_net = False
    else:
        status_net = True
    print(status_net)
    return status_net
def checke_net():
    # exit_code = popen('ping www.baidu.com -c 2').read()#windows 下检测网络 # linux 下用 "ping -q -c 2 baidu.com"
    # if exit_code.find("100% packet loss") != -1:
    #     status_net = False
    # else:
    #     status_net = True
    status_net = ping_net()
    if not status_net:
        for i in range(5):
            write_file = open("recode.txt", "a")
            try :
                driver = openChrome()
                url = ["http://2.2.2.2/", "http://192.168.112.30/index_18.html"]
                driver.get(url[i % 2])
                sleep(2)
                driver.find_element(By.XPATH,"//input[@id='username']").send_keys(User_name)
                #driver.find_element_by_xpath("//input[@id='username']").send_keys("212060358") # old version
                driver.find_element(By.XPATH,"//input[@id='password']").send_keys(Passwd)
                driver.find_element(By.XPATH,"//button[@id='login-account']").send_keys(Keys.ENTER)
                sleep(3)
                driver.quit()
                ts = get_time()
                if ping_net():
                    write_file.writelines(ts)
                    write_file.write("Success!! Get net!\n")
                    write_file.close()
                    print(ts, "Success!")
                    break
                else:
                    write_file.write(str(ts) + "i Error!! No get net\n")
                    write_file.close()
            except:
                ts = get_time()
                write_file.writelines(ts)
                write_file.write("error!! Can not get net!\n")
                write_file.close()
                print(ts, "Error!!!,Please Check!!!")
            sleep(30)
        print("即将退出程序...")


def net_monitor(Time):
    ts = get_time()
    print('do func  time :', ts)
    schedule.clear()
    schedule.every(Time).minutes.do(checke_net)
    checke_net()
    while True:
        schedule.run_pending()
        sleep(2)

if __name__ == '__main__':
    net_monitor(Time_inter)
