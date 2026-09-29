import pytest

from src.booking_service import BookingService
from src.database import Database


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "operacao.db"
    db = Database(path)
    with db.connection:
        db.connection.executemany(
            "INSERT INTO aeronaves VALUES (?, ?, ?)",
            [(1, "PR-ABC", "LIBERADO"), (2, "PR-DEF", "EM_INSPECAO")],
        )
        db.connection.execute("INSERT INTO pilotos VALUES (1, 'Piloto de teste')")
    yield db
    db.close()
    path.unlink()


@pytest.fixture
def service(database):
    return BookingService(database)
