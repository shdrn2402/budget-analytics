import json
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
ACCESS_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.exchangerate.host/timeframe"
CURRENCY_PAIR = "ILS,%20USD"
OUTPUT_PATH = "../data/exchange_rates_2023_2025.json"
REQUEST_TIMEOUT = 10  # seconds
REQUEST_PAUSE = 1.5   # seconds


def build_query(start_date, end_date):
    return (
        f"{BASE_URL}?access_key={ACCESS_KEY}"
        f"&currencies={CURRENCY_PAIR}&start_date={start_date}&end_date={end_date}"
    )


def fetch_exchange_rates(start_1, end_1, start_2, end_2):
    url1 = build_query(start_1, end_1)
    response = requests.get(url1, timeout=REQUEST_TIMEOUT)
    if response.status_code != 200:
        raise Exception(f"First request failed with status code: {response.status_code}")
    first_year_data = response.json()

    time.sleep(REQUEST_PAUSE)

    url2 = build_query(start_2, end_2)
    response = requests.get(url2, timeout=REQUEST_TIMEOUT)
    if response.status_code != 200:
        raise Exception(f"Second request failed with status code: {response.status_code}")
    second_year_data = response.json()

    return first_year_data, second_year_data


def save_exchange_rates_to_file():
    first, second = fetch_exchange_rates(
        "2023-06-01", "2024-05-31", "2024-06-01", "2025-05-31"
    )

    # Merge quotes from both years into one flat dictionary
    merged_quotes = {**first["quotes"], **second["quotes"]}

    # Save only merged date→rate mapping
    with open(OUTPUT_PATH, "w") as f:
        json.dump(merged_quotes, f, indent=2)


if __name__ == "__main__":
    save_exchange_rates_to_file()
    print("Exchange rates saved successfully.")


# import json
# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# ACCESS_KEY = os.getenv("EXCHANGE_API_KEY")

# first_year_query = (
#     f"https://api.exchangerate.host/timeframe?access_key={ACCESS_KEY}"
#     "&currencies=ILS,%20USD&start_date=2023-06-01&end_date=2024-05-31"
# )

# second_year_query = (
#     f"https://api.exchangerate.host/timeframe?access_key={ACCESS_KEY}"
#     "&currencies=ILS,%20USD&start_date=2024-06-01&end_date=2025-05-31"
# )


# def fetch_exchange_rates():
#     response = requests.get(first_year_query)
#     if response.status_code != 200:
#         raise Exception("Failed to fetch exchange rates for the first year")
    
#     first_year_data = response.json()

#     response = requests.get(second_year_query)
#     if response.status_code != 200:
#         raise Exception("Failed to fetch exchange rates for the second year")
    
#     second_year_data = response.json()

#     return first_year_data, second_year_data

# def save_exchange_rates_to_file():
#     first, second = fetch_exchange_rates()

#     with open("../data/exchange_rates_2023_2025.json", "w") as f:
#         json.dump({"first_year": first, "second_year": second}, f, indent=2)


# if __name__ == "__main__":
#     save_exchange_rates_to_file()
#     print("Exchange rates saved successfully.")