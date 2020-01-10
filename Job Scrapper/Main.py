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


   
def usr_inputs():
    switch = True
    keywords = []
    print('''
          Help : 
          del - deletes last entry,
          clr - clears the input list, 
          shw - shows current entries, 
          done - run with given parameters,
          ''')
    print("Please enter a Keyword / Location to append to search Critia \n \n")  

    while switch == True:      
        print("\n#",len(keywords) + 0, " :Waiting for input")
        x = input()       
        #Check contents 
        if x == "del":
            #remove last entry
            keywords.pop()
        if x == "clr":
            #Empty the array
            keywords = []
        if x == "shw":
            #Show all current entries
            for y in keywords:
                print(y)
        if x == "done":
            #break from loop
            print("\n Completed\n\n")
            break
        elif x != "del" and x != "cls":
            #append new input
            keywords.append(x)
                      
    return keywords
        
    
def Angel_Login():
    
    def json_login():
        with open('data.json') as json_file:
            data = json.load(json_file)
        driver = browser
        driver.find_element_by_id("user_email").send_keys(data['user[email]'])
        driver.find_element_by_id ("user_password").send_keys(data['user[password]'])
        driver.find_element_by_xpath('//input[@type="submit"]').click()
        return driver
        
    def input_login():
        data = []
        print("Enter Email")
        data.append(input())
        print("Enter Password")
        data.append(input()) 
        driver = browser
        driver.find_element_by_id("user_email").send_keys(data[0])
        driver.find_element_by_id ("user_password").send_keys(data[1])
        driver.find_element_by_xpath('//input[@type="submit"]').click()
        return driver
    
    url = "https://angel.co/login" 
    #Selenium FF browser options for headless 
    options = Options()
    #Run Driver in headerless mode
    options.headless = False
    #Set the driver with its options 
    browser = webdriver.Firefox(options=options)
    #Get the results from our headless browser for our objects page
    browser.get(url)
         
    #Choose login funciton, using Json file to avoid repetitveness of logins
    driver = json_login()
    
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
        for x in arg:
            searchbox.send_keys(x)
            searchbox.send_keys(Keys.RETURN)
    
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]').click()
    time.sleep(2)
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
    i = 0
    while True and i < 10:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i += 1
        
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
    #Get Inputs store them as keywords
    kw = usr_inputs()
    #Kill Previous Instances due to headless mode(Kills firefox instances)
    kill_gecko()
    #Login into angel list
    driver = Angel_Login()
    #Search for desired skills/locations
    soup = Angel_JobScrap(driver,kw)
    #Process with soup
    Companies(soup)


if __name__ == "__main__":
    main()
