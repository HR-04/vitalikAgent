import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl


wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Medium Posts"
ws.append(["Post URL", "Title", "Content"])


options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("https://medium.com/@VitalikButerin")
    time.sleep(3) 
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    post_links = set()
    articles = driver.find_elements(By.XPATH, '//a[contains(@href, "/@VitalikButerin/")]')
    for article in articles:
        href = article.get_attribute("href")
        if href and "medium.com" in href and "source=home" not in href:
            clean_url = href.split('?')[0]  
            post_links.add(clean_url)

    print(f"Found {len(post_links)} unique posts. Scraping content...")

    for url in post_links:
        try:
            driver.get(url)
            time.sleep(2)  

            title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1 | //h2'))
            ).text


            paragraphs = driver.find_elements(By.XPATH, '//div[@role="article"]//p | //article//p')
            content = "\n".join([p.text for p in paragraphs if p.text.strip()])

            if title.lower() != "medium" and content:
                ws.append([url, title, content])
                print(f"Scraped: {title}")
                
        except Exception as e:
            print(f"Error scraping {url}: {str(e)[:100]}...")  
        time.sleep(3)  

    # Save Excel
    wb.save("VitalikButerin_Medium_Posts.xlsx")
    print(f"Successfully saved {len(post_links)} posts to 'VitalikButerin_Medium_Posts.xlsx'")

finally:
    driver.quit()