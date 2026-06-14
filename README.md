# Sustainable Cloud & AI Dashboard

A Streamlit-based dashboard for analyzing cloud costs, estimating AI energy consumption, comparing cloud platforms, and generating sustainability reports.

## Overview

This project helps users understand how digital infrastructure affects sustainability and costs. It combines three core areas:

- Cloud cost estimation for compute, storage, and data transfer
- AI energy and carbon footprint estimation for different model sizes
- Comparison of major cloud providers based on pricing, scalability, and sustainability rating

The goal is to make sustainability-aware decisions easier for developers, students, and teams working with cloud infrastructure and AI systems.

## Features

- Cloud Cost Calculator
  - Estimate monthly cloud expenses using custom compute, storage, and transfer inputs
- Sustainable AI Tokens
  - Estimate energy use and CO2 emissions for AI inference
  - Optional optimization mode to show potential efficiency improvement
- Cloud Comparison
  - Compare AWS, Google Cloud, and Microsoft Azure on pricing and sustainability indicators
- Export Report
  - Generate a downloadable PDF report of the current analysis

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- FPDF

## Project Structure

- app.py — Main Streamlit application
- utils.py — Core utility functions for cost calculation, AI energy estimation, and PDF export
- Project_Report.md — Detailed project report and analysis
- requirements.txt — Python dependencies

## Installation

1. Clone the repository
2. Navigate to the project folder
3. Create and activate a virtual environment (recommended)
4. Install dependencies

```bash
pip install -r requirements.txt
```

## Run Locally

Start the dashboard using:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually http://localhost:8501).

## How It Works

### 1. Cloud Cost Calculator
You can enter:
- compute hours
- hourly compute rate
- storage in GB
- storage rate per GB
- data transfer in GB
- transfer rate per GB

The app calculates the total monthly cost and shows a breakdown by component.

### 2. Sustainable AI Tokens
You can choose a model scale and estimate:
- energy consumption in kWh
- carbon footprint in kg CO2
- possible savings from optimization

### 3. Cloud Comparison
The app compares major cloud providers using simplified sustainability and pricing metrics.

### 4. Export Report
You can generate a PDF report containing your current analysis for sharing or documentation.

## Why This Project Matters

This project highlights the importance of sustainable computing by showing how:

- cloud resource usage affects cost
- AI inference consumes energy
- efficient design choices can reduce environmental impact

It is especially useful for learning, presentations, and exploring sustainability-focused cloud decision making.

## Future Improvements

Possible enhancements include:

- real cloud pricing API integration
- more accurate AI energy models
- historical usage charts
- user authentication and saved sessions
- export to CSV and Excel

## License

This project is intended for educational and demo purposes.

## Author

Built as a sustainability and cloud-efficiency dashboard project.
