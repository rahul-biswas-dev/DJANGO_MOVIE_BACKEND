import csv
import os

def read_movie_names_from_csv(file_paths):
    movie_names = set()
    for file_path in file_paths:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(full_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                movie_names.update(row)
    return movie_names

def write_unique_movie_names_to_csv(unique_movie_names, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for movie_name in unique_movie_names:
            writer.writerow([movie_name])

if __name__ == "__main__":
    # Paths to the CSV files
    csv_files = ['1.csv', '2.csv', '3.csv', '4.csv']

    # Read movie names from CSV files
    all_movie_names = read_movie_names_from_csv(csv_files)

    # Write unique movie names to a new CSV file
    write_unique_movie_names_to_csv(all_movie_names, 'unique_movie_names.csv')

    print("Unique movie names saved to 'unique_movie_names.csv'.")
