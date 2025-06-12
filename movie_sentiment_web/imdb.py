import requests

def get_movie_details(movie_title, rapidapi_key):
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }

    url_find = "https://imdb8.p.rapidapi.com/title/find"
    params_find = {"q": movie_title}
    response_find = requests.get(url_find, headers=headers, params=params_find)
    if response_find.status_code != 200:
        print("[FIND ERROR]", response_find.text)
        return {}

    data_find = response_find.json()
    results = data_find.get('results', [])
    if not results:
        print("[NO RESULTS FOUND]")
        return {}

    first_movie = results[0]
    movie_id = first_movie.get('id', '')
    if not movie_id:
        print("[NO MOVIE ID]")
        return {}

    tconst = movie_id.split('/')[-2]

    url_details = "https://imdb8.p.rapidapi.com/title/get-overview-details"
    params_details = {"tconst": tconst, "currentCountry": "US"}
    response_details = requests.get(url_details, headers=headers, params=params_details)
    if response_details.status_code != 200:
        print("[DETAILS ERROR]", response_details.text)
        return {}

    data_details = response_details.json()

    title = data_details.get('title', {}).get('title', movie_title)
    year = data_details.get('title', {}).get('year', '')
    poster = data_details.get('title', {}).get('image', {}).get('url', '')
    plot = (
        data_details.get('plotSummary', {}).get('text') or
        data_details.get('plotOutline', {}).get('text') or
        "No plot available"
    )


    return {
        "title": title,
        "year": year,
        "poster": poster,
        "plot": plot,
    }
