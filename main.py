"""
Web Scraping (Listed companies' balance sheets)
"""

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def main() :
  pass
  ##
  ##
  def drivetable(soup, number):
    header = soup.find_all("table")[number].find("tr")
    list_header = []
    for items in header:
        try:
            list_header.append(items.get_text())
        except:
            continue

    # for getting the data
    HTML_data = soup.find_all("table")[number].find_all("tr")[1:]
    data = []
    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)
    df = pd.DataFrame(data=data, columns=list_header).T
    return df
  ##
  driver = webdriver.Chrome()
  ##
  # Load the announcements for each company
  driver.get('https://my.codal.ir/fa/statements/?company_id=&my_basket=&statement_type=146&period=12&financial_years=&company_type=0&status=1&tracing_number=&publisher_state=&title=&from_date=&to_date=&parent_or_subset=1&consolidated_or_not=&per_page=100#scroll_to_results')
  # Save the link of each row
  links=[]
  for i in range(100):
    reports = (
                driver.find_element_by_id("tTable")
                .find_element_by_class_name("grid-txt")
                .find_elements_by_xpath(f"//*[@id='template-container']/tr[{i}]/td[4]/a")
            )
    for report in reports:
        url = report.get_attribute("href")
        links.append(url)
	##
	for i in range(2,100):
    driver.get(f'https://my.codal.ir/fa/statements/?company_id=&my_basket=&statement_type=146&period=12&financial_years=&company_type=0&status=1&tracing_number=&publisher_state=&title=&from_date=&to_date=&parent_or_subset=1&consolidated_or_not=&per_page=100&page={i}')
    for j in range(100):
        reports = (
                driver.find_element_by_id("tTable")
                .find_element_by_class_name("grid-txt")
                .find_elements_by_xpath(f"//*[@id='template-container']/tr[{j}]/td[4]/a")
            )
        for report in reports:
            url = report.get_attribute("href")
            links.append(url)
	##
	# '0' at the end of links means that that address contains the balance sheet
	links = [i +'0' for  i in links]
	##
	file_names=[]
	for link in links:
    try:
        driver.get(link)
        name = driver.find_element_by_id('ctl00_txbSymbol').text
        period= driver.find_element_by_id('ctl00_lblPeriod').text
        date = driver.find_element_by_id('ctl00_lblPeriodEndToDate').text[:4]
        r = driver.page_source
        soup = BeautifulSoup(r, "html.parser")
        drivetable(soup, 0).T.to_excel(f'C:/Users/hosein/Desktop/{name+period+date}.xlsx')
        file_names.append(name+period+date)
    except:
        continue
##


if __name__ == "__main__" :
    main()
    print(f'{Path(__file__).name} Done!')
	
