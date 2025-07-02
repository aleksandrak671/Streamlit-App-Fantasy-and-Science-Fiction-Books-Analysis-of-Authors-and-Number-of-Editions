import requests

def load_books_json():
    # fantasy
    url_fantasy = 'https://openlibrary.org/subjects/fantasy.json?limit=1000'
    response_fantasy = requests.get(url_fantasy)
    fantasy_data = response_fantasy.json().get("works", []) if response_fantasy.status_code == 200 else []

    # science fiction
    url_scifi = 'https://openlibrary.org/subjects/science_fiction.json?limit=1000'
    response_scifi = requests.get(url_scifi)
    scifi_data = response_scifi.json().get("works", []) if response_scifi.status_code == 200 else []

    return fantasy_data, scifi_data
