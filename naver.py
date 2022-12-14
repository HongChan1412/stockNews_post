#-*- coding: utf-8 -*-
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
import random

options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_experimental_option("prefs", {
    'profile.default_content_setting_values.notifications': 1,
    'profile.default_content_setting_values.clipboard': 1
})
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('window-size=1920x1080')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36')
options.add_experimental_option('excludeSwitches', ['enable-automation'])


class MyChrome(webdriver.Chrome):
    def quit(self):
        webdriver.Chrome.quit(self)
        self.session_id = None

class Naver:
    def __init__(self, id, pw, proxyLIST) -> None:
        self.id=id
        self.pw=pw
        if proxyLIST:
            with open(proxyLIST, 'r') as proxyLists:
                d = proxyLists.readlines()
                fileLists = list(map(lambda e: e.strip("\n"), d))
                random.shuffle(fileLists)
                options.add_argument('--proxy-server=%s' %fileLists[0])
        self.driver = MyChrome(ChromeDriverManager().install(), options = options)

    def login(self):
        self.driver.get("https://nid.naver.com/nidlogin.login")
        self.driver.execute_script("document.getElementsByName('id')[0].value=\'" + self.id + "\'")
        self.driver.execute_script("document.getElementsByName('pw')[0].value=\'" + self.pw + "\'")
        
        time.sleep(1)
        # self.driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
        self.driver.find_element_by_class_name('btn_login').click()
        # self.driver.find_element_by_class_name('btn_login').click()
        time.sleep(1)
        return self.is_logged_in()
        #return True

    def post(self, editor_link, title, link):
        count = 0
        self.driver.get(editor_link)    

        time.sleep(0.5)
        try:
            alert = self.driver.switch_to_alert()
            alert.accept()
        except:
            print('????????? ??????')
        #print(self.driver.current_url)
        if "Fwrite-error" not in self.driver.current_url :
            time.sleep(10)

            self.driver.find_element_by_class_name('textarea_input').send_keys(title)   #?????? ??????    
            try:
                for i in link:
                    os.system('echo off | clip')    #???????????? ?????????
                    count = self.linkposting(i, count)
                    # print(count)
                
                if count >= len(link) :
                    time.sleep(1)
                    self.driver.find_element_by_xpath('//span[contains(text(),"??????")]').click()
                    return "??????"
                else:
                    #print("?????????????????? ?????????")
                    self.driver.quit()
                    self.driver = MyChrome(options=options)
                    self.login()
                    
                    return "??????"
            except Exception as e:
                print(f'?????? ?????? :\n{e}')
                return "??????"
        else :
            return -1   #?????? ??????


    def linkposting(self, link, count):    #?????? ?????????
        element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-oglink-toolbar-button.se-document-toolbar-basic-button.se-text-icon-toolbar-button')))    #??????
        time.sleep(0.5)
        element.click()

        element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//input[@class="se-popup-oglink-input"]')))   #?????? ?????? ????????????
        time.sleep(0.5)
        element.send_keys(link)

        element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-popup-oglink-button')))    #?????? ???????????? ???????????? ????????? ?????? ??????
        time.sleep(0.5)
        element.click()

        try:
            element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-popup-button.se-popup-button-confirm')))      #?????? ????????? ??? "??????"?????? ????????? ?????? ??????
            time.sleep(0.5)
            element.click()
            count+=1

            return count

        except Exception as e:
            element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'se-popup-close-button')))      #?????? ?????? ?????? ??????
            time.sleep(1)
            element.click()

            print("?????? ?????? ?????? ??????")
            print(f'?????? ?????? :\n{e}')

            return count
  
  
    def is_logged_in(self):
        self.driver.get('https://shopping.naver.com/my/p/home.nhn') #????????? ????????? ????????? ??????
        self.driver.implicitly_wait(10)
        try:
            alert = self.driver.switch_to_alert()
            print(alert.text)
            alert.accept()
        except:
            print('naver alert')
        time.sleep(1)
        current_url = self.driver.current_url
        if current_url.split('?')[0] == 'https://nid.naver.com/nidlogin.login':
            #print('===========login error=============')
            return False
        return True


