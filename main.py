"""Selenium modules"""
from selenium import webdriver  # main driver import
from selenium.webdriver.common.by import By     # BY locating
# Se web driver await for load
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Se error handling
from selenium.common.exceptions import *
# Chrome options
from selenium.webdriver.chrome.options import Options
"""data visualization"""
import matplotlib.pyplot as plt
import numpy as np
"""paralellism"""
# import threading

# TODO migrate gui from Kivy to Tkinter!

# adds parallelism /// pretty useless rn    TODO: asyncio?
# class MyThread(threading.Thread):
#     def __init__(self, threadName: str):
#         threading.Thread.__init__(self)
#         self.threadName = threadName


#     def run(self):


class DataDownloader:
    """
    is connecting with OCED server and loads the website, after that searches through it and
    downloads required data via table content
    can be run by any driver (headless chrome recommended)

    __init__ sets on driver and gets into the website (driver procedure initialization) also sets variables that
    will be used in the future development (TIMEOUT)

    chrome arguments are arguments for chrome driver that allows it to run headless on windows (recommended not crucial)
    """
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
        # TODO: find out / code moving mouse emulator!
    # def set_time_period(self, timePeriod: list, frequency: str = "yearly") -> "changes time period shown in table":
    #     websiteTimePeriod = [
    #         WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "start"))).text,
    #         WebDriverWait(DRIVER, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "end"))).text]

    def get_table_header(self) -> list:
        """while connected with website by __init__ this method is searching through the main table for it's header
        and saves it temporally as a list type with str elements"""
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

    def get_country_header(self) -> list:
        """while connected with website by __init__ this method is searching through the main table for countries
        that whole data is about, returns a list with a str elements"""
        tableLocator = WebDriverWait(DRIVER, TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-chart-tbody")))
        rows = tableLocator.find_elements(By.TAG_NAME, "tr")
        dataHeaderCountry = []
        for row in rows:
            thCol = row.find_elements(By.TAG_NAME, "th")
            for thData in thCol:
                dataHeaderCountry.append(thData.text)

        return dataHeaderCountry

    def get_table_data(self) -> list:
        """while connected with website by __init__ this method is searching through the main table for the main data
        (data for all countries in database OCED shown on website) returns list of lists which contain strings
        convertible for float type"""
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
    """gets given data and makes a plt from it, handy dandy thing supported fully by matplotlib and numpy module"""
    @staticmethod
    def clear_input(*args: "list I guess but it's so spaghetti that idk even know for now") -> "clean data lists":
        """executed inside methods that create charts to clean up the data:
        > converts str types into floats
        > changes '-' (no data provided) symbols into 0 as a default value
        *args are data lists from chart generating methods"""
        for _ in args:
            for j in range(len(_)):
                if _[j] != "":
                    try:
                        _[j] = float(_[j])
                    except ValueError:
                        _[j] = 0
                else:
                    _[j] = 0

    @staticmethod
    def single_chart(chosenCountry: str, countryList: list, data: list, time: list,
                     step: float = 0.1) -> "window with a plt chart":
        """generates regular plt based on provided data
        note: default step can be changed but it is not recommended as it may cause optimization errors
        flexible step necessary while generating charts for countries with hyperinflation rates (Venezuela u good?)"""
        countryIndex = countryList.index(chosenCountry)
        ChartGenerator.clear_input(data[countryIndex])

        plt.plot(time, data[countryIndex], color="k", marker="o")   # plot line
        # just some descriptions and visuals
        plt.ylabel("Value\n(National currency units/US dollar)")
        plt.xlabel("Year")
        plt.title(f"Values for {chosenCountry}")
        # step setting based on max value of NCU/USD value rate
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
        plt.plot(figsize=(6.4 * 2, 4.8 * 2))    # ???
        plt.gcf().canvas.set_window_title(f"Single chart for {chosenCountry}")  # window label
        plt.show()

    @staticmethod
    def comparing_chart(chosenCountry: str, secondCountry: str,
                        countryList: list, data: list, time: list) -> "window with comparing plt chart":
        """same as above but for two countries at once to compare their NCU/USD rates, no flexible step here as it'd be
        inefficient to use it as a chart labeling determinant"""
        countryIndex = countryList.index(chosenCountry)
        secondCountryIndex = countryList.index(secondCountry)
        ChartGenerator.clear_input(data[countryIndex], data[secondCountryIndex])
        # print(len(data[secondCountryIndex]), len(data[countryIndex]))
        """God has abandoned lines below skip them and be happy that it works"""
        fig, host, = plt.subplots()
        # print(data[countryIndex], data[secondCountryIndex], time)
        p1, = host.plot(['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
                         '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'], np.array(data[countryIndex]),
                        "b-", label=chosenCountry)
        # TODO: while showing off code explain issues with array dimensions in _base.py
        p2, = host.plot(['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
                         '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'],
                        np.array(data[secondCountryIndex]), "r-", label=secondCountry)

        lines = [p1, p2]

        host.legend(lines, [l.get_label() for l in lines])

        plt.ylabel("Value\n(National currency units/US dollar)")
        plt.xlabel("Year")
        plt.title(f"Values for {chosenCountry} and {secondCountry}")
        plt.gcf().canvas.set_window_title(f"Comparing {chosenCountry} and {secondCountry}")
        plt.show()

        """if code works do not ask where it was stolen from
                                ~ Confucius "Art of War" """


def download_data() -> list:
    """uh... like it helps executing classes above, thats all"""
    print("Please wait... Downloading data!\n")
    DD = DataDownloader()
    # print(DD.get_table_data())
    return [DD.get_table_data(), DD.get_country_header(), DD.get_table_header()]


def single_country(dd: list):
    """uh... like it helps executing classes above, that's all"""
    for country in dd[1]:
        print(country)
    while True:
        chosenCountry = input("Choose a country from one of the above: \n")
        if chosenCountry.lower() == "q":
            exit()
        if chosenCountry not in dd[1]:
            print("Selected country does not exist in the database, try again.")
            continue
        break

    cGen = ChartGenerator
    cGen.single_chart(chosenCountry=chosenCountry, countryList=dd[1], data=dd[0], time=dd[2])


def comparing_country(dd: list):
    """uh... like it helps executing classes above, that's all"""
    for country in dd[1]:
        print(country)
    while True:
        chosenCountry = input("Choose a country from one of the above: \n")
        if chosenCountry.lower() == "q":
            exit()
        elif chosenCountry not in dd[1]:
            print("Selected country does not exist in the database, try again.")
            continue
        break
    while True:
        secondCountry = input("Choose a country from one of the above: \n")
        if secondCountry.lower() == "q":
            exit()
        elif secondCountry not in dd[1]:
            print("Selected country does not exist in the database, try again.")
            continue
        break

    cGen = ChartGenerator
    cGen.comparing_chart(chosenCountry=chosenCountry, secondCountry=secondCountry,
                         countryList=dd[1], data=dd[0], time=[2])


if __name__ == "__main__":
    """code execution goes brrrrr"""
    try:
        dd = download_data()
        DRIVER.quit()
        while True:
            chartSelect = input("Single [s] or comparing? [c]")
            if chartSelect.lower() == "s":
                single_country(dd)
            elif chartSelect.lower() == "c":
                comparing_country(dd)
            elif chartSelect.lower() == "q":
                exit()
    except KeyboardInterrupt:
        exit()
"""Hooray!"""
