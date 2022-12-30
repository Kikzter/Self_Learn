import xl_utils
import one
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import csv

one.delete_view()
#executable_path=r"C:\Users\mohmejn\Desktop\CSI_Scrapper\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=r"C:\Users\mohmejn\Desktop\CSI_Scrapper\chromedriver.exe", chrome_options=options)


path="input.xlsx"

rows = xl_utils.getRowCount(path, 'Sheet1')


for r in range(2, rows+1):
        try:
                asin_id = xl_utils.readData(path, 'Sheet1', r, 1)
                mp_id = str(xl_utils.readData(path, 'Sheet1', r, 2))
                attribute_value = '^incontinence_protector_size$'
                url='https://csi.amazon.com/view?view=blame_o&item_id='+ asin_id + '&marketplace_id='+ mp_id + '&customer_id=&merchant_id=&sku=&fn_sku=&gcid=&fulfillment_channel_code=&listing_type=purchasable&submission_id=&order_id=&external_id=&search_string=%5Eincontinence_protector_size%24&realm=USAmazon&stage=prod&domain_id=&keyword=&submit=Show' 
                driver.get(url)
                WebDriverWait(driver, 30).until(EC.url_contains((url)))
                driver.maximize_window()
                
                driver.get('http://csi.amazon.com/view?view=blame_o&item_id=' + asin_id + '&marketplace_id='+ mp_id +'&customer_id=&merchant_id=&sku=&fn_sku=&gcid=&fulfillment_channel_code=&listing_type=purchasable&submission_id=&order_id=&external_id=&search_string=%5Eincontinence_protector_size%24&realm=USAmazon&stage=prod&domain_id=&keyword=&submit=Show&display=csv')
                print(asin_id, 'try')
                if r == rows:
                        time.sleep(3)


        except:
                print(asin_id,'expect')
                pass
one.collate_data()

