import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import re


npo_jobs = {}
job_no = 0
list2 = []
company_name = "Inceed"
current_date = date.today().strftime("%d/%m/%Y")
job_Type = "NA"
contact = "(866) 462-3331"
Work_Type = "NA"
pay_rate = "NA"
job_postdate = "NA"
joburl = "NA"
jobtitle = "NA"
joblocation = "NA"
jobdate = "NA"

keywords = ["Data Analyst", "Business Analyst", "System Analyst", "Data Scientists", "Data engineer", "Business System Analyst"]

for value in keywords:
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://jobs.inceed.com/")
    driver.maximize_window()
    time.sleep(8)
    wait = WebDriverWait(driver, 20)

    select_contract = wait.until(EC.element_to_be_clickable((By.XPATH, '(//span[text()="Contract"])[1]')))
    select_contract.click()
    time.sleep(5)

    search_title = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@placeholder="Search Jobs by Keyword or Job Title"]')))
    search_title.send_keys(value)
    time.sleep(5)

    click_select_title = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="fwp-submit"]')))
    driver.execute_script("arguments[0].click();", click_select_title)
    time.sleep(10)

    try:
        jobs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"job_listing")]')))
        for job in jobs:
            joburl = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
            jobtitle = job.find_element(By.XPATH, './/*[@class="inceed_jobs_title"]').text

            if all(keyword.lower() in jobtitle.lower() for keyword in value.split()):
                job_no += 1
                print(joburl)
                print(jobtitle)
                job_Type = job.find_element(By.XPATH, './/*[@class="inceed_jobs_more_info js_jb_type"]//span').text
                print(job_Type)
                pay_amount = job.find_element(By.XPATH, './/*[@class="inceed_jobs_more_info sal_2"]//span').text
                pay_rate = pay_amount + "/hour"
                print(pay_rate)

                posted_date = job.find_element(By.XPATH, './/*[@class="inceed_jobs_posted_date"]').text
                match = re.search(r'on (.+)', posted_date)

                if match:
                    job_postdate = match.group(1)
                    print(job_postdate)
                else:
                    print("Date not found in the given string.")

                joblocation = job.find_element(By.XPATH, '(.//*[@class="inceed_jobs_more_info"]//span)[1]').text
                print(joblocation)
                Work_Type = job.find_element(By.XPATH, '(.//*[@class="inceed_jobs_more_info"]//span)[2]').text
                print(Work_Type)

                if joburl not in list2:
                    list2.append(joburl)

                list1 = [company_name, current_date, jobtitle, job_Type, pay_rate, joburl, joblocation, jobdate, contact, Work_Type]
                npo_jobs[job_no] = list1

    except Exception:
        print(f"No jobs available for the required Role {value} ")

if job_no == 0:
    print("No jobs available for the particular job.")
else:
    print("Generating CSV file")
    npo_jobs_df = pd.DataFrame.from_dict(npo_jobs, orient='index',
                                         columns=['Vendor Company Name', 'Date & Time Stamp', 'Job Title',
                                                  'Job Type', 'Pay Rate', 'Job Posting Url', 'Job Location',
                                                  'Job Posting Date', 'Contact Person', 'Work Type (Remote /Hybrid /Onsite)'])

    print(npo_jobs_df.head(job_no))
    current_date = date.today().strftime("%d/%m/%Y").replace('/', '_')
    file_name = 'Inceed_' + current_date + '.csv'
    npo_jobs_df.to_csv(file_name, index=False)
    print(f"CSV file '{file_name}' has been generated.")
