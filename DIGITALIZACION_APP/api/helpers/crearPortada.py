import os
from os import remove
from datetime import datetime
import qrcode
from barcode import Gs1_128
from barcode.writer import ImageWriter
from fpdf import FPDF

def createFechaApertura(date):
    print(date)
    fechaApertura = ''
    for i in date:
        if i == ' ':
            break
        fechaApertura += i
    # Convertir la cadena a un objeto datetime
    date_obj = datetime.strptime(fechaApertura , '%Y-%m-%d')
    # Formatear la fecha en el nuevo formato 'dd-mm-yyyy'
    new_date_str = date_obj.strftime('%d-%m-%Y')    
    return new_date_str

def folioPORI(folio):
    if folio == None:
        return ''
    else:
        return folio

def create_rectangle(pdf, x, y, width, height):
    pdf.rect(x, y, width, height)

def create_qr_code(expediente_data, path_img):
    # Asegura que la carpeta existe antes de guardar
    os.makedirs(path_img, exist_ok=True)

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(expediente_data.get("clave"))
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(f'{path_img}qr_{expediente_data.get("clave")}.png')

    code = Gs1_128(expediente_data.get("clave"), writer=ImageWriter())
    code.save(f'{path_img}bar_code_{expediente_data.get("clave")}')

def get_expedient_data(clave, expediente, vigencia_ids, valoresDocumentales_array, serie_id):
    # Acceso a las vigencias por su id
    vigenciaTramite = vigencia_ids.get(1)
    vigenciaConcentracion = vigencia_ids.get(2)
    vigenciaTotal = vigencia_ids.get(3)

    expediente_data = {}
    expediente_data['clave'] = clave
    expediente_data['reclamante'] = '' if expediente.reclamante == 'nan' else expediente.reclamante
    expediente_data['idMacroproceso'] = expediente.idMacroproceso.nombre
    expediente_data['idProceso'] = expediente.idProceso.nombre
    expediente_data['valores_documentales'] = "/".join(valoresDocumentales_array)
    expediente_data['vigenciaTramiteAnios'] = vigenciaTramite.get('anios') if vigenciaTramite else ''
    expediente_data['vigenciaTramiteMeses'] = vigenciaTramite.get('meses') if vigenciaTramite else ''
    expediente_data['vigenciaTramiteDias'] = vigenciaTramite.get('dias') if vigenciaTramite else ''
    expediente_data['vigenciaConcentracionAnios'] = vigenciaConcentracion.get('anios') if vigenciaConcentracion else ''
    expediente_data['vigenciaConcentracionMeses'] = vigenciaConcentracion.get('meses') if vigenciaConcentracion else ''
    expediente_data['vigenciaConcentracionDias'] = vigenciaConcentracion.get('dias') if vigenciaConcentracion else ''
    expediente_data['vigenciaTotalAnios'] = vigenciaTotal.get('anios') if vigenciaTotal else ''
    expediente_data['vigenciaTotalMeses'] = vigenciaTotal.get('meses') if vigenciaTotal else ''
    expediente_data['vigenciaTotalDias'] = vigenciaTotal.get('dias') if vigenciaTotal else ''
    expediente_data['idSerie'] = expediente.idSerie.nombre
    expediente_data['folioSIO'] = expediente.folioSIO
    expediente_data['pori'] = expediente.pori
    expediente_data['fechaApertura'] = expediente.fechaApertura
    expediente_data['formatoSoporte'] = expediente.formatoSoporte
    if expediente.idInstitucion:
        expediente_data['institucion_financiera'] = expediente.idInstitucion.denominacion_social
    else:
        expediente_data['institucion_financiera'] = ''
    expediente_data['resumenContenido'] = expediente.resumenContenido
    return expediente_data

def crear_portada(BASE_DIR, path_img, clave, expediente, vigencia_ids, valoresDocumentales_array, serie_id):
    expediente_data = get_expedient_data(clave, expediente, vigencia_ids, valoresDocumentales_array, serie_id)
    date = str(expediente_data.get("fechaApertura"))
    fechaApertura = createFechaApertura(date)
    folioPori = folioPORI(expediente_data.get("pori"))

    # CREAR CÓDIGO QR y CÓDIGO DE BARRAS (Se asegura la carpeta antes de guardar)
    create_qr_code(expediente_data, path_img)

    # CREAMOS EL PDF EN FORMATO LEGAL
    pdf = FPDF(orientation='P', unit='mm', format='Letter')
    pdf.add_page()  # NECESITAMOS DECLARAR UNA PÁGINA

    # ============== PRIMERA SECCIÓN ===============
    create_rectangle(pdf, 13, 11, 192.13, 73.1)  # CONTENEDOR PRINCIPAL
    create_rectangle(pdf, 13, 11, 53.91, 73.1)   # ======== CONTENEDOR LOGOS =======
    pdf.image(f'{path_img}SHCP_logo.png', x=16, y=16, w=47.51, h=13, link='')
    pdf.image(f'{path_img}CONDUSEF-LOGO.png', x=20, y=34, w=40, h=18, link='')
    pdf.image(f'{path_img}qr_{expediente_data.get("clave")}.png', x=31, y=57, w=20, h=20, link='')

    create_rectangle(pdf, 67, 11, 138.20, 9.53) # =======HEADER=======
    pdf.set_font('Arial', 'B', 10)
    pdf.text(x=73, y = 15, txt='FONDO COMISIÓN NACIONAL PARA LA PROTECCIÓN Y DEFENSA DE LOS')
    pdf.text(x=100, y = 19, txt='USUARIOS DE SERVICIOS FINANCIEROS')

    pdf.set_font('Arial', '', 11)
    pdf.text(x=78, y=30, txt='CCA:')
    pdf.rect(x=92, y=24, w=109.71, h=8.65)
    pdf.text(x=127, y=30, txt=f"{expediente_data.get('clave')}")

    pdf.set_font('Arial', '', 11)
    pdf.text(x=76, y=38, txt='Macro')
    pdf.text(x=73, y=42, txt='proceso:')
    pdf.set_font('Arial', '', 8)
    pdf.set_xy(92,34)
    pdf.multi_cell(w=109.71, h=6.91, txt=f'{expediente_data.get("idMacroproceso")}', align='C', border=1)

    pdf.set_font('Arial', '', 11)
    pdf.text(x=76, y=55, txt='Proceso:')
    pdf.set_font('Arial', '', 8)
    pdf.set_xy(92,50)
    pdf.multi_cell(w=109.71, h=6.91, txt=f'{expediente_data.get("idProceso")}', align='C', border=1)

    pdf.set_font('Arial', '', 11)
    pdf.text(x=76, y=71, txt='Serie:')
    pdf.set_font('Arial', '', 8)
    pdf.set_xy(92,66)
    pdf.multi_cell(w=109.71, h=6.91, txt=f'{expediente_data.get("idSerie")}', align='C', border=1)

    #============== SEGUNDA SECCIÓN ===============
    create_rectangle(pdf, 13, 88, 192.13, 82.7) #CONTENEDOR PRINCIPAL

    pdf.set_font('Arial', '', 10)
    pdf.text(x=26, y=97, txt='Asunto/')
    pdf.text(x=26, y=101, txt='Expediente')
    create_rectangle(pdf, 48.5, 90.5, 153, 16.69)

    pdf.text(x=27, y=113, txt='Folio')
    pdf.text(x=16, y=117, txt='SIO/Expediente')
    pdf.text(x=51, y=116, txt=f'{expediente_data.get("folioSIO")}')
    create_rectangle(pdf, 48.5, 110.5, 83.09, 8.83)
    
    pdf.text(x=134, y=116, txt='PORI')
    pdf.set_xy(144.5,110.5)
    pdf.cell(w=56.94, h=8.83, txt=f'{folioPori}', align='C', border=1)

    pdf.text(x=22, y=130, txt='Reclamante')
    pdf.set_xy(48.5,122.5)
    pdf.multi_cell(w=153, h=10.1, txt=f'{expediente_data.get("reclamante")}', align='C', border=1)

    pdf.text(x=24, y=142, txt='Institución')
    pdf.set_xy(48.5,138)
    pdf.multi_cell(w=153, h=6.1, txt=f'{expediente_data.get("institucion_financiera")}', align='C', border=1)

    pdf.text(x=20, y=155.5, txt='Resumen del')
    pdf.text(x=24, y=158.5, txt='contenido')
    pdf.set_xy(48.5,152.5)
    pdf.multi_cell(w=153, h=4.5, txt=f'{expediente_data.get("resumenContenido")}', align='C', border=1)

    #============== TERCERA SECCIÓN ===============
    create_rectangle(pdf, 13, 175, 192.13, 52.21) #CONTENEDOR PRINCIPAL

    pdf.set_font('Arial', '', 10)
    pdf.text(x=33, y=183, txt='Fecha')
    create_rectangle(pdf, 48.5, 177.5, 153, 19) #=========CONTNEDOR TABLA 1=========

    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=80, y=181, txt='Apertura')
    create_rectangle(pdf, 48.5, 177.5, 76.5, 4.75)
    pdf.text(x=155, y=181, txt='Cierre')
    create_rectangle(pdf, 125, 177.5, 76.5, 4.75)
    pdf.set_font('Arial', '', 9)
    pdf.set_xy(48.5,182.25)
    pdf.cell(w=76.5, h=4.75, txt=f'{fechaApertura}', align='C', border=1)
    pdf.set_font('Arial', '', 9)
    pdf.text(x=148, y=186, txt='')
    create_rectangle(pdf, 125, 182.25, 76.5, 4.75)
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=80, y=191, txt='Trámite')
    create_rectangle(pdf, 48.5, 187, 76.5, 4.75)
    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=150, y=191, txt='Concentración')
    create_rectangle(pdf, 125, 187, 76.5, 4.75)
    pdf.set_font('Arial', '', 9)
    pdf.text(x=68, y=195, txt=f'{expediente_data.get("vigenciaTramiteAnios")} años {expediente_data.get("vigenciaTramiteMeses")} meses {expediente_data.get("vigenciaTramiteDias")} días' )
    pdf.set_font('Arial', '', 9)
    pdf.text(x=145, y=195, txt=f'{expediente_data.get("vigenciaConcentracionAnios")} años {expediente_data.get("vigenciaConcentracionMeses")} meses {expediente_data.get("vigenciaConcentracionDias")} días')
    create_rectangle(pdf, 125, 191.75, 76.5, 4.75)

    pdf.set_font('Arial', '', 10)
    pdf.text(x=30, y=197, txt='Vigencia')
    pdf.text(x=26, y=201, txt='documental')

    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=121, y=201, txt='Total')
    create_rectangle(pdf, 87, 196.5,76.8, 10)
    pdf.set_font('Arial', '', 9)
    pdf.text(x=107, y=205, txt=f'{expediente_data.get("vigenciaTotalAnios")} años {expediente_data.get("vigenciaTotalMeses")} meses {expediente_data.get("vigenciaTotalDias")} días')
    create_rectangle(pdf, 87, 196.5, 76.8, 5)

    pdf.set_font('Arial', '', 10)
    pdf.text(x=30, y=211, txt='Volúmen')
    create_rectangle(pdf, 48.5, 206.5,153, 19) #=========CONTNEDOR TABLA 2========= 

    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=74, y=210, txt='Número de legajos')
    create_rectangle(pdf, 48.5, 206.5, 76.5, 4.75)
    pdf.text(x=149, y=210, txt='Número de fojas')
    pdf.rect(x=125, y=206.5, w=76.5, h=4.75)

    pdf.set_font('Arial', '', 9)
    pdf.text(x=85, y=215, txt='') #NÚMERO DE LEGAJOS
    create_rectangle(pdf, 48.5, 211.25, 76.5, 4.75)
    pdf.text(x=161, y=215, txt='') #NÚMERO DE FOJAS
    create_rectangle(pdf, 125, 211.25, 76.5, 4.75)

    pdf.set_font('Arial', 'B', 9)
    pdf.text(x=74, y=219.5, txt='Valor Documental')
    create_rectangle(pdf, 48.5, 216, 76.5, 4.75)
    pdf.text(x=149, y=219.5, txt='Formato Soporte')
    create_rectangle(pdf, 125, 216, 76.5, 4.75)

    pdf.set_font('Arial', '', 9)
    pdf.text(x=73.8, y=224.5, txt=f'{expediente_data.get("valores_documentales")}')
    create_rectangle(pdf, 48.5, 220.75, 76.5, 4.75)
    pdf.text(x=158, y=224.5, txt=f'{expediente_data.get("formatoSoporte")}')
    create_rectangle(pdf, 125, 220.75, 76.5, 4.75)

    pdf.text(x=80, y=234, txt='Contiene información confidencial SI/NO')
    create_rectangle(pdf, 140, 230.5, 4.75, 4.75)

    pdf.set_font('Arial', '', 7)
    pdf.text(x=23, y=241, txt='De conformidad con el Artículo 214 del Código Penal Federal es delito el desglose de este expediente, así como la sustracción indebida de cualquiera de sus fojas.')

    pdf.image(f'{path_img}bar_code_{expediente_data.get("clave")}.png', x=80, y=242, w=76, h=22.28, link='')

    # Crear las carpetas si no existen para el PDF de portada
    actual_year = datetime.now().year
    actual_month = datetime.now().month
    actual_day = datetime.now().day
    directory = os.path.join(BASE_DIR, f'archexpedientes/uridec/pdf_portadas/{actual_year}/{actual_month}/{actual_day}/')
    os.makedirs(directory, exist_ok=True)
    pdf.output(f'{directory}{expediente_data.get("clave")}_portada.pdf','F')  # GUARDAMOS EL PDF GENERADO

    # Eliminar archivo QR
    qr_path = os.path.join(path_img, f'qr_{expediente_data.get("clave")}.png')
    if os.path.exists(qr_path):
        os.remove(qr_path)
    else:
        print(f"El archivo QR {qr_path} no existe.")

    # Eliminar archivo de barras
    bar_path = os.path.join(path_img, f'bar_code_{expediente_data.get("clave")}.png')
    if os.path.exists(bar_path):
        os.remove(bar_path)
    else:
        print(f"El archivo de barras {bar_path} no existe.")