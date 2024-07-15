import csv
import requests

# Your TMDb API key
api_key = "21b13c128bd411a0c38bb67b5702fb00"
# Path to the CSV file containing IMDb IDs
csv_file_path = r"E:/movie_website/MOVIE_BACKEND_DJANGO/data_automation/logo/logo.csv"


def logo(imdb_id):
    url = f"https://api.themoviedb.org/3/movie/{imdb_id}/images?api_key={api_key}"
    response = requests.get(url)

    try:
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        for logo in response.json()["logos"]:
            if logo:  # ["iso_639_1"] == "en"
                logo_url = f"https://image.tmdb.org/t/p/original{logo['file_path']}"
                return logo_url
            else:
                print("No English logo found.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching logo for IMDb ID {imdb_id}: {e}")
    except (KeyError, ValueError):
        print(f"Error parsing response for IMDb ID {imdb_id}")

    return None


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
        writer.writerow(headers + ["logo URLs", "Status"])
        writer.writerows(rows)


def process_imdb_ids(num_times):
    headers, imdb_rows = read_imdb_ids_from_csv()

    for i, row in enumerate(imdb_rows[:num_times]):
        imdb_id = row[0]
        if imdb_id:
            logo_url = logo(imdb_id)
            if logo_url:
                row.append(logo_url)
                row.append("Found")
                print(f"IMDb ID: {imdb_id}, logo URL: {logo_url}")
            else:
                row.append("")
                row.append("Not Found")
                print(f"IMDb ID: {imdb_id}, No logos found")
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
