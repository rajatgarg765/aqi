# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 06:47:48 2021

@author: info
"""


from plotting_avg import avg_data_2013,avg_data_2014,avg_data_2015,avg_data_2016
import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv

def met_data(month, year):
 #reading the html files that we scarpped from web   
    file_html = open('Data/html_Data/{}/{}.html'.format(year,month), 'rb')
    plain_text = file_html.read()

    tempD = []
    finalD = []

#using beatufil soup to get the html tags and getting the text inside it
#using the class found in inspect
    soup = BeautifulSoup(plain_text, "html.parser")
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a = tr.get_text()
                tempD.append(a)
#finding the total no rows by (m*n=total elemnts)
    rows = len(tempD) / 15
#storing in the forms of rows so looping upto 15 as we have 15 featurs
    for times in range(round(rows)):
        newtempD = []
        for i in range(15):
            newtempD.append(tempD[0])
            tempD.pop(0)
        finalD.append(newtempD)

    length = len(finalD)
#deleing the first line that contain names of feature 
#deleing the last line that is of no use
    finalD.pop(length - 1)
    finalD.pop(0)
#since we dont need the empy the values therefore deleingall empy 
#using for and pop
    for a in range(len(finalD)):
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)

    return finalD
#combine all csv data in one file
def data_combine(year, cs):
    for a in pd.read_csv('data/Real-Data/real_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist


if __name__ == "__main__":
   #making the directory names  real data 
    if not os.path.exists("data/Real-Data"):
        os.makedirs("data/Real-Data")
#making files with real_2013 and all using open   
    for year in range(2013, 2017):
        final_data = []
        with open('data/Real-Data/real_' + str(year) + '.csv', 'w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
#adding the festures row manually
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
#we will get all the data from html files and we adding to final data for every month
#so that we can append to the one file         
        for month in range(1, 13):
            temp = met_data(month, year)
            final_data = final_data + temp
#below statement is used to astore the avg of PM2.5 and below for loop loop 
#is use to append in our csv file            
        pm = getattr(sys.modules[__name__], 'avg_data_{}'.format(year))()
#no required at all
        if len(pm) == 364:
            pm.insert(364, '-')
#appending at the last feature that is PM2.5 
        for i in range(len(final_data)-1):
            # final[i].insert(0, i + 1)
            final_data[i].insert(8, pm[i])
#making new file whivh will have final data that is combined
        with open('data/Real-Data/real_' + str(year) + '.csv', 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
#drooping the empyty places in final data           
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)
                    
    data_2013 = data_combine(2013, 600)
    data_2014 = data_combine(2014, 600)
    data_2015 = data_combine(2015, 600)
    data_2016 = data_combine(2016, 600)
     
    total=data_2013+data_2014+data_2015+data_2016
#another csv file     
    with open('data/Real-Data/Real_Combine.csv', 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
        
        
df=pd.read_csv('data/Real-Data/Real_Combine.csv')