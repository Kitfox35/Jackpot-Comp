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

def get_price_data(query):
    """Return prices and average for a given hardware inquiry."""
    query = query.strip().lower()

    if not query:
        return{"error" : "Please enter a search term."}
    prices = HARDWARE_PRICES.get(query)
    if prices is None:
        suggestions = ",".join(
            k.upper() for k in list(HARDWARE_PRICES.keys()) [:4]
        )
        return{"error": f'No results for "{query}". Try: {suggestions}'}
    
    avg =round(sum(prices) / len (prices), 2)
    low = min(prices)
    high = max(prices)
    
    return {
        "prices": prices,
        "avg": avg,
        "low": low,
        "high": high,
        "error": None,
    }

# --- Routes ---

@app.route("/", methods=["GET", "POST"])
def home():
    result = {}
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "")
        prices, avg, error = get_price_data(query)

    return render_template("index.html", prices=prices, avg=avg, error=error,query=query)

if __name__ == "__main__":
    app.run(debug=True)
    