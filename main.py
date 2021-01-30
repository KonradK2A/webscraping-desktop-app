"""This is the 1.0.0 version of the application made by Konrad Kihan"""

"""Python built ins"""
import ctypes

"""Installed via pip / modules of the app"""
try:
    """Selenium modules"""
    from selenium import webdriver  # main driver import
    from selenium.webdriver.common.by import By  # BY locating
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

    """gui stuff"""
    from tk_gui import AppWindow
except ImportError as e:
    ctypes.windll.user32.MessageBoxW(0, f"During program execution following error occurred:\n{e}", "Error!", 0x10)
    exit(1)


# TODO asyncio?


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
        self.TIMEOUT: int = 10  # timeout in seconds
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        self.DRIVER = webdriver.Chrome(options=chrome_options)
        self.DRIVER.get("https://data.oecd.org/conversion/exchange-rates.htm")

        self.dataHeaderYear: list = []
        self.fullData: list = []
        self.dataHeaderCountry: list = []

        # sets time period we want to download our data for   /// pretty useless rn
        # TODO: find out / code moving mouse emulator!

    # def set_time_period(self, timePeriod: list, frequency: str = "yearly") -> "changes time period shown in table":
    #     websiteTimePeriod = [
    #         WebDriverWait(self.DRIVER, self.TIMEOUT)
    #             .until(EC.presence_of_element_located((By.CLASS_NAME, "start"))).text,
    #         WebDriverWait(self.DRIVER, self.TIMEOUT)
    #             .until(EC.presence_of_element_located((By.CLASS_NAME, "end"))).text
    #     ]

    def get_table_header(self) -> list:
        """while connected with website by __init__ this method is searching through the main table for it's header
        and saves it temporally as a list type with str elements"""
        tableHead = WebDriverWait(self.DRIVER, self.TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-chart-thead")))
        thHeadRows = tableHead.find_elements(By.TAG_NAME, "tr")
        for thRow in thHeadRows:
            thCol = thRow.find_elements(By.TAG_NAME, "th")
            for thData in thCol:
                self.dataHeaderYear.append(thData.text.replace("▾ ", ""))
        self.dataHeaderYear.pop(0)

        return self.dataHeaderYear

    def get_country_header(self) -> list:
        """while connected with website by __init__ this method is searching through the main table for countries
        that whole data is about, returns a list with a str elements"""
        tableLocator = WebDriverWait(self.DRIVER, self.TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-chart-tbody")))
        rows = tableLocator.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            thCol = row.find_elements(By.TAG_NAME, "th")
            for thData in thCol:
                self.dataHeaderCountry.append(thData.text)

        return self.dataHeaderCountry

    def get_table_data(self) -> list:
        """while connected with website by __init__ this method is searching through the main table for the main data
        (data for all countries in database OCED shown on website) returns list of lists which contain strings
        convertible for float type"""
        tableLocator = WebDriverWait(self.DRIVER, self.TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "table-chart-tbody")))
        rows = tableLocator.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            dataOfCountry = []  # helper list that saves data of one country
            col = row.find_elements(By.TAG_NAME, "td")
            for data in col:
                dataOfCountry.append(data.text)
            self.fullData.append(dataOfCountry)

        return self.fullData


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

        plt.plot(time, data[countryIndex], color="k", marker="o")  # plot line
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
        plt.plot(figsize=(6.4 * 2, 4.8 * 2))
        plt.gcf().canvas.set_window_title(f"Single chart for {chosenCountry}")  # window label
        plt.show()

    @staticmethod
    def comparing_chart(firstCountry: str, secondCountry: str,
                        countryList: list, data: list, time: list) -> "window with comparing plt chart":
        """same as above but for two countries at once to compare their NCU/USD rates, no flexible step here as it'd be
        inefficient to use it as a chart labeling determinant"""
        countryIndex = countryList.index(firstCountry)
        secondCountryIndex = countryList.index(secondCountry)
        ChartGenerator.clear_input(data[countryIndex], data[secondCountryIndex])
        """God has abandoned lines below skip them and be happy that it works
        thy matplotlib raises an error when the array same as in case of single_country is put, so to
        help  executing the app time values are hardcoded"""
        fig, host, = plt.subplots()
        try:
            p1, = host.plot(time,
                            np.array(data[countryIndex]),
                            "b-", label=firstCountry)

        except ValueError:
            time = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
                    '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
        try:
            p2, = host.plot(time,
                            np.array(data[secondCountryIndex][0:len(time) + 1]),
                            "r-", label=secondCountry)

        except ValueError:
            pass
        finally:
            p1, = host.plot(time,
                            np.array(data[countryIndex][0:len(time) + 1]),
                            "b-", label=firstCountry)
            p2, = host.plot(time,
                            np.array(data[secondCountryIndex][0:len(time) + 1]),
                            "r-", label=secondCountry)

            lines = [p1, p2]

            try:
                host.legend(lines, [i.get_label() for i in lines])
            except IndexError:
                exit(2)

        plt.ylabel("Value\n(National currency units/US dollar)")
        plt.xlabel("Year")
        plt.title(f"Values for {firstCountry} and {secondCountry}")
        plt.gcf().canvas.set_window_title(f"Comparing {firstCountry} and {secondCountry}")
        plt.show()

        """if code works do not ask where it was stolen from
                                ~ Confucius "Art of War" """


class MainRunner:
    """clarifies code execution and helps to execute the DataDownloader and ChartGenerator"""

    @staticmethod
    def download_data() -> list:
        DD = DataDownloader()
        return [DD.get_table_data(), DD.get_country_header(), DD.get_table_header()]

    @staticmethod
    def single_country(dd: list, firstCountry: str):
        if firstCountry not in dd[1]:
            raise ctypes.windll.user32.MessageBoxW(0, f"No such country in the database.",
                                                   "Warning!", 0x10)

        cGen = ChartGenerator
        cGen.single_chart(chosenCountry=firstCountry, countryList=dd[1], data=dd[0], time=dd[2])

    @staticmethod
    def comparing_country(dd: list, firstCountry: str, secondCountry: str):
        cGen = ChartGenerator
        cGen.comparing_chart(firstCountry=firstCountry, secondCountry=secondCountry,
                             countryList=dd[1], data=dd[0], time=dd[2])


if __name__ == "__main__":
    """code execution goes brrrrr"""
    msgBox = ctypes.windll.user32 \
        .MessageBoxW(0, f"Data will be downloaded. Do you want to proceed?", "Data download", 0x01)
    dd = MainRunner.download_data()  # download data
    appWindow = AppWindow()
    appWindow.hello_window()
    guiValuesReturned = appWindow.return_values()
    mode = guiValuesReturned[0]
    if mode == "SINGLE":
        firstCountry = guiValuesReturned[1]
        MainRunner.single_country(dd, firstCountry=firstCountry)
    elif mode == "CMP":
        firstCountry, secondCountry = guiValuesReturned[1], guiValuesReturned[2]
        MainRunner.comparing_country(dd, firstCountry=firstCountry, secondCountry=secondCountry)
    else:
        try:
            raise ctypes.windll.user32.MessageBoxW(0, f"Application raised an error.",
                                                   "Warning!", 0x10)
        except:
            raise ctypes.windll.user32.MessageBoxW(0, f"Application raised error so critical that even it's creator"
                                                      f"didn't expect that to happen!.",
                                                   "Error!", 0x10)
        finally:
            exit(1)
