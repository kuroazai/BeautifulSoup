# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 01:40:06 2019

@author: KuroAzai 

Retrieving information from the league of legends website for every characters name.
Practically we can just use the offical API for this, but the rogue method is more fun. 

"""


from bs4 import BeautifulSoup
import urllib3 
http = urllib3.PoolManager()
urllib3.disable_warnings() 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#system
import re
import os
import random


class legends: 
    
    def __init__ (self):
        self.champions = []
        self.nofchampions = None
        
    def count_champions(self): 
        self.nofchampions = len(self.champions)
        return print(self.nofchampions) 
    
    def Clear_Champions(self):
        #Create an empty list
        self.champions = []
        #Update the size 
        self.nofchampions = len(self.champions)
        #Completion msg 
        return print("\nChampions Cleared")
    
    def Add_Champion(self, champion):
        if type(champion) == list:
            for x in champion: 
                self.champions.append(x)
        else:    
            self.champions.append(champion)
            #Update Count
            self.count_champions()
            #Completion msg 
            return print("\n" + str(champion) + " has been added")
        #Update Count
        self.count_champions()
        #Completion msg
        return print("\nChampions have been Added")

    def Remove_Champion(self,champion):
         #Convert to set
         self.champions = set(self.champions)
         #Remove Matching element
         self.champions.remove(champion)
         #Revert back to list 
         self.champions = list(self.champions)
         #Update Count
         self.count_champions()
         #Completion msg
         return print("\nRemoved " + str(champion))
         

def kill_gecko():
    #Onstart/finish Ensure all instances are closed
    os.system("taskkill /f /im geckodriver.exe /T")
    #WARNING CLOSES ALL FIREFOX INSTANCES ~ 
    os.system("taskkill /f /im firefox.exe /T")
    
def retrieve_names(): 
    #Url
    url = "https://na.leagueoflegends.com/en/game-info/champions/"    
    #Selenium FF browser options for headless 
    options = Options()
    options.headless = True 
    #Set the driver with its options 
    browser = webdriver.Firefox(options=options)
    #Get the results from our headless browser for our objects page
    browser.get(url)    
    #Make the Soup
    soup = BeautifulSoup(browser.page_source, 'lxml')
    #print(soup) champion-grid-Aatrox
    result = re.findall('"champion-grid-([^"]*)"', str(soup))
    return result
    
def append_names(names):
    #for all names within the list
    for x in names: 
        lol.champions.append(x)
    #Count Entries
    print(lol.count_champions())

#Create the object
lol = legends()   
#Retrieve the names from the website   
a = retrieve_names()
#Remove the first 2 elements that are irrelevant
a = a[2:len(a)-1]
#Run function to add all champion names to the object
lol.Add_Champion(a)
#Pick a random number 
rng  = random.randint(0,lol.nofchampions-1)
#Save the name 
b = lol.champions[rng]
print(lol.champions[rng])

#Remove The champion 
lol.Remove_Champion(b)
#Add The champion
lol.Add_Champion(b)
#Clear List 
lol.Clear_Champions()

#Finished
print("Completed mi'lord")
