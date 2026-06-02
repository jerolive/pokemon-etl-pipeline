import requests
import pandas as pd
import numpy as np

API_URL = "https://pokeapi.co/api/v2/pokemon?limit=151"


# ========== EXTRACT ==========

pokemon_details = []

try:
    # Fetch initial list of pokemon
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()
    initial_pokemon_data = response.json()["results"]

    print("Success! Initial results received. Fetching details...")

    # Open a session to batch perform all individual requests
    session = requests.Session()

    for pokemon in initial_pokemon_data:
        try:
            # Fetch individual pokemon details
            detail_response = session.get(pokemon["url"], timeout=5)
            detail_response.raise_for_status()
            detail_data = detail_response.json()
            
            # Results stored as dicts for pandas
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

# Handles initial fetch failures
except requests.exceptions.RequestException as err:
    print(f"An unexpected error occurred during initial fetch: {err}")


# ========== TRANSFORM ==========

if len(pokemon_details) > 0:

    bmi_df = pd.DataFrame(pokemon_details)

    # Convert to Meters and Kilograms
    bmi_df["height"] = bmi_df["height"] / 10
    bmi_df["weight"] = bmi_df["weight"] / 10

    # BMI Formula: Weight/Height^2
    bmi_df["bmi"] = bmi_df["weight"] / (bmi_df["height"] ** 2)
    bmi_df["bmi"] = bmi_df["bmi"].round(2)

    # BMI Classification
    classification_bins = [0, 18.5, 25, 30, 35, 40, np.inf]
    classification_labels = [
        'Underweight',
        'Normal Weight',
        'Overweight',
        'Obese Class I',
        'Obese Class II',
        'Obese Class III'
    ]

    bmi_df["bmi_class"] = pd.cut(bmi_df["bmi"], bins=classification_bins, labels=classification_labels, right=False)

    print(bmi_df)

else:
    print("Skipping Transform step: No data was extracted.")
