# Tênis Markoviano

Nesse trabalho, analisamos uma simulação de um jogo de tênis modelado por uma Cadeia de Markov. A imagem a seguir descreve o modelo utilizado:

<img src="images/match_model.png" alt="Modelo da partida em CM" width="500">

## Simulação

A simulação é feita pelo script `simulate_matches.py`. É possível gerar um arquivo em formato `.csv` executando:

    python simulate_matches.py dir/para/output.csv p n

Onde `p` é a probabilidade $p$ do jogador **A** fazer um ponto (consequentemente, a probabilidade do jogador **B** fazer um ponto $q=1-p$) e `n` é o número de partidas diferentes para simular.

A simulação também pode ser executada importanto a função `simulate_matches`:

```py
from simulate_matches import simulate_matches

simulate_matches('dir/para/output', p, n)
```

O log da partida é escrito no arquivo passado fornecido. Ele tem formato `csv` e cada linha contêm as seguintes informações: `match,set,game,state,state,point`.

- `match`: o número da partida (valores de 0 a n-1);
- `set`: o número do set;
- `game`: o número do jogo (valores de 0 a 2);
- `state`: o número da jogada;
- `state`: o estado do jogo (um dos estados especificados);
- `point`: o jogador que fez ponto na jogada (`a`, `b` ou `n`, para o estado `0-0`).

Um exemplo de arquivo de saída é:

    match,set,game,play,state,point
    0,0,0,0,0-0,n
    0,0,0,1,15-love,a
    0,0,0,2,15-15,b
    0,0,0,3,15-30,b
    0,0,0,4,15-40,b
    0,0,0,5,win_b,b
    0,0,1,0,0-0,n
    0,0,1,1,15-love,a
    0,0,1,2,30-love,a
    0,0,1,3,40-love,a
    0,0,1,4,win_a,a
    0,0,2,0,0-0,n
    0,0,2,1,love-15,b
    0,0,2,2,love-30,b
    0,0,2,3,love-40,b
    0,0,2,4,15-40,a
    0,0,2,5,win_b,b

## Metodologia

Duas partidas foram simuladas com `n=50` cada. A primeira representa uma situação em que um jogador é muito melhor que o outro ($p=0.75$ e $q=0.25$). A segunda partida representa uma situação em que ambos os jogadores possuem habilidades similares ($p=0.52$ e $q=0.48$).

Para cada caso, vamos analisar:

- A probabilidade de um jogador ganhar a partida;
- A distribuição do número de sets, games

## Resultados
Os resultados podem ser vistos integralmente no notebook `trab.ipynb`. Nele, mostramos alguns comentários dos resultados e o código gerador, além de alguns gráficos que ajudam na análise.

No texto abaixo, as regiões com fundo cinza são referentes à saída dos códigos em Python utilizados para a análise, e também podem ser conferidas no notebook.

### Partida 1
#### Análise das vitórias dos jogadores
Vamos fazer uma análise da probabilidade de cada jogador ganhar na partida 1. Para isso, o dataset foi dividido em 3 e verificou-se, de 3 em 3 partidas, quantas o jogador A e o jogador B ganham, obtendo como saída:
```
Player A won 120 and Player B won 0
```

Vamos calcular o valor médio de vitórias a cada 3 partidas, assim como o desvio padrão para a nossa amostra:
```
A's average: 3.0
A's standard deviation: 0.0
B's average: 0.0
B's standard deviation: 0.0
```

#### Probabilidades analíticas
Vamos analisar o jogo como uma Cadeia de Markov e calcular a probabilidade real dos jogadores ganharem as partidas:
```
Probability of A to win a match: 0.9999999999999997
Probability of B to win a match: 3.3306690738754696e-16
```
A probabilidade de um jogador ganhar a partida é dada por $ \mu = \sum {x_i*P(x_i)} $, sendo que $P(x_i)$ é a probabilidade do jogador ganhar um número $x_i$ de partidas (nesse caso, $x_i = i$). Essas probabilidade são, para o jogador A e B respectivamente, dadas pelas seguintes expressões:

$$ P_A(x_i) = \binom{3}{i}(1-p_a)^{3-i}*p_a^i,\space i=0,1,2,3 $$
$$ P_B(x_i) = \binom{3}{i}(1-p_a)^i*p_a^{3-i},\space i=0,1,2,3 $$

Onde $p_a$ é a probabilidade do jogador A ganhar uma partida. O desvio padrão é dado por $ \sigma = \sqrt { \sum {(x_i - \mu)^2*P(x_i)} } $, onde $\mu$ é o valor médio do número de partidas ganhas. Uma análise analítica mais aprofundada sobre pontos, games, sets e partidas com possibilidade de tie break pode ser encontrada no [link](https://datagenetics.com/blog/august12018/index.html).

Vamos, então, computar os valores médios e desvios padrões reais para A e B:
```
A's real average: 3.0000e+00
A's real standard deviation: 3.1610e-08
B's real average: 9.9920e-16
B's real standard deviation: 3.1610e-08
```

Percebemos que, realmente, o valor médio de partidas ganhas é muito próximo de 3 para A e muito próximo de 0 para B. O desvio padrão para ambos é, também, muito próximo de 0.

Vamos observar a relação entre $p$ e $p_a$ (além da probabilidade de se ganhar um game e um set):
<img src="images\probabilities_for_given_p.png" width="500">

Como podemos ver, a probabilidade do jogador ganhar a partida é extremamente sensível à diferença de habilidade dos jogadores $p$. Além disso, percebemos que a sensibilidade à $p$ aumenta quando observamos a probabilidade de se ganhar um ponto, um jogo e um set.

#### Análise de sets, games e pontos
Podemos realizar também análises individuais a cerca dos sets, games e pontos, verificando o impacto da diferença entre os jogadores nos resultados.
```
Player A won 100.00% sets and Player B won 0.00% sets
Player A won 95.36% games and Player B won 4.64% games
Player A won 75.36% points and Player B won 24.64% points
```

Observa-se que além de perder todos os jogos, o segundo jogador também perdeu todos os sets. Nos games é possível observar os primeiros resultados positivos deste jogador, e nos pontos tem-se uma proporção próxima da probabilidade de cada jogador.
```
A's average: 2.00
A's standard deviation: 0.00
B's average: 0.00
B's standard deviation: 0.00
```

O resultado acima é o esperado, visto que o jogador B não ganhou nenhum set. Já observando os games, podemos notar diferenças:
```
A's average: 12.00
A's standard deviation: 0.00
B's average: 0.58
B's standard deviation: 0.85
```

Já é possível perceber valores de média para B diferentes de 0, porém ainda muito baixos em relação ao jogador vencedor. Nos pontos tem-se maior proximidade entre os jogadores:
```
A's average: 51.50
A's standard deviation: 3.00
B's average: 16.84
B's standard deviation: 5.97
```
<img src="images\boxplot1.png" width="500">

E assim podemos concluir que uma probabilidade maior de marcar pontos contra o adversário resulta em probabilidades ainda muito mais expressivas de vitória quando relacionadas a partes maiores do jogo, como games e sets.

### Partida 2
#### Análise do número de vitórias para a partida 2
```
Player A won 84 and Player B won 36
```

Vamos verificar a média de vitórias em cada 3 partidas para $p=0.52$
```
A's average: 2.1000
A's standard deviation: 0.8307
B's average: 0.9000
B's standard deviation: 0.8307
```
<img src="images\match.png" width="500">

Percebemos que, agora, os dois jogadores possuem habilidades bem similares, o que significa que o jogador B possui muito mais chances de vencer. Ainda assim, o jogador A possui muita vantagem em cima do jogador B, ganhando 2 em 3 partidas.

#### Valores reais de probabilidade
Novamente, vamos calcular analiticamente a média de jogos ganhos dentre os 3:
```
Probability of A to win a match: 0.7493
Probability of B to win a match: 0.2507
```

```
A's real average: 2.2478
A's real standard deviation: 0.7507
B's real average: 0.7522
B's real standard deviation: 0.7507
```

Percebemos que os valores obtidos da análise da simulação é bem próximo do que foi obtido analiticamente.

Novamente, observamos a sensibilidade da vitória à probabilidade $p$. Com uma diferença de apenas $0.04$ de habilidade, o jogador A consegue vencer pelo menos duas partidas em cada 3.

#### Análise de sets, games e pontos para a partida 2
Como realizado na partida 1, verificaremos os efeitos das probabilidades de ponto na quantidade de sets, games e pontos ganhos na partida 2.
```
Player A won 64.00% sets and Player B won 36.00% sets
Player A won 55.01% games and Player B won 44.99% games
Player A won 52.02% points and Player B won 47.98% points
```

Percebe-se que as probabilidades próximas também aproximam consideravelmente as vitórias dentro do jogo em níveis além da partida, apresentando resultados interessantes.
```
A's average: 1.60
A's standard deviation: 0.66
B's average: 0.90
B's standard deviation: 0.83
```

Nos sets conseguimos observar valores não tão distantes de média e muito próximos de desvio padrão, mostrando assim regularidade nas simulações. Podemos com isso, esperar comportamento semelhante nos games e pontos:
```
A's average: 13.14
A's standard deviation: 3.01
B's average: 10.75
B's standard deviation: 4.41
```
```
A's average: 83.38
A's standard deviation: 20.47
B's average: 76.90
B's standard deviation: 24.36
```

<img src="images\boxplot2.png" width="500">

Como esperado, conseguimos ver que as médias e os desvios entre os dois jogadores são próximos em todas as medidas, demonstrando assim consistência nos resultados obtidos pela simulação.

### Análise com 12 amostras
Realizaremos agora análises com apenas 12 amostras, com o intuito de observar como a limitação do número de simulações pode afetar nos resultados finais de média e desvio padrão.

#### Partida 1
##### Estatísticas de vitórias e derrotas
```
Player A won 12 matches and Player B won 0 matches
Player A won 24 sets and Player B won 0 sets
Player A won 144 games and Player B won 13 games
Player A won 628 points and Player B won 225 points
```
```
n=12
A's average: 3.0000
A's standard deviation: 0.0000
B's average: 0.0000
B's standard deviation: 0.0000

n=120
A's average: 3.0000
A's standard deviation: 0.0000
B's average: 0.0000
B's standard deviation: 0.0000
```
<img src="images\match_distribution1.png" width="500">

##### Estatísticas para sets
```
n=12
A's average: 2.00
A's standard deviation: 0.00
B's average: 0.00
B's standard deviation: 0.00

n=120
A's average: 2.00
A's standard deviation: 0.00
B's average: 0.00
B's standard deviation: 0.00
```

##### Estatísticas para games
```
n=12
A's average: 12.00
A's standard deviation: 0.00
B's average: 1.08
B's standard deviation: 1.11

n=120
A's average: 12.00
A's standard deviation: 0.00
B's average: 0.58
B's standard deviation: 0.85
```

##### Estatísticas para pontos
```
n=12
A's average: 52.33
A's standard deviation: 2.75
B's average: 18.75
B's standard deviation: 5.66

n=120
A's average: 51.50
A's standard deviation: 3.00
B's average: 16.84
B's standard deviation: 5.97
```

##### Análise geral
<img src="images\distribution11.png" width="500"> <br>
<img src="images\distribution12.png" width="500">

Percebemos principalmente nos pontos uma diferença considerável no desvio padrão dos resultados, sendo superiores principalmente na contagem de pontos.

#### Partida 2
##### Estatísticas de vitórias e derrotas
```
Player A won 9 matches and Player B won 3 matches
Player A won 19 sets and Player B won 9 sets
Player A won 156 games and Player B won 125 games
Player A won 1032 points and Player B won 951 points
```
```
n=12
A's average: 2.2500
A's standard deviation: 0.4330
B's average: 0.7500
B's standard deviation: 0.4330

n=120
A's average: 2.1000
A's standard deviation: 0.8307
B's average: 0.9000
B's standard deviation: 0.8307
```
<img src="images\distribution21.png" width="500">
<img src="images\distribution22.png" width="500">

##### Estatísticas para sets
```
n=12
A's average: 1.58
A's standard deviation: 0.76
B's average: 0.75
B's standard deviation: 0.83

n=120
A's average: 1.60
A's standard deviation: 0.66
B's average: 0.90
B's standard deviation: 0.83
```

##### Estatísticas para games
```
n=12
A's average: 13.00
A's standard deviation: 3.81
B's average: 10.42
B's standard deviation: 4.80

n=120
A's average: 13.14
A's standard deviation: 3.01
B's average: 10.75
B's standard deviation: 4.41
```

##### Estatísticas para pontos
```
n=12
A's average: 86.00
A's standard deviation: 26.14
B's average: 79.25
B's standard deviation: 27.83

n=120
A's average: 83.38
A's standard deviation: 20.47
B's average: 76.90
B's standard deviation: 24.36
```

##### Análise geral
<img src="images\distribution31.png" width="500"> <br>
<img src="images\distribution32.png" width="500">

Já na segunda partida, vemos que os resultados não apresentam alteração significativa. Isso pode ser percebido principalmente pelo fato da probabilidade igual de cada jogador ganhar um ponto.