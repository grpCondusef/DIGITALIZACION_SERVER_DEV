from fpdf import FPDF

def generar_certificacion_pdf(leyenda_interpolada: str, output_path: str):
    """
    Genera un PDF de una sola página con la leyenda interpolada.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, leyenda_interpolada)
    pdf.output(output_path)
    return output_path