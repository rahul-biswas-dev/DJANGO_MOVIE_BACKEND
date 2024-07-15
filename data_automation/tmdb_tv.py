import requests

# Replace with your TMDB API key
TMDB_API_KEY = "864652493e0d189c6fa554212812c137"

# TMDB API base URL
TMDB_BASE_URL = "https://api.themoviedb.org/3"


# Function to fetch episode details from TMDB
def get_episode_details(tmdb_id):
    # Construct the API endpoint URL
    endpoint = f"{TMDB_BASE_URL}/tv/{tmdb_id}"

    # Set the query parameters
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",  # You can change the language if needed
    }

    try:
        # Make the request to the TMDB API
        response = requests.get(endpoint, params=params)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Extract the episode details
        episode_name = data["name"]
        episode_overview = data["overview"]
        episode_rating = data["vote_average"]

        # Return the episode details
        return {
            "name": episode_name,
            "overview": episode_overview,
            "rating": episode_rating,
            "data": data,
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching episode details: {e}")
        return None


# Example usage
tmdb_id = 257646  # Replace with the actual TMDB ID

episode_details = get_episode_details(tmdb_id)
print(episode_details)
