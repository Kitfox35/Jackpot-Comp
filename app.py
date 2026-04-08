from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, session
from ebay_api import search_prices

app = Flask(__name__)
app.secret_key = "rigradar-dev-key" # Note to self: change this to something random before deploying
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

    # Try real API first, fall back to hardcoded data
    api_results = search_prices(query)

# Build labeled listings
    listings = []
    prices = [item["price"] for item in api_results]
    avg = round(sum(prices) / len(prices), 2)
    low = min(prices)
    high = max(prices)
    trend = get_trend(prices)
    
    for item in api_results :
        price = item["price"]
        if price < avg:
            label = "Good Deal"
        elif price > avg:
            label = "Overpriced"
        else:
            label = "Fair"
        listings.append({
        "price": price,
        "label": label,
        "title": item.get("title", "Unknown"),
        "url": item.get("url", "#")
    })






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

    # Initialize history list if first visit
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        result = get_price_data(query)

        # Only save to history if it was a valid search
        if not result.get("error") and query:
            history = session["history"]

            # Remove duplicate if it already exists
            if query.lower() in history:
                history.remove(query.lower())

            # Add to front of list, keep max 5
            history.insert(0, query.lower())
            session["history"] = history[:5]
            session.modified = True

    return render_template("index.html", result=result, query=query, history=session["history"])

@app.route("/compare", methods=["GET", "POST"])
def compare():
    print("COMPARE ROUTE HIT")
    result_a = {}
    result_b = {}
    query_a = ""
    query_b = ""
    winner = None

    if request.method == "POST":
        query_a = request.form.get("query_a", "").strip()
        query_b = request.form.get("query_b", "").strip()

        if query_a:
            result_a = get_price_data(query_a)
        if query_b:
            result_b = get_price_data(query_b)

        if result_a.get("avg") and result_b.get("avg"):
            if result_a["avg"] < result_b["avg"]:
                winner = "a"
            elif result_b["avg"] < result_a["avg"]:
                winner = "b"
            else:
                winner = "tie"
# TEMP FOR TESTIING
    print(f"query_a={query_a}, query_b={query_b}")
    
    
    return render_template("compare.html",
        result_a=result_a, result_b=result_b,
        query_a=query_a, query_b=query_b,
        winner=winner
    )









if __name__ == "__main__":
    app.run(debug=True)
    