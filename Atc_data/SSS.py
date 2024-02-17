import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests

npo_jobs = {}
job_no = 0
list2=[]
company_name = "Strategic Staffing Solutions"
current_date = date.today().strftime("%d/%m/%Y")
job_Type = "NA"
contact = "s3corporate@strategicstaff.com"
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
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://careers.strategicstaff.com/")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # Wait until the search input is present and then enter the desired job title
    select_title = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="facetwp-search"]')))
    select_title.send_keys(value)
    time.sleep(3)

    # Select the job type as "Contract"
    select_jobtype = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@data-value="contract"]')))
    select_jobtype.click()
    time.sleep(7)

    while True:
        try:
            nextpage = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="fwp-load-more"]')))
            nextpage.click()
            time.sleep(3)
        except:
            break

    try:
        jobs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class,"job_listing")]')))
        for job in jobs:
            wait=WebDriverWait(job,20)
            jobtitle = job.find_element(By.TAG_NAME, 'h3').text
            if all(keyword.lower() in jobtitle.lower() for keyword in value.split()):
                job_no+=1
                print(jobtitle)
                joburl=wait.until(EC.presence_of_element_located((By.TAG_NAME,'a'))).get_attribute('href')
                print(joburl)
                job_Type=wait.until(EC.presence_of_element_located((By.XPATH,'.//*[@class="job-type contract"]'))).text
                print(job_Type)
                joblocation=wait.until(EC.presence_of_element_located((By.XPATH,'.//*[@class="location"]'))).text
                print(joblocation)
                print()
                if joburl not in list2:
                    list2.append(joburl)
                    list1 = [company_name, current_date, jobtitle, job_Type, pay_rate, joburl, joblocation,
                             jobdate, contact, Work_Type]
                    npo_jobs[job_no] = list1

    except Exception:
        print(f"No jobs for this Role:{value}")


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
    file_name = 'Strategic_Staffing_Solutions_' + current_date  +'.csv'
    npo_jobs_df.to_csv(file_name, index=False)
    print(f"CSV file '{file_name}' has been generated.")