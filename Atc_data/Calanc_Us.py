import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pandas as pd
import requests
import re
npo_jobs = {}
job_no = 0
list2=[]

company_name = "Calance_US"
current_date = date.today().strftime("%d/%m/%Y")
job_Type = "NA"
contact = "https://www.calanceus.com/contact-us"
Work_Type = "NA"
pay_rate = "NA"
job_postdate = "NA"
joburl = "NA"
jobtitle = "NA"
joblocation = "NA"
jobdate = "NA"

keywords = ["Python Engineer", "Business Analyst", "System Analyst", "Data Scientists", "Data engineer","Business System Analyst"]

for value in keywords:

    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.calanceus.com/careers")
    driver.maximize_window()
    time.sleep(4)
    wait=WebDriverWait(driver,20)

    jobs=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="job-listing-card__list"]')))
    for job in jobs:
        wait=WebDriverWait(job,20)
        jobtitle=wait.until(EC.presence_of_element_located((By.XPATH,'.//*[@class="job-listing-card__list--title"]'))).text
        if value.lower() in jobtitle.lower():
            Location=wait.until(EC.presence_of_element_located((By.XPATH,'.//*[@class="job-listing-card__list--id"]'))).text
            joburl=wait.until(EC.presence_of_element_located((By.TAG_NAME,'a'))).get_attribute('href')
            joblocation=Location[10:]
            if "India".lower() not in joblocation.lower():
                print(joblocation)
                if "Hybrid".lower() in joblocation.lower():
                    Work_Type="Hybrid"
                elif "Remote".lower() in joblocation.lower():
                    Work_Type="Remote"
                else:
                    Work_Type="Onsite"
                print(Work_Type)
                if joburl not in list2:
                    job_no+=1
                    list2.append(joburl)
                    list1 = [company_name, current_date, jobtitle, job_Type, pay_rate, joburl, joblocation,
                             jobdate, contact, Work_Type]
                    npo_jobs[job_no] = list1


    if job_no == 0:
        print(f"No jobs available for the particular job: {value}")

if job_no == 0:
    print(f"No jobs available")
else:
    print("Generating CSV file")
    npo_jobs_df = pd.DataFrame.from_dict(npo_jobs, orient='index',
                                         columns=['Vendor Company Name', 'Date & Time Stamp', 'Job Title',
                                                  'Job Type', 'Pay Rate', 'Job Posting Url', 'Job Location',
                                                  'Job Posting Date', 'Contact Person', 'Work Type (Remote /Hybrid /Onsite)'])

    print(npo_jobs_df.head(job_no))
    current_date = date.today().strftime("%d/%m/%Y").replace('/','_')
    file_name = 'Calance_us_' + current_date  +'.csv'
    npo_jobs_df.to_csv(file_name, index=False)
    print(f"CSV file '{file_name}' has been generated.")