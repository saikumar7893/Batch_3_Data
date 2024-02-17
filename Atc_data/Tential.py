import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

npo_jobs = {}
job_no = 0
list2 = []
company_name = "Tential"
current_date = date.today().strftime("%d/%m/%Y")
job_Type = "NA"
contact = "(844) 885-0161"
Work_Type = "NA"
pay_rate = "NA"
job_postdate = "NA"
joburl = "NA"
jobtitle = "NA"
joblocation = "NA"
jobdate = "NA"

chrome_options = Options()
chrome_options.add_argument('--window-size=1920,1080')
# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.tential.com/careers/")
driver.maximize_window()
time.sleep(8)
wait=WebDriverWait(driver,20)
select_title=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@class="wpupg-filter-text-input"]')))
select_title.send_keys("Business Analyst")
time.sleep(6)


select_contract=wait.until(EC.presence_of_element_located((By.XPATH,'(//*[@data-value="wpupg-dropdown-placeholder"])[1]')))
select_contract.click()
time.sleep(5)

click_contract=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@data-value="contract"]')))
click_contract.click()
time.sleep(5)
#

jobs=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="wpupg-grid-jobs"]//a')))
for job in jobs:
    wait=WebDriverWait(job,20)
    jobtitle=wait.until(EC.presence_of_element_located((By.TAG_NAME,'h3'))).text
    print(jobtitle)
    joburl=job.get_attribute('href')
    print()









