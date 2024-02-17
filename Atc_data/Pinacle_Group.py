import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests

list3 = []
npo_jobs = {}
job_no = 0
list2 = []
company_name = "Pinacle_Groups"
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

keywords = ["Data Analyst", "Business Analyst", "System Analyst", "Data Scientists", "Data engineer", "Business System Analyst"]

for value in keywords:
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://jobs.pinnacle1.com/")
    driver.maximize_window()
    time.sleep(10)
    wait = WebDriverWait(driver, 20)

    search_title = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-automation-id="novo-search-input"]')))
    search_title.send_keys(value)
    time.sleep(5)

    while True:
        try:
            loadmore = wait.until(EC.element_to_be_clickable((By.XPATH, '(//*[@class="flex-wrapper"])[4]')))
            loadmore.click()
            time.sleep(3)
        except Exception:
            break

    try:
        jobs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="job-card"]')))
        for job in jobs:
            jobtitle = job.find_element(By.TAG_NAME, 'h6').text
            if all(keyword.lower() in jobtitle.lower() for keyword in value.split()):
                job_no += 1
                print(jobtitle)
                joburl = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
                print(joburl)

                try:
                    jobdetails = job.find_elements(By.XPATH, './/*[@class="mid-card"]')
                    joblocation = jobdetails[0].text if jobdetails else "NA"
                    job_Type = jobdetails[1].text if jobdetails and len(jobdetails) > 1 else "NA"
                    job_postdate = jobdetails[2].text if jobdetails and len(jobdetails) > 2 else "NA"

                    print(joblocation)
                    print(job_Type)
                    print(job_postdate)

                    if joburl not in list3:
                        list3.append(joburl)
                        list1 = [company_name, current_date, jobtitle, job_Type, pay_rate, joburl, joblocation,
                                 jobdate, contact, Work_Type]
                        npo_jobs[job_no] = list1
                except Exception as details_exception:
                    print(f"Error extracting job details: {details_exception}")

    except Exception as jobs_exception:
        print(f"Error finding job elements: {jobs_exception}")
        print("No jobs for the particular Role")

    driver.quit()

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
    file_name = 'Pinacle_groups_' + current_date + '.csv'
    npo_jobs_df.to_csv(file_name, index=False)
    print(f"CSV file '{file_name}' has been generated.")
