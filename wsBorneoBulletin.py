from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from datetime import date
import pandas as pd

today_news_list = []
news_headline_list = []
news_category_list = []
news_date_list = []
news_link_list = []
news_description_list = []

SITE_NAV_LIST = [
            {'section' : 'national'}, 
            {'section' : 'southeast'}, 
            {'section' : 'world'},
            {'section' : 'business'},
            {'section' : 'tech'},
            {'section' : 'lifstyle'},
            {'section' : 'entertainment'},
            {'section' : 'sports'},
            {'section' : 'features'},
            {'section' : 'opinion'} 
            ]

page = 1
today = date.today()
gecko = 'geckodriver.exe'
STARTING_PAGE = "https://borneobulletin.com.bn/"

service = Service(executable_path=gecko)
firefox_options = Options()
# firefox_options.add_argument("-headless") 
driver = webdriver.Firefox(service=service, options=firefox_options)

def save_data(category, headline, date, link):
    news_category_list.append(category)
    news_headline_list.append(headline)
    news_date_list.append(date)
    news_link_list.append(link)

def close_popup():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'tdm-popup-modal'))
    )
    closeAds = driver.find_element(By.CLASS_NAME, "tdm-pmh-close")
    closeAds.click()

def block55_scraper(news_category):
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
                
            save_data(news_category, news_headline, news_date, news_link)

def block92_scraper(news_category, page=1):
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

                save_data(news_category, news_headline, news_date, news_link)
                thereIs_news = True
        
        if not thereIs_news:
            print("no more news here")
            page = 1 #reset num
            break

        print("going to next page...")
        page += 1
        nextPage = driver.find_element(By.CSS_SELECTOR, '[aria-label="next-page"]')
        nextPage.click()

def page_scraper():
    for site_nav in SITE_NAV_LIST:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'tdb-menu-item-text'))
        )
        print(f"\n----- {site_nav['section']} News ------------------")
        news_category = site_nav['section']
        driver.get(f'https://borneobulletin.com.bn/category/{site_nav['section']}/')

        block55_scraper(news_category)
        block92_scraper(news_category)

    print(f"today {site_nav['section']} news retrieved")

def get_description():
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

def news_compiler():
    print('Compiling news...')
    count = 0
    for news in news_headline_list:
        today_news_list.append([
            news_category_list[count], 
            news_headline_list[count], 
            news_date_list[count], 
            news_link_list[count], 
            news_description_list[count]
            ])
        count+=1

    df = pd.DataFrame(today_news_list, columns=['Category', 'Headline', 'Date', 'Link', 'Description'])
    df.to_csv(f'todaynews_{today}.csv', encoding='utf-8-sig')
    print("today news compiled\n")

def scraper():
    driver.get(STARTING_PAGE) 
    print('\nToday is,', today)

    close_popup()
    page_scraper()
    get_description()
    print("\nALL today news retrieved!")

    driver.quit()

    news_compiler()



if __name__ == '__main__':
    scraper()