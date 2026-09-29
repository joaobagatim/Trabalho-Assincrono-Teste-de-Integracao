# Testes de integração — Agendamento de helicópteros

Trabalho de Qualidade e Teste de Software — João Victor Bagatim.

## Instalação e execução

Requisito: Python 3.10 ou superior. No terminal, dentro desta pasta:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -v
.venv\Scripts\python -m pytest -v --cov=src --cov-branch --cov-report=term-missing
```

Em Linux/macOS, substitua `.venv\Scripts\python` por `.venv/bin/python`.

## Estrutura e funcionamento

- `src/database.py`: tabelas aeronaves, pilotos e agendamentos; consultas e inserção com parâmetros SQL.
- `src/validation.py`: verifica período, existência da aeronave, manutenção e sobreposição de horários.
- `src/booking_service.py`: chama a validação e salva o agendamento em uma transação SQLite.
- `tests/conftest.py`: cria uma base temporária por teste, com duas aeronaves e um piloto fictício; fecha a conexão e remove o arquivo após cada teste.
- `tests/test_flight_integration.py`: quatro cenários obrigatórios e verificações complementares simples.
- `evidencias/`: saídas e imagens geradas a partir da execução real dos testes.

Os horários usam `datetime` sem fuso e o mesmo horário local. O conflito ocorre quando `inicio_existente < fim_novo` e `fim_existente > inicio_novo`. Portanto, um voo que termina às 11h permite outro começar às 11h. O cadastro do piloto é uma referência no banco, sem regras adicionais de escala.

O contexto transacional confirma a inserção quando a operação termina e desfaz alterações se houver exceção. As recusas de negócio são verificadas antes da inserção. O isolamento dos testes usa bases separadas, sem depender de rollback entre testes.

## Cenários

1. Agendamento válido, confirmado por outra conexão SQLite.
2. Conflito de horário, mantendo o estado anterior das três tabelas.
3. Aeronave em inspeção, mantendo o banco inalterado.
4. Isolamento com fixture, executado duas vezes com os mesmos dados.
5. Horários adjacentes permitidos.
6. Intervalo inválido recusado.
7. Aeronave inexistente recusada.

São oito execuções porque o cenário de isolamento possui dois parâmetros. A cobertura mede apenas os módulos em `src`; não comprova segurança operacional nem substitui testes de concorrência e uma validação completa de um sistema real.

## Resultado verificado

Execução em Windows com Python 3.13.7, pytest 9.1.1 e pytest-cov 7.1.0: oito testes aprovados; cobertura de 100% das 40 instruções e dos oito ramos dos módulos em `src`.
