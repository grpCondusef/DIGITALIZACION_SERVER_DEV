def interpolar_leyenda(
    leyenda: str,
    nombre_completo: str,
    num_fojas: int,
    folio_expediente: str,
    recurrente: str,
    fecha_certificacion: str
) -> str:
    """
    Reemplaza los placeholders de la leyenda con los datos proporcionados.
    """
    return leyenda.format(
        nombre_completo=nombre_completo,
        num_fojas=num_fojas,
        folio_expediente=folio_expediente,
        recurrente=recurrente,
        fecha_certificacion=fecha_certificacion
    )