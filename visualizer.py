import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_plotly_charts(df: pd.DataFrame):
    plots = []
    numeric_columns = df.select_dtypes(include='number').columns.tolist()

    for col in numeric_columns:
        fig = px.histogram(df, x=col, title=f"Distribution of {col}")
        plots.append(fig)

    if len(numeric_columns) >= 2:
        fig = px.scatter_matrix(df[numeric_columns], title="Scatter Matrix")
        plots.append(fig)

    return plots