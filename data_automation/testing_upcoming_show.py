import requests
from datetime import datetime

# Replace with your actual Trakt.tv API client_id and access_token
API_KEY = "55d0518bc73494065097f51bac63426c1f756e6eb34f998c7da138b7bb88aa3d"
ACCESS_TOKEN = "879c932f6d18c059684183b662e1cbbaa31719bee69598c785e3fcc605c13d74"  # Obtained from the previous step

# Trakt.tv API base URL and endpoint for upcoming shows
BASE_URL = "https://api.trakt.tv"
ENDPOINT = "/calendars/all/shows/{start_date}/{days}"  # Corrected endpoint

# Parameters
start_date = datetime.now().strftime("%Y-%m-%d")  # Today's date in correct format
days = 7  # Number of days to fetch upcoming shows for

# Construct the API URL
url = BASE_URL + ENDPOINT.format(start_date=start_date, days=days)

# Set up the headers
headers = {
    "Content-Type": "application/json",
    "trakt-api-key": API_KEY,
    "trakt-api-version": "2",
    "Authorization": f"Bearer {ACCESS_TOKEN}",  # OAuth token for authenticated requests
}

try:
    # Make the request
    response = requests.get(url, headers=headers)
    print(response.json())

except requests.exceptions.RequestException as e:
    print(f"Error fetching upcoming shows: {e}")

   