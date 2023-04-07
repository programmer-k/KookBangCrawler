from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Constants
search_keywords = ("과학화", "최첨단", "4차", "빅데이터", "인공지능")
directory = "data/"
page_to_crawl = 13


for search_keyword in search_keywords:
    # Make an option
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    #chrome_options.add_argument('--headless')

    # Open a website
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://kookbang.dema.mil.kr/newsWeb/ATCE_CTGR_0010030000/list.do")

    # Click the search button
    elem = driver.find_element(By.CSS_SELECTOR, "#gnb > ul > li.search_btn > a")
    elem.click()

    # Wait until the search box is visible
    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#mainSearch")))

    # Enter the keyword
    search_box.send_keys(search_keyword)
    search_box.send_keys(Keys.RETURN)

    # Click 국방 section
    elem = driver.find_element(By.CSS_SELECTOR, "#container > div.full_search_box > div > ul > li:nth-child(2) > a")
    elem.click()

    # Click 육군 section
    elem = driver.find_element(By.CSS_SELECTOR, "#container > div.full_search_box > div > div.menu_search > div > div > div:nth-child(3) > a")
    elem.click()

    try:
        for i in range(page_to_crawl):
            # Find all elements for each article
            elems = driver.find_elements(By.CSS_SELECTOR, "#container > div.full_search_box > div > div.box > ul > li > a > div.txt > h3")

            # Loop for each article
            for elem in elems:
                # Click the element and open a new tab for the article
                elem.click()
                driver.switch_to.window(driver.window_handles[1])

                # Search for the title
                wait = WebDriverWait(driver, 10)
                title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#contents > div.article_top > h2")))
                
                # Open a file to write
                fp = open(directory + title.text.replace("/", "|") + "{" + search_keyword + "}_.txt", "w")
                fp.write(title.text)

                # Search for the text contents
                text_content = driver.find_element(By.CSS_SELECTOR, "#article_body_view")
                fp.write(text_content.text)

                # Close the file
                fp.close()

                # Close the tab and switch back to the original tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            # Click the next page button
            elem = driver.find_element(By.CSS_SELECTOR, "#container > div.full_search_box > div > div.pagination > a.active + a")
            elem.click()
    except TimeoutException:
        # The server detects crawling.
        # Move to next keyword.
        pass

    driver.close()
