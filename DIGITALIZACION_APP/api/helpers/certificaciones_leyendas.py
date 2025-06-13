# -*- coding: utf-8 -*-
"""
Diccionario que asocia el nombre del área (unidad) con su leyenda de certificación.
El área debe coincidir exactamente con el campo User.area.nombre.
Los placeholders a reemplazar deben ser:
    {nombre_completo}, {num_fojas}, {folio_expediente}, {recurrente}, {fecha_certificacion}
"""

LEYENDAS = {
    "UNIDAD DE ATENCION A USUARIOS A1 (METROPOLITANA CENTRAL)": (
        "El/La Lic. {nombre_completo}, Titular de la Unidad de Atención a Usuarios Metropolitana 1, de la Comisión Nacional para la Protección y Defensa de los Usuarios de Servicios Financieros, "
        "con fundamento en los artículos 3; 4; 16; 26, fracción XX, y 28 de la Ley de Protección y Defensa al Usuario de Servicios Financieros; 1, 2, fracción II; 3, fracción I, numeral 2, inciso a, subinciso i; "
        "5, fracción I; 14, fracción XI y último párrafo; 31, fracción X, y 34, párrafo primero, del Estatuto Orgánico de esta Comisión Nacional."
        "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ "
        "CERTIFICA --------------------------------------------------------------------------------------- "
        "Que la presente copia fotostática, constante en {num_fojas} fojas útiles que se certifican, es fiel y exacta reproducción de las constancias originales que integran el expediente número {folio_expediente}, "
        "mismo que se tuvo a la vista y que obra en la Unidad de Red Integral Digitalizadora de Expedientes CONDUSEF (URIDEC); y se expide a fin de remitirlo a la Dirección General de Servicios Jurídicos para la tramitación del recurso de revisión interpuesto por {recurrente}. "
        "------------------------- {fecha_certificacion}."
    ),
    "Unidad de Atención a Usuarios Metropolitana 2": (
        "El/La Lic. {nombre_completo}, Titular de la Unidad de Atención a Usuarios Metropolitana 2, de la Comisión Nacional para la Protección y Defensa de los Usuarios de Servicios Financieros, "
        "con fundamento en los artículos 3; 4; 16; 26, fracción XX, y 28 de la Ley de Protección y Defensa al Usuario de Servicios Financieros; 1, 2, fracción II; 3, fracción I, numeral 2, inciso a, subinciso i; "
        "5, fracción I; 14, fracción XI y último párrafo; 31, fracción X, y 34, párrafo primero, del Estatuto Orgánico de esta Comisión Nacional."
        "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- "
        "CERTIFICA --------------------------------------------------------------------------------------- "
        "Que la presente copia fotostática, constante en {num_fojas} fojas útiles que se certifican, es fiel y exacta reproducción de las constancias originales que integran el expediente número {folio_expediente}, "
        "mismo que se tuvo a la vista y que obra en la Unidad de Red Integral Digitalizadora de Expedientes CONDUSEF (URIDEC); y se expide a fin de remitirlo a la Dirección General de Servicios Jurídicos para la tramitación del recurso de revisión interpuesto por {recurrente}. "
        "--------------------------- {fecha_certificacion}."
    ),
    "Unidad de Atención a Usuarios Metropolitana 3": (
        "El/La Lic. {nombre_completo}, Titular de la Unidad de Atención a Usuarios Metropolitana 3, de la Comisión Nacional para la Protección y Defensa de los Usuarios de Servicios Financieros, "
        "con fundamento en los artículos 3; 4; 16; 26, fracción XX, y 28 de la Ley de Protección y Defensa al Usuario de Servicios Financieros; 1, 2, fracción II; 3, fracción I, numeral 2, inciso a, subinciso i; "
        "5, fracción I; 14, fracción XI y último párrafo; 31, fracción X, y 34, párrafo primero, del Estatuto Orgánico de esta Comisión Nacional."
        "------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- "
        "CERTIFICA --------------------------------------------------------------------------------------- "
        "Que la presente copia fotostática, constante en {num_fojas} fojas útiles que se certifican, es fiel y exacta reproducción de las constancias originales que integran el expediente número {folio_expediente}, "
        "mismo que se tuvo a la vista y que obra en la Unidad de Red Integral Digitalizadora de Expedientes CONDUSEF (URIDEC); y se expide a fin de remitirlo a la Dirección General de Servicios Jurídicos para la tramitación del recurso de revisión interpuesto por {recurrente}. "
        "--------------------------- {fecha_certificacion}."
    ),
    # ... Agrega aquí todas las áreas restantes siguiendo el mismo patrón ...
    "Dirección General de Sanciones": (
        "El/La Lic. {nombre_completo}, Titular de la Dirección General de Sanciones, de la Comisión Nacional para la Protección y Defensa de los Usuarios de Servicios Financieros, "
        "con fundamento en los artículos 3; 4; 16; 26, fracción XX, y 28 de la Ley de Protección y Defensa al Usuario de Servicios Financieros; 1; 3, fracción I, numeral 1, inciso a; 14, fracción XI, y 15, fracción XI, del Estatuto Orgánico de esta Comisión Nacional."
        "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- "
        "CERTIFICA ------------------------------------------------------------------------------------- "
        "Que la presente copia fotostática, constante en {num_fojas} fojas útiles que se certifican, es fiel y exacta reproducción de las constancias originales que integran el expediente número {folio_expediente}, "
        "mismo que se tuvo a la vista y que obra en la Unidad de Red Integral Digitalizadora de Expedientes CONDUSEF (URIDEC); y se expide a fin de remitirlo a la Dirección General de Servicios Jurídicos para la tramitación del recurso de revisión interpuesto por {recurrente}. "
        "--------------------------- {fecha_certificacion}."
    ),
    # ... y así sucesivamente para cada unidad/área ...
}