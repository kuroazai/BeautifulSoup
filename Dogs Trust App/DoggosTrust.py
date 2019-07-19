# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 22:13:14 2019

@author: KuroAzai

early version of a script that's being used in an personal project am creating for an application that notifies the user for specific breeds they are looking to adopt. 

"""


from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings() #NOT RECOMMENEDED!!!
import re
import ListCleaner
http = urllib3.PoolManager()




#Dogulus Rift Class that allows us to store information on search paramters and contents of the page(not included in this)

#Build search String   
    
def SearchForDoggos(): 
    #paramters is the area code, breed code, breed size and breed age
    example = "https://www.dogstrust.org.uk/rehoming/dogs/filters/~~~~~n~"
    #Make the soup 
    response = http.request('GET', example) 
    soup = BeautifulSoup(response.data, "html.parser") 
    #Doggos 
    Doggos = soup.findAll("div", {"class": "col-xs-6 col-sm-4 col-lg-3"})
    
    result = re.findall('"([^"]*)"', str(Doggos))
    #get the breed of the doggo
    span = re.findall('<span>([^"]*)</span>', str(Doggos))
    spans = []
    
    c = 0
    #print(len(span))
    for x in span :
        #print(x)
        x = str(x).splitlines()
        spans.append(x)
        c += 1
        #print(c)
      
    #Clean up the name and the breed 
    span = []
    for x in spans :    
        x = ListCleaner.clean(x)
        span.append(x)
    
    #span = str(span[0]).replace("<span>", "")
    #print(h3[0])
    Dog = []
    for x in result :
        if "JPG" in x:
            pic = x 
            for y in result:
                if "/rehoming/dogs/dog/filters/" in y:
                    y = y.split("/")
                    name = y[len(y)-1]
                    Dog.append([name,pic])       
            
    return Dog,span

#Obtain information 
def ObtainDoggos():
    #The url we wish to "Extract" data from 
    url = "https://www.dogstrust.org.uk"
    response = http.request('GET', url) 
    soup = BeautifulSoup(response.data, "html.parser") 
    
    #Empty arrays ~ ~ ~ 
    locations = []
    DogSize = []
    DogBreeds = [[]]
    DogAge = []
    

    '''LOCATIONS'''    
    #Get possible Locations 
    locations = soup.findAll("div", {"class": "form-group form-group--primary"})
    #Split text string as this is "1" entire element
    locations = str(locations).splitlines()
    #Storage for all the locations 
    LocList = []
    for x in locations : 
        #Find tags with "value" 
        if "value" in str(x):
            result = re.findall('"([^"]*)"', x)
            #Remove the first value
            if len(result) > 1: 
                del result[0]
            LocList.append(result)
            
            
            
    '''DOG SIZES'''
    #Get the Dog Size Catagories 
    DogSize = soup.findAll("div", {"class": "form-group form-group--primary form-group--mid"})
    SizeList = [] 
    #Split text string as this is "1" entire element and allows for us to iterate
    DogSize = str(DogSize).splitlines()
    for x in DogSize : 
        if "value" in str(x):
            result = re.findall('"([^"]*)"', x)
            #Remove the first value
            if len(result) > 1: 
                del result[0]
            SizeList.append(result)
            
            
            
    '''DOG Breeds'''
    #Get the dog breeds
    DogBreeds = soup.findAll("div", {"class": "form-group form-group--secondary"})
    BreedList = [] 
    #Split text string as this is "1" entire element and allows for us to iterate
    DogBreeds = str(DogBreeds).splitlines()
    for x in DogBreeds : 
        if "value" in str(x):
            #Find the code for the breed
            code = re.findall('"([^"]*)"', x)
            #Find the breed name 
            breed = re.findall('>([^"]*)<', x)
            #Remove the first value
            if len(result) > 1: 
                del result[0]
            BreedList.append([code, breed])
            
            
            
    '''DOG Ages'''
    #Get the dog ages 
    DogAge = soup.findAll("div", {"class": "form-group form-group--secondary form-group--tertiary"})
    AgeList = [] 
    #Split text string as this is "1" entire element and allows for us to iterate
    DogAge = str(DogAge).splitlines()
    for x in DogAge : 
        if "value" in str(x):
            result = re.findall('>([^"]*)<', x)
            code = re.findall('"([^"]*)"', x)
            #Remove the first value
            if len(result) > 1: 
                del result[0]
            AgeList.append([code,result])            
    return AgeList

            
#Return values from functions
a = ObtainDoggos()
b,c = SearchForDoggos()



#Set a counter
counter = 0 
#Print all the dogs alongside their information
for x in b:
    if counter < len(c) - 1 :
        print("\n\nDog Name : ", x[0], "\nDog Pic : ", x[1], "\nDog Breed : ", c[counter][0], "\nDog Location : " , c[counter][1])
    counter += 1


