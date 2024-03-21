"""
Question 1: Web Scrape Task
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re
import argparse
from datetime import datetime

"""
This function scrapes https://www.11meigui.com/tools/currency
and finds the code for the currency and returns a dictionary
with this information. For example: {'HKD' : '港币'}.
"""
def getCurrencyDict():
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.11meigui.com/tools/currency")
        
        # Use parser to query the html of the page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        target_rows = soup.find_all('tr')
        
        result_map = {}
        for row in target_rows:
            columns = row.find_all('td')
            if len(columns) >= 2:
                # Get the second column and second to last column
                second_col = columns[1].get_text().strip()
                second_to_last_col = columns[-2].get_text().strip()
                result_map[second_to_last_col] = second_col
        
        # Filter the output, then return
        filtered_dict = {key: value for key, value in result_map.items() if re.match('^[A-Z\*]+$', key)}
        return filtered_dict

    except Exception as e:
        print("An error occurred:", e)
        return None

    finally:
        if 'driver' in locals():
            driver.quit()
            
"""
This function scrapes https://srh.bankofchina.com/search/whpj/search_cn.jsp
by quering the date, currency and referring to the currencyDict to find the
现汇买入价 value for the date and currency.
"""
def queryBOC(date, currency, currencyDict):
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.boc.cn/sourcedb/whpj/")
        
        # End Time Input
        end_time_input = driver.find_element(By.CSS_SELECTOR, "input[name='nothing']")
        end_time_input.click()
        end_time_input.clear()
        end_time_input.send_keys(date.strftime("%Y-%m-%d"))
        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "calendarClose")))
        close_button.click()
        
        # Currency Drop Down
        val = currencyDict[currency]
        currency_dropdown = Select(driver.find_element(By.ID, "pjname"))
        currency_dropdown.select_by_visible_text(val)
        
        # Search Button
        button_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='search_btn' and @onclick='executeSearch()']")))
        button_element.click()      
        
        # Find all rows in the table
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div = soup.find('div', class_='BOC_main publish')
        res = None
        if div:
            table = div.find('table')
            
            if table:
                # Get the value of the first row
                odd_rows = table.find_all('tr', class_='odd')[0]
                if odd_rows:
                    cells = odd_rows.find_all('td')
                    row_data = [cell.text.strip() for cell in cells]
                    res = row_data[1]
        return res
    
    except Exception as e:
        print("An error occurred:", e)
        return None
        
    finally:
        if 'driver' in locals():
            driver.quit()

"""
Adjusts the dictionary for certain values, since the website for the
reference is not exactly the same as the values on the Bank of China
website.
"""
def updateDict(currencyDict):
    currencyDict["HKD"] = "港币"
    currencyDict["JPY"] = "日圆"
    currencyDict["CAD"] = "加拿大元"
    currencyDict["THP"] = "泰铢"
    currencyDict["KPW"] = "园"
    currencyDict["ESP"] = "比塞塔"
    currencyDict["ITL"] = "里拉"
    currencyDict["BRC"] = "新克鲁赛罗"
    currencyDict["BRC"] = "卢比"
    currencyDict["ZAR"] = "兰特"
    currencyDict["SAR"] = "亚尔"
    currencyDict["TRL"] = "土耳其镑"
    return currencyDict

def main():
    # Parse arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('date', type=str, help="date in YYYYMMDD format")
    parser.add_argument('currency', type=str, help="currency")
    args = parser.parse_args()
    
    # Get the dictionary from the website, and include error checking
    currencyDict = getCurrencyDict()
    # print("Scraped currency dict: ", currencyDict)
    currencyDict = updateDict(currencyDict)
    # print("Dict with some values to match BOC site: ", currencyDict)
    
    try:
        date = datetime.strptime(args.date, '%Y%m%d').date()
    except ValueError:
        print("Error: Invalid date format. Date should be in YYYYMMDD format.")
        return
    currency = args.currency
    if currency not in currencyDict:
        print("Error: Currency not found in the dictionary.")
        return
    
    # Query the value for given date and currency
    value = queryBOC(date, currency, currencyDict)
    print("Answer: ", value)
    
    
if __name__ == "__main__":
    main()