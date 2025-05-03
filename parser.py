import pandas as pd 
import fitz 


def parser_csv(file_path):
    return pd.read_csv(file_path)

def parser_excel(file_path):
    return pd.read_excel(file_path)

def parser_pdf(file_path):
    pdf = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in pdf])
    return text