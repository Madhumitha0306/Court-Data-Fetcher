from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

def save_pdf_from_url(pdf_url, case_id):
    response = requests.get(pdf_url)
    filename = f"static/orders/{case_id}.pdf"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename

def fetch_case_details(case_type, case_number, filing_year):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        driver.get("https://services.ecourts.gov.in/ecourtindia_v6/")
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Case Status"))).click()
        Select(wait.until(EC.presence_of_element_located((By.ID, "sess_state_code")))).select_by_visible_text("Tamil Nadu")
        Select(wait.until(EC.presence_of_element_located((By.ID, "sess_dist_code")))).select_by_visible_text("Cuddalore")
        time.sleep(2)

        wait.until(EC.element_to_be_clickable((By.ID, "case_no_radio"))).click()
        Select(driver.find_element(By.ID, "case_type")).select_by_visible_text(case_type)
        driver.find_element(By.ID, "case_number").send_keys(case_number)
        driver.find_element(By.ID, "case_year").send_keys(filing_year)
        driver.find_element(By.ID, "submitbtn").click()
        wait.until(EC.presence_of_element_located((By.ID, "partyName")))

        parties = driver.find_element(By.ID, "partyName").text.strip()
        filing_date = driver.find_element(By.ID, "FilingDate").text.strip()
        next_hearing = driver.find_element(By.ID, "NextDate").text.strip()

        try:
            pdf_element = driver.find_element(By.PARTIAL_LINK_TEXT, ".pdf")
            pdf_url = pdf_element.get_attribute("href")
            local_pdf = save_pdf_from_url(pdf_url, f"{case_type}_{case_number}_{filing_year}")
        except:
            pdf_url = None
            local_pdf = None

        return {
            'parties': parties,
            'filing_date': filing_date,
            'next_hearing': next_hearing,
            'latest_order_link': pdf_url,
            'local_copy': local_pdf
        }

    except Exception as e:
        return None
    finally:
        #driver.quit()
        pass
