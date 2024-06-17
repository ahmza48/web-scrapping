# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import pandas as pd
# from selenium.common.exceptions import NoSuchElementException



# options = webdriver.ChromeOptions()
# # options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-extensions")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# options.add_argument('--ignore-certificate-errors')
# options.add_experimental_option('detach', True)
# driver = webdriver.Chrome(options=options)
# driver.maximize_window()


# user_name='shopswaveo'
# # URL to Scrape
# tiktok_profile_url = 'https://www.tiktok.com/@{user_name}'

# # Open Browser
# driver.get(tiktok_profile_url)


# # Bypass the "Continue as guest" modal
# try:
#     continue_as_guest_button = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//div[@role='link' and contains(text(), 'Continue as guest')]"))
#     )
#     if continue_as_guest_button.is_displayed() and continue_as_guest_button.is_enabled():
#         continue_as_guest_button.click()
#         time.sleep(3)
# except Exception as e:
#     print(f"Continue as guest button not found or clickable")


# # Scroll to load videos
# actions = ActionChains(driver)
# for _ in range(2):  # Adjust based on the number of videos to load
#     actions.send_keys(Keys.PAGE_DOWN).perform()
#     time.sleep(2)


# videos = driver.find_elements(By.XPATH, '//a[contains(@href, "/video/")]')[:20]
# video_data = []

# # eliminating duplicate video links
# for i in range(0, len(videos), 2):
#     video = videos[i]
#     video_url = video.get_attribute('href')
#     print('video_url\n')
#     print(video_url)
#     video_data.append({'url': video_url})

# # Initialize list to hold comments
# comments_data = []

# # Visit each video to get comments
# for video in video_data:

#     print('**************************************************')
#     print(f'Scraping individual video: {video['url']}')
#     driver.get(video['url'])
#     time.sleep(2)  # Wait for video page to load

#     try:
#         pop_up = driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div/div[2]/div/div[2]')
#         pop_up.click()
#     except NoSuchElementException:
#         pass  # Continue without clicking on the pop-up

#     # Click on the pause/play button
#     try:
#         play_button = driver.find_element(By.XPATH, '//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div[2]/div[1]/div[1]')
#         print('------------BUTTON FOUND-------------')
#         play_button.click()
#     except NoSuchElementException:
#         pass  # Continue without clicking on the play button

#     try:
#         video_description = driver.find_element(By.XPATH, '//*[@data-e2e="browse-video-desc"]').text
#     except NoSuchElementException:
#         video_description = ""
#     print('description: ', video_description)
#     # Scrolling to load comments
#     for _ in range(5):  # Adjust based on the number of comments to load
#         actions.send_keys(Keys.PAGE_DOWN).perform()
#         time.sleep(2)


#     #Waiting untill comments load
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, '//*[@data-e2e="search-comment-container"]'))
#     )

#     comments = driver.find_elements(By.XPATH, '//*[@data-e2e="comment-level-1"]')[:50]
    
#     for comment in comments:
#         # comments_data.append({'description': video['description'], 'comment': comment.text})
#         comments_data.append({'description': video_description, 'comment': comment.text})
#         print(comment.text)
#     continue

# # Convert to DataFrame
# df = pd.DataFrame(comments_data)
# # Save to CSV
# df.to_csv('tiktok_scraped.csv', index=False)

# # Close the WebDriver
# driver.quit()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

def initialize_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def scroll_to_load_videos(driver):
    actions = ActionChains(driver)
    for _ in range(2):  # Adjust based on the number of videos to load
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)

def scrape_videos(driver, user_name):
    tiktok_profile_url = f'https://www.tiktok.com/@{user_name}'
    driver.get(tiktok_profile_url)
    time.sleep(2)
    # Check if the Account is valid or not
    try:
        error_message = driver.find_element(By.CLASS_NAME, "css-51ovqurc-PTitle")        
        if error_message.text()=='Couldn\'t find this account':
            print(f"User '{user_name}' not found on TikTok.")
            return 'User Not Found'
    except NoSuchElementException:
        pass
    scroll_to_load_videos(driver)
    videos = driver.find_elements(By.XPATH, '//a[contains(@href, "/video/")]')[:20]
    video_data = []
    for i in range(0, len(videos), 2):
        video = videos[i]
        video_url = video.get_attribute('href')
        video_data.append({'url': video_url})
    return video_data

def scrape_comments(driver, video_data):
    comments_data = []
    actions = ActionChains(driver)
    for video in video_data:
        driver.get(video['url'])
        time.sleep(2)  # Wait for video page to load
        # continue without logging in
        try:
            pop_up = driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div/div[2]/div/div[2]')
            pop_up.click()
        except NoSuchElementException:
            pass
        # pause the video to scrape comments
        try:
            play_button = driver.find_element(By.XPATH, '//*[@id="main-content-video_detail"]/div/div[2]/div[1]/div[1]/div[1]/div[4]/div[2]/div[1]/div[1]')
            play_button.click()
        except NoSuchElementException:
            pass
        # scrape description
        try:
            video_description = driver.find_element(By.XPATH, '//*[@data-e2e="browse-video-desc"]').text
        except NoSuchElementException:
            video_description = ""
        for _ in range(5):  # Adjust based on the number of comments to load
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(2)

        # wait untill comments load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@data-e2e="search-comment-container"]')))
        comments = driver.find_elements(By.XPATH, '//*[@data-e2e="comment-level-1"]')[:50]
        for comment in comments:
            comments_data.append({'description': video_description, 'comment': comment.text})
            print(comment.text)
    return comments_data

def scrape_tiktok(user_name):
    driver = initialize_driver()
    try:
        video_data = scrape_videos(driver, user_name)
        if video_data=='User Not Found':
            user_name = input("User not found.\n Enter another TikTok username: ")
            scrape_tiktok(user_name)
            return
        if not video_data:
            print(f'No videos are posted by {user_name}')
            return
        comments_data = scrape_comments(driver, video_data)
        df = pd.DataFrame(comments_data)
        # df.to_csv('tiktok_scraped.csv', index=False)
        csv_filename = f"{user_name}_tiktok_scraped.csv"
        df.to_csv(csv_filename, index=False)

    finally:
        driver.quit()

user_name = input("Enter TikTok username: ")
scrape_tiktok(user_name)
