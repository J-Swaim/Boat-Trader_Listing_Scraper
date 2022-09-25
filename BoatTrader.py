# Author: James P Swaim
# Start Date: 2022-09-03
# Revision 1: 2022-09-04
# Script for getting listing from boattrader.com
# Requirements: Provide a URL for a valid search on Boat Trader

#Imports
from bs4 import BeautifulSoup   # HTML Scraper to get data
import requests                 # HTML Library to get page
from datetime import date       # To get current date
import csv                      # CSV Writer to write data

# Scrapes an individual listing's unique page
class BoatTraderPage:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    
    # Default Constructor
    def __init__(self):
        print('No URL Given')
    
    # URL Constructor
    def __init__(self, url):
        self.url = url
        
        #Get listing page and clean up
        page = requests.get(self.url, headers=self.headers)
        webpage = BeautifulSoup(page.content, 'html.parser')
        self.cleanPage = BeautifulSoup(webpage.prettify(), 'html.parser')
        
    # Function to scrape page
    # Returns an array of information on the listing following the format:
    # "&Description&: &Value&"
    def scrape(self):
        # Array of page information
        info = []
        
        # Basic information available in same place on all listings
        info.append(self.cleanPage.find(class_='heading').get_text().strip())
        info.append(self.cleanPage.find(class_='payment-total').get_text().strip())
        info.append(self.cleanPage.find(class_='location').get_text().strip())
        
        # Advanced info not consistently available in all listings
        for word in self.cleanPage.find_all(class_='datatable-item'):
            entryTitle = word.find(class_='datatable-title').get_text().strip()
            val = word.find(class_='datatable-value').get_text().strip()
            entry = entryTitle + ': ' + val
            info.append(entry)
        
        #return the array of information gathered from the listing
        return info

# Scrapes the search page to get URLs for individual listings
class BoatTraderSearch:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    
    # Default Constructor
    def __init__(self):
        print('No URL Given')
    
    # URL Constructor
    def __init__(self, url):
        self.url = url
        
        # Get search page and clean up
        page = requests.get(self.url, headers=self.headers)
        webpage = BeautifulSoup(page.content, 'html.parser')
        self.cleanPage = BeautifulSoup(webpage.prettify(), 'html.parser')
        
    # Function to scrape page
    # Returns an array of URLs to individual listings
    def scrape(self):
        links = []
        
        for word in self.cleanPage.find_all(class_='main-link'):
            links.append(word['href'])
            
        return links

# Class to write results to a CSV file
class CsvWriter():
    
    # Default Constructor
    def __init__(self):
        self.filename = 'BoatTrader.csv'
        
    # Existing file Constructor
    def __intit__(self, filename):
        self.filename = filename
        
    # Function to write a 2D array of information to a CSV file
    def writeEntry(self, allInfo):
        with open(self.filename, 'w', newline='', encoding='UTF8') as file:
            for entry in allInfo:
                writer = csv.writer(file)
                writer.writerow(entry)

# Create a boat trader search object to get an array of listing URLs
trader2 = BoatTraderSearch('https://www.boattrader.com/boats/type-sail/zip-50701/radius-300/length-30/price-0,30000/')

# Array to hold the results. This initialization creates headers for the information that will be in all listings
allInfo = [['Title','Price','Location','Date','Link']]

# Gets individual listing info for every search result
for link in trader2.scrape():
    # Create a trader page object for the current search result
    traderPage = BoatTraderPage(link)
    
    # Add info from listing page
    pageInfo = traderPage.scrape()
    
    # Add URL and current date to each entry
    pageInfo.insert(3,link)
    pageInfo.insert(3,date.today())
    
    # Add the current listing info the the array of all results
    allInfo.append(pageInfo)

# Write the results to a CSV file
righter = CsvWriter()
righter.writeEntry(allInfo)
