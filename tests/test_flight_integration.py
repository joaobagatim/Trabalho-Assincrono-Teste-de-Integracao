import sqlite3
from datetime import datetime

import pytest


def horario(hora):
    return datetime(2026, 9, 29, hora)


def estado(database):
    return {
        tabela: [tuple(row) for row in database.connection.execute(
            f"SELECT * FROM {tabela} ORDER BY id"
        )]
        for tabela in ("aeronaves", "pilotos", "agendamentos")
    }


def test_agendamento_valido(service, database):
    booking_id = service.agendar(1, 1, horario(10), horario(11))
    path = database.connection.execute("PRAGMA database_list").fetchone()[2]
    # Outra conexão confirma que o registro foi efetivamente persistido.
    with sqlite3.connect(path) as connection:
        row = connection.execute(
            "SELECT * FROM agendamentos WHERE id = ?", (booking_id,)
        ).fetchone()
    connection.close()
    assert row == (booking_id, 1, 1, "2026-09-29T10:00:00.000000",
                   "2026-09-29T11:00:00.000000", "AGENDADO")


def test_conflito_de_horario(service, database):
    service.agendar(1, 1, horario(10), horario(11))
    antes = estado(database)
    with pytest.raises(ValueError, match="Conflito de horário"):
        service.agendar(1, 1, horario(10), horario(11))
    assert estado(database) == antes


def test_aeronave_em_manutencao(service, database):
    antes = estado(database)
    with pytest.raises(ValueError, match="Aeronave não liberada"):
        service.agendar(2, 1, horario(10), horario(11))
    assert estado(database) == antes


@pytest.mark.parametrize("execucao", [1, 2])
def test_isolamento_com_fixture(service, database, execucao):
    assert estado(database)["agendamentos"] == []
    service.agendar(1, 1, horario(10), horario(11))
    assert len(estado(database)["agendamentos"]) == 1


def test_intervalos_adjacentes(service, database):
    service.agendar(1, 1, horario(10), horario(11))
    service.agendar(1, 1, horario(11), horario(12))
    assert len(estado(database)["agendamentos"]) == 2


def test_intervalo_invalido(service, database):
    antes = estado(database)
    with pytest.raises(ValueError, match="O fim deve ser posterior"):
        service.agendar(1, 1, horario(11), horario(10))
    assert estado(database) == antes


def test_aeronave_inexistente(service, database):
    antes = estado(database)
    with pytest.raises(ValueError, match="Aeronave não cadastrada"):
        service.agendar(99, 1, horario(10), horario(11))
    assert estado(database) == antes
