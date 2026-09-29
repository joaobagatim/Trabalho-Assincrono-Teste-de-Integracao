class ValidationModule:
    def __init__(self, database):
        self.database = database

    def validar(self, aeronave_id, inicio, fim):
        if inicio >= fim:
            raise ValueError("O fim deve ser posterior ao início")
        aeronave = self.database.buscar_aeronave(aeronave_id)
        if aeronave is None:
            raise ValueError("Aeronave não cadastrada")
        if aeronave["status_manutencao"] != "LIBERADO":
            raise ValueError("Aeronave não liberada para voo")
        if self.database.tem_conflito(aeronave_id, inicio, fim):
            raise ValueError("Conflito de horário da aeronave")
