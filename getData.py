import numpy as np
import requests
from bs4 import BeautifulSoup
from Utils.excelUtils import getColumnData
import pandas as pd
import time
from requests.sessions import session
import warnings
warnings.filterwarnings('ignore')

def check_news(key, title, keywords) :
    start_index = title.find(key)
    string = [' ', '.', ',', '\"', '\'', '(', ')', '[', ']', '!', '?', '-']
    if keywords :
        for i in range(len(keywords)) :
            if keywords[i] in title :
                #print(title, keywords[i], "포함 O")
                if start_index == 0 :
                    #print("시작", key, title)
                    return True
                elif title[start_index-1:start_index] in string  and title[start_index+len(key):start_index+len(key)+1] in string :
                    #print("앞뒤 공백", key, title)
                    return True
                else : 
                    #print("조건에 맞지않음", key, title)
                    return False
            #print(title, keywords[i],"포함 X")
    else :
        if start_index == 0 :
            #print("시작", key, title)
            return True
        elif title[start_index-1:start_index] in string  and title[start_index+len(key):start_index+len(key)+1] in string :
            #print("앞뒤 공백", key, title)
            return True
        else : 
            #print("조건에 맞지않음", key, title)
            return False
    
def getNaverNews(delay, posted_title, keywords, stocks):
    '''
    네이버 뉴스
    '''    
    newsData = {'key':[],'title':[],'url':[]}
    data = pd.DataFrame(newsData)
    t_end = time.time() + 60*delay
    dataisin = False
    corp_list = []

    while time.time() < t_end:
        try:
            res = requests.get("https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001", headers={'User-Agent':'Mozilla/5.0'})
            html = res.text
            soup = BeautifulSoup(html, "html.parser")
            contents = soup.select("#main_content > div.list_body.newsflash_body > ul > li > dl > dt:not(.photo) > a")

            for k in stocks:
                try:
                    corp_csv = open(k,"rt",encoding='cp949')
                    corp_list += getColumnData(corp_csv, 2)
                except:
                    corp_csv = open(k,"rt",encoding='utf-8-sig')
                    corp_list += getColumnData(corp_csv, 2)
                corp_csv.close()
            
            for i in range(len(contents)):
                title = (contents[i].get_text().strip())
                newsUrl = (contents[i].get('href'))

                for j in corp_list:
                    if j in title:
                        if check_news(j, title, keywords) :
                            dataisin = True             #data에 값 들어갔는지 확인
                            data_to_insert = {'key' : j, 'title' : title, 'url' : newsUrl}
                            data = data.append(data_to_insert, ignore_index=True)
                            data = data.drop_duplicates()
                            data = data.drop_duplicates(subset=['title'])        #같은제목 삭제
                            data = data.drop_duplicates(subset=['url'])

        except Exception as e:
            print("Error occurred : ", [getNaverNews.__name__, e])
        time.sleep(3)

    if not dataisin :   #data에 값 안들어가있으면 다시 뉴스 검색
        return None, None, None, posted_title, dataisin

    if posted_title :
        for i in range(len(posted_title)) :
            data = data.drop(index=data.loc[data.title == posted_title[i]].index)

    data['cnt'] = data.groupby(['key'])['key'].transform('count')   #key값 중복개수 카운트 및 행 추가
    data = data.sort_values(by=['cnt'], ascending=False)  #cnt값으로 정렬
    data = data.set_index('key', inplace=False).reset_index() #인덱스 초기화

    max_key = data.iloc[0]['key']   #값 가져오기
    max_cnt = data.iloc[0]['cnt']
    data = data.drop(index=data.loc[data.key != max_key].index)  #key값아닌 행 삭제

    top_news = data.iloc[0]['title']
    newsList = data.loc[0:max_cnt-1, ['url']]
    newsList = np.array(newsList['url'].tolist())   #뉴스 url값 배열 변환
    titleList = data.loc[0:max_cnt-1, ['title']]
    titleList = np.array(titleList['title'].tolist())

    for i in range(len(titleList)) :
        posted_title.append(titleList[i])
        
    return max_key, top_news, newsList, posted_title, dataisin

def getData(inputUrl):

    cafeUrl = inputUrl
    res = requests.get(cafeUrl,
        headers={'User-Agent':'Mozilla/5.0'})
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    
    cafetitle = soup.select_one("div#front-cafe > a").get('href').split('clubid=')[1]
    listMenu = soup.select("ul.cafe-menu-list > li > img:not(.ico-link)+a")

    menuTitle = []
    menuId = []

    #print(f'카페 아이디값 : {cafetitle}')


    for i in listMenu:
        listTitle = i.get_text().strip()
        listId = i.get('href').strip()
        listId = listId.split("menuid=")[-1].split("&")[0]

        if "clubid" not in listId and 1<len(listTitle):
            # print(f'{listTitle} / {listId}')
            menuTitle.append(listTitle)
            menuId.append(listId)


    return cafetitle, menuTitle, menuId

def getIpoNews(posted_title):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time
    from bs4 import BeautifulSoup
    pc_headers = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36', #chrome 88
    ]
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headlsess')
    chrome_options.add_argument('blink-settings=imagesEnabled=false') #이미지 로딩 X
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("lang=ko_KR")
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument(f"user-agent={pc_headers}")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-setuid-sandbodx")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-browser-side-navigation")
    prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}  
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30) 
    url = "http://www.38.co.kr/html/news/?m=nostock"
    driver.get(url)
    time.sleep(3)
    res = driver.find_element(By.XPATH, "/html/body/table[3]/tbody/tr/td/table[1]/tbody/tr/td[1]/table[2]/tbody/tr[2]/td/a/font").get_attribute("innerHTML").strip()
    
    if posted_title:
        if res in posted_title:
            return False, False, posted_title
    
    driver.get(f"https://search.naver.com/search.naver?where=news&query={res}&sm=tab_opt&sort=0&photo=0&field=0&pd=4&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1d&is_sug_officeid=0")
    time.sleep(3)
    
    pageString = driver.page_source  
    bsObj = BeautifulSoup(pageString, 'html.parser') 
    text = bsObj.find_all(class_="news_tit")
    
    news_link = []
    
    
    for i in text:
        news_link.append(i['href'])
    
    if not news_link:
        return False, False, posted_title
    
    posted_title.append(res)
    
    return res, news_link, posted_title
        
