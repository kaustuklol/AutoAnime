import requests

def fetch_anime_info(name):
    # Set up the API endpoint and query
    url = 'https://graphql.anilist.co'
    query = '''
    query ($name: String, $page: Int, $perPage: Int) {
      Page (page: $page, perPage: $perPage) {
        media (search: $name, type: ANIME) {
          id
          title {
            english
            romaji
          }
          genres
          episodes
          status
          studios {
            nodes {
              name
            }
          }
          nextAiringEpisode {
            episode
            timeUntilAiring
          }
        }
      }
    }
    '''

    # Set the variables for the query
    variables = {
        'name': name,
        'page': 1,
        'perPage': 1
    }

    # Make the API request
    response = requests.post(url, json={'query': query, 'variables': variables})

    # Extract the relevant data from the response
    data = response.json()['data']['Page']['media'][0]
    title_english = data['title']['english']
    title_romaji = data['title']['romaji']
    studio = data['studios']['nodes'][0]['name']
    latest_episode = data['nextAiringEpisode']['episode'] if data['nextAiringEpisode'] else None
    # genres = 
    genres = (data['genres'])
    status = data['status']

    if latest_episode>1:
        latest_episode = latest_episode-1
    # Create a dictionary containing the requested information
    anime_info = {
        'title_english': title_english,
        'title_romaji': title_romaji,
        'studio': studio,
        'latest_episode': latest_episode,
        'genres': genres,
        'status': status
    }

    return anime_info

# print(fetch_anime_info("detective conan"))