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
# Se error handling
from selenium.common.exceptions import *

# data visualization
import pandas as pd
import matplotlib.pyplot as plt

# multithreading
# import threading

# Others. Lol.
import time

TIMEOUT = 10    # timeout in seconds

# connect with the website and download all data
class DataDownloader():
    def __init__(self):
        global DRIVER
        DRIVER = webdriver.PhantomJS()
        DRIVER.get("https://data.oecd.org/conversion/exchange-rates.htm")    

    # sets time period we want to download our data for
    def set_time_period(self, timePeriod: list, frequency: str = "yearly") -> None:
        websiteTimePeriod = [WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "start"))).text,
                            WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "end"))).text]
            

    # downloads table header (list of years) and saves it as a list dataYear 
    def get_table_header(self) -> list:
        tableHead = WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "table-chart-thead")))
        thHeadRows = tableHead.find_elements(By.TAG_NAME, "tr")
        self.dataHeaderYear = []
        for thRow in thHeadRows:
            thCol = thRow.find_elements(By.TAG_NAME, "th")
            for thData in thCol:
                self.dataHeaderYear.append(thData.text.replace("▾ ", ""))
        self.dataHeaderYear[0] = "Location"

        return self.dataHeaderYear


    # downloads row descriptions (names of countries)
    def get_country_header(self) -> list:
        tableLocator = WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "table-chart-tbody")))
        rows = tableLocator.find_elements(By.TAG_NAME, "tr")
        self.dataHeaderCountry = []
        for row in rows:
            thCol = row.find_elements(By.TAG_NAME, "th")
            for thData in thCol:
                self.dataHeaderCountry.append(thData.text)
        
        return self.dataHeaderCountry


    # downloads table content (list of string that represents floats), stored as list of lists
    def get_table_data(self) -> list:
        tableLocator = WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "table-chart-tbody")))
        rows = tableLocator.find_elements(By.TAG_NAME, "tr")
        self.fullData = []
        for row in rows:
            dataOfCountry = []  # helper list that saves data of one coutry
            col = row.find_elements(By.TAG_NAME, "td")
            for data in col:
                dataOfCountry.append(data.text) 
            self.fullData.append(dataOfCountry)

        return self.fullData

# class MyThread(threading.Thread):
#     def __init__(self, threadName: str):
#         threading.Thread.__init__(self)
#         self.threadName = threadName


#     def run(self):
        


DRIVER.quit()