
import math


class Pagination:

    def __init__(self, query, elementos_por_pagina, pagina_actual):
        self.query = query
        self.elementos_por_pagina = elementos_por_pagina
        self.pagina_actual = pagina_actual
        self.elementos_pag_actual = []

    def totalExpedientes(self):
        return len(self.query)

    def paginasTotales(self):
        if self.elementos_por_pagina > len(self.query):
            return 1
        else:
            self.paginas_totales = len(self.query) / self.elementos_por_pagina
            return math.ceil(self.paginas_totales)

    def elementosDePaginaActual(self):
        self.paginas_totales = self.paginasTotales()
        if self.elementos_por_pagina > len(self.query):
            return self.query
        else:
            # SI ESTAMOS EN LA ÚLTIMA PÁGINA Y EL NÚMERO DE ELEMENTOS SOBRANTES ES IMPAR
            if self.pagina_actual == self.paginas_totales and len(self.query) % self.elementos_por_pagina != 0:
                self.elements = self.query[self.elementos_por_pagina:]
                for i in self.elements:
                    self.elementos_pag_actual.append(i)
                return self.elementos_pag_actual
            else:
                for i in range((self.elementos_por_pagina * self.pagina_actual) - self.elementos_por_pagina, (self.elementos_por_pagina * self.pagina_actual)):
                    self.elementos_pag_actual.append(self.query[i])
                return self.elementos_pag_actual

    def paginasList(self):
        self.paginas = []
        self.paginas_totales = self.paginasTotales()
        for i in range(self.paginas_totales):
            self.paginas.append(i + 1)
        return self.paginas

    def paginaActual(self):
        return self.pagina_actual

    def siguientePagina(self):
        self.paginas_totales = self.paginasTotales()
        if self.pagina_actual < self.paginas_totales:
            return int(self.pagina_actual + 1)
        else:
            False

    def paginaAnterior(self):
        if self.pagina_actual > 1 and self.elementos_por_pagina < len(self.query):
            return int(self.pagina_actual - 1)
        else:
            False