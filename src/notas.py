class Notas:
    def __init__(self, name, nota, criterio):
        self.name = name
        self.nota = nota
        self.criterio = criterio

    def formato_doc(self):
        return {
            'name': self.name,
            'nota': self.nota,
            'criterio': self.criterio,
        }
