# Se stuff
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
# Se error handling
from selenium.common.exceptions import *
# Chrome  options
from selenium.webdriver.chrome.options import Options

# data visualization
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# multithreading
# import threading

# Others. Lol.
import time
import sys


# adds parallelism /// pretty useless rn
# class MyThread(threading.Thread):
#     def __init__(self, threadName: str):
#         threading.Thread.__init__(self)
#         self.threadName = threadName


#     def run(self):


# connect with the website and download all data
class DataDownloader():
    def __init__(self):
        global DRIVER
        global TIMEOUT
        TIMEOUT = 10  # timeout in seconds
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        DRIVER = webdriver.Chrome(options=chrome_options)
        DRIVER.get("https://data.oecd.org/conversion/exchange-rates.htm")

        # sets time period we want to download our data for   /// pretty useless rn

    def set_time_period(self, timePeriod: list, frequency: str = "yearly") -> "changes time period shown in table":
        websiteTimePeriod = [
            WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "start"))).text,
            WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "end"))).text]

    # downloads table header (list of years) and saves it as a list dataYear

    def get_table_header(self) -> list:
        tableHead = WebDriverWait(DRIVER, TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-chart-thead")))
        thHeadRows = tableHead.find_elements(By.TAG_NAME, "tr")
        dataHeaderYear = []
        for thRow in thHeadRows:
            thCol = thRow.find_elements(By.TAG_NAME, "th")
            for thData in thCol:
                dataHeaderYear.append(thData.text.replace("▾ ", ""))
        dataHeaderYear.pop(0)

        return dataHeaderYear

    # downloads row descriptions (names of countries)
    def get_country_header(self) -> list:
        tableLocator = WebDriverWait(DRIVER, TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-chart-tbody")))
        rows = tableLocator.find_elements(By.TAG_NAME, "tr")
        dataHeaderCountry = []
        for row in rows:
            thCol = row.find_elements(By.TAG_NAME, "th")
            for thData in thCol:
                dataHeaderCountry.append(thData.text)

        return dataHeaderCountry

    # downloads table content (list of string that represents floats), stored as list of lists
    def get_table_data(self) -> list:
        tableLocator = WebDriverWait(DRIVER, TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-chart-tbody")))
        rows = tableLocator.find_elements(By.TAG_NAME, "tr")
        fullData = []
        for row in rows:
            dataOfCountry = []  # helper list that saves data of one coutry
            col = row.find_elements(By.TAG_NAME, "td")
            for data in col:
                dataOfCountry.append(data.text)
            fullData.append(dataOfCountry)

        return fullData


class ChartGenerator:
    def __init__(self):
        pass

    @staticmethod
    def clear_input(*args: "list I guess but it's so spaghetti that idk even know for now"):
        for i in args:
            for j in range(len(i)):
                if i[j] != "":
                    try:
                        i[j] = float(i[j])
                    except ValueError:
                        i[j] = 0
                else:
                    i[j] = 0

    @staticmethod
    def single_chart(chosenCountry: str, countryList: list, data: list, time: list,
                     step: float = 0.1) -> "window with a plt chart":
        countryIndex = countryList.index(chosenCountry)
        ChartGenerator.clear_input(data[countryIndex])

        plt.plot(time, data[countryIndex], color="k", marker="o")
        plt.ylabel("Value\n(National currency units/US dollar)")
        plt.xlabel("Year")
        plt.title(f"Values for {chosenCountry}")
        if max(data[countryIndex]) <= 5:
            plt.yticks(np.arange(0, max(data[countryIndex]) + step, step))
        elif 10 <= max(data[countryIndex]) <= 50:
            plt.yticks(np.arange(0, max(data[countryIndex]) + step * 10, step * 10))
        elif 50 < max(data[countryIndex]) <= 100:
            plt.yticks(np.arange(0, max(data[countryIndex]) + step * 50, step * 50))
        elif 100 < max(data[countryIndex]) <= 300:
            plt.yticks(np.arange(0, max(data[countryIndex]) + step * 100, step * 100))
        else:
            pass
        plt.plot(figsize=(6.4 * 2, 4.8 * 2))
        plt.gcf().canvas.set_window_title(f"Single chart for {chosenCountry}")
        plt.show()

    @staticmethod
    def comparing_chart(chosenCountry: str, secondCountry: str,
                        countryList: list, data: list, time: list,
                        step: float = 0.1) -> "window with comparing plt chart":

        countryIndex = countryList.index(chosenCountry)
        secondCountryIndex = countryList.index(secondCountry)

        ChartGenerator.clear_input(data[countryIndex], data[secondCountryIndex])
        print(data[countryIndex], data[secondCountryIndex])


def download_data() -> list:
    print("Please wait... Downloading data!\n")
    DD = DataDownloader()
    print(DD.get_table_data())
    return [DD.get_table_data(), DD.get_country_header(), DD.get_table_header()]


def single_country(dd: list):
    for country in dd[1]:
        print(country)
    while True:
        chosenCountry = input("Choose a country from one of the above: \n")
        if chosenCountry not in dd[1]:
            print("Selected country does not exist in the database, try again.")
            continue
        break

    cGen = ChartGenerator
    # cGen.single_chart(chosenCountry=chosenCountry, countryList=dd[1], data=dd[0], time=dd[2])
    cGen.comparing_chart(chosenCountry=chosenCountry, secondCountry="Canada", countryList=dd[1], data=dd[0], time=[2])


if __name__ == "__main__":
    dd = download_data()
    single_country(dd)

    DRIVER.quit()
