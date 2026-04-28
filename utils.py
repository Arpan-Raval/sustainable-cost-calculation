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
        self.set_font('Arial', 'B', 16)
        self.set_text_color(16, 185, 129) # Emerald Green
        self.cell(0, 10, 'Sustainable Cloud & AI Project Report', 0, 1, 'C')
        self.ln(5)
        self.set_draw_color(16, 185, 129)
        self.line(10, 25, 200, 25)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(31, 41, 55)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(55, 65, 81)
        self.multi_cell(0, 8, body)
        self.ln()

    def create_table(self, header, data):
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(243, 244, 246)
        col_width = 190 / len(header)
        for h in header:
            self.cell(col_width, 10, h, 1, 0, 'C', 1)
        self.ln()
        self.set_font('Arial', '', 10)
        for row in data:
            for item in row:
                self.cell(col_width, 10, str(item), 1, 0, 'C')
            self.ln()
        self.ln(5)

def generate_pdf_report(cloud_data, ai_data, comparison_df):
    pdf = PDF()
    pdf.add_page()
    
    # Section 1: Executive Summary
    pdf.chapter_title("1. Executive Summary")
    pdf.chapter_body(
        "This project focuses on the intersection of cloud efficiency and environmental sustainability. "
        "As global computing demands increase, optimizing resources such as compute, storage, and data transfer "
        "is essential for reducing the carbon footprint of digital infrastructure."
    )

    # Section 2: Cloud Cost Calculation
    pdf.chapter_title("2. Cloud Cost Calculation")
    pdf.chapter_body(
        "The following table provides a detailed breakdown of monthly cloud costs based on current configurations. "
        "Efficient resource allocation is key to both financial savings and energy reduction."
    )
    
    cloud_table_header = ["Component", "Value", "Monthly Cost ($)"]
    cloud_table_data = [
        ["Compute", f"{cloud_data.get('compute_h', 0)} hrs", f"${cloud_data['compute']:.2f}"],
        ["Storage", f"{cloud_data.get('storage_g', 0)} GB", f"${cloud_data['storage']:.2f}"],
        ["Data Transfer", f"{cloud_data.get('transfer_g', 0)} GB", f"${cloud_data['transfer']:.2f}"],
        ["Grand Total", "-", f"${cloud_data['total']:.2f}"]
    ]
    pdf.create_table(cloud_table_header, cloud_table_data)

    # Section 3: Sustainable Tokens for AI
    pdf.add_page()
    pdf.chapter_title("3. Sustainable Tokens for AI")
    pdf.chapter_body(
        f"Artificial Intelligence systems consume significant energy during inference. For the selected "
        f"model ({ai_data['model']}), the environmental impact for {ai_data['tokens']:,} tokens is estimated below."
    )
    
    ai_table_header = ["Metric", "Value"]
    ai_table_data = [
        ["Model Scale", ai_data['model']],
        ["Total Tokens", f"{ai_data['tokens']:,}"],
        ["Energy Consumption", f"{ai_data['energy']:.4f} kWh"],
        ["Carbon Footprint", f"{ai_data['carbon']:.4f} kg CO2"],
        ["Tree Absorption Eq.", f"{ai_data['carbon']/20:.2f} trees/yr"]
    ]
    pdf.create_table(ai_table_header, ai_table_data)
    
    pdf.chapter_body(
        "Optimization techniques such as quantization, pruning, and efficient prompt engineering "
        "can reduce this consumption by up to 40-60%, making AI deployments more sustainable."
    )

    # Section 4: Cloud Platform Comparison
    pdf.chapter_title("4. Comparison of Cloud Platforms")
    pdf.chapter_body(
        "Evaluating major cloud providers based on real-world e-commerce requirements: Pricing, "
        "Scalability, Performance, and Sustainability Ratings."
    )
    
    comp_header = ["Platform", "Price Index", "Scalability", "Sustainability"]
    comp_data = comparison_df[["Platform", "Base Price Index", "Scalability", "Sustainability Rating"]].values.tolist()
    pdf.create_table(comp_header, comp_data)

    # Section 5: Real-Life Examples & Conclusion
    pdf.add_page()
    pdf.chapter_title("5. Case Study: E-Commerce Platform")
    pdf.chapter_body(
        "For an e-commerce platform with 1M monthly requests, selecting a provider like Google Cloud (GCP) "
        "provides a superior sustainability rating due to their carbon-intelligent workload scheduling. "
        "AWS, while slightly higher in price, offers the best tools for cost granularization."
    )
    
    pdf.chapter_title("6. Conclusion")
    pdf.chapter_body(
        "Sustainable computing is achieved when financial efficiency meets environmental responsibility. "
        "By using tools like this dashboard, organizations can make informed decisions to optimize their "
        "digital footprint for a greener future."
    )
    
    return pdf.output(dest='S').encode('latin-1')

def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}.pdf">Click here to download {file_label}</a>'
    return href
