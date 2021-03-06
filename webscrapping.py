from itertools import count
import os
from click import option
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.chrome.service import Service

global counter
global num_pages
counter = 0
num_pages = 1410


class Flipkart():

    def __init__(self,url):

        self.driver_path = r'/home/amal/Downloads/Chrome Driver/chromedriver_linux64/chromedriver'#'chromedriver'
        self.service = Service(executable_path=self.driver_path)
        self.options = webdriver.ChromeOptions()
        # Here i get path of current workind directory
        self.current_path = os.getcwd()
        self.url = url
        # Chromedriver is just like a chrome. you can dowload latest by it website
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def page_load(self):

        self.driver.get(self.url)
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        y = 1000
        for timer in range(0,50):
            self.driver.execute_script("window.scrollTo(0, "+str(y)+")")
            y += 1000  
            if y>=last_height:
                break
            time.sleep(0.1)
        
        # try:
        #     login_pop = self.driver.find_element_by_class_name('_29YdH8')
        #     # Here .click function use to tap on desire elements of webpage
        #     login_pop.click()
        #     print('pop-up closed')
        # except:
        #     pass
        # # Here I get search field id from driver
        # search_field = self.driver.find_element_by_class_name('desktop-searchBar')
        # # Here .send_keys is use to input text in search field
        # search_field.send_keys('kurtas' + '\n')
        # # Here time.sleep is used to add delay for loading context in browser
        time.sleep(2)
        # Here we fetched driver page source from driver.
        page_html = self.driver.page_source
        # Here BeautifulSoup is dump page source into html format
        self.soup = BeautifulSoup(page_html, 'html.parser')

    def create_csv_file(self):

        # Here I created CSV file with desired header.
        rowHeaders = ["Name", "Storage_details", "Screen_size", "Camera_details", "Battery_details", "Processor", "Warranty", "Price in Rupees"]
        self.file_csv = open('Flipkart_output.csv', 'w', newline='', encoding='utf-8')
        self.mycsv = csv.DictWriter(self.file_csv, fieldnames=rowHeaders)
        # Writeheader is pre-defined function to write header
        self.mycsv.writeheader()

    def data_scrap(self):

        # Here I fetch all products div elements
        with open('page_html.txt', 'w') as f:
            f.write(str(self.soup))
        # first_page_mobiles = (self.soup.find_all('div', class_='search-searchProductsContainer row-base'))
        # for i in first_page_mobiles:
        #print(self.soup.find_all('img', {"class": 'img-responsive'})[0]['src'])
        all_divs = self.soup.find_all('img', {"class": 'img-responsive'})
        for i in all_divs:
            image_data = requests.get(i['src']).content 
            global counter
            image_path = self.current_path + '/images/' + str(counter) + '.jpg'
            with open(image_path, 'wb') as handler:
                handler.write(image_data)
                counter += 1
        # print(first_page_mobiles)
        # with open('myntra.txt', 'w') as f:
        #     f.write(str(first_page_mobiles[0]))
        # divTag = soup.find_all("div", {"class": "tablebox"}):

        # for tag in divTag:
        #     tdTags = tag.find_all("td", {"class": "align-right"})
        #     for tag in tdTags:
        #         print tag.text

        # for i in first_page_mobiles:
        #     Name = i.find('img', class_='_1Nyybr')['alt']
        #     price = i.find('div', class_='_1vC4OE _2rQ-NK')
        #     details = i.find_all("li")
        #     storage = details[0].text
        #     camera_details = details[2].text
        #     screen_size = details[1].text
        #     battery_details = details[3].text
        #     processor = details[4].text
        #     try:
        #         warranty_details = [j.text for j in details if j.text[:14] == "Brand Warranty"][0]
        #     except:
        #         warranty_details = "No data available"
        #     price = price.text[1:]
        #     self.mycsv.writerow({"Name": Name, "Storage_details": storage, "Screen_size": screen_size, "Camera_details": camera_details, "Battery_details": battery_details, "Processor": processor, "Warranty": warranty_details, "Price in Rupees": price})

    def tearDown(self):

        # Here driver.quit function is used to close chromedriver
        self.driver.quit()
        # Here we also need to close Csv file which I generated above
        self.file_csv.close()

    def set_url(self,url):

        self.url = url

if __name__ == "__main__":
    current_page = 1
    flipkart = Flipkart('')
    while current_page <= num_pages:
        url = f'https://www.myntra.com/women-kurtas-kurtis-suits?p={current_page}'
        flipkart.set_url(url)
        flipkart.page_load()
        flipkart.create_csv_file()
        flipkart.data_scrap()
        print(f"Task completed for page {current_page}")
        current_page += 1
    flipkart.tearDown()