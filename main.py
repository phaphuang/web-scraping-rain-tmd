#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
import time
from bs4 import BeautifulSoup

import pandas as pd
# set pandas encoding to utf-8
pd.options.display.encoding = str('utf-8')

browser = webdriver.Chrome("C:\chromedriver.exe")
browser.get('https://www.tmd.go.th/climate/climate.php?FileID=1')

# Create Global DataFrame
all_station_df = pd.DataFrame()
temp_df = pd.DataFrame()

file_no = 0
begin = 0

thirty_one_days_month = [1, 3, 5, 7, 8, 10, 12]
thirty_days_month = [4, 6, 9, 11]

for y in range(2015, 2019):
    time.sleep(5)
    if (y < 2018):
        end_month = 12
    else:
        end_month = 3

    for m in range(1, end_month + 1):
        time.sleep(5)
        if (y == 2018 and m == 3):
            end_days = 13
        else:
            if (m in thirty_one_days_month):
                end_days = 31
            elif (m in thirty_days_month):
                end_days = 30
            else:
                end_days = 28

        for d in range(1, end_days + 1):
            try:
                time.sleep(5)
                day = browser.find_element_by_xpath("//select[@name='ddlDay']/option[@value='" + str(d) + "']")
                day.click()

                month = browser.find_element_by_xpath("//select[@name='ddlMonth']/option[@value='2018-01']")
                browser.execute_script("return arguments[0].value='" + str(y) + "-" + str(m) + "'", month)
                #print(browser.execute_script("return arguments[0].value='2017-11'", month))
                month.click()

                date_time = str(y) + "-" + str(m) + '-' + str(d)
                print(date_time)

                page = BeautifulSoup(browser.page_source,"html5lib")
                province_rows = page.find_all("tr", {"align": "center"})
                print(province_rows)

                for (i, tr) in enumerate(province_rows):
                    number_of_cols = len(tr.find_all("td"))
                    #print(number_of_cols)
                    if (number_of_cols == 8):
                        station_row = tr.find_all("td")
                        station_name = station_row[0].text.strip()
                        station_name = station_name.encode('utf-8')
                        #print(station_name)

                        column_name = ['date', station_name]
                        #print(column_name)
                        station_df = pd.DataFrame(columns=column_name)
                        #print(station_row[6].text.strip())
                        station_df = station_df.append({'date': date_time, station_name: station_row[6].text.strip()}, ignore_index=True)
                        station_df.set_index('date', inplace=True)
                        #print(station_df)

                        if (i == 0):
                            temp_df = station_df
                        else:
                            temp_df = pd.concat([temp_df, station_df], axis=1)

                #print(temp_df)

                if (begin == 0):
                    all_station_df = temp_df
                    begin = 1
                else:
                    all_station_df = pd.concat([all_station_df, temp_df], axis=0)

                temp_df = pd.DataFrame()

                print(all_station_df)

                all_station_df.to_csv('result/rain_station_' + str(file_no) + '.csv', encoding='utf-8')
                file_no = file_no + 1
            except Exception as e:
                print(e)
