import streamlit as st 
import os 
import pandas as pd 
from fpdf import FPDF
from datetime import datetime
from parser import parser_csv, parser_excel, parser_pdf
from insights import get_llm_insights
from visualizer import generate_plotly_charts
from pdf_generator import generate_pdf

st.set_page_config(page_title="File Analyzer", layout="wide")
st.title("📊 File Analysis System with LLM Using Euri")

# Ensure directories exist
os.makedirs("output", exist_ok=True)
os.makedirs("assets/uploads", exist_ok=True)

uploaded_file = st.file_uploader("Upload your Excel, CSV, or PDF file", type=["csv", "xlsx", "xls", "pdf"])


if uploaded_file:
    file_path = os.path.join("assets/uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    file_stem = f"output/{uploaded_file.name.split('.')[0]}"
    # print(file_stem)
    
    # file_stem = "output"

    # Handle CSV/Excel
    if uploaded_file.name.endswith(".csv"):
        df = parser_csv(file_path)
    elif uploaded_file.name.endswith((".xlsx", ".xls")):
        df = parser_excel(file_path)
    else:
        # PDF logic
        pdf_text = parser_pdf(file_path)
        st.subheader("📄 PDF Content")
        st.text_area("Text Extracted from PDF:", pdf_text[:5000], height=300)

        if st.button("Generate Insights from PDF"):
            with st.spinner("Thinking..."):
                st.session_state.insight = get_llm_insights(f"Summarize this PDF:\n{pdf_text[:8000]}")

        if "insight" in st.session_state:
            st.success("📌 Insight:")
            st.write(st.session_state.insight)

            # Generate downloadable PDF
            pdf_file_name = f"{file_stem}/Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf_path = generate_pdf(st.session_state.insight, pdf_file_name)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button("📥 Download Insight PDF", data=pdf_file, file_name=pdf_file_name)

        st.stop()

    # CSV/Excel analysis
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(20))

    if st.button("🔍 Analyze Data with LLM"):
        with st.spinner("Generating Insights..."):
            st.session_state.insight = get_llm_insights(f"Analyze this dataset:\n{df.head(100).to_csv(index=False)}")

    if "insight" in st.session_state:
        st.success("📌 Insights:")
        st.write(st.session_state.insight)

        # Generate downloadable PDF
        pdf_file_name = f"{file_stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = generate_pdf(st.session_state.insight, pdf_file_name)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button("📥 Download Insight PDF", data=pdf_file, file_name=pdf_file_name)

    # Visualizations
    st.subheader("📈 Auto Visualizations")
    plots = generate_plotly_charts(df)
    for fig in plots:
        st.plotly_chart(fig, use_container_width=True)
