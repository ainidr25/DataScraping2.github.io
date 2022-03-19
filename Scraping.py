from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import json
from datetime import datetime
import urllib.request

PATH = "C:\Program Files (x86)\Phyton\Phyton3\chromedriver.exe"
driver = webdriver.Chrome(PATH)
count = 1
page = 1
data = []
now = datetime.now()
createnote = open('title_list.txt', 'w',encoding='utf-8')
createJson = open('hasil_scrap.json', 'w',encoding='utf-8')
driver.get("https://www.novelupdates.com/latest-series/")
while(count<100):
    for novel in driver.find_elements(by=By.CLASS_NAME,value='search_main_box_nu'):
        count_string = '#' + str(count)
        Title = novel.find_element(by=By.CLASS_NAME,value='search_title')
        temp_title = Title.text
        Title = temp_title.replace(count_string,'')
        Ratings = novel.find_element(by=By.CLASS_NAME,value='search_ratings').text
        Origin,Rating = Ratings.split(' ')
        Genre = novel.find_element(by=By.CLASS_NAME,value='search_genre').text
        link_cover = novel.find_element(by=By.TAG_NAME,value='img').get_attribute('src')
        for image in novel.find_elements_by_tag_name("img"):
            urllib.request.urlretrieve(image.get_attribute("src"), str(count)+".png")
            break
        print(str(count),'. ',Title,Ratings,Genre,link_cover)
        createnote.write(Title)
        createnote.write(" ")
        createnote.write(Ratings)
        createnote.write('\n')
        data.append({"Title": Title,
                 "Genre": Genre , 
                 "Rating": Rating,
                 "Origin": Origin,
                 "img_src" : image.get_attribute("src"),
                 "Waktu_scrapping": now.strftime("%d/%m/%Y %H:%M:%S")})
        if count>=100:
            break
        count+=1
    try:
        page+=1
        driver.find_element(by=By.CLASS_NAME,value="digg_pagination").find_element(by=By.PARTIAL_LINK_TEXT, value=str(page)).click()
    except NoSuchElementException as e:
        break;
createnote.close()
jdumps = json.dumps(data, indent=5)
createJson.writelines(jdumps)
createJson.close()
driver.quit()