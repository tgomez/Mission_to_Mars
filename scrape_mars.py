## this file was originally Mission_to_Mars.ipynb
## I used '$jupyter nbconvert Mission_to_Mars.ipynb --to python' to convert file to python
# coding: utf-8

# In[1]:


#Import dependencies needed
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import tweepy
import json
import time 
from bs4 import BeautifulSoup
import requests
import pymongo


#Import dependencies needed to get Mars Weather from Twitter
from APITweeter2 import consumer_key
from APITweeter2 import consumer_secret
from APITweeter2 import access_token
from APITweeter2 import access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define database and collection
db = client.Mars
collection = db.Mars


def init_browser():
    executable_path = {"executable_path": "/Users/tiffanygomez/Downloads/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
def scrape():
    browser = init_browser()

    # Create a dictionary for all of the scraped data
    mars_data = {}


    #NASA Mars News
    #News Article Content
    UrlArticle = "https://mars.nasa.gov/news/"
    browser.visit(UrlArticle)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Save Recent Article Info
    article = soup.find("div", class_="list_text")
    news_p = article.find("div", class_="article_teaser_body").text
    news_title = article.find("div", class_="content_title").text
    news_date = article.find("div", class_="list_date").text

    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["summary"] = news_p

    # Featured Mars Image

    # Visit the url for JPL's Featured Space Image
    urlImage = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(urlImage)

    # Scrape and save image url
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url

    #add img to dict
    mars_data["featured_image_url"] = featured_image_url

    # Download and save Img
   
    # Mars Weather
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target = "@MarsWxReport"
    weather = (api.user_timeline(target, count=1, result_type="recent"))[0]["text"]
    weather

    # add to dict
    mars_data["mars_weather"] = mars_weather

    # Mars Facts
    urlFacts = "https://space-facts.com/mars/"
    browser.visit(urlFacts)

    grab=pd.read_html(urlFacts)
    mars_data=pd.DataFrame(grab[0])
    mars_data.columns=['Mars','Data']
    mars_table=mars_data.set_index("Mars")
    marsdata = mars_table.to_html(classes='marsdata')
    marsdata=marsdata.replace('\n', ' ')
    marsdata

    #add to dict
    mars_data["mars_table"] = marsinformation

    # Mars Hemisperes
    # Visit the USGS Astrogeology site
    urlHem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(urlHem)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    mars_hemis=[]



    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemis.append(dictionary)
        browser.back()

    mars_data['mars_hemis'] = mars_hemi

    return mars_data

# Dictionary to be inserted as a MongoDB document
post = {mars_data}

collection.insert_one(post)



