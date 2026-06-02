import requests

API_URL = "https://pokeapi.co/api/v2/pokemon?limit=151"
pokemon_details = []

try:
    # Fetch initial list of pokemon.
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()
    initial_pokemon_data = response.json()["results"]

    print("Success! Initial results received. Fetching details...")

    # Open a session to batch perform all individual requests.
    session = requests.Session()

    for pokemon in initial_pokemon_data:
        try:
            # Fetch individual pokemon details.
            detail_response = session.get(pokemon["url"], timeout=5)
            detail_response.raise_for_status()
            detail_data = detail_response.json()
            
            # Results stored as dicts for pandas.
            pokemon_details.append({
                "name": pokemon["name"],
                "height": detail_data["height"],
                "weight": detail_data["weight"]
            })

        # Allows for individual errors without crashing everything
        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to fetch data for {pokemon['name']}: {e}")
            continue

    print(f"Success! Extracted data for {len(pokemon_details)} Pokemon.")

    print(pokemon_details[:3]) # TEMP (Remove later)

# Handles initial fetch failures
except requests.exceptions.RequestException as err:
    print(f"An unexpected error occurred during initial fetch: {err}")