from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import os
import requests
from pprint import pprint


def init_browser():
    # @NOTE: double check the actual path to chromedriver.exe
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

################################################################################

def scrape():       
    browser = init_browser()
    # response = requests.get (url)
    time.sleep(1)  
    
# -- Scrape #1 ---- Web Scrape for Mars News  -------------------

    # Visit NASA URL
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    # =======================================================================

    time.sleep(4)    
    # =======================================================================
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    time.sleep(2)    
    # =======================================================================
    # Find all div elements with class = list_text
    results = soup.find_all("div",class_="list_text")
    # soup.title.text
    
       
    for result in results[:1]:
        try:
            title=result.find('div',class_="content_title").a.text
            description=result.find('div',class_="article_teaser_body").text
            # print("title and descriptions are :")
            # print("-----------------------------")
            # if(title and description):
            if(description and title):
                print(title)
                print(description)
        except AttributeError as e:
            print(e)
            
    # Capture the date of the Latest Mars_news
    news_date=result.find('div',class_="list_date").text
    print(news_date)

    # save title, descripton and News Date into news dictionary
    marsinfo = {
        "title": title,
        "news_sum": description,
        "date": news_date
    }    
    # =======================================================================

# -- Scrape #2 ---- Web Scrape for NASA Featured Image  -------------------

    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(3)

    soup2 = bs(browser.html, 'html.parser')
    result_img=soup2.find('article', class_="carousel_item")

    featured_image_urlx = result_img['style'][23:-3]
    featured_image_url = 'https://www.jpl.nasa.gov/' + featured_image_urlx
    print(featured_image_url)
    # save to news dictionary
    marsinfo["featured_image_url"]=featured_image_url

# -- Scrape #3 ---- Mars Weather (Twitter Account Web Scraping)  -------------------

    url="https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    soup3 = bs(browser.html, 'html.parser')
    results3 = soup3.find_all('div', class_="js-tweet-text-container")
    
    for result in results3[:1]:
       mars_weather=result.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    # save to news dictionary
    marsinfo["mars_weather"]=mars_weather
    marsinfo["mars_weather"]
    print(result)
    
    # -- Scrape #4 ---- Mars Facts scraped with Pandas Web Scraping  -------------------
    
    facts_url = 'https://space-facts.com/mars/'
    panda_tables = pd.read_html(facts_url)
    facts_df = panda_tables[0]
    facts_df.columns = ['Fact Category', 'Data']
    facts_df.set_index('Fact Category', inplace=True)
    # save to a html file
    facts_df.to_html('mars_facts_table.html')
    # save the dataframe to a html string
    mars_facts_table = facts_df.to_html()
    ## remove all the \n characters (for new lines) ##
    mars_facts_table2 = mars_facts_table.replace('\n', '')
    # save to news dictionary
    marsinfo['mars_facts']= mars_facts_table2
    print(facts_df)
    
    # -- Scrape #5 ---- Mars Hemisphere Photos - Web Scraping  -------------------

    url_images = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_images)
    html_images = browser.html
    soup4 = bs(html_images, 'html.parser')

    headers = []
    titles = soup4.find_all('h3')
    time.sleep(5)
    for title in titles:
        headers.append(title.text)
    
    images = []
    count = 0
    for thumb in headers:
        browser.find_by_css('img.thumb')[count].click()
        images.append(browser.find_by_text('Sample')['href'])
        browser.back()
        count = count+1
        
    hemisphere_images_urls = []  #initialize empty list to collect titles
    counter2 = 0
    for item in images:
        hemisphere_images_urls.append({"title":headers[counter2],"img_url":images[counter2]})
        counter2 = counter2+1

    time.sleep(2)
    marsinfo["hemisphere_images_urls"]=hemisphere_images_urls
    print()
    print(hemisphere_images_urls)


# ------------------------------------------------------------------------------

    # Close the browser after scraping
    browser.quit()
    
    return marsinfo


    
