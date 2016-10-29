import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# hitting the ffiec website with a "get" request
r = requests.get("https://www.ffiec.gov/nicpubweb/nicweb/HCSGreaterThan10B.aspx")
# saving response
html_doc = r.text
# parsing the page using BeautifulSoup module
soup = BeautifulSoup(html_doc, 'html.parser')
# reading option tag to know all the quarters
option_tags = soup.findAll('option')
# list to save data of all the files
records =[]
# list to header of all the columns
headers=[]
flag = 0
# for loop to traverse data for all quarters
for tags in option_tags:
    date = tags.contents
    # preparing the AJAX call to load data "quarter" wise
    date_str= str(date[0])
    if(date_str=='20131231'):        
        VIEWSTATE = '/wEPDwUKLTE2MjA0NjMwOA9kFgICAQ9kFggCAQ9kFgICAQ9kFgICDQ8PFgQeCENzc0NsYXNzBRRuYXYtbWVudUl0ZW1TZWxlY3RlZB4EXyFTQgICZGQCCw8QDxYEHg5EYXRhVmFsdWVGaWVsZAUCRFQeC18hRGF0YUJvdW5kZ2QQFQ8IMjAxNjA2MzAIMjAxNjAzMzEIMjAxNTEyMzEIMjAxNTA5MzAIMjAxNTA2MzAIMjAxNTAzMzEIMjAxNDEyMzEIMjAxNDA5MzAIMjAxNDA2MzAIMjAxNDAzMzEIMjAxMzEyMzEIMjAxMzA5MzAIMjAxMzA2MzAIMjAxMzAzMzEIMjAxMjEyMzEVDwgyMDE2MDYzMAgyMDE2MDMzMQgyMDE1MTIzMQgyMDE1MDkzMAgyMDE1MDYzMAgyMDE1MDMzMQgyMDE0MTIzMQgyMDE0MDkzMAgyMDE0MDYzMAgyMDE0MDMzMQgyMDEzMTIzMQgyMDEzMDkzMAgyMDEzMDYzMAgyMDEzMDMzMQgyMDEyMTIzMRQrAw9nZ2dnZ2dnZ2dnZ2dnZ2cWAQIJZAIRDw8WBB4EVGV4dAUvUGFnZSAxIG9mIDEmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDseB1Zpc2libGVnZGQCFQ9kFgICCA8PFgIeC05hdmlnYXRlVXJsBSkuLi9jb250ZW50L2hlbHAvSGVscEhjc0dyZWF0ZXJUaGFuMTBCLmh0bWRkZBWwz/JYEV3bp28EgBHdJMZZYIMXGitD9jM4w27uvSJU'
        VALIDATOR = '/wEdABHz6Ttalw9C7KoFbon/Gd6UK+AQNYofFo7sCHGzEgQxXqf3s5xgLdyEUgvHD7OB/TQU0JCm6twziTq7ZKu7C9V8rKO3BZ74DE9Va4euE9tdacmWeJcB3SD2bCBOuZB2caD0Gn1/cihgqKrQi/n2rsMMEn4f+9ehEisEvfvqS9vqtnSWyOyjlg4UMvMiJsjP/q5bXeMjR3EO/lQaBQQwSHzuvnkaPZrSK8Njo+YhAaaws1X+F5mNVvSmAxaDYJuf1rwsc+Kmv6CAM5kJKGVsg/WjZx50RJhDbtiAlUnLZHhM9O0wN4rz9ntuuIyvsyIXFhx19HsQApn8TrZo63GPCizoQf9+sfo7S7EA3mQfdUT0sE/gjRbWhvOyClU5yBbHz7631ZAd3e6UhWeHRLxAOdql'
    else:
        VIEWSTATE = '/wEPDwUKLTE2MjA0NjMwOA9kFgICAQ9kFggCAQ9kFgICAQ9kFgICDQ8PFgQeCENzc0NsYXNzBRRuYXYtbWVudUl0ZW1TZWxlY3RlZB4EXyFTQgICZGQCCw8QDxYEHg5EYXRhVmFsdWVGaWVsZAUCRFQeC18hRGF0YUJvdW5kZ2QQFQ8IMjAxNjA2MzAIMjAxNjAzMzEIMjAxNTEyMzEIMjAxNTA5MzAIMjAxNTA2MzAIMjAxNTAzMzEIMjAxNDEyMzEIMjAxNDA5MzAIMjAxNDA2MzAIMjAxNDAzMzEIMjAxMzEyMzEIMjAxMzA5MzAIMjAxMzA2MzAIMjAxMzAzMzEIMjAxMjEyMzEVDwgyMDE2MDYzMAgyMDE2MDMzMQgyMDE1MTIzMQgyMDE1MDkzMAgyMDE1MDYzMAgyMDE1MDMzMQgyMDE0MTIzMQgyMDE0MDkzMAgyMDE0MDYzMAgyMDE0MDMzMQgyMDEzMTIzMQgyMDEzMDkzMAgyMDEzMDYzMAgyMDEzMDMzMQgyMDEyMTIzMRQrAw9nZ2dnZ2dnZ2dnZ2dnZ2cWAQIKZAIRDw8WBB4EVGV4dAUvUGFnZSAxIG9mIDEmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDsmbmJzcDseB1Zpc2libGVnZGQCFQ9kFgICCA8PFgIeC05hdmlnYXRlVXJsBSkuLi9jb250ZW50L2hlbHAvSGVscEhjc0dyZWF0ZXJUaGFuMTBCLmh0bWRkZONxUmPX1g0JUI7fbXVvU7sJfGEaRpHwKpeACNj+2/rR'
        VALIDATOR = '/wEdABEkIZcMwABddn+Wq77q7NHuK+AQNYofFo7sCHGzEgQxXqf3s5xgLdyEUgvHD7OB/TQU0JCm6twziTq7ZKu7C9V8rKO3BZ74DE9Va4euE9tdacmWeJcB3SD2bCBOuZB2caD0Gn1/cihgqKrQi/n2rsMMEn4f+9ehEisEvfvqS9vqtnSWyOyjlg4UMvMiJsjP/q5bXeMjR3EO/lQaBQQwSHzuvnkaPZrSK8Njo+YhAaaws1X+F5mNVvSmAxaDYJuf1rwsc+Kmv6CAM5kJKGVsg/WjZx50RJhDbtiAlUnLZHhM9O0wN4rz9ntuuIyvsyIXFhx19HsQApn8TrZo63GPCizoQf9+sfo7S7EA3mQfdUT0sO5Xe47+MU0Y0AWVTQ9cqJ81XjQoMtFu8dPXV0jESt9m'
    
    payload = {'__EVENTTARGET': 'DateDropDown', 'DateDropDown':date_str, '__VIEWSTATE':VIEWSTATE, '__VIEWSTATEGENERATOR':'9686313C', '__EVENTVALIDATION':VALIDATOR}
    # hitting the ffiec website with a "post" request for specific date
    req = requests.post('https://www.ffiec.gov/nicpubweb/nicweb/HCSGreaterThan10B.aspx', data=payload)
    # saving response for specific date
    current_page = req.text 
    # parsing the page using BeautifulSoup module
    current_soup = BeautifulSoup(current_page, 'html.parser')
    # reading the table of our interest
    tabl = current_soup.find("table",attrs={'id':'dgTop50'})
    if tabl:                                # "if condtion" to check whether the data available for that date
        tbl = tabl.findAll("tr")
        # "for loop" to read all rows of data
        for tr in tbl[1:]:
            trs = tr.findAll('td')
            # list for individual row of data
            record=[]
            # extracting RSSID
            record.append((trs[1].text).strip("\n")[-8:-1])
            # extracting Bank Name
            record.append((trs[1].text).strip("\n")[:-10])
            # extracting Location
            record.append(trs[2].text)
            # extracting Assets value
            record.append(trs[3].text)
            # new column to keep quarter date
            record.append(date_str)
            # saving the record in a list
            records.append(record)
            
        # "for loop" to read all headers of columns
        if(flag==0):
            for tr in tbl[:1]:
                trh = tr.findAll("th")
                # RSSID
                headers.append(trh[1].text[-8:-1])
                # Bank Name
                headers.append(trh[1].text[:-10])
                # Location
                headers.append(trh[2].text)
                # Total Assets
                headers.append(re.sub("[^a-zA-Z]+", "", trh[3].text))
                headers.append("Date")
                flag = 1

# converting above table into a DataFrame
df = pd.DataFrame(data= records,columns=headers)
# saving the same into a CSV file (stacked version)
df.to_csv("main.csv",sep=",",index=False)
# converting it to different DataFrame pivoted on quarters
df1 = pd.pivot_table(df,index=["RSSD ID","Institution Name","Location"],columns="Date",values="TotalAssets",aggfunc='first')
# saving ito to a CSV file (unstacked version)
df1.to_csv("main_unstack.csv",sep=",")

