from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import requests

driver = webdriver.Chrome()

driver.get("https://dash.tradier.com")
driver.implicitly_wait(60)

print("Please log in and navigate to the documents page.")
input()

done = list()
skipped = list()

while len(done) < 72:
    button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/header/div/div[2]/div/div[3]/div/button")
    button.click()

    acct_list = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/header/div/div[2]/div/div[3]/div/div/div[1]").find_elements(By.TAG_NAME, "button")

    for acct_elem in acct_list:
        name = acct_elem.text
        if name in done:
            continue
        print(name)
        ActionChains(driver).move_to_element(acct_elem).click().perform()

        try:
            a = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div/div/div/div[2]/div[1]/div[2]/div/div/div/table/tbody/tr/td[3]/div/div/a')
            href = a.get_attribute("href")
        
            r = requests.get(href, stream=True)
            with open(f"downloads/{name}.pdf", 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
            print("saveed")
        except NoSuchElementException:
            skipped.append(name)
            print("skipped")
        done.append(name)
        break
    driver.refresh()

print(f"Saved: {done}")
print(f"Skipped: {skipped}")
