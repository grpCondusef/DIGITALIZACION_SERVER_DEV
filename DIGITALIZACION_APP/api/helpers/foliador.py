import fitz

def insertFolio(page, counter):
    folio_number = f'{counter:05}'
    annotation_text = f'No. {folio_number}'
    shape = page.new_shape()
    shape.insert_text((page.mediabox.x1 - 165, page.mediabox.y1 - 755), annotation_text, fontsize=26, fontname="HELV", encoding=fitz.TEXT_ENCODING_CYRILLIC)
    shape.commit()

def foliador(document, name_out_document, portada):
    pdf_document = fitz.open(document)

    for counter, page in enumerate(pdf_document, start=1):
        #insertFolio(page, counter) if counter >= 1 and not portada else None
        
        if counter == 1:
            pass
        else: 
            #print(portada)
            if portada:
                insertFolio(page, counter - 1)
            else:
                insertFolio(page, counter)
            
        
    pdf_document.save(name_out_document)
    pdf_document.close()
