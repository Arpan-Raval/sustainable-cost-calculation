import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    calculate_cloud_cost, 
    estimate_ai_energy, 
    get_platform_comparison, 
    generate_pdf_report,
    get_binary_file_downloader_html
)

# Page Config
st.set_page_config(
    page_title="Sustainable Cloud & AI Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        color: #ffffff;
    }
    .css-1d391kg {
        background-color: #161b22;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 {
        color: #10b981 !important;
    }
    .stButton>button {
        background-color: #10b981;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #059669;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🌱 EcoCloud Admin")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Overview", "Cloud Cost Calculator", "Sustainable AI Tokens", "Cloud Comparison", "Export Report"])

# --- SESSION STATE INITIALIZATION ---
if 'cloud_results' not in st.session_state:
    st.session_state.cloud_results = {"total": 0, "compute": 0, "storage": 0, "transfer": 0}
if 'ai_results' not in st.session_state:
    st.session_state.ai_results = {"model": "Large", "tokens": 0, "energy": 0, "carbon": 0}

# --- PAGE: OVERVIEW ---
if page == "Overview":
    st.title("Sustainable Computing Dashboard")
    st.markdown("Welcome to the **EcoCloud** dashboard. This platform helps you analyze cloud costs, optimize AI energy consumption, and compare platform sustainability.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Projected Cost", f"${st.session_state.cloud_results['total']:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("AI Carbon Footprint", f"{st.session_state.ai_results['carbon']:.2f} kg CO2")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Optimization Status", "In Progress", delta="12%")
        st.markdown('</div>', unsafe_allow_html=True)

    # Informational Graph
    st.subheader("Industry Sustainability Trends")
    df_trends = pd.DataFrame({
        "Year": [2020, 2021, 2022, 2023, 2024],
        "Cloud Efficiency (%)": [45, 52, 60, 68, 75],
        "AI Energy Demand (TWh)": [10, 15, 25, 45, 80]
    })
    fig = px.line(df_trends, x="Year", y=["Cloud Efficiency (%)", "AI Energy Demand (TWh)"], 
                 title="Cloud Efficiency vs AI Demand", template="plotly_dark", color_discrete_sequence=["#10b981", "#ef4444"])
    st.plotly_chart(fig, width="stretch")

# --- PAGE: CLOUD COST CALCULATOR ---
elif page == "Cloud Cost Calculator":
    st.title("💰 Cloud Cost Calculation")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Parameters")
        compute_h = st.number_input("Compute Hours (Monthly)", value=720, min_value=0)
        compute_r = st.number_input("Hourly Rate ($)", value=0.05, format="%.4f")
        storage_g = st.number_input("Storage (GB)", value=500, min_value=0)
        storage_r = st.number_input("Storage Rate ($/GB)", value=0.02, format="%.4f")
        transfer_g = st.number_input("Data Transfer (GB)", value=100, min_value=0)
        transfer_r = st.number_input("Transfer Rate ($/GB)", value=0.09, format="%.4f")
        
        if st.button("Calculate Cost"):
            df_breakdown, total = calculate_cloud_cost(compute_h, compute_r, storage_g, storage_r, transfer_g, transfer_r)
            st.session_state.cloud_results = {
                "total": total,
                "compute": compute_h * compute_r,
                "storage": storage_g * storage_r,
                "transfer": transfer_g * transfer_r,
                "compute_h": compute_h,
                "storage_g": storage_g,
                "transfer_g": transfer_g,
                "df": df_breakdown
            }
            st.success(f"Calculation Complete: ${total:.2f}")

    with col2:
        if "df" in st.session_state.cloud_results:
            st.subheader("Cost Breakdown")
            fig = px.pie(st.session_state.cloud_results["df"], values="Cost ($)", names="Component", 
                        hole=0.4, color_discrete_sequence=px.colors.sequential.Greens_r, template="plotly_dark")
            st.plotly_chart(fig, width="stretch")
            st.table(st.session_state.cloud_results["df"])
        else:
            st.info("Enter parameters and click Calculate to see results.")

# --- PAGE: SUSTAINABLE AI TOKENS ---
elif page == "Sustainable AI Tokens":
    st.title("🤖 Sustainable AI Tokens")
    st.markdown("Estimate the environmental impact of your AI inference and explore optimization methods.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        model_type = st.selectbox("Model Scale", ["Small (e.g., DistilBERT)", "Medium (e.g., Llama-7B)", "Large (e.g., GPT-4)"])
        tokens = st.number_input("Number of Tokens (Millions)", value=1.0, step=0.1) * 1_000_000
        opt_enabled = st.toggle("Enable Optimization (Efficient Models/Token Pruning)")
        
        energy, carbon = estimate_ai_energy(tokens, model_type, opt_enabled)
        st.session_state.ai_results = {
            "model": model_type,
            "tokens": tokens,
            "energy": energy,
            "carbon": carbon
        }
        
        st.metric("Estimated Energy", f"{energy:.4f} kWh", delta=f"-40%" if opt_enabled else None)
        st.metric("Carbon Footprint", f"{carbon:.4f} kg CO2")

    with col2:
        st.subheader("Sustainability Impact")
        # Visualizing carbon offset equivalent
        trees = carbon / 20 # 1 tree absorbs ~20kg CO2/year
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = carbon,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Carbon Footprint (kg CO2)", 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [None, 5]},
                'bar': {'color': "#10b981"},
                'steps': [
                    {'range': [0, 1], 'color': "#064e3b"},
                    {'range': [1, 3], 'color': "#065f46"},
                    {'range': [3, 5], 'color': "#047857"}],
            }
        ))
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, width="stretch")
        st.write(f"💡 This is equivalent to the annual carbon absorption of **{trees:.2f}** mature trees.")

# --- PAGE: CLOUD COMPARISON ---
elif page == "Cloud Comparison":
    st.title("⚖️ Cloud Platform Comparison")
    st.markdown("Comparison for a standard E-commerce workload (approx. 1M requests/mo).")
    
    df_comp = get_platform_comparison()
    
    # Custom display
    for index, row in df_comp.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            c1.subheader(row['Platform'])
            c2.metric("Pricing Index", row['Base Price Index'])
            c3.metric("Scalability", row['Scalability'])
            c4.metric("Sustainability", row['Sustainability Rating'])
            st.markdown("---")
            
    st.subheader("Comparison Visualization")
    fig = px.bar(df_comp, x="Platform", y="Base Price Index", color="Sustainability Rating",
                title="Pricing vs Sustainability", template="plotly_dark",
                color_discrete_map={"A": "#10b981", "B+": "#34d399", "B": "#6ee7b7"})
    st.plotly_chart(fig, width="stretch")

# --- PAGE: EXPORT REPORT ---
elif page == "Export Report":
    st.title("📄 Export Project Report")
    st.markdown("Generate a PDF report of your current analysis.")
    
    if st.button("Generate PDF Report"):
        with st.spinner("Compiling report..."):
            pdf_bytes = generate_pdf_report(
                st.session_state.cloud_results,
                st.session_state.ai_results,
                get_platform_comparison()
            )
            html = get_binary_file_downloader_html(pdf_bytes, 'Sustainability_Report')
            st.markdown(html, unsafe_allow_html=True)
            st.balloons()
            st.success("Report ready for download!")

st.sidebar.markdown("---")