from PyPDF2 import PdfMerger

def merge_files(paths, output_path):
    merger = PdfMerger()
    for path in paths:
        merger.append(open(str(path), "rb"))
    with open(output_path, "wb") as salida:
        merger.write(salida)