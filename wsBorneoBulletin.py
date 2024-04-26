from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from datetime import date
import pandas as pd

today_news = []
news_headline_list = []
news_category_list = []
news_date_list = []
news_link_list = []
news_description_list = []

site_nav_list = [
            {'section' : 'national'}, 
            {'section' : 'southeast', }, 
            {'section' : 'world', },
            {'section' : 'business', },
            {'section' : 'tech', },
            {'section' : 'lifstyle', },
            {'section' : 'entertainment', },
            {'section' : 'sports', },
            {'section' : 'features', },
            {'section' : 'opinion', } 
            ]

service = Service(executable_path="geckodriver.exe")
firefox_options = Options()
firefox_options.add_argument("-headless") 
driver = webdriver.Firefox(service=service, options=firefox_options)

driver.get("https://borneobulletin.com.bn/")

today = date.today()
print('\nToday is,', today)

page = 1

# CLOSE POPUP
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'tdm-popup-modal'))
)
closeAds = driver.find_element(By.CLASS_NAME, "tdm-pmh-close")
closeAds.click()

for site_nav in site_nav_list:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'tdb-menu-item-text'))
    )
    print(f"\n----- {site_nav['section']} News ------------------")
    news_category = site_nav['section']
    
    driver.get(f'https://borneobulletin.com.bn/category/{site_nav['section']}/')

    news_col = driver.find_element(By.ID, "tdi_55")
    news_box = news_col.find_elements(By.CLASS_NAME, "td-module-meta-info")

    print("Collecting news from ID 55 block")
    for box in news_box:
        news_title = box.find_element(By.CLASS_NAME, "td-module-title") 
        news_headline = news_title.find_element(By.TAG_NAME, "a").text

        news_date = box.find_element(By.CLASS_NAME, "entry-date")
        news_date = str(news_date.get_attribute("datetime"))
        
        if news_date[:10] == str(today):
            news_link = news_title.find_element(By.TAG_NAME, "a").get_attribute("href")

            if news_category == 'lifstyle':
                news_category = 'lifestyle'
                
            news_category_list.append(news_category)
            news_headline_list.append(news_headline)
            news_date_list.append(news_date)
            news_link_list.append(news_link)
    
    print("Collecting news from ID 92 block")
    while True:    
        print("Collecting news from PAGE", page)
        thereIs_news = False

        WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, 'td_fadeOut_to_1'))
        )

        news_2_col = driver.find_element(By.CLASS_NAME, "tdi_92")
        news_2_box = news_2_col.find_elements(By.CLASS_NAME, "td-module-meta-info") 
        
        for box in news_2_box:
            news_title_2 = box.find_element(By.CLASS_NAME, "td-module-title") 
            news_headline = news_title_2.find_element(By.TAG_NAME, "a").text

            news_date = box.find_element(By.CLASS_NAME, "entry-date")
            news_date = str(news_date.get_attribute("datetime"))

            if news_date[:10] == str(today):
                news_link = news_title_2.find_element(By.TAG_NAME, "a").get_attribute("href")

                news_category_list.append(news_category)
                news_headline_list.append(news_headline)
                news_date_list.append(news_date)
                news_link_list.append(news_link)
                thereIs_news = True
        
        if not thereIs_news:
            print("no more news here")
            page = 1 
            thereIs_news = False
            break

        print("going to next page...")
        page += 1
        nextPage = driver.find_element(By.CSS_SELECTOR, '[aria-label="next-page"]')
        nextPage.click()

    print(f"today {site_nav['section']} news retrieved")

#TODO if empty string try again
print('\nReading news article...')
for newsLink in news_link_list:
    driver.delete_all_cookies()
    driver.get(f"{newsLink}")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'tdi_69'))
    )

    paragraphs_container = driver.find_element(By.CLASS_NAME, 'tdi_69')
    paragraphs_container = paragraphs_container.find_element(By.CLASS_NAME, 'tdb-block-inner')
    paragraph =  paragraphs_container.find_elements(By.TAG_NAME, 'p')
    news_description = ' '.join(p.text for p in paragraph)

    news_description_list.append([news_description])  

print("\nALL today news retrieved!")
driver.quit()

print('Compiling news...')
count = 0
for news in news_headline_list:
    today_news.append([
        news_category_list[count], 
        news_headline_list[count], 
        news_date_list[count], 
        news_link_list[count], 
        news_description_list[count]
        ])
    count+=1

df = pd.DataFrame(today_news, columns=['Category', 'Headline', 'Date', 'Link', 'Description'])
df.to_csv(f'todaynews_{today}.csv', encoding='utf-8-sig')
print("today news compiled\n")