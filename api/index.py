import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template_string, request

from utils import calculate_cloud_cost, estimate_ai_energy, get_platform_comparison

app = Flask(__name__)


HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>EcoCloud Sustainability Dashboard</title>
  <style>
    :root { color-scheme: dark; }
    body { font-family: Arial, sans-serif; margin: 0; background: linear-gradient(135deg,#07111f,#0f172a 45%,#111827); color: #e5eefb; }
    .wrap { max-width: 1100px; margin: 0 auto; padding: 24px; }
    .card { background: rgba(15,23,42,0.92); border: 1px solid #24364a; border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.35); padding: 18px; margin-bottom: 18px; }
    h1,h2 { color: #34d399; }
    p { color: #cbd5e1; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }
    label { display: block; font-size: 0.95rem; color: #dbeafe; margin-bottom: 6px; }
    input, select { width: 100%; box-sizing: border-box; padding: 10px; border-radius: 8px; border: 1px solid #334155; background: #111827; color: #fff; }
    button { background: linear-gradient(135deg,#10b981,#059669); color: #fff; border: none; border-radius: 999px; padding: 10px 16px; cursor: pointer; font-weight: 700; }
    button:hover { filter: brightness(1.08); }
    .pill { display: inline-flex; align-items: center; gap: 8px; padding: 6px 10px; border-radius: 999px; background: #1f2937; border: 1px solid #374151; }
    .metric { display: flex; justify-content: space-between; gap: 12px; padding: 12px; border-radius: 12px; background: #111827; border: 1px solid #24364a; }
    .metric span { color: #bfdbfe; font-size: 0.92rem; }
    .metric strong { display: block; font-size: 1.35rem; color: #f8fafc; margin-top: 4px; }
    table { width: 100%; border-collapse: collapse; overflow: hidden; border-radius: 12px; }
    th, td { text-align: left; padding: 10px; border-bottom: 1px solid #24364a; }
    th { color: #bbf7d0; background: #111827; }
    .ok { color: #bbf7d0; }
    .warn { color: #fca5a5; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>🌱 EcoCloud Sustainability Dashboard</h1>
      <p>This live version is hosted on Vercel and uses the same sustainability logic as your Streamlit project.</p>
      <div class="pill">Status: Live on Vercel</div>
    </div>

    <div class="grid">
      <div class="card">
        <h2>Cloud Cost Calculator</h2>
        <form method="post">
          <label>Compute Hours (Monthly)</label>
          <input type="number" step="1" name="compute_hours" value="{{ compute_hours if compute_hours else 720 }}" />
          <label>Hourly Rate ($)</label>
          <input type="number" step="0.0001" name="compute_rate" value="{{ compute_rate if compute_rate else 0.05 }}" />
          <label>Storage (GB)</label>
          <input type="number" step="1" name="storage_gb" value="{{ storage_gb if storage_gb else 500 }}" />
          <label>Storage Rate ($/GB)</label>
          <input type="number" step="0.0001" name="storage_rate" value="{{ storage_rate if storage_rate else 0.02 }}" />
          <label>Data Transfer (GB)</label>
          <input type="number" step="1" name="transfer_gb" value="{{ transfer_gb if transfer_gb else 100 }}" />
          <label>Transfer Rate ($/GB)</label>
          <input type="number" step="0.0001" name="transfer_rate" value="{{ transfer_rate if transfer_rate else 0.09 }}" />
          <br /><br />
          <button type="submit">Calculate</button>
        </form>
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
          <input type="number" step="0.1" name="tokens_millions" value="{{ tokens_millions if tokens_millions else 1.0 }}" />
          <label>Optimization</label>
          <select name="optimization">
            <option value="0" {% if not optimization %}selected{% endif %}>Off</option>
            <option value="1" {% if optimization %}selected{% endif %}>On</option>
          </select>
          <br /><br />
          <button type="submit">Estimate</button>
        </form>
      </div>
    </div>

    {% if cloud_total is not none %}
    <div class="card">
      <h2>Cloud Cost Result</h2>
      <div class="grid">
        <div class="metric"><div><span>Total Monthly Cost</span><strong>${{ "%.2f"|format(cloud_total) }}</strong></div></div>
        <div class="metric"><div><span>Compute</span><strong>${{ "%.2f"|format(compute_amount) }}</strong></div></div>
        <div class="metric"><div><span>Storage</span><strong>${{ "%.2f"|format(storage_amount) }}</strong></div></div>
        <div class="metric"><div><span>Data Transfer</span><strong>${{ "%.2f"|format(transfer_amount) }}</strong></div></div>
      </div>
      <table>
        <thead><tr><th>Component</th><th>Cost ($)</th></tr></thead>
        <tbody>
          {% for row in breakdown %}
          <tr><td>{{ row['Component'] }}</td><td>{{ "%.2f"|format(row['Cost ($)']) }}</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
    {% endif %}

    {% if ai_energy is not none %}
    <div class="card">
      <h2>AI Impact Result</h2>
      <div class="grid">
        <div class="metric"><div><span>Model</span><strong>{{ model_type }}</strong></div></div>
        <div class="metric"><div><span>Energy</span><strong>{{ "%.4f"|format(ai_energy) }} kWh</strong></div></div>
        <div class="metric"><div><span>Carbon Footprint</span><strong>{{ "%.4f"|format(ai_carbon) }} kg CO2</strong></div></div>
        <div class="metric"><div><span>Optimization</span><strong>{{ 'Enabled' if optimization else 'Disabled' }}</strong></div></div>
      </div>
    </div>
    {% endif %}

    <div class="card">
      <h2>Cloud Provider Comparison</h2>
      <table>
        <thead>
          <tr><th>Platform</th><th>Base Price Index</th><th>Scalability</th><th>Sustainability</th></tr>
        </thead>
        <tbody>
          {% for row in comparison %}
          <tr>
            <td>{{ row['Platform'] }}</td>
            <td>{{ row['Base Price Index'] }}</td>
            <td>{{ row['Scalability'] }}</td>
            <td>{{ row['Sustainability Rating'] }}</td>
          </tr>
          {% endfor %}
        </tbody>
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
        compute_amount=0.0,
        storage_amount=0.0,
        transfer_amount=0.0,
        breakdown=[],
        ai_energy=None,
        ai_carbon=None,
        model_type='Large (e.g., GPT-4)',
        tokens_millions=1.0,
        optimization=False,
        comparison=get_platform_comparison().to_dict(orient='records'),
        compute_hours=720,
        compute_rate=0.05,
        storage_gb=500,
        storage_rate=0.02,
        transfer_gb=100,
        transfer_rate=0.09,
    )


@app.post("/")
def submit():
    compute_hours = float(request.form.get('compute_hours', 720) or 0)
    compute_rate = float(request.form.get('compute_rate', 0.05) or 0)
    storage_gb = float(request.form.get('storage_gb', 500) or 0)
    storage_rate = float(request.form.get('storage_rate', 0.02) or 0)
    transfer_gb = float(request.form.get('transfer_gb', 100) or 0)
    transfer_rate = float(request.form.get('transfer_rate', 0.09) or 0)

    breakdown, total = calculate_cloud_cost(compute_hours, compute_rate, storage_gb, storage_rate, transfer_gb, transfer_rate)
    compute_amount = compute_hours * compute_rate
    storage_amount = storage_gb * storage_rate
    transfer_amount = transfer_gb * transfer_rate

    model_type = request.form.get('model_type', 'Large (e.g., GPT-4)')
    tokens_millions = float(request.form.get('tokens_millions', 1.0) or 0)
    optimization = request.form.get('optimization', '0') == '1'
    tokens = tokens_millions * 1_000_000
    ai_energy, ai_carbon = estimate_ai_energy(tokens, model_type, optimization)

    return render_template_string(
        HTML,
        cloud_total=total,
        compute_amount=compute_amount,
        storage_amount=storage_amount,
        transfer_amount=transfer_amount,
        breakdown=breakdown.to_dict(orient='records'),
        ai_energy=ai_energy,
        ai_carbon=ai_carbon,
        model_type=model_type,
        tokens_millions=tokens_millions,
        optimization=optimization,
        comparison=get_platform_comparison().to_dict(orient='records'),
        compute_hours=compute_hours,
        compute_rate=compute_rate,
        storage_gb=storage_gb,
        storage_rate=storage_rate,
        transfer_gb=transfer_gb,
        transfer_rate=transfer_rate,
    )


if __name__ == '__main__':
    app.run(debug=True)
