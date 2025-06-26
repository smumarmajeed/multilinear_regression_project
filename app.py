from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        x1 = list(map(float, request.form['x1'].split(',')))
        x2 = list(map(float, request.form['x2'].split(',')))
        y = list(map(float, request.form['y'].split(',')))

        n = len(y)
        steps = []

        # Sums
        sum_x1 = sum(x1)
        sum_x2 = sum(x2)
        sum_y = sum(y)
        sum_x1x1 = sum([v**2 for v in x1])
        sum_x2x2 = sum([v**2 for v in x2])
        sum_x1x2 = sum([x1[i] * x2[i] for i in range(n)])
        sum_x1y = sum([x1[i] * y[i] for i in range(n)])
        sum_x2y = sum([x2[i] * y[i] for i in range(n)])

        steps.append(f"∑x1 = {sum_x1}, ∑x2 = {sum_x2}, ∑y = {sum_y}")
        steps.append(f"∑x1² = {sum_x1x1}, ∑x2² = {sum_x2x2}, ∑x1·x2 = {sum_x1x2}")
        steps.append(f"∑x1·y = {sum_x1y}, ∑x2·y = {sum_x2y}")

        # Solve system
        a11 = sum_x1x1
        a12 = sum_x1x2
        a21 = sum_x1x2
        a22 = sum_x2x2
        c1 = sum_x1y
        c2 = sum_x2y

        D = a11 * a22 - a12 * a21
        D1 = c1 * a22 - c2 * a12
        D2 = a11 * c2 - a21 * c1

        b1 = D1 / D
        b2 = D2 / D

        steps.append(f"Solve system:")
        steps.append(f"{a11:.2f}·b1 + {a12:.2f}·b2 = {c1:.2f}")
        steps.append(f"{a21:.2f}·b1 + {a22:.2f}·b2 = {c2:.2f}")
        steps.append(f"Determinant D = {D}, D1 = {D1}, D2 = {D2}")
        steps.append(f"b1 = {b1:.4f}, b2 = {b2:.4f}")
        steps.append(f"Final Equation: y = {b1:.4f}·x1 + {b2:.4f}·x2")

        # Predicted Y values
        predicted_y = [b1 * x1[i] + b2 * x2[i] for i in range(n)]
        steps.append("📊 Predicted Y values:")
        for i in range(n):
            steps.append(f"y{i+1}′ = {b1:.4f} * {x1[i]} + {b2:.4f} * {x2[i]} = {predicted_y[i]:.4f}")

        # For graph
        X_vals = [[x1[i], x2[i]] for i in range(n)]
        Y_vals = y
        result = [b1, b2]

        return render_template("calculate.html", result=result, steps=steps, X_vals=X_vals, Y_vals=Y_vals, predicted_y=predicted_y)

    return render_template("calculate.html")




if __name__ == '__main__':
    app.run(debug=True)
