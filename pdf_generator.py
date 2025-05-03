from fpdf import FPDF
import os
import re

def generate_pdf(content, file_name):
    class PDF(FPDF):
        def __init__(self):
            super().__init__()
            self.set_auto_page_break(auto=True, margin=15)
            self.add_page()
            self.set_font("Arial", size=12)

        def add_logo(self, path):
            if os.path.exists(path):
                self.image(path, x=80, w=50)
                self.ln(30)

        def add_title(self, title):
            self.set_font("Arial", "B", size=16)
            self.cell(0, 10, title, ln=True, align="C")
            self.ln(5)
            self.set_font("Arial", size=12)

        def render_markdown(self, text):
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    self.ln(3)
                    continue

                # Header (e.g., "1. Title:")
                if re.match(r"^\d+\.\s", line):
                    clean_line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)  # strip ** in headers
                    self.set_font("Arial", "B", size=13)
                    self.multi_cell(0, 8, clean_line)
                    self.set_font("Arial", size=12)
                    continue

                # Bullet point (starts with "-" or "*")
                is_bullet = False
                if line.startswith("-") or line.startswith("*"):
                    is_bullet = True
                    line = line[1:].strip()
                    self.write(8, "* ")

                # Handle bold **text** within any line
                parts = re.split(r"(\*\*.*?\*\*)", line)
                for part in parts:
                    if part.startswith("**") and part.endswith("**"):
                        self.set_font("Arial", "B", size=12)
                        self.write(8, part[2:-2])  # remove **
                        self.set_font("Arial", size=12)
                    else:
                        self.write(8, part)
                self.ln()

        def add_footer_note(self):
            self.ln(10)
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Thank You", ln=True, align="C")
            self.cell(0, 10, "Mohammad Wasiq", ln=True, align="C")

            self.set_font("Arial", "", 9)
            self.multi_cell(0, 6, "\nNote: This is an LLM-generated report. It may not be 100% accurate or correct.", align="C")

        def add_bottom_logo(self, path):
            if os.path.exists(path):
                self.set_y(-50)
                self.image(path, x=80, w=50)

    # === Start PDF Rendering ===
    pdf = PDF()

    # Optional: use logo if available
    # pdf.add_logo("img/logo.jpg")

    filename = file_name.split("/")[-1]
    cleaned_name = filename.split("_")[:-2]  # remove timestamp parts
    saving_file_name = " ".join(cleaned_name).replace("_", "").title()

    pdf.add_title(f"{saving_file_name} Summary")
    pdf.render_markdown(content)

    # Optional: use bottom logo
    # pdf.add_bottom_logo("img/logo.jpg")
    pdf.add_footer_note()

    pdf_output_path = os.path.join("assets", file_name)
    pdf.output(pdf_output_path)
    return pdf_output_path
