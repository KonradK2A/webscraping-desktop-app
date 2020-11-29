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
# Chrome headless options
from selenium.webdriver.chrome.options import Options


# data visualization
import pandas as pd
import matplotlib.pyplot as plt

# multithreading
# import threading

# Others. Lol.
import time

# connect with the website and download all data
class DataDownloader():
    def __init__(self):
        global DRIVER
        global TIMEOUT
        TIMEOUT = 10    # timeout in seconds
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        DRIVER = webdriver.Chrome(options=chrome_options)
        DRIVER.get("https://data.oecd.org/conversion/exchange-rates.htm")    

    # sets time period we want to download our data for   /// pretty useless rn
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
        self.dataHeaderYear.pop(0)

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


# adds parallelism /// pretty useless rn
# class MyThread(threading.Thread):
#     def __init__(self, threadName: str):
#         threading.Thread.__init__(self)
#         self.threadName = threadName


#     def run(self):
        
class ChartGenerator():
    def __init__(self):
        pass


    def single_chart(self, chosenCountry: str, countryList: list, data: list, time: list) -> "window with a plt chart":
        countryIndex = countryList.index(chosenCountry)
        for i in range(len(data[countryIndex])):
            if data[countryIndex][i] != '':
                try:
                    data[countryIndex][i] = float(data[countryIndex][i])
                except ValueError:
                    data[countryIndex][i] = 0
            else:
                data[countryIndex][i] = 0
        
        plt.plot(time, data[countryIndex], color="k", marker="o")
        plt.ylabel("Value\n(National currency units/US dollar)")
        plt.xlabel("Year")
        plt.title(f"Values for {chosenCountry}")
        plt.show() 

def downlad_data():
    print("Please wait... Downloading data!\n"
    "I̶t̶ ̶w̶o̶u̶l̶d̶ ̶h̶a̶v̶e̶ ̶b̶e̶e̶n̶ ̶a̶ ̶l̶i̶l̶ ̶b̶i̶t̶ ̶f̶a̶s̶t̶e̶r̶ ̶b̶u̶t̶ ̶s̶o̶m̶e̶o̶n̶e̶ ̶g̶o̶t̶ ̶a̶n̶ ̶i̶d̶e̶a̶ ̶t̶o̶ ̶u̶n̶r̶e̶c̶o̶m̶m̶e̶n̶d̶ ̶P̶h̶a̶n̶t̶o̶m̶J̶S̶ ̶a̶n̶d̶ ̶p̶u̶t̶ ̶C̶h̶r̶o̶m̶e̶d̶r̶i̶v̶e̶r̶ ̶w̶/ ̶-̶-̶h̶e̶a̶d̶l̶e̶s̶s̶ ̶p̶a̶r̶a̶m̶e̶t̶e̶r̶ ̶w̶h̶i̶c̶h̶ ̶i̶s̶ ̶k̶i̶n̶d̶a̶ ̶s̶l̶o̶w̶ ̶b̶u̶t̶ ̶l̶o̶l̶ ̶w̶h̶o̶ ̶c̶a̶r̶e̶s̶ ̶a̶b̶o̶u̶t̶ ̶o̶p̶t̶y̶m̶a̶l̶i̶z̶a̶t̶i̶o̶n̶ ̶N̶O̶T̶ ̶M̶E̶ ̶")
    DD = DataDownloader()
    return [DD.get_table_data(), DD.get_country_header(), DD.get_table_header()]


if __name__ == "__main__":
    dd = downlad_data()
    
    # beta just bc no gui lol
    for country in dd[1]:
        print(country)
    while True:
        chosenCountry = input("Choose a country from one of the above: \n")
        if chosenCountry not in dd[1]:
            print("Selected country does not exist in the database... exiting...")
            continue
        break

    cGen = ChartGenerator()
    cGen.single_chart(chosenCountry = chosenCountry, data = dd[0] , countryList = dd[1], time = dd[2])
    




    DRIVER.quit()