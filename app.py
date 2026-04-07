from flask import Flask, render_template, request

app = Flask(__name__)
#--- Data layer ---
# Later, this gets replaced by an API call
HARDWARE_PRICES = {
    "rtx 4070": [520, 550, 500],
    "rtx 4080": [700, 720, 710],
    "rx 7800 xt": [480, 510, 495],
    "rx 7900 xt": [600, 620, 590],
    "i7 12700k": [300, 320, 310],
    "i9 13900k": [550, 580, 560],
    "ryzen 7 7700x": [290, 310, 300],
}

def get_trend(prices):
      
   # Compare first half average vs second half average.
    #Returns 'up', 'down', or 'stable'.
    
    if len(prices) < 2:
        return "stable"

    mid = len(prices) // 2
    first_half = sum(prices[:mid]) / len(prices[:mid])
    second_half = sum(prices[mid:]) / len(prices[mid:])

    if second_half > first_half:
        return "up"
    elif second_half < first_half:
        return "down"
    else:
        return "stable"


def get_price_data(query):
    """Return prices and average for a given hardware inquiry."""
    query = query.strip().lower()

        # Case 1: empty submission
    if not query:
        return {"error": "Enter a GPU or CPU name to get started."}

    if len(query) < 3:
        return {"error": f'"{query}" is too short. Try something like "RTX 4070" of i& 12700k.'}


        # Case 3: no match found — show suggestions

    prices = HARDWARE_PRICES.get(query)

    # Case 3: no match found — show suggestions
    if prices is None:
        suggestions = [k.upper() for k in HARDWARE_PRICES.keys()]
        suggestions_str = ", ".join(suggestions)
        return {"error": f'No results for "{query.upper()}". Available parts: {suggestions_str}'}
    
    avg =round(sum(prices) / len (prices), 2)
    low = min(prices)
    high = max(prices)
    # Build labeled listings
    listings = []
    for price in prices :
        if price < avg:
            label = "Good Deal"
        elif price > avg:
            label = "Overpriced"
        else:
            lavel = "Fair"
        listings.append({"price": price, "label": label})


    trend = get_trend(prices)

    return {
        "listings": listings,  # replaces "prices"
        "avg": avg,
        "low": low,
        "high": high,
        "trend": trend,
        "error": None,
    }

# --- Routes ---

@app.route("/", methods=["GET", "POST"])
def home():
    result = {}
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "")
        result = get_price_data(query)

    return render_template("index.html", result=result, query=query)

if __name__ == "__main__":
    app.run(debug=True)
    