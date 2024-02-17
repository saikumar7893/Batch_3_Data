import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
list2=[]
npo_jobs = {}
job_no = 0
list2=[]
company_name = "SBS_Createx_IT_Consultants"
current_date = date.today().strftime("%d/%m/%Y")
job_Type = "NA"
contact = "NA"
Work_Type = "NA"
pay_rate = "NA"
job_postdate = "NA"
joburl = "NA"
jobtitle = "NA"
joblocation = "NA"
jobdate = "NA"

keywords = ["Data Analyst", "Business Analyst", "System Analyst", "Data Scientists", "Data engineer","Business System Analyst"]
for value in keywords:

    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://careers.sbscreatix.com/#/jobs")
    driver.maximize_window()
    time.sleep(10)
    wait=WebDriverWait(driver,20)
    search_title=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@class="search ng-pristine ng-untouched ng-valid ng-empty"]')))
    search_title.send_keys(value)
    time.sleep(10)
    try:

        jobs=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@class="card-wrapper ng-scope"]')))
        for job in jobs:
            jobtitle=job.find_element(By.XPATH,'.//*[@class="card-title ng-binding"]').text
            if all(keyword.lower() in jobtitle.lower() for keyword in value.split()):
                job_no+=1
                print(jobtitle)
                joblocation=job.find_element(By.XPATH,'.//*[@class="card-location ng-binding"]').text
                print(joblocation)
                job_Type=job.find_element(By.XPATH,'.//*[@class="card-type ng-binding"]').text
                print(job_Type)
                job_postdate=job.find_element(By.XPATH,'.//*[@class="card-date ng-binding ng-scope"]').text
                print(job_postdate)
                joburl=job.find_element(By.TAG_NAME,'a').get_attribute('href')
                print(joburl)
                print()
                if joburl not in list2:
                    list2.append(joburl)
                    list1 = [company_name, current_date, jobtitle, job_Type, pay_rate, joburl, joblocation,
                             jobdate, contact, Work_Type]
                    npo_jobs[job_no] = list1

    except Exception:
        print("No jobs for the particular Role:")

if job_no == 0:
    print("No jobs available for the particular job.")
else:
    print("Generating CSV file")
    npo_jobs_df = pd.DataFrame.from_dict(npo_jobs, orient='index',
                                         columns=['Vendor Company Name', 'Date & Time Stamp', 'Job Title',
                                                  'Job Type', 'Pay Rate', 'Job Posting Url', 'Job Location',
                                                  'Job Posting Date', 'Contact Person', 'Work Type (Remote /Hybrid /Onsite)'])

    print(npo_jobs_df.head(job_no))
    current_date = date.today().strftime("%d/%m/%Y").replace('/','_')
    file_name = 'SBS_Createx_IT_Consultants' + current_date  +'.csv'
    npo_jobs_df.to_csv(file_name, index=False)
    print(f"CSV file '{file_name}' has been generated.")
