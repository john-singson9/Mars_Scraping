
# coding: utf-8

# # Mission to Mars

# # # Pseudocodes
# ### Step 2 Codes: MongoDB and Flask
# 1.  Convert the notebook to a python script:  scrape_mars.py
# 2.  Add a function called 'scrape' to execute all the scraping code from above to return one python dictionary
# 3.  Use flask to create a route called '/scrape'
# 4.  Import scrape_mars.py and call scrape function
# 5.  Store everything in a MongoDB as a dictionary
# 6.  Create a route '/' to query MongoDB database
# 7.  Pass the mars data into an HTML template
# 8.  Create html file: index.html
# 9.  take teh mars data dictionary and display data in appropriate HTML element
# 10. design the website

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

def scrape():
    browser = Browser('chrome', **executable_path, headless=False)

    #final data dictionary
    final_data = {}

    #Mars News
    News_url = 'https://mars.nasa.gov/news/'
    browser.visit(News_url)
    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')
    news_title = news_soup.find('div', class_='content_title').text
    news_p = news_soup.find('div', class_='rollover_description_inner').text

    #Featured Mars Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    image_html = browser.html
    image_soup = bs(image_html, 'html.parser')
    mars_url = image_soup.find('a', class_='button fancybox')['data-fancybox-href']
    featured_image_url = "https://www.jpl.nasa.gov" + mars_url

    #Mars Weather
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    weather_html = browser.html
    weather_soup = bs(weather_html, 'html.parser')
    mars_weather = weather_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text


    #Mars Facts
    facts_url = "https://space-facts.com/mars/"
    facts_html = pd.read_html(facts_url)
    mars_dataframe = pd.DataFrame(facts_html[0])
    mars_dataframe = mars_dataframe.rename(columns={0: 'Description', 1: 'Values'})
    mars_dataframe = mars_dataframe.set_index('Description')
    mars_facts = mars_dataframe.to_html(classes='mars table', header=True, index=True)
    mars_table = mars_facts.replace('\n', ' ')


    #Mars Hemispheres
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'html.parser')

    hemispheres = hemisphere_soup.find('div', class_='collapsible results')
    hemisphere_image_urls = []

    for hemisphere in hemispheres:
        try:
            title = hemisphere.find('h3').text
            url = hemisphere.find('a')['href']
            if (title and url):
                link = "https://astrogeology.usgs.gov" + url
                browser.visit(link)
                html = browser.html
                soup = bs(html, 'html.parser')
                hemi_image = soup.find('div', class_='downloads')
                hemi_link = hemi_image.find('a')['href']
#             print(hemi_link)
                hemisphere_image_urls.append({"title": title, "img_url": hemi_link})
        except:
            print("This data is not added to the dictionary.  Title and link does not exist")

    # Check Outputs
    print(news_title)
    print(news_p)
    print(featured_image_url)
    print(mars_weather)
    print(mars_table)
    print(hemisphere_image_urls)  

    #Append the final data
    final_data["latest_news"] = news_title
    final_data["snippet"] = news_p
    final_data["image"] = featured_image_url
    final_data["weather"] = mars_weather
    final_data["table"] = mars_table
    final_data["hemispheres"] = hemisphere_image_urls

    browser.quit()

    return final_data

scrape()