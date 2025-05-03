from fpdf import FPDF
import os

def generate_pdf(content, file_name):
    from fpdf import FPDF

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

                # Header line (e.g., "1. Dataset Overview")
                if line[0].isdigit() and '.' in line[:4]:
                    self.set_font("Arial", "B", size=13)
                    self.multi_cell(0, 8, line)
                    self.set_font("Arial", size=12)
                    continue

                # Bullet points with bold inline
                if line.startswith("-"):
                    clean_line = line[1:].strip()
                    if "**" in clean_line:
                        parts = clean_line.split("**")
                        self.write(8, "* ")  # Replaced bullet with *
                        for i, part in enumerate(parts):
                            if i % 2 == 1:
                                self.set_font("Arial", "B", size=12)
                                self.write(8, part)
                                self.set_font("Arial", size=12)
                            else:
                                self.write(8, part)
                        self.ln()
                    else:
                        self.multi_cell(0, 8, f"* {clean_line}")  # Replaced bullet with *
                else:
                    self.multi_cell(0, 8, line)

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
    pdf.add_logo("img/logo.jpg")
    pdf.add_title(f"{file_name} Summary")
    pdf.render_markdown(content)
    pdf.add_bottom_logo("img/logo.jpg")
    pdf.add_footer_note()

    pdf_output_path = os.path.join("assets", file_name)
    pdf.output(pdf_output_path)
    return pdf_output_path
