import csv
import requests
import signal
import sys

batch_size = 10


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
    with open(file_path, "r", newline="", encoding="ISO-8859-1") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the headers
        for row in reader:
            imdb_ids.append(row)
    return headers, imdb_ids


# Function to write results back to the original CSV file
def write_results_to_csv(file_path, headers, rows):
    with open(file_path, "w", newline="", encoding="ISO-8859-1") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)


def signal_handler(signal, frame):
    print("\nKeyboard interrupt detected. Exiting gracefully...")
    sys.exit(0)


def movie_exists_in_database(imdb_id, base_url):
    url = f"{base_url}h/check/{imdb_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["exists"], data.get("title")
        else:
            print(
                f"Failed to check movie existence for: {imdb_id} - Status Code: {response.status_code}"
            )
            return False, None
    except requests.exceptions.RequestException as e:
        print(f"Error checking movie existence for: {imdb_id} - {e}")
        return False, None


# Main function to process IMDb IDs
def process_imdb_ids(input_file_path, base_url, num_times):
    headers, imdb_rows = read_imdb_ids_from_csv(input_file_path)
    if "Comment" not in headers:
        headers.append("Comment")

    fetched_count = 0
    already_in_database_count = 0
    failed_to_fetch_count = 0

    signal.signal(signal.SIGINT, signal_handler)

    try:
        for i, row in enumerate(imdb_rows[:num_times]):
            imdb_id = row[0]
            movie_title = row[1]

            exists, title = movie_exists_in_database(imdb_id, base_url)
            if exists:
                print(f"Movie '{imdb_id} {title}' already exists in the database.")
                comment = "already exists in database"
                already_in_database_count += 1
            else:
                fetched_title = fetch_movie_data(imdb_id, base_url)
                if fetched_title:
                    print(f"Movie '{imdb_id} {movie_title}' was fetched and saved.")
                    comment = "movie was fetched and saved"
                    fetched_count += 1
                else:
                    print(
                        f"Failed to fetch movie '{imdb_id} {movie_title}' for IMDb ID: {imdb_id}"
                    )
                    comment = "failed to fetch movie"
                    failed_to_fetch_count += 1

            if len(row) > 3:
                row[2] = comment
            else:
                row.append(comment)

            if (i + 1) % batch_size == 0 or i == num_times - 1:
                write_results_to_csv(input_file_path, headers, imdb_rows)
                print(f"Data saved after processing {i + 1} movies.")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Saving data and exiting gracefully...")
    finally:
        write_results_to_csv(input_file_path, headers, imdb_rows)
        print(f"\nSummary:")
        print(f"Movies already in database: {already_in_database_count}")
        print(f"Movies fetched and saved: {fetched_count}")
        print(f"Movies failed to fetch: {failed_to_fetch_count}")
        sys.exit(0)


if __name__ == "__main__":
    # Base URL of your Django server
    base_url = "http://127.0.0.1:8000/"

    # Path to CSV file containing IMDb IDs
    input_csv_file_path = r"E:/movie_website/MOVIE_BACKEND_DJANGO/data_automation/fetch_movie_automation/imdb_data.csv"

    # Take input for the number of movies to process
    num_times = int(input("Enter the number of IMDb IDs to process: "))

    # Process the IMDb IDs
    process_imdb_ids(input_csv_file_path, base_url, num_times)
