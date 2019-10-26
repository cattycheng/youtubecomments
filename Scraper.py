import csv
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd

# Create a Chrome browser
chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--no-sandbox') # Bypass OS security model
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument("--disable-extensions")

chrome_driver = os.getcwd() + "\\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)

# Create an empty data array to store your outputs
data = []

# Grab the url This URL is a tester URL, you'll want to write code to either search a list of movie names and keyword
# "trailer" and then scrape those URLs Or, pass in a file with a list of URLs that you can then use a for loop to
# iterate through You'll also want to modify the code to include a "Movie" column so you can label what movie
urls = ["https://www.youtube.com/watch?v=YyEm_TK5SsI", "https://www.youtube.com/watch?v=ZESuUQMTKqQ"]

for url in urls:

    # Open the url from the command line
    driver.get(url)
    SCROLL_PAUSE_TIME = 1
    time.sleep(SCROLL_PAUSE_TIME)

    total_time = 0

    # Get current number of comments
    last_comments = len(driver.find_elements_by_id("content-text"))

    while True:
        # Scroll down to bottom
        driver.find_element_by_tag_name('body').send_keys(Keys.END)

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new number of comments
        new_comments = len(driver.find_elements_by_id("content-text"))

        comment_section = len(driver.find_elements_by_id("comments"))
        print(last_comments, new_comments, comment_section)

        # If new comments and last comments are the same and comment section has already loaded
        if new_comments == last_comments and comment_section == 1:
            time.sleep(SCROLL_PAUSE_TIME)
            new_comments = len(driver.find_elements_by_id("content-text"))
            if new_comments == last_comments:
                break
        last_comments = new_comments

    while True:
        try:
            # Get the title and date of the video
            title = driver.find_element_by_tag_name("h1").text
            date = driver.find_element_by_xpath('//*[@id="date"]/yt-formatted-string').text
            views = driver.find_element_by_xpath('//*[@id="count"]/yt-view-count-renderer/span[1]').text
            # Find the total number of comments
            comment_count = driver.find_element_by_xpath('//*[@id="count"]/yt-formatted-string').text
            break
        except:
            if total_time > 5:
                break
            else:
                total_time += 0.5
                time.sleep(SCROLL_PAUSE_TIME)

    # find the comments and times posted of comments
    comments = driver.find_elements_by_id("content-text")
    times = driver.find_elements_by_xpath('//*[@id="header-author"]/yt-formatted-string')

    data = []

    # If total number of comments matches total number of times, store both
    if len(comments) == len(times):
        for num, comment in enumerate(comments):
            data.append([title, date, views, comment_count, times[num].text, comment.text])
    # Else, just store comments
        # If total number of comments matches total number of times, store both
        if len(comments) == len(times):
            for num, comment in enumerate(comments):
                data.append([title, date, views, comment_count, "", comment.text])

    print(title, date, views, comment_count)

column_names = ['title', 'date', 'views', 'comment_count', 'time', 'comment']
df = pd.DataFrame(data, columns=column_names)

# If file doesn't exist yet, make the file with headers, else, append to existing file
if os.path.isfile('./output.csv'):
    df.to_csv('output.csv', encoding="UTF-8", mode='a', header=False, index=False)
else:
    df.to_csv('output.csv', encoding="UTF-8", header=column_names, index=False)

# Close the browser
driver.close()
