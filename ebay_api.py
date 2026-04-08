import requests
import base64
import time

# ---  eBay credentials ---

import os

APP_ID = os.environ.get("EBAY_APP_ID")
CERT_ID = os.environ.get("EBAY_CERT_ID")

# --- Results cache ---
_results_cache = {}
CACHE_DURATION = 30 * 60 # 30 minutes in seconds


# --- Token cache (so we don't fetch a new token every search) ---
_token_cache = {
    "token": None,
    "expires_at": 0
}

def get_access_token():
    """Fetch a new OAuth token, or return the cached one if still valid."""
    now = time.time()

    if _token_cache["token"] and now < _token_cache["expires_at"]:
        return _token_cache["token"]

    # Base64 encode "APP_ID:CERT_ID"
    credentials = f"{APP_ID}:{CERT_ID}"
    encoded = base64.b64encode(credentials.encode()).decode()

    response = requests.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded}"
        },
        data={
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }
    )

    data = response.json()
    token = data["access_token"]

    # Cache it for slightly less than 2 hours to be safe
    _token_cache["token"] = token
    _token_cache["expires_at"] = now + data["expires_in"] - 60

    return token


def search_prices(query, limit=10):
    """
    Search eBay for a hardware item and return a list of prices.
    Returns cached results if the same query was made within 30 minutes.

    """
    cache_key = query.strip().lower()
    now = time.time()
     
    # Return cached result if still fresh
    if cache_key in _results_cache:
        cached = _results_cache[cache_key]
        if now - cached ["timestamp"] < CACHE_DURATION:
            return cached["data"]

    # Otherwise fetch from eBay
    token = get_access_token()

    response = requests.get(
        "https://api.ebay.com/buy/browse/v1/item_summary/search",
        headers={
            "Authorization": f"Bearer {token}",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
        },
        params={
            "q": query,
            "limit": limit,
            "filter": "buyingOptions:{FIXED_PRICE},conditions:{NEW|USED_EXCELLENT}"
        }
    )

    data = response.json()
    items = data.get("itemSummaries", [])

    results = []
    for item in items:
        price_info = item.get("price", {})
        price = float(price_info.get("value", 0))

        if price > 0:
            results.append({
                "price": price,
                "title": item.get("title", "Unknown"),
                "url": item.get("itemWebUrl", "#")
            })

    return results