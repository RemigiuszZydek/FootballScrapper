from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def create_driver(headless=False):
    options = Options()

    if headless:
        options.add_argument("--headless=new") 

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    return driver, wait


def stats_scraping(match_url: str):
    driver, wait = create_driver(headless=True)

    driver.get(match_url)

    stats_dict = {}

    info = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#info")))
    info.click()

    date_element = wait.until(
    EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#tab-content-Info > div.Vh > button:nth-child(1) > div.Xh > span")
        )
    )

    # teraz date_element jest pojedynczym WebElement
    date_text = date_element.text
    match_date_obj = datetime.strptime(date_text,"%d %b %Y")
    stats_dict["match_date"] = match_date_obj

    stats = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#statistics")))
    stats.click()

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-id$="_mtc-dtl-stat"]')
        )
    )

    all_stats = driver.find_elements(By.CSS_SELECTOR, '[data-id$="_mtc-dtl-stat"]')

    for stat in all_stats:
        numbers_section = stat.find_element(By.CLASS_NAME, "Ne")

        home = numbers_section.find_element(By.CSS_SELECTOR, "span.Re").text
        away = numbers_section.find_element(By.CSS_SELECTOR, "span.Se").text
        name = numbers_section.find_element(By.CLASS_NAME, "Ye").text

        if "Shots on target" in name:
            stats_dict["home_shots_on_target"] = int(home)
            stats_dict["away_shots_on_target"] = int(away)
        
        elif "Possession" in name:
            stats_dict["home_possession"] = int(home.replace("%", ""))
            stats_dict["away_possession"] = int(away.replace("%", ""))

        elif "Corner" in name:
            stats_dict["home_corners"] = int(home)
            stats_dict["away_corners"] = int(away)

        elif "Yellow cards" in name:
            stats_dict["home_yellow_cards"] = int(home)
            stats_dict["away_yellow_cards"] = int(away)


    driver.quit()

    return stats_dict