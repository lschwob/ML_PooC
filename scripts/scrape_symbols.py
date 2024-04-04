from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def scrape_sp500(urls):
    """
    Fonction qui permet de scraper les symboles des actions du site : https://www.slickcharts.com/sp500.
    Les symboles scrapés sont ceux du S&P500.
    La fonction prend en paramètre l'URL du site et retourne une liste de symboles.

    Args:
        urls (list): Liste des URLs des sites à scraper sous forme de string.
        Uniquement un url supporté pour le moment.

    Returns:
        list: Liste des symboles des actions du S&P500.
    """
    
    driver = webdriver.Chrome()
    for url in urls:
        driver.get(url)
        # wait for loading and then click on the button
        cookies = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')))
        cookies.click()
        
        try:
            # get the table
            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div[1]/div/div/table')))
            # get the rows
            rows = table.find_elements(By.TAG_NAME, 'tr')
            symbols = [row.find_elements(By.TAG_NAME, 'td')[2].text for row in rows[1:]]        
        
        except NoSuchElementException:
            print("Table element not found.")
        
        #Save the list in a txt file
        with open('../data/symbols.txt', 'w') as f:
            for item in symbols:
                f.write(item + '\n')
                
        return symbols