# 🖥️ RigRadar

**Real-time PC hardware price tracker**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-rigradar--p6zk.onrender.com-blue?style=for-the-badge&logo=render)](https://rigradar-p6zk.onrender.com)
[![GitHub](https://img.shields.io/badge/GitHub-Kitfox35%2FJackpot--Comp-181717?style=for-the-badge&logo=github)](https://github.com/Kitfox35/Jackpot-Comp)

---

## 📖 About

RigRadar pulls live listings from the eBay Browse API so you can instantly see what PC parts are actually selling for. Search any component, get real prices, and know right away whether a listing is a good deal or overpriced.

Built as a Hack Club submission and portfolio project. 

---

## ✨ Features

### 🔍 Search & Results
- **Live eBay API data** — real listings, real prices, updated on every search
- **Price insights panel** — average, lowest, and highest price for your query
- **Good Deal / Overpriced labels** on each listing based on market average
- **Price trend indicator** — shows whether prices are trending up, down, or stable
- **Loading animation** while results are fetched

### 🕘 Search History & Autocomplete
- **Session-based search history** displayed as clickable chips — re-run any past search instantly
- **Autocomplete dropdown** with keyboard navigation for common PC parts

### 🔧 Filter & Sort
- Sort results: low to high, high to low
- Filter to show Good Deals only

### 💰 Profit Calculator
- Enter a buy price and sell price
- Get instant profit/loss and a comparison against the current market average

### ⚖️ Compare Mode
- Side-by-side comparison of two different parts
- Winner highlight so you can see which part offers better value at a glance

### ⚡ Performance
- **30-minute API result caching** to minimize eBay API calls and keep the app snappy on the free tier

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Data Source | eBay Browse API |
| Hosting | Render (free tier) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12
- An [eBay Developer account](https://developer.ebay.com/) with a production app — you'll need `EBAY_APP_ID` and `EBAY_CERT_ID`

### Local Setup

**1. Clone the repo**
```bash
git clone https://github.com/Kitfox35/Jackpot-Comp.git
cd Jackpot-Comp
```

**2. Create a `.env` file in the project root**
```
EBAY_APP_ID=your_app_id_here
EBAY_CERT_ID=your_cert_id_here
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
py -3.12 app.py
```

The app will be available at `http://localhost:5000`.

---

## 📁 Project Structure

```
Jackpot-Comp/
├── static/              # CSS, JavaScript, and static assets
├── templates/           # Jinja2 HTML templates
├── app.py               # Flask app — routes and caching logic
├── ebay_api.py          # eBay Browse API wrapper and price analysis
├── requirements.txt     # Python dependencies
├── Procfile             # Render deployment config
└── .gitignore
```

## 👤 Author

Built by Zayd Mohammad — [Kitfox35 on GitHub](https://github.com/Kitfox35).

---

> RigRadar is not affiliated with or endorsed by eBay. All pricing data is fetched live from the eBay Browse API.
