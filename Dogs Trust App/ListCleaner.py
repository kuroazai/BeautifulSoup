# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 02:04:07 2019

@author: KuroAzai
"""

def clean(span):
    span = [x for x in span if x]
    NameLoc = []
    for x in span : 
        invalid = ["<span>", "</span>", "<strong>", "</strong>"]
        #print(x)
        for y in invalid:
            if y in str(x): 
                x = x.replace(str(y),"")
                NameLoc.append(x)
    NameLoc = [x for x in NameLoc if x]
    #Second check 
    span = []
    c = 0
    for x in NameLoc:
        #Strip Empty space
        NameLoc[c] = x.rstrip()
        NameLoc[c] = x.lstrip()
        invalid = ["<span>", "</span>", "<strong>", "</strong>"]
        for y in invalid:
            if y in str(x): 
                NameLoc[c] = x.replace(str(y),"")
        c += 1
    NameLoc = [x for x in NameLoc if x]
    return NameLoc