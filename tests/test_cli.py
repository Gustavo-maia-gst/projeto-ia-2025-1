import argparse
from unittest.mock import MagicMock

import pytest
import sympy
import sys
import runpy

import cli

@pytest.fixture
def parser():
    return argparse.ArgumentParser()

# Mock para a classe Params para não depender do arquivo real
@pytest.fixture(autouse=True)
def mock_params_class(monkeypatch):
    mock = MagicMock()
    mock.DEFAULT_POPULATION_SIZE = 10
    mock.DEFAULT_STEP_SIZE = 0.1
    mock.DEFAULT_MAX_STEPS = 100
    mock.DEFAULT_TOURNAMENT_RATE = 0.5
    mock.DEFAULT_TOURNAMENT_SIZE = 5
    mock.DEFAULT_ELITISM_RATE = 0.1
    mock.DEFAULT_CROSSOVER_RATE = 0.2
    mock.DEFAULT_CROSSOVER_MUTATION_RATE = 0.05
    mock.DEFAULT_LOTTERY_RATE = 0.1
    mock.DEFAULT_RANDOM_RATE = 0.05
    mock.DEFAULT_FPS = 10
    mock.DEFAULT_DEPTH = 20
    mock.DEFAULT_PLOT_LEVELS_2D = 15

    monkeypatch.setattr(cli, 'Params', mock)
    return mock


def test_define_params(parser):
    cli.define_params(parser)

    assert len(parser._actions) == 13 + 1


def test_get_params(parser, monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['cli.py', '--population-size', '99', '--depth', '42'])
    
    cli.define_params(parser)
    params_obj = cli.get_params(parser)

    assert params_obj.POPULATION_SIZE == 99
    assert params_obj.DEPTH == 42

    assert params_obj.MAX_STEPS == 100


def test_main_success_path(monkeypatch, capsys):

    monkeypatch.setattr('builtins.input', lambda _: 'x**2')
    
    monkeypatch.setattr(cli, 'Genetic', MagicMock())
    mock_plotter_instance = MagicMock()
    monkeypatch.setattr(cli, 'Plotter', lambda *args, **kwargs: mock_plotter_instance)
    
    monkeypatch.setattr(sys, 'argv', ['cli.py'])

    cli.main()

    mock_plotter_instance.show.assert_called_once()


def test_main_invalid_function_error(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'x + * y')
    monkeypatch.setattr(sys, 'argv', ['cli.py'])

    with pytest.raises(SystemExit) as e:
        cli.main()
    
    assert e.value.code == 1
    
    captured = capsys.readouterr()
    assert "Função inválida" in captured.out


def test_main_type_error(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'some_input')
    monkeypatch.setattr(sys, 'argv', ['cli.py'])
    
    monkeypatch.setattr(sympy, 'sympify', lambda _: (_ for _ in ()).throw(TypeError('mocked type error')))
    
    with pytest.raises(SystemExit) as e:
        cli.main()

    assert e.value.code == 1

    captured = capsys.readouterr()
    assert "A entrada fornecida não é uma string válida" in captured.out

def test_main_invalid_function_error(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'x + * y')
    monkeypatch.setattr(sys, 'argv', ['cli.py'])
    with pytest.raises(SystemExit) as e:
        cli.main()
    assert e.value.code == 1
    assert "Função inválida" in capsys.readouterr().out


def test_main_type_error(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'some_input')
    monkeypatch.setattr(sys, 'argv', ['cli.py'])

    monkeypatch.setattr(sympy, 'sympify', lambda _: (_ for _ in ()).throw(TypeError('mocked')))
    with pytest.raises(SystemExit) as e:
        cli.main()
    assert e.value.code == 1
    assert "não é uma string válida" in capsys.readouterr().out


def test_entry_point_calls_original_main_and_stops(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: (_ for _ in ()).throw(StopIteration))
    monkeypatch.setattr(sys, 'argv', ['cli.py'])

    with pytest.raises(StopIteration):
        runpy.run_module('cli', run_name='__main__')