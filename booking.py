import time
from selenium.webdriver.common.keys import Keys
import booking.constant as const
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl

class Booking(webdriver.Firefox):
    def __init__(self, driver_path=r"C:\Users\Asus\Desktop\web_scraping\geckodriver.exe",teardown = False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown :
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def close_sign_in(self):
        try:
            element = self.find_element(By.XPATH,"//button[@aria-label='Dismiss sign-in info.']")
            element.click()
        except:
            pass

    def change_currency_to_usd(self):
        button = self.find_element(By.XPATH,"//button[@data-testid='header-currency-picker-trigger']")
        button.click()
        usd_button= self.find_element(By.CSS_SELECTOR,'.f82f96f550 > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > button:nth-child(1)')
        usd_button.click()

    def select_place_to_go(self,place_to_go):
        search_field = self.find_element(By.ID,':rh:')
        search_field.clear()
        search_field.send_keys(place_to_go)
        time.sleep(2)
        first_resault = self.find_element(By.CSS_SELECTOR,'#autocomplete-result-0 > div:nth-child(1)')
        first_resault.click()

    def select_data(self,check_in_date,check_out_date):
        try:
            cookies = self.find_element(By.ID, "onetrust-accept-btn-handler")
            cookies.click()
        except:

            pass

        next_month_element = self.find_element(By.XPATH, f"//button[@aria-label='Next month']")

        while True :
            try:
                check_in_element = self.find_element(By.XPATH, f"//span[@data-date='{check_in_date}']")
                check_in_element.click()
                break
            except:
                next_month_element.click()

        while True :
            try:
                check_out_element = self.find_element(By.XPATH, f"//span[@data-date='{check_out_date}']")
                check_out_element.click()
                break
            except:
                next_month_element.click()

    def select_adults(self,count=1):
        options_button = self.find_element(By.XPATH, "//button[@data-testid='occupancy-config']")
        options_button.click()
        try:

            cookies = self.find_element(By.ID, "onetrust-accept-btn-handler")
            cookies.click()
        except:
            pass

        adult_value_element = self.find_element(By.ID,'group_adults')
        adult_value = int(adult_value_element.get_attribute('value'))

        increase_adult_element = self.find_element(By.XPATH,'//*[@id=":ri:"]/div/div[1]/div[2]/button[2]')
        for _ in range(count-2):
            increase_adult_element.click()


    def submit(self):
        submit=  self.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/form/div[1]/div[4]/button")
        submit.click()

    def apply_star(self,*star_values):
        for star_value in star_values :
            star_filtration_box = self.find_element(By.XPATH, f"//div[@data-filters-item='class:class={star_value}']")
            star_filtration_box.click()

    def lowest_price_first(self):
        element = self.find_element(By.XPATH, '//button[@data-testid="sorters-dropdown-trigger"]')
        element.click()
        lowest_first_element = self.find_element(By.CSS_SELECTOR,
                                                        '.e3b9881f01 > li:nth-child(3) > button:nth-child(1)')
        lowest_first_element.click()


    def resault_box(self, more_results_selector='button.more-results', scroll_pause_time=2):

        wait = WebDriverWait(self, 10)


        last_height = self.execute_script("return document.body.scrollHeight")

        while True:

            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(scroll_pause_time)

            try:
                more_results_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.ea757ee64b')))
                more_results_button.click()
                time.sleep(scroll_pause_time)
            except:
                pass

            new_height = self.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def create_excel_file(self, filename='properties.xlsx'):
        name_box = self.find_elements(By.XPATH, "//div[@data-testid='title']")
        names = [element.text for element in name_box]

        price_box = self.find_elements(By.XPATH, "//span[@data-testid='price-and-discounted-price']")
        prices = [element.text for element in price_box]


        workbook = openpyxl.Workbook()
        sheet = workbook.active


        sheet.append(['Property Name', 'Price'])


        for name, price in zip(names, prices):
            sheet.append([name, price])


        workbook.save(filename)
        print(f"Excel file '{filename}' created successfully.")

