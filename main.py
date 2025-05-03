import streamlit as st 
import os 
import pandas as pd 
from parser import parser_csv,parser_excel,parser_pdf
from insights import get_llm_insights
from visualizer import generate_plotly_charts

st.set_page_config(page_title = "file analyzer" , layout = "wide")
st.title("file analysis system with llm ")

uploaded_file = st.file_uploader("uplopad your excel , csv or pdf file ",type = ["csv" , "xlsx","xls","pdf"])


if uploaded_file:
    file_path = os.path.join("assets/uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    if uploaded_file.name.endswith(".csv"):
        df = parser_csv(file_path)
    elif uploaded_file.name.endswith((".xlsx", ".xls")):
        df = parser_excel(file_path)
    else:
        pdf_text = parser_pdf(file_path)
        st.subheader("PDF Content")
        st.text_area("Text Extracted from PDF:", pdf_text[:5000], height=300)

        if st.button("Generate Insights from PDF"):
            with st.spinner("Thinking..."):
                insight = get_llm_insights(f"Summarize this PDF:\n{pdf_text[:8000]}")
                st.success("Insight:")
                st.write(insight)
        st.stop()

    st.subheader("Data Preview")
    st.dataframe(df.head(20))

    if st.button("Analyze Data with LLM"):
        with st.spinner("Generating insight..."):
            insight = get_llm_insights(f"Analyze this dataset:\n{df.head(100).to_csv(index=False)}")
            st.success("Insight:")
            st.write(insight)

    st.subheader("Auto Visualizations")

    plots = generate_plotly_charts(df)
    for fig in plots:
        st.plotly_chart(fig, use_container_width=True)
