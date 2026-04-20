import pandas as pd
from fpdf import FPDF
import base64

def calculate_cloud_cost(compute_hours, compute_rate, storage_gb, storage_rate, transfer_gb, transfer_rate):
    compute_total = compute_hours * compute_rate
    storage_total = storage_gb * storage_rate
    transfer_total = transfer_gb * transfer_rate
    grand_total = compute_total + storage_total + transfer_total
    
    breakdown = {
        "Component": ["Compute", "Storage", "Data Transfer"],
        "Cost ($)": [compute_total, storage_total, transfer_total]
    }
    return pd.DataFrame(breakdown), grand_total

def estimate_ai_energy(tokens, model_type="Large", optimization=False):
    # Energy consumption in kWh per million tokens (estimated)
    energy_rates = {
        "Small (e.g., DistilBERT)": 0.05,
        "Medium (e.g., Llama-7B)": 0.2,
        "Large (e.g., GPT-4)": 1.5
    }
    
    rate = energy_rates.get(model_type, 1.0)
    if optimization:
        rate *= 0.6 # 40% reduction with optimization
        
    energy_kwh = (tokens / 1_000_000) * rate
    carbon_kg = energy_kwh * 0.4 # Avg 0.4kg CO2 per kWh
    
    return energy_kwh, carbon_kg

def get_platform_comparison():
    data = {
        "Platform": ["AWS", "Google Cloud", "Microsoft Azure"],
        "Base Price Index": [1.0, 0.95, 1.05],
        "Scalability": ["High", "Very High", "High"],
        "Performance": ["Premium", "Standard+", "Premium"],
        "Sustainability Rating": ["B", "A", "B+"]
    }
    return pd.DataFrame(data)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Sustainable Cloud & AI Dashboard Report', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_pdf_report(cloud_data, ai_data, comparison_df):
    pdf = PDF()
    pdf.add_page()
    
    # Cloud Section
    pdf.chapter_title("1. Cloud Cost Summary")
    cloud_body = f"Total Monthly Cloud Cost: ${cloud_data['total']:.2f}\n"
    cloud_body += f"Breakdown:\n- Compute: ${cloud_data['compute']:.2f}\n- Storage: ${cloud_data['storage']:.2f}\n- Transfer: ${cloud_data['transfer']:.2f}"
    pdf.chapter_body(cloud_body)
    
    # AI Section
    pdf.chapter_title("2. AI Energy & Sustainability")
    ai_body = f"Model Type: {ai_data['model']}\n"
    ai_body += f"Total Tokens: {ai_data['tokens']:,}\n"
    ai_body += f"Estimated Energy: {ai_data['energy']:.4f} kWh\n"
    ai_body += f"Carbon Footprint: {ai_data['carbon']:.4f} kg CO2"
    pdf.chapter_body(ai_body)
    
    # Comparison Section
    pdf.chapter_title("3. Platform Comparison")
    comp_body = "Comparison of major cloud providers based on pricing, scalability, and sustainability."
    pdf.chapter_body(comp_body)
    
    # Save PDF to string
    return pdf.output(dest='S').encode('latin-1')

def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}.pdf">Click here to download {file_label}</a>'
    return href
