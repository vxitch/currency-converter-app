from flask import Flask, render_template, request

app = Flask(__name__)

# Very simple, hard‑coded exchange rates
RATES = {
    "USD": {"GBP": 0.79, "EUR": 0.92},
    "GBP": {"USD": 1.27, "EUR": 1.16},
    "EUR": {"USD": 1.09, "GBP": 0.86}
}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        amount = request.form.get("amount")
        from_currency = request.form.get("from_currency")
        to_currency = request.form.get("to_currency")

       
        # Convert entered amount to float .
        amount = float(amount) 
	
	# Convert currency
        rate = RATES[from_currency][to_currency]
        result = amount * rate

	# Return result	
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
