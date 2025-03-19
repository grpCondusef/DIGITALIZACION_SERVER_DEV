
def generarConsecutivo(claves_archivisticas):
    if len(claves_archivisticas) > 0:
        consecutivos_array = []
        for clave in claves_archivisticas:
            point_counter = 0
            consecutivo = ''
            for clave_item in clave:
                if clave_item == '.':
                    point_counter += 1
                if point_counter == 4:
                    if clave_item != '.':
                        consecutivo = consecutivo + clave_item
            if point_counter == 4:
                consecutivos_array.append(int(consecutivo))
        return str((max(consecutivos_array) + 1)).zfill(6) #AGREGAMOS CEROS PARA QUE SEAN 6 DÍGITOS
    else:
        return str(1).zfill(6)  #AGREGAMOS CEROS PARA QUE SEAN 6 DÍGITOS

