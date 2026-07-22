from flask import Flask, render_template, request

app = Flask(__name__)

# Very simple, hard-coded exchange rates
RATES = {
    "USD": {"GBP": 0.79, "EUR": 0.92},
    "GBP": {"USD": 1.27, "EUR": 1.16},
    "EUR": {"USD": 1.09, "GBP": 0.86}
}


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        amount = request.form.get("amount", "")
        from_currency = request.form.get("from_currency")
        to_currency = request.form.get("to_currency")

        # Bug fix (a): empty input previously crashed float("")
        if not amount or not amount.strip():
            error = "Please enter an amount."
        else:
            # Bug fix (b): non-numeric input previously crashed float("abc")
            try:
                amount = float(amount)
            except ValueError:
                error = "Please enter a valid number."
            else:
                if from_currency == to_currency:
                    # Same currency: no lookup needed (RATES has no USD->USD entry)
                    result = round(amount, 2)
                else:
                    rate = RATES[from_currency][to_currency]
                    # Round to 2 dp to avoid floating point artefacts in output
                    result = round(amount * rate, 2)

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
