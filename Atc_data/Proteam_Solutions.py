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
company_name = "Proteam_Solutions_"
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
    # chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www1.jobdiva.com/portal/?a=57jdnwt0v43w1xmr9o0bx69yjzpn3g08537mt0fo34qt7061lje4nlkurahvcrcj&compid=0#/")
    driver.maximize_window()
    time.sleep(8)
    wait = WebDriverWait(driver, 20)
    time.sleep(3)
    # Corrected XPATH for the search input element
    search_title_xpath = '//*[@class="form-control jd-form jd-form-medium"]'
    search_title = wait.until(EC.presence_of_element_located((By.XPATH, search_title_xpath)))
    search_title.send_keys(value)
    time.sleep(4)

    # Click on the apply button
    apply_search = wait.until(EC.presence_of_element_located((By.XPATH, '(//*[@class="btn jd-btn jd-btn-block"])[1]'))).click()
    time.sleep(7)

    try:


        # Locate all job elements
        jobs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="list-group-item list-group-item-action"]')))
        for i in range(len(jobs)):
            job_no+=1
            # Re-find the elements within the loop to avoid StaleElementReferenceException
            jobs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="list-group-item list-group-item-action"]')))
            jobtitle = jobs[i].find_element(By.XPATH, '//span[@class="text-capitalize jd-nav-label"]').text
            print(jobtitle)
            jobdata = jobs[i].find_elements(By.XPATH, './/*[@class="d-flex text-muted"]')
            list2 = []
            for data in jobdata:
                print(data.text)
            click_job = jobs[i].find_element(By.XPATH, '//*[@class="btn jd-btn"]').click()
            joburl = driver.current_url
            print(joburl)
            time.sleep(5)
            job_Type=driver.find_element(By.XPATH,'(.//*[@class="jd-svg-span-10"])[2]').text
            print(job_Type)
            print()
            time.sleep(5)
            driver.back()
            time.sleep(5)

            if joburl not in list2:
                list2.append(joburl)
                list1 = [company_name, current_date, jobtitle, job_Type, pay_rate, joburl, joblocation, jobdate, contact, Work_Type]
                npo_jobs[job_no] = list1


    except Exception:
        print(f"No Job available for the particular {value}")

    # Close the webdriver when done
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
    file_name = 'Proteam_Solutions_' + current_date + '.csv'
    npo_jobs_df.to_csv(file_name, index=False)
    print(f"CSV file '{file_name}' has been generated.")
