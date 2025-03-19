
import os
from DIGITALIZACION_APP.models import Portadas

def get_documents_paths(BASE_DIR, documentos, documents_array):
    for documento in documentos:
        documento_path = os.path.join(BASE_DIR, f'archexpedientes{str(documento.path)}')
        documents_array.append(documento_path)