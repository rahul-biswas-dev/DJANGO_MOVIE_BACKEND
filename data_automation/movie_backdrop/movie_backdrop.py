import requests

# # Your TMDb API key


# # Function to find a movie by IMDb ID and get its TMDb ID
# def find_movie_by_imdb_id(imdb_id):
#     find_url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&external_source=imdb_id"
#     response = requests.get(find_url)
#     data = response.json()

#     if data["movie_results"]:
#         tmdb_id = data["movie_results"][0]["id"]
#         print(f"Found TMDb ID {tmdb_id} for IMDb ID {imdb_id}")
#         return tmdb_id

#     else:
#         print(f"No results found for IMDb ID {imdb_id}")
#         return None


# # Function to get up to 5 4K backdrop URLs for a movie by TMDb ID
# def get_4k_backdrop_urls_by_tmdb_id(tmdb_id):
#     images_url = (
#         f"https://api.themoviedb.org/3/movie/{tmdb_id}/images?api_key={api_key}"
#     )
#     response = requests.get(images_url)
#     data = response.json()

#     urls = []
#     count = 0

#     for backdrop in data["backdrops"]:
#         if count >= 5:
#             break

#         width = backdrop["width"]
#         height = backdrop["height"]
#         file_path = backdrop["file_path"]
#         urls.append(f"https://image.tmdb.org/t/p/original{file_path}")

#         if width >= 3840 and height >= 2160:
#             urls.append(f"https://image.tmdb.org/t/p/original{file_path}")
#             count += 1
#         elif width >= 1920 and height >= 1080:
#             urls.append(f"https://image.tmdb.org/t/p/original{file_path}")
#             count += 1
#         else:
#             if count == 0:
#                 urls.append(f"https://image.tmdb.org/t/p/original{file_path}")
#                 count += 1

#     return urls


# # Example usage
# tmdb_id = find_movie_by_imdb_id(imdb_id)
# if tmdb_id:
#     print(f"TMDb ID for IMDb ID {imdb_id} is {tmdb_id}")
#     backdrop_urls = get_4k_backdrop_urls_by_tmdb_id(tmdb_id)
#     if backdrop_urls:
#         print("4K Backdrop URLs:")
#         for url in backdrop_urls:
#             print(url)
#     else:
#         print("No 4K backdrops found for this movie")

api_key = "864652493e0d189c6fa554212812c137"
imdb_id = "tt11389872"  # Replace with your desired IMDb ID (e.g., Inception)


def fetch_movie_backdrop(imdb_id, key):
    url = f"https://api.themoviedb.org/3/movie/{imdb_id}/images?api_key={key}"

    response = requests.get(url)
    urls = []
    count = 0

    for backdrop in response.json()["backdrops"]:
        if count >= 5:
            break

        width = backdrop["width"]
        height = backdrop["height"]
        file_path = backdrop["file_path"]
        iso_639_1 = backdrop["iso_639_1"]
        urls.append(f"https://image.tmdb.org/t/p/original{file_path}")

        if width >= 3840 and height >= 2160:
            urls.append(f"https://image.tmdb.org/t/p/original{file_path}")
            count += 1
        elif width >= 1920 and height >= 1080:
            urls.append(f"https://image.tmdb.org/t/p/original{file_path}")
            count += 1
        else:
            urls.append(f"https://image.tmdb.org/t/p/original{file_path}")
            count += 1

    return urls[0]



print(fetch_movie_backdrop("tt11389872", api_key))
