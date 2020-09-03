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
#from bs4 import BeautifulSoup as bs

#data visualization
import pandas as pd
import matplotlib.pyplot as plt

#  Others. Lol.
import time


# generates charts...?
class ChartGenerator:
    def __init__(self):
        pass
    # takes data from source website
    def getTableFromWebsite(self, timePeriod="May 2009", chartType="SDRCV"):
        with webdriver.PhantomJS() as driver:
            driver.get("https://www.imf.org/external/np/fin/data/param_rms_mth.aspx")
            
            # select date [SELECT]
            timeSelect = Select(driver.find_element_by_name("SelectDate"))
            timeSelect.select_by_visible_text(timePeriod)

            # select the report [RADIO]
            sdrSelect = driver.find_element_by_css_selector(f"input[type='radio'][value='{chartType}']").click()

            # go for the report [BUTTON]
            getReportButton = driver.find_element_by_xpath("//input[@type='submit' and @value='Get Report']").click()

            # get data from table and put it into the list
            table = driver.find_element_by_class_name("tighter")
            self.dataList = []

            # gets header            
            dataHeader = []
            rawHeader = driver.find_elements_by_xpath("//tbody/tr/th")
            for i in range(len(rawHeader)):
                dataHeader.append(rawHeader[i].text)

            self.dataList.append(dataHeader)

            # iterates thru the table and collects all data
            for row in table.find_elements_by_xpath(".//tr"):
                raw_row = [td.text for td in row.find_elements_by_xpath(".//td")]
                self.dataList.append(raw_row) # list structure be like: list of lists, structure: [[header for two tables], [row1], [row2] ]
            
            # work with driver is over party
            driver.quit()

            # clear table header
            forbiddenHeads = ['Download this file', 'SDRs per Currency unit for May 2009', 'Currency',
                                'SDRs per Currency unit for May 2009 (Continued)', 'Disclaimer', 'Notes:']
            self.dataList[0] = [elem for elem in self.dataList[0] if elem not in forbiddenHeads]
            
            #cleans empty elements
            i = 0 
            while i < len(self.dataList)-1:
                if not self.dataList[i]:
                    try:
                        self.dataList.pop(i)
                    except IndexError as e:
                        print(e)
                else:
                    i += 1
            #print(self.dataList)


    def plotChart(self, currency):
        for i in range(len(self.dataList)):
            self.dL = self.dataList[i]
            if self.dL[0] == currency:
                # normalizes NA values in table
                for i in range(len(self.dL)):
                    if self.dL[i] == "NA":
                        self.dL[i] = 0
                    else:
                        pass

                names = self.dataList[0][0:11]
                values = self.dL[1:]
                plt.bar(names, values); 
                plt.ylabel("Value"); plt.xlabel("Time"); plt.suptitle(f"{currency} values over time")
                plt.show()
                

                print(self.dataList[i])
                break
            else:
                pass    #ERROR


f = ChartGenerator()
f.getTableFromWebsite()
f.plotChart(currency="Swedish krona")