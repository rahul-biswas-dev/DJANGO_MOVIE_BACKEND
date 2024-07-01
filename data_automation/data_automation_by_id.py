import csv
import requests


# Function to check if a movie exists in the database
def movie_exists_in_database(imdb_id, base_url):
    url = f"{base_url}h/check/{imdb_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["exists"], data.get("title", "Unknown Title")
        else:
            print(
                f"Failed to check movie existence for: {imdb_id} - Status Code: {response.status_code}"
            )
            return False, None
    except requests.exceptions.RequestException as e:
        print(f"Error checking movie existence for: {imdb_id} - {e}")
        return False, None


# Function to fetch and store movie data
def fetch_movie_data(imdb_id, base_url):
    url = f"{base_url}f/fetch/{imdb_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("title", "Unknown Title")
        else:
            print(
                f"Failed to fetch movie data for: {imdb_id} - Status Code: {response.status_code}"
            )
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie data for: {imdb_id} - {e}")
        return None


# Function to read IMDb IDs from CSV file
def read_imdb_ids_from_csv(file_path):
    imdb_ids = []
    with open(file_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the headers
        for row in reader:
            imdb_ids.append(row)
    return headers, imdb_ids


# Function to write results back to the original CSV file
def write_results_to_csv(file_path, headers, rows):
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)


# Main function to process IMDb IDs
def process_imdb_ids(input_file_path, base_url, num_times):
    headers, imdb_rows = read_imdb_ids_from_csv(input_file_path)
    if "Comment" not in headers:
        headers.append("Comment")

    fetched_count = 0
    already_in_database_count = 0
    failed_to_fetch_count = 0

    for i, row in enumerate(imdb_rows[:num_times]):
        imdb_id = row[0]
        exists, title = movie_exists_in_database(imdb_id, base_url)
        if exists:
            print(f"Movie '{title}' is already in the database.")
            row.append("movie is in database")
            already_in_database_count += 1
        else:
            fetched_title = fetch_movie_data(imdb_id, base_url)
            if fetched_title:
                print(f"Movie '{fetched_title}' was fetched and saved.")
                row.append("movie was fetched and saved")
                fetched_count +=1
            else:
                print(f"Failed to fetch movie for IMDb ID: {imdb_id}")
                row.append("failed to fetch movie")
                failed_to_fetch_count += 1

    # Write the results back to the input CSV file
    write_results_to_csv(input_file_path, headers, imdb_rows)

    # Print summary
    print(f"\nSummary:")
    print(f"Movies fetched and saved: {fetched_count}")
    print(f"Movies already in database: {already_in_database_count}")
    print(f"Movies failed to fetch: {failed_to_fetch_count}")


if __name__ == "__main__":
    # Base URL of your Django server
    base_url = "http://127.0.0.1:8000/"

    # Path to CSV file containing IMDb IDs
    input_csv_file_path = r"E:/movie_website/BACKEND/data_automation/title.csv"

    # Take input for the number of movies to process
    num_times = int(input("Enter the number of IMDb IDs to process: "))

    # Process the IMDb IDs
    process_imdb_ids(input_csv_file_path, base_url, num_times)
