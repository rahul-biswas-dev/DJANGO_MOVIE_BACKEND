import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime


# Path to the CSV file containing IMDb IDs
csv_file_path = (
    r"E:/movie_website/BACKEND/data_automation/movie_date_fix/movie_date.csv"
)

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the CSV file and read the IMDb IDs
imdb_data = []
with open(csv_file_path, "r") as file:
    reader = csv.reader(file)
    headers = next(reader)  # Read the header row
    imdb_data = list(reader)  # Read the IMDb IDs

# Take input for the number of IMDb IDs to process
num_ids = int(input("Enter the number of IMDb IDs to process: "))

# Batch size for saving data
batch_size = 20  # Adjust this value as per your preference

try:
    # Update the IMDb data with release dates
    for i in range(num_ids):
        row = imdb_data[i]
        imdb_id = row[0]  # Assuming IMDb IDs are in the first column

        # Navigate to the release info page
        driver.get(f"https://www.imdb.com/title/{imdb_id}/releaseinfo/")

        try:
            # Wait for the release date element to be present
            wait = WebDriverWait(driver, 10)
            release_date_element = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div[2]/ul/li[1]/div/ul/li/span[1]",
                    )
                )
            )

            # Extract the release date
            release_date_str = release_date_element.text

            # Convert the release date to the desired format
            try:
                release_date = datetime.datetime.strptime(
                    release_date_str, "%B %d, %Y"
                ).strftime("%d-%m-%Y")
            except ValueError:
                try:
                    release_date = datetime.datetime.strptime(
                        release_date_str, "%d-%m-%Y"
                    ).strftime("%d-%m-%Y")
                except ValueError:
                    release_date = ""

            # Add the release date to the IMDb data
            row.append(release_date)
            row.append("Found")
            print(f"IMDb ID: {imdb_id}, Release Date: {release_date}")

        except Exception as e:
            print(f"Error occurred while processing '{imdb_id}': {e}")
            row.append("")  # Add an empty release date for failed movies
            row.append("Not Found")

        # Delay for 2 seconds before the next search
        # time.sleep(2)

        # Save data after processing a batch
        if (i + 1) % batch_size == 0:
            with open(csv_file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    headers + ["Release Date", "Status"]
                )  # Write the header row with additional columns
                writer.writerows(imdb_data)  # Write the updated IMDb data
            print(f"Processed {i + 1} IMDb IDs. Data saved.")

except KeyboardInterrupt:
    print("\nScript interrupted. Saving fetched data...")

    # Write the updated IMDb data to the original CSV file
    with open(csv_file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            headers + ["Release Date", "Status"]
        )  # Write the header row with additional columns
        writer.writerows(imdb_data)  # Write the updated IMDb data

    print("Data saved successfully.")

# Write the updated IMDb data to the original CSV file
with open(csv_file_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        headers + ["Release Date", "Status"]
    )  # Write the header row with additional columns
    writer.writerows(imdb_data)  # Write the updated IMDb data

# Close the browser
driver.quit()
