# (working fine)
# import csv
# import re
# import time
# import threading
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# stop_requested = threading.Event()
# data_lock = threading.Lock()
# current_state = []  # List to keep track of current state of processed movies


# def listen_for_stop():
#     input("Press Enter to stop the script...\n")
#     stop_requested.set()


# def get_trailer_url(movie_name, year):
#     driver = webdriver.Chrome()
#     driver.minimize_window()
#     try:
#         driver.get("https://www.youtube.com")
#         search_box = driver.find_element(By.NAME, "search_query")
#         search_query = f"{movie_name} {year} trailer"
#         search_box.send_keys(search_query)
#         search_box.send_keys(Keys.RETURN)
#         time.sleep(3)
#         videos = driver.find_elements(By.XPATH, '//*[@id="video-title"]')

#         potential_url = None  # Initialize potential_url with None

#         for video in videos:
#             title = video.get_attribute("title").lower()
#             if movie_name.lower() in title:
#                 if "official trailer" in title or "trailer" in title:
#                     video_url = video.get_attribute("href")
#                     return video_url
#                 else:
#                     potential_url = video.get_attribute("href")

#         if potential_url:
#             return potential_url
#         else:
#             return "No official trailer found for the given year."
#     finally:
#         time.sleep(2)
#         driver.quit()


# def save_periodically(csv_file, fieldnames):
#     while not stop_requested.is_set():
#         time.sleep(30)
#         with data_lock:
#             if current_state:  # Only save if there is some data to save
#                 with open(csv_file, mode="w", newline="") as file:
#                     writer = csv.DictWriter(file, fieldnames=fieldnames)
#                     writer.writeheader()
#                     writer.writerows(current_state)
#                 print("Data saved periodically.")


# def process_trailers(csv_file, run, num_threads=4):
#     with open(csv_file, mode="r", newline="") as file:
#         reader = csv.DictReader(file)
#         movies = list(reader)

#     global current_state
#     current_state = movies  # Initialize the current state

#     success_count = 0
#     failure_count = 0

#     fieldnames = reader.fieldnames + ["trailer_url", "status"]

#     # Start the periodic saving thread
#     saving_thread = threading.Thread(
#         target=save_periodically, args=(csv_file, fieldnames)
#     )
#     saving_thread.start()

#     # Create a list of threads
#     threads = []

#     # Divide the movies into chunks for each thread
#     chunk_size = (run + num_threads - 1) // num_threads
#     movie_chunks = [movies[i : i + chunk_size] for i in range(0, run, chunk_size)]

#     # Start the threads
#     for i in range(num_threads):
#         if i < len(movie_chunks):
#             thread = threading.Thread(
#                 target=process_movie_chunk,
#                 args=(movie_chunks[i], fieldnames, current_state),
#             )
#             threads.append(thread)
#             thread.start()

#     # Wait for all threads to complete
#     for thread in threads:
#         thread.join()

#     # Save the final state
#     with data_lock:
#         with open(csv_file, mode="w", newline="") as file:
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerows(current_state)

#     print("\nSummary:")
#     print(f"Total processed: {run}")
#     print(f"Total URLs added: {success_count}")
#     print(f"Total failures: {failure_count}")

#     stop_requested.set()  # Stop the periodic saving thread
#     saving_thread.join()


# def process_movie_chunk(movies, fieldnames, current_state):
#     success_count = 0
#     failure_count = 0

#     for i, movie in enumerate(movies):
#         if stop_requested.is_set():
#             break

#         movie_name = movie["title"]
#         year = movie["released_date"]
#         trailer_url = get_trailer_url(movie_name, year)
#         movie["trailer_url"] = trailer_url
#         movie["status"] = "Found" if "youtube.com" in trailer_url else "Not Found"

#         with data_lock:
#             current_state[i] = movie  # Update the current state

#         if "youtube.com" in trailer_url:
#             success_count += 1
#         else:
#             failure_count += 1

#     return success_count, failure_count


# # Example usage:
# trailer = "E:/movie_website/BACKEND/data_automation/trailer.csv"
# run = int(input("Enter the number of movies to process: "))  # Define run here

# # Start listening for the Enter key press
# threading.Thread(target=listen_for_stop).start()

# # Process trailers with 4 threads
# process_trailers(trailer, run, num_threads=4)

# implementing 1 crome window and 5 tab multi threading

import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the CSV file containing movie titles
csv_file_path = r"E:/movie_website/BACKEND/data_automation/Youtube_trailer/trailer.csv"

# Initialize the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--start-minimized")  # Start Chrome in minimized mode
driver = webdriver.Chrome(options=options)

# Open the CSV file and read the movie titles
movie_data = []
with open(csv_file_path, "r") as file:
    reader = csv.reader(file)
    headers = next(reader)  # Read the header row
    movie_data = list(reader)  # Read the movie titles

# Take input for the number of movies to process
num_movies = int(input("Enter the number of movies to process: "))

# Batch size for saving data
batch_size = 20  # Adjust this value as per your preference

try:
    # Update the movie data with trailer URLs
    for i in range(num_movies):
        row = movie_data[i]
        movie_title = row[0]  # Assuming movie titles are in the first column

        # Open a new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])

        # Navigate to the YouTube search page
        driver.get(
            f"https://www.youtube.com/results?search_query={movie_title}+trailer"
        )

        try:
            # Wait for the first video element to be present
            wait = WebDriverWait(driver, 10)
            video_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a#video-title"))
            )

            # Extract the trailer URL
            trailer_url = video_element.get_attribute("href")

            # Add the trailer URL to the movie data
            row.append(trailer_url)
            row.append("Found")
            print(f"Movie: {movie_title}, Trailer URL: {trailer_url}")

        except Exception as e:
            print(f"Error occurred while processing '{movie_title}': {e}")
            row.append("")  # Add an empty trailer URL for failed movies
            row.append("Not Found")

        # Close the current tab
        driver.close()

        # Switch back to the main window
        driver.switch_to.window(driver.window_handles[0])

        # Save data after processing a batch
        if (i + 1) % batch_size == 0:
            with open(csv_file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    headers + ["Trailer URL", "Status"]
                )  # Write the header row with additional columns
                writer.writerows(movie_data)  # Write the updated movie data
            print(f"Processed {i + 1} movies. Data saved.")

except KeyboardInterrupt:
    print("\nScript interrupted. Saving fetched data...")

    # Write the updated movie data to the original CSV file
    with open(csv_file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            headers + ["Trailer URL", "Status"]
        )  # Write the header row with additional columns
        writer.writerows(movie_data)  # Write the updated movie data

    print("Data saved successfully.")

# Write the updated movie data to the original CSV file
with open(csv_file_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        headers + ["Trailer URL", "Status"]
    )  # Write the header row with additional columns
    writer.writerows(movie_data)  # Write the updated movie data

# Close the browser
driver.quit()
