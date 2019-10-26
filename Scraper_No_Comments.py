# Does the same thing as the other code but doesn't pull comments, just pulls the view/comment count

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

    total_time = 0

    # Open the url from the command line
    driver.get(url)

    SCROLL_PAUSE_TIME = 0.5

    while True:
        # Scroll down to bottom
        driver.find_element_by_tag_name('body').send_keys(Keys.END)

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        comment_section = len(driver.find_elements_by_id("comments"))

        # If new comments and last comments are the same and comment section has already loaded
        if comment_section == 1:
            break

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

    # Add your output to the array
    print(title, date, views, comment_count)
    data.append([title, date, views, comment_count])

column_names = ['title', 'date', 'views', 'comment_count']
df = pd.DataFrame(data, columns=column_names)

# If file doesn't exist yet, make the file with headers, else, append to existing file
if os.path.isfile('./output_no_comments.csv'):
    df.to_csv('output_no_comments.csv', encoding="UTF-8", mode='a', header=False, index=False)
else:
    df.to_csv('output_no_comments.csv', encoding="UTF-8", header=column_names, index=False)

# Close the browser
driver.close()
