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
# Path of Webdriver for example:
path = r"C:\Program Files (x86)\chromedriver.exe"
from selenium.webdriver.chrome.options import Options
# to get selenium faster
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")




def main() :
  pass
  ##
  ##
	#Functions
	def first_type(link):
		driver.get(link)
		name = driver.find_element_by_id('ctl00_txbSymbol').text
		period= driver.find_element_by_id('ctl00_lblPeriod').text
		date = driver.find_element_by_id('ctl00_lblPeriodEndToDate').text[:4]
		r = driver.page_source
		soup = BeautifulSoup(r, "html.parser")
		st_df = drivetable(soup, 0).T
		st_df.to_excel(f'C:/Users/hosein/Desktop/balance/test/{name+period+date}.xlsx')


	def sec_type(link):
		driver.get(link)
		name = driver.find_element_by_id('ctl00_txbSymbol').text
		period= driver.find_element_by_id('ctl00_lblPeriod').text
		date = driver.find_element_by_id('ctl00_lblPeriodEndToDate').text[:4]
		table= driver.find_element_by_id('ctl00_cphBody_ucSFinancialPosition_grdSFinancialPosition')
		dfbase = pd.DataFrame()
		table =WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ctl00_cphBody_ucSFinancialPosition_grdSFinancialPosition"))).get_attribute("outerHTML")
		df=pd.read_html(str(table))[0]
		dfbase=dfbase.append(df,ignore_index=True)
		dfbase.to_excel(f'C:/Users/hosein/Desktop/balance/test2/{name+period+date}.xlsx')

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
  driver = webdriver.Chrome(path, options=chrome_options)
  ##
	#Links of all statements
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
	# To get BalanceSheet Page
	links = [i +'0' for  i in links]
	##
	numer_of_error=0


	for number, link in enumerate(Balance_Links):
			print(number)
			try:
					driver.get(link)
					r = driver.page_source
					soup = BeautifulSoup(r, "html.parser")
					st_df = drivetable(soup, 0).T
					if len(st_df)<13:
							sec_type(link)
					else:
							first_type(link)
			except:
	
					print(numer_of_error)
					numer_of_error+=1
##


if __name__ == "__main__" :
    main()
    print(f'{Path(__file__).name} Done!')
	
