import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_trailer_url(movie_name, year):
    driver = webdriver.Chrome()
    driver.minimize_window()
    try:
        driver.get("https://www.youtube.com")
        search_box = driver.find_element(By.NAME, "search_query")
        search_query = f"{movie_name} {year} trailer"
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        videos = driver.find_elements(By.XPATH, '//*[@id="video-title"]')

        potential_url = None  # Initialize potential_url with None

        for video in videos:
            title = video.get_attribute("title").lower()
            if movie_name.lower() in title:
                if "official trailer" in title or "trailer" in title:
                    video_url = video.get_attribute("href")
                    return video_url
                else:
                    potential_url = video.get_attribute("href")

        if potential_url:
            return potential_url
        else:
            return "No official trailer found for the given year."
    finally:
        time.sleep(2)
        driver.quit()

# Example usage
movie_name = "Delhi-6"
year = "2009"
trailer_url = get_trailer_url(movie_name, year)
print(trailer_url)
