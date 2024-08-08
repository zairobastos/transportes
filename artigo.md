### 1. Metodologia

Esta seção detalha a abordagem metodológica utilizada para prever séries temporais com o auxílio de Large Language Models (LLMs). A metodologia é dividida em cinco subseções principais: Conjunto de Dados, LLMs Utilizadas, Prompt Elaborado, Ambiente de Execução dos Testes e Avaliação. Cada subseção é descrita a seguir:

##### 1.1 Conjunto de Dados

Esta subseção detalha os conjuntos de dados utilizados e explica a modelagem dos dados realizada para conduzir esta pesquisa. Foram utilizados dois conjuntos de dados: um de embarques em linhas de ônibus e um de vendas de produtos do varejo. Estes dados possuem padrões distintos e foram modelados como entrada para o prompt que será passado para os modelos largos de linguagem, com o intuito de prever a quantidade de embarques e de vendas vários passos à frente.

###### 1.1.1 Vendas de Produtos em um Supermercado:

O primeiro conjunto de dados trata de séries temporais de vendas de produtos de uma loja do varejo, do setor de supermercado, localizado em Fortaleza (Ceará). Os dados foram obtidos de uma grande varejista, através de um projeto de pesquisa em parceria com a Universidade de Fortaleza. Foram obtidas informações de vendas de vinte produtos da curva A (itens com maior contribuição no faturamento da loja) em um período de 02 de Janeiro de 2017 a 30 de Abril de 2019, totalizando cerca de 850 dias. As vendas dos produtos, por unidades ou por quilogramas, foram agrupadas por dias para cada um dos produtos analisados, e montadas as séries temporais finais. Os identificadores dos produtos foram anonimizados. Os peŕiodo de 2 de Janeiro de 2017 a 2 de Janeiro de 2019 foram separados como treino e o restante do mês de Janeiro de 2019 a Abril de 2019 como teste. A Figura 1(A) ilustra uma série temporal de venda por dia de um produto da curva A em uma amostra de 240 dias.

Nesse dataset, não houve necessidade de realizar correções no dataset de vendas de produtos, uma vez que essa base de dados foi recebida sem nenhum tipo de dado duplicado ou incorreto. Isso nos permitiu utilizar diretamente as informações para a modelagem e previsão, garantindo um processo mais eficiente e ágil.

###### 1.1.2 Linhas de Ônibus de Fortaleza:

O segundo conjunto de dados trata de séries temporais do número de embarques de passageiros nas vinte linhas de ônibus com maior uso dentro do sistema de transporte público na cidade de Fortaleza (Ceará). Os passageiros do sistema de ônibus possuem um smart card com o identificador do usuário e, toda vez que este cartão é usado, um registro de embarque é gravado. Os dados foram cedidos pela Prefeitura de Fortaleza e foram utilizados em outros artigos [Caminha et al. 2018][Ponte et al. 2018][Bomfim et al. 2020][Ponte et al. 2021]. Estes dados correspondem a um intervalo de 1º de Janeiro de 2018 a 31 de Julho de 2018 e os valores de número de embarque de passageiros foram agrupados por hora para cada uma das vinte linhas de ônibus com mais embarques na cidade. Desta forma, foram geradas vinte séries temporais com mais de 5000 horas de embarques para cada linha de ônibus. Os meses de Janeiro a Junho foram separados como treino e o mês de Julho como teste. A Figura 1(B) ilustra uma série temporal de embarque por hora de uma linha de ônibus, detalhando os padrões de sazonalidade que ocorrem nos veículos em uma amostra de cerca de 10 dias.

Durante a preparação dos dados, identificamos a presença de alguns dados duplicados e a ausência de informações em determinados horários. Especificamente, houve linhas de ônibus que não operavam em certos horários da madrugada, resultando em registros faltantes. Para garantir a integridade do conjunto de dados, realizamos as seguintes correções:

* **Remoção de Dados Duplicados:** Todos os registros duplicados foram identificados e removidos para evitar influências indevidas nas previsões.
* **Tratamento de Dados Faltantes:** Para os horários em que certas linhas de ônibus não operavam, imputamos o valor zero para o número de passageiros, refletindo a ausência de operação nestes períodos.

Essas correções foram essenciais para garantir a precisão e a consistência das análises subsequentes. Após uma análise exploratória em ambos os conjuntos de dados, foi identificado que existiam dados não contíguos, ou seja, entradas de dados faltantes. Estes dados faltantes indicam momentos em que não ocorrem embarques de passageiros em uma certa hora do dia ou não ocorreram vendas de um determinado produto no dia. Desta forma, estes momentos foram preenchidos com valores zeros, com o objetivo de não romper com a estrutura temporal da série.

Ambos os conjuntos de dados foram selecionados pela sua capacidade de capturar variabilidades temporais complexas e pela presença de eventos periódicos e não periódicos, oferecendo um rico cenário para testar a eficácia das LLMs na previsão de séries temporais.


### Modelo Largo de Linguagem Utilizadas

Este trabalho propõe a criação de um prompt genérico que possa ter excelentes resultados em diferentes modelos largos de linguagem, com o objetivo de prever
