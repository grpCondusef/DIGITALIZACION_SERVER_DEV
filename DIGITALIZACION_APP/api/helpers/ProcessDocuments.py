from rest_framework.response import Response
from rest_framework import status
import cv2
import PyPDF2
import fitz  # PyMuPDF, imported as fitz for backward compatibility reasons
from os import remove
import os
from datetime import datetime
from pathlib import Path
import uuid
from CATALOGOS.models import TipoDocumental
from DIGITALIZACION_APP.models import SplitDocuments

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

def remove_noise(image,  num1, num2, num3):
    return cv2.bilateralFilter(image, num1, num2, num3)


def QRDetector( document, user_id, array):
    counter = 0
    doc = fitz.open(document) 
    pdfReader = PyPDF2.PdfReader(document)
    pages = len(pdfReader.pages)
    counter = 0
    initial_positions = []
    final_positions = []
    tipos_documentales = []
    position_arrays = 0
    sections_array = []
    num2 = 165
    num3 = 165

    for page in doc:
        item = {}
        counter += 1
        len_data_qr = 0
        pix = page.get_pixmap()  # render page to an image
        pix.save(f'pagina-{counter}-de-{pages}.png')
        pdf_image = 'pagina-{}-de-{}.png'.format(counter, pages)
        
        pdf_image = cv2.imread(pdf_image, cv2.IMREAD_GRAYSCALE)
        ret, th1 = cv2.threshold(pdf_image, 127, 255, cv2.THRESH_TOZERO)
        
        try:

            while num2 >= 0 and len_data_qr == 0:
                num2 -= 5
                num3 -= 5
                pdf_image = remove_noise(th1, 1, num2, num3)
                qrDetector = cv2.QRCodeDetector()
                data, bbox, rectifiedImage = qrDetector.detectAndDecode(pdf_image)
                len_data_qr = len(data)
                #print(num2)
                #print(num2)
                #print(len_data_qr)
                
            #print(f'página {counter}')
            
            pdf_image = remove_noise(th1, 1, num2, num3)
            qrDetector = cv2.QRCodeDetector()
            data, bbox, rectifiedImage = qrDetector.detectAndDecode(pdf_image)

            remove(f'pagina-{counter}-de-{pages}.png')
            
            if counter == 2:
                remove(f'pagina-1-de-{pages}.png')
            
            if pdf_image.size > 0:
                
                #PARAR EJECUCIÓN CUANDO NO LEE EL QR INICIAL
                if counter == 1:
                    cv2.imwrite(f'pagina-{counter}-de-{pages}.png', pdf_image)
                    if len(data) < 1:
                        return 'Parece que ha ocurrido un error!!!'

                if counter == pages:
                    final_positions.append(pages)
                    tipo_documental = TipoDocumental.objects.get(clave=tipos_documentales[-1])

                    item['tipo_id'] = tipo_documental.id
                    item['name'] = tipo_documental.nombre
                    item['pages'] = list(range(initial_positions[-1], final_positions[-1]))
                    sections_array.append(item)

                if len(data) > 0 and data in array:
                    initial_positions.append(counter)
                    tipos_documentales.append(data)

                    if counter > 1:
                        final_positions.append(counter-1)

                    if len(final_positions) > 0:
                        tipo_documental = TipoDocumental.objects.get(clave=tipos_documentales[position_arrays])

                        item['tipo_id'] = tipo_documental.id
                        item['name'] = tipo_documental.nombre
                        item['pages'] = list(
                            range(initial_positions[position_arrays], final_positions[position_arrays]))
                        sections_array.append(item)

                    if counter > 1 and len(final_positions) > 0:
                        position_arrays += 1

        except Exception as e:
            remove(f'pagina-{counter}-de-{pages}.png')
            print(f'Hubo un error leyengo el qr:{e}')

    return sections_array


def get_total_expediente_documents(expediente_id):
    documents_counter = SplitDocuments.objects.filter(expediente_id=expediente_id).count()
    return documents_counter


def process_document(document, array, clave, expediente_id, user_id):
    try:
        with open(document, 'rb') as pdf:
            reader = PyPDF2.PdfReader(pdf)
            documents_counter = get_total_expediente_documents(expediente_id)
            sections_array = QRDetector(document, user_id, array)
            cadena_unique_identifier = str(uuid.uuid4())
            added_files = []
            
            # =========== SI "sections_array" ES UN ARRAY Y NO ESTA VACÍO =========
            if len(sections_array) > 0 and isinstance(sections_array, list):
                counter = -1
                for section in sections_array:
                    documents_counter += 1
                    counter += 1
                    exec('c{}writer = PyPDF2.PdfWriter()'.format(counter))

                    section_pages = section.get('pages')
                    tipo_documetal = section.get('tipo_id')

                    for page in range(len(reader.pages)):
                        if page in section_pages:
                            exec('c{}writer.add_page(reader.pages[page])'.format(counter))

                    # Crear las carpetas si no existen
                    actual_year = datetime.now().year
                    actual_month = datetime.now().month
                    actual_day = datetime.now().day
                    directory = os.path.join(BASE_DIR, 'archexpedientes/uridec/split_documents/{}/{}/{}'.format(actual_year, actual_month, actual_day))
                    os.makedirs(directory, exist_ok=True)

                    file_name = '{}.- {}_{}_{}.pdf'.format(documents_counter, tipo_documetal, clave, cadena_unique_identifier)

                    with open(os.path.join(directory, '{}.- {}_{}_{}.pdf'.format(documents_counter, tipo_documetal, clave, cadena_unique_identifier)), 'wb') as f2:
                        exec('c{}writer.write(f2)'.format(counter))
                        SplitDocuments.objects.create(
                            name=file_name,
                            path='/uridec/split_documents/{}/{}/{}/{}'.format(actual_year, actual_month, actual_day, file_name),
                            expediente_id=expediente_id,
                            tipo_id=tipo_documetal,
                            user_id=user_id
                        )
                        
                    added_files.append({
                        'file_number': documents_counter,
                        'file_name': sections_array[counter]['name']
                    })
                    
                return {
                        'msg': 'Separación de pdf´s concluida',
                        'uploaded_files': added_files
                    }

    except Exception as e:
        print(f'Ha habido un error {e}')