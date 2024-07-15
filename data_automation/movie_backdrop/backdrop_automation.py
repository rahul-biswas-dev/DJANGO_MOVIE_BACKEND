import csv
import requests
from typing import List
import time

# Your TMDb API key
api_key = "21b13c128bd411a0c38bb67b5702fb00"

# Path to the CSV file containing IMDb IDs
csv_file_path = (
    r"E:/movie_website/MOVIE_BACKEND_DJANGO/data_automation/movie_backdrop/backdrop.csv"
)


# Function to find a movie by IMDb ID and get its TMDb ID
def find_movie_by_imdb_id(imdb_id):
    find_url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&external_source=imdb_id"
    response = requests.get(find_url)
    time.sleep(2)
    data = response.json()

    if data["movie_results"]:
        tmdb_id = data["movie_results"][0]["id"]
        return tmdb_id
    else:
        print(f"No results found for IMDb ID {imdb_id}")
        return None


# Function to get 4K or 1080p backdrop URLs for a movie by TMDb ID
def get_backdrop_urls_by_tmdb_id(tmdb_id) -> List[str]:
    images_url = (
        f"https://api.themoviedb.org/3/movie/{tmdb_id}/images?api_key={api_key}"
    )
    response = requests.get(images_url)
    time.sleep(2)
    data = response.json()

    urls = []
    count = 0

    for backdrop in data["backdrops"]:
        if count >= 1:
            break

        width = backdrop["width"]
        height = backdrop["height"]
        file_path = backdrop["file_path"]

        if width >= 3840 and height >= 2160:
            urls.append(f"https://image.tmdb.org/t/p/original{file_path}")
            count += 1
        else :
            if count == 0:
                urls.append(f"https://image.tmdb.org/t/p/original{file_path}")
            count += 1

    if len(urls) > 1:
        return [urls[1]]  # Return the second URL
    elif len(urls) == 1:
        return urls
    else:
        return []


# Function to read IMDb IDs from CSV file
def read_imdb_ids_from_csv():
    imdb_ids = []
    with open(csv_file_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the headers
        for row in reader:
            imdb_ids.append(row)
    return headers, imdb_ids


# Function to write results back to the original CSV file
def write_results_to_csv(headers, rows):
    with open(csv_file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers + ["Backdrop URLs", "Status"])
        writer.writerows(rows)


# Main function to process IMDb IDs
def process_imdb_ids(num_times):
    headers, imdb_rows = read_imdb_ids_from_csv()

    for i, row in enumerate(imdb_rows[:num_times]):
        imdb_id = row[0]
        tmdb_id = find_movie_by_imdb_id(imdb_id)
        if tmdb_id:
            backdrop_urls = get_backdrop_urls_by_tmdb_id(tmdb_id)
            if backdrop_urls:
                row.append(", ".join(backdrop_urls))
                row.append("Found")
                print(f"IMDb ID: {imdb_id}, Backdrop URLs: {', '.join(backdrop_urls)}")
            else:
                row.append("")
                row.append("Not Found")
                print(f"IMDb ID: {imdb_id}, No backdrops found")
        else:
            row.append("")
            row.append("Not Found")
            print(f"IMDb ID: {imdb_id}, No TMDb ID found")

        # Save data after processing a batch
        if (i + 1) % 10 == 0:
            write_results_to_csv(headers, imdb_rows)
            print(f"Processed {i + 1} IMDb IDs. Data saved.")

    # Write the final results to the CSV file
    write_results_to_csv(headers, imdb_rows)


if __name__ == "__main__":
    try:
        # Take input for the number of movies to process
        num_times = int(input("Enter the number of IMDb IDs to process: "))

        # Process the IMDb IDs
        process_imdb_ids(num_times)
    except KeyboardInterrupt:
        print("\nScript interrupted. Saving fetched data...")
        headers, imdb_rows = read_imdb_ids_from_csv()
        write_results_to_csv(headers, imdb_rows)
        print("Data saved successfully.")
