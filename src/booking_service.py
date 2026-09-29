from src.validation import ValidationModule


class BookingService:
    def __init__(self, database):
        self.database = database
        self.validation = ValidationModule(database)

    def agendar(self, aeronave_id, piloto_id, inicio, fim):
        """Recebe datetime sem fuso, usando o mesmo horário local da operação."""
        inicio_iso = inicio.isoformat(timespec="microseconds")
        fim_iso = fim.isoformat(timespec="microseconds")
        with self.database.connection:
            self.validation.validar(aeronave_id, inicio_iso, fim_iso)
            return self.database.inserir_agendamento(
                aeronave_id, piloto_id, inicio_iso, fim_iso
            )
