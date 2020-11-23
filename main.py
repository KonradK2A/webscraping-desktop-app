# Se stuff
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
# error handling
from selenium.common.exceptions import *

#data visualization
import pandas as pd
import matplotlib.pyplot as plt

#  Others. Lol.
import time

TIMEOUT = 10    # timeout in seconds
DRIVER = webdriver.Chrome()

class DataDownloader():
    def __init__(self):
        pass

    def set_time_period(self, timePeriod: list, frequency: str = "yearly") -> None:
        DRIVER.get("https://data.oecd.org/conversion/exchange-rates.htm")    
        websiteTimePeriod = [WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "start"))).text,
                            WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "end"))).text]
            
        print(websiteTimePeriod)

        

d = DataDownloader()
d.set_time_period([2000,2020])



DRIVER.quit()