# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 7:00:45 2020

@author: Kuro Azai
Selenium Appraoch
"""


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import urllib3
import os 
import time
import json 
urllib3.disable_warnings() 
http = urllib3.PoolManager()


   
def Angel_Login():
    url = "https://angel.co/login" 
    #Selenium FF browser options for headless 
    options = Options()
    #Run Driver in headerless mode
    options.headless = True
    #Set the driver with its options 
    browser = webdriver.Firefox(options=options)
    #Get the results from our headless browser for our objects page
    browser.get(url)
    
    #Open Json with login data
    with open('data.json') as json_file:
        data = json.load(json_file)
        
    driver = browser
    driver.find_element_by_id("user_email").send_keys(data['user[email]'])
    driver.find_element_by_id ("user_password").send_keys(data['user[password]'])
    driver.find_element_by_xpath('//input[@type="submit"]').click()
    time.sleep(3)
    return driver

def Angel_JobScrap(driver,*args):
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #Find Keywords
    mydivs = soup.findAll("div", {"class": "new_taggings tag_edit"}) 
    #Clear Existing Keywords
    i = 0
    while i < len(mydivs):
        kw = 'html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/img'  
        driver.find_element_by_xpath(kw).click()
        i += 1
    #Input New Keywords
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]').click()
    searchbox = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/input')
    for arg in args:
        searchbox.send_keys(arg)
        searchbox.send_keys(Keys.RETURN)
    
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]').click()
    #Scroll to the bottom of the page
    Scroll_Down(driver)

    #Make another soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def Scroll_Down(driver):
    #Feature by OWADVL
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
def Companies(soup):    
    jobs = soup.findAll("a", {"class": "startup-link"})
    
    for x in jobs:
        print(x.contents[0], "\n", x['href'] , "\n")
     

def kill_gecko():
    #Onstart/finish Ensure all instances are closed
    os.system("taskkill /f /im geckodriver.exe /T")
    #WARNING CLOSES ALL FIREFOX INSTANCES ~ 
    os.system("taskkill /f /im firefox.exe /T")
    

def main():
    #Kill Previous Instances due to headless mode
    kill_gecko()
    #Login into angel list
    driver = Angel_Login()
    #Search for desired skills/locations
    soup = Angel_JobScrap(driver,"Python","Oxford")
    #Process with soup
    Companies(soup)


if __name__ == "__main__":
    main()