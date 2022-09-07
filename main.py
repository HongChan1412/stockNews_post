from bleach import clean
import getData as gd
import re
from naver import Naver
import time



def cleanTitle(inputString):
  text_rmv = re.sub('[-=+#/\?:;^@*※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', inputString)#.,""
  text_rmv = re.sub('  ', ' ', text_rmv).strip(" ")
  return text_rmv
    
def stockNews(input_url, delay, posted_title, keywords, naver, stocks, titleform, ipo_search):

  if ipo_search:
    try:
      title, newsList, posted_title = gd.getIpoNews(posted_title)
      time.sleep(60*delay)
      
      if title:
        newsTitle = clean(title)
        res = naver.post(input_url, newsTitle, newsList)
        return res, title, posted_title
      return -2, None, posted_title
    
    except Exception as e:
      print(e)
      return None, None, posted_title
  
  else:
    try:
      max_key, newsTitle, newsList, posted_title, dataisin = gd.getNaverNews(delay, posted_title, keywords, stocks)
      if dataisin :
      #print(f'제목 : {newsTitle}')
        newsTitle = cleanTitle(newsTitle)
        if titleform == "":
          title = newsTitle
        else:
          title = f'{max_key} {titleform} : {newsTitle}'

        res=naver.post(input_url, title, newsList)
        #print(res, title)
        return res, title, posted_title
      return -2, None, posted_title
    except Exception as e:
      print(e)
      return None, None, posted_title


