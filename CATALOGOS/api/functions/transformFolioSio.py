
def transformFolioSio(folio):
    position_counter = 0
    new_folio = ''
    consecutivo = ''
    for i in folio:
        if i == '/':
            position_counter += 1
        if position_counter < 2:
            new_folio = new_folio + i
        if position_counter == 2:
            consecutivo = consecutivo + i
    consecutivo = consecutivo.replace('/', '')
    consecutivo = int(consecutivo)

    new_folio = f'{new_folio}/{str(consecutivo)}'

    return new_folio
