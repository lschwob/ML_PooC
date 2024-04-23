from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

from tqdm import tqdm
import csv
import os
import requests
import time

import pandas as pd

def scrape_symbols(urls, savefile):
    
    try :
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    
    for url in urls:
        driver.get(url)
        # cookies = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
        # wait for loading and then click on the button
        cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')))
        cookies.click()
        
        try:
            # get the table
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div[1]/div/div/table')))
            # get the rows
            rows = table.find_elements(By.TAG_NAME, 'tr')
            symbols = [row.find_elements(By.TAG_NAME, 'td')[2].text for row in rows[1:]]
            # get the headers
            headers = rows[0].find_elements(By.TAG_NAME, 'th')
        
        except NoSuchElementException:
            print("Table element not found.")
        
        #Save the list in a txt file
        with open(savefile, 'w') as f:
            for item in symbols:
                f.write(item + '\n')
                
        return symbols
    
def scrape_financial(symbols, progress_file):
    links = []
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=500,800")
    
    try :
        
        driver = webdriver.Chrome(options=options)
    except:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    

    #Look for the progress file and get the symbols already scraped not to do it again
    try :
        with open(progress_file, 'r') as f:
            progress = f.readlines()
            progress = [line.split(':')[0] for line in progress]
    except:
        with open(progress_file, 'w') as f:
            pass
        progress = []

    symbols = [symbol for symbol in symbols if symbol not in progress]
    for symbol in tqdm(symbols, desc='Scraping financial data'):
        url = f'https://fr.finance.yahoo.com/quote/{symbol}/history'
        driver.get(url)
        driver.delete_all_cookies()
        
        try:
            try:
                cookies = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[2]')))
                cookies.click()
            except :
                try : 
                    cookies_form =  WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="consent-page"]/div/div/div/form/div[2]')))
                    driver.execute_script("arguments[0].scrollIntoView();", cookies_form)
                    
                    cookies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button[2]')))
                    cookies.click()
                except :
                    pass
            
            date = driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div')
            date.click()
            
            date_select = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[1]/div[1]/div/div/div[2]/div/ul[2]/li[4]/button/span')
            date_select.click()
            
            confirm = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[2]/div/div/section/div[1]/div[1]/button')
            confirm.click()
            
            try : 
                link = driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')
                download_link = link.get_attribute('href')
                
                #Save the progression in a txt file
                links.append(download_link)
                with open (progress_file, 'a') as f:
                    f.write(symbol + ':' + download_link + '\n')
            except :
                pass
        except:
            #Quit driver and try again
            driver.quit()
            scrape_financial(symbols, progress_file=progress_file)
        
    return links

def download_data(file, download_path='../../data/financials/'):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    with open(file, 'r') as f:
        lines = f.readlines()
        urls = [(line.split(':')[0], line.split(':')[1] + ':' + line.split(':')[2]) for line in tqdm(lines, desc='Extracting URLs')]
    
    for symbol, url in tqdm(urls, desc='Downloading data'):
        try:
            r = requests.get(url, headers=header)
            with open(f'{download_path}{symbol}.csv', 'wb') as f:
                f.write(r.content)
        except:
            print(f'Error downloading {symbol}.')
        # time.sleep(5)
    return 'Files downloaded successfully.'
    