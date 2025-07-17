# Algoritmo genético para encontrar máximo de função

Para iniciar rode
```bash
pip install -e .
```

caso não instale as dependências
```bash
pip install -r requirements.txt
```

rode o arquivo **cli.py**


## Argumentos de Linha de Comando

Cada hiperparâmetro pode ser ajustado via flags do `argparse`. Se não informados, usam-se os valores-padrão listados abaixo:

| Argumento                     | Tipo    | Default | Descrição                                                                      |
|-------------------------------|---------|---------|--------------------------------------------------------------------------------|
| `--population-size`           | int     | 32      | Tamanho da população (número de cromossomos, tem que ser potência de 2)                                   |
| `--step-size`                 | float   | 1.0     | Taxa de mutação (amplitude do passo)                                           |
| `--max-steps`                 | int     | 1000    | Número máximo de gerações                                                     |
| `--tournament-rate`           | float   | 0.4     | Proporção (0–1) de indivíduos selecionados por torneio                         |
| `--tournament-size`           | int     | 4       | Número de competidores em cada torneio                                         |
| `--elitism-rate`              | float   | 0.1     | Proporção (0–1) de indivíduos mantidos por elitismo                            |
| `--crossover-rate`            | float   | 0.3     | Proporção (0–1) de indivíduos gerados por crossover                            |
| `--crossover-mutation-rate`   | float   | 0.05    | Taxa de mutação aplicada **após** crossover                                    |
| `--lottery-rate`              | float   | 0.1     | Proporção (0–1) de indivíduos sorteados “na loteria”                           |
| `--random-rate`               | float   | 0.1     | Proporção (0–1) de indivíduos escolhidos aleatoriamente                        |
| `--fps`                       | int     | 5       | Frames por segundo da animação                                                 |
| `-d`, `--depth`               | int     | 50      | Profundidade (resolução) do gráfico                                            |
| `--plot-levels`               | int     | 35      | Número de níveis para plotagem 2D  