import requests

def anime_url(api_key, anime, ep):
    base = "https://api.techzbots.live"
    link = ""
    # Getting anime_id by name
    try:
        data = requests.get(
                    f"{base}/gogo/search/?query={anime}&api_key={api_key}"
                ).json()
        anime_id = data['results'][0]['id']


    except Exception as e:
        print(f"Anime Search Failed due to this error: {e}")
        print(data['results'])
        return e

    try:
        # Getting anime by id
        data = requests.get(
                    f"{base}/gogo/episode/?id={anime_id}-episode-{ep}&api_key={api_key}"
                ).json()
        link = data['results']['DL']['SUB']['720p']
        # print(anime_id)
    except Exception as e:
        print(f"Link using: {base}/gogo/episode/?id={anime_id}-episode-{ep}&api_key={api_key}")
        print(f"Extracting links Failed due to this error: {e}")
        return e
    return link
# print(anime_url("UBDVXP", "rdie Wing Golf Girls Story", "2"))