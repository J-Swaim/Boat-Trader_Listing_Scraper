# Author: James P Swaim
# Start Date: 2022-09-03
# Revision 1: 2022-09-04
# Web scraper class - Individual Listings on Boat Trader
# Intended for use with list of URLs from scraping search page

#Imports
from bs4 import BeautifulSoup   # HTML Scraper
import requests
from datetime import date

import smtplib                  # Email Sender
import csv                      # CSV Creator

class BoatTraderPage:
    # Global variable declarations (Common to all instances)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    
    # Default Constructor
    def __init__(self):
        # Instance variable declarations (Instance specific)
        print('No URL Given')
    
    # URL Constructor
    def __init__(self, url):
        # Instance variable declarations (Instance specific)
        self.url = url
        
        page = requests.get(self.url, headers=self.headers)
        
        webpage = BeautifulSoup(page.content, 'html.parser')
        self.cleanPage = BeautifulSoup(webpage.prettify(), 'html.parser')
        
    # Scrape URL
    # Returns an array of information on the listing following the format
    # "&Description&: &Value&"
    def scrape(self):
        # Scrape function
        info = []
        
        info.append(self.cleanPage.find(class_='heading').get_text().strip())
        info.append(self.cleanPage.find(class_='payment-total').get_text().strip())
        info.append(self.cleanPage.find(class_='location').get_text().strip())
        
        for word in self.cleanPage.find_all(class_='datatable-item'):
            entryTitle = word.find(class_='datatable-title').get_text().strip()
            val = word.find(class_='datatable-value').get_text().strip()
            entry = entryTitle + ': ' + val
            
            info.append(entry)
        
        return info

class BoatTraderSearch:
    # Global variable declarations (Common to all instances)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    
    # Default Constructor
    def __init__(self):
        # Instance variable declarations (Instance specific)
        print('No URL Given')
    
    # URL Constructor
    def __init__(self, url):
        # Instance variable declarations (Instance specific)
        self.url = url
        
        page = requests.get(self.url, headers=self.headers)
        
        webpage = BeautifulSoup(page.content, 'html.parser')
        self.cleanPage = BeautifulSoup(webpage.prettify(), 'html.parser')
        
    # Scrape URL
    def scrape(self):
        # Scrape function
        links = []
        
        for word in self.cleanPage.find_all(class_='main-link'):
            links.append(word['href'])
            
        return links

class CsvWriter():
    #New File Constructor
    
    def __init__(self):
        self.filename = 'BoatTrader.csv'
        
        with open(self.filename, 'w', newline='', encoding='UTF8') as file:
            writer = csv.writer(file)
        
    #Existing file Constructor
    def __intit__(self, filename):
        self.filename = filename
        
        with open(self.filename, 'w', newline='', encoding='UTF8') as file:
            writer = csv.writer(file)
        
    def writeEntry(self, allInfo):
        with open(self.filename, 'w', newline='', encoding='UTF8') as file:
            for entry in allInfo:
                writer = csv.writer(file)
                writer.writerow(entry)

trader2 = BoatTraderSearch('https://www.boattrader.com/boats/type-sail/zip-50701/radius-300/length-30/price-0,30000/')

allInfo = [['Title','Price','Location','Date','Link']]

for link in trader2.scrape():
    traderPage = BoatTraderPage(link)
    
    pageInfo = traderPage.scrape()
    pageInfo.insert(3,link)
    pageInfo.insert(3,date.today())
    
    allInfo.append(pageInfo)

righter = CsvWriter()
righter.writeEntry(allInfo)
