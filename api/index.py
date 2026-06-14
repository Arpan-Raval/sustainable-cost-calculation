import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template_string, request

from utils import calculate_cloud_cost, estimate_ai_energy, get_platform_comparison

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Sustainable Cloud & AI Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #0f172a; color: #e5eefb; }
    .wrap { max-width: 980px; margin: 0 auto; padding: 20px; }
    .card { background: #111827; border: 1px solid #1f2937; border-radius: 14px; padding: 16px; margin-bottom: 16px; }
    h1, h2 { color: #34d399; }
    label { display: block; margin-top: 8px; font-size: 13px; color: #bfdbfe; }
    input, select { width: 100%; box-sizing: border-box; padding: 8px; border-radius: 8px; border: 1px solid #334155; background: #020617; color: #fff; margin-top: 4px; }
    button { margin-top: 12px; background: #10b981; color: #fff; border: 0; border-radius: 8px; padding: 10px 14px; font-weight: 700; cursor: pointer; }
    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th, td { border-bottom: 1px solid #24364a; padding: 8px; text-align: left; }
    th { color: #bbf7d0; }
    .small { color: #cbd5e1; font-size: 13px; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>Sustainable Cloud & AI Dashboard</h1>
      <p class="small">This is the Vercel deployment entry point for the existing sustainability project.</p>
    </div>

    <div class="card">
      <h2>Cloud Cost Calculator</h2>
      <form method="post">
        <label>Compute Hours</label>
        <input type="number" name="compute_hours" value="{{ compute_hours }}" />
        <label>Hourly Rate ($)</label>
        <input type="number" step="0.0001" name="compute_rate" value="{{ compute_rate }}" />
        <label>Storage (GB)</label>
        <input type="number" name="storage_gb" value="{{ storage_gb }}" />
        <label>Storage Rate ($/GB)</label>
        <input type="number" step="0.0001" name="storage_rate" value="{{ storage_rate }}" />
        <label>Data Transfer (GB)</label>
        <input type="number" name="transfer_gb" value="{{ transfer_gb }}" />
        <label>Transfer Rate ($/GB)</label>
        <input type="number" step="0.0001" name="transfer_rate" value="{{ transfer_rate }}" />
        <button type="submit">Calculate Cost</button>
      </form>
      {% if cloud_total is not none %}
      <p><strong>Total:</strong> ${{ "%.2f"|format(cloud_total) }}</p>
      <table>
        <tr><th>Component</th><th>Cost ($)</th></tr>
        {% for row in breakdown %}
        <tr><td>{{ row['Component'] }}</td><td>{{ "%.2f"|format(row['Cost ($)']) }}</td></tr>
        {% endfor %}
      </table>
      {% endif %}
    </div>

    <div class="card">
      <h2>AI Sustainability Estimate</h2>
      <form method="post">
        <label>Model Scale</label>
        <select name="model_type">
          <option value="Small (e.g., DistilBERT)" {% if model_type=='Small (e.g., DistilBERT)' %}selected{% endif %}>Small</option>
          <option value="Medium (e.g., Llama-7B)" {% if model_type=='Medium (e.g., Llama-7B)' %}selected{% endif %}>Medium</option>
          <option value="Large (e.g., GPT-4)" {% if model_type=='Large (e.g., GPT-4)' %}selected{% endif %}>Large</option>
        </select>
        <label>Tokens (Millions)</label>
        <input type="number" step="0.1" name="tokens_millions" value="{{ tokens_millions }}" />
        <label>Optimization</label>
        <select name="optimization">
          <option value="0" {% if not optimization %}selected{% endif %}>Off</option>
          <option value="1" {% if optimization %}selected{% endif %}>On</option>
        </select>
        <button type="submit">Estimate AI Impact</button>
      </form>
      {% if ai_energy is not none %}
      <p>Energy: {{ "%.4f"|format(ai_energy) }} kWh</p>
      <p>Carbon Footprint: {{ "%.4f"|format(ai_carbon) }} kg CO2</p>
      {% endif %}
    </div>

    <div class="card">
      <h2>Cloud Platform Comparison</h2>
      <table>
        <tr><th>Platform</th><th>Price Index</th><th>Scalability</th><th>Sustainability</th></tr>
        {% for row in comparison %}
        <tr>
          <td>{{ row['Platform'] }}</td>
          <td>{{ row['Base Price Index'] }}</td>
          <td>{{ row['Scalability'] }}</td>
          <td>{{ row['Sustainability Rating'] }}</td>
        </tr>
        {% endfor %}
      </table>
    </div>
  </div>
</body>
</html>
"""


@app.get("/")
def index():
    return render_template_string(
        HTML,
        cloud_total=None,
        breakdown=[],
        ai_energy=None,
        ai_carbon=None,
        model_type="Large (e.g., GPT-4)",
        tokens_millions=1.0,
        optimization=False,
        comparison=get_platform_comparison().to_dict(orient="records"),
        compute_hours=720,
        compute_rate=0.05,
        storage_gb=500,
        storage_rate=0.02,
        transfer_gb=100,
        transfer_rate=0.09,
    )


@app.post("/")
def submit():
    compute_hours = float(request.form.get("compute_hours", 720) or 0)
    compute_rate = float(request.form.get("compute_rate", 0.05) or 0)
    storage_gb = float(request.form.get("storage_gb", 500) or 0)
    storage_rate = float(request.form.get("storage_rate", 0.02) or 0)
    transfer_gb = float(request.form.get("transfer_gb", 100) or 0)
    transfer_rate = float(request.form.get("transfer_rate", 0.09) or 0)

    breakdown, total = calculate_cloud_cost(
        compute_hours, compute_rate, storage_gb, storage_rate, transfer_gb, transfer_rate
    )

    model_type = request.form.get("model_type", "Large (e.g., GPT-4)")
    tokens_millions = float(request.form.get("tokens_millions", 1.0) or 0)
    optimization = request.form.get("optimization", "0") == "1"
    tokens = tokens_millions * 1_000_000
    ai_energy, ai_carbon = estimate_ai_energy(tokens, model_type, optimization)

    return render_template_string(
        HTML,
        cloud_total=total,
        breakdown=breakdown.to_dict(orient="records"),
        ai_energy=ai_energy,
        ai_carbon=ai_carbon,
        model_type=model_type,
        tokens_millions=tokens_millions,
        optimization=optimization,
        comparison=get_platform_comparison().to_dict(orient="records"),
        compute_hours=compute_hours,
        compute_rate=compute_rate,
        storage_gb=storage_gb,
        storage_rate=storage_rate,
        transfer_gb=transfer_gb,
        transfer_rate=transfer_rate,
    )


if __name__ == "__main__":
    app.run(debug=True)
