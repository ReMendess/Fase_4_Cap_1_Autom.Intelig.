# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Cap 1 - Construindo uma Máquina Agrícola

<div align="center">

|        Grupo             |                   RM                   |
|:------------------------:|:--------------------------------------:|
| **Arthur Luiz Rosado Alves** | RM562061                          |
| **Renan de Oliveira Mendes** | RM563145                          |

</div>

# Sensores

Nessa Fase 4, aprimoramos nosso sensores. Adicionamos um display LCD, para mostrar em tempo real os valores lidos.
Utilizamos o Serial Plotter para visualizar graficamente de forma rápida os valores, diretamente de nosso sistema físico.
Melhoramos a performance de memória de nosso ESP32, utilizando váriaves com tipos especificos e mais precisos para cada utilização.

Nossa aplicação na fase anterior:

<p align="center">
<img src="assets/wokwi_1.jpg" ></a>
</p>

## Display LCD
Adicionamos um display LCD 16x2, barramento I2C (pinos SDA e SCL), para exibir os dados captados de Temperatura, Umidade, pH, Fósforo e Potássio.
Dessa forma o usuário consegue ter um feedback em tempo real no local de operação, por meio de uma interface simples.


<p align="center">
<img src="assets/wokwiw.png" ></a>
</p>

## Serial Plotter
Também implementamos o uso de Serial Plotter para disponibilizar uma análise gráfica para o operador ou usuário.

<p align="center">
<img src="assets/wokwi5.png" ></a>
</p>


## Otimização
Otimizamos nosso código C, realizando a alteração do tipo de algumas variáveis, utilizando int16_t e unit8_t para economizar memória e melhorar o desempenho.

<p align="center">
<img src="assets/wokwi.png" ></a>
</p>


# Banco de Dados
Aprimoramos nosso banco de dados, adicionando novas tabelas, melhorando o código e permitindo novas funcionalidades.

## Novas Tabelas
Adicionamos duas novas tabelas: Temperatura e Umidade.

<p align="center">
<img src="assets/banco_dados5.png" ></a>
</p>


## Novas Funcionalidades
Atualizamos nossa aplicação CRUD para permitir a manipulação de dados considerando as novas tabelas.
Adicionamos também uma nova funcionalidade que permite exportar um arquivo csv com os dados de determinado sensor.

<p align="center">
<img src="assets/banco_dados1.png" ></a>
</p>

<p align="center">
<img src="assets/banco_dados.png" ></a>
</p>
<p align="center">
<img src="assets/banco_dados3.png" ></a>
</p>

# Análise e Predição com Streamlit
Desenvolvemos uma aplicação com a biblioteca Scikit-learn e Streamlit.
Realizamos o tratamento e análise dos dados. Plotamos graficos e criamos um modelo preditivo que verificar a necessidade de irrigação.
Link da aplicação: https://fase4cap1automintelig-n3hqyyxxjbmt2qtkguk38y.streamlit.app

## Simulando Dados
Criamos uma função de gerar dados, levando em conta alguns aspectos e correlações entre as variáveis.
<p align="center">
<img src="assets/simular_dados.png" ></a>
</p>

## Análise Exploratória
Realizamos a análise e uma exploração estatística dos dados.
Plotamos vários graficos, e utilizando as ferramentas do Streamlit, disponibilizamos uma feature que permite o usuário plotar outro determinado gráfico.
Apenas filtrando e escolhendo pela barra vertical no lado esquerdo.

<p align="center">
<img src="assets/analise_exp.png" ></a>
</p>

<p align="center">
<img src="assets/analise_exp2.png" ></a>
</p>

<p align="center">
<img src="assets/analise_exp3.png" ></a>
</p>

## Modelos de Predição com Scikit-learn
Utilizando os dados trabalhado e a biblioteca Scikit-learn, treinamos dois modelo para apoiar na decisão de necessidade irrigação.
O primeiro modelo leva em conta o limiar de umidade, que é um valor de referência para determinar se o solo ou ambiente está suficientemente úmido para precisar de irrigação.
Dessa forma, o modelo consegue tomar a decisão de ativar a irrigação de forma autonoma e automatica, levando em conta as medições atuais.
Utilizamos RandomForestClassifier para classificar a necessidade de irrigação.
Exemplo:
Se a umidade estiver abaixo do limiar, significa que está seco demais, logo precisa irrigar.
Se a umidade estiver acima do limiar, significa que está úmido o suficiente, dessa forma não precisa irrigar.

<p align="center">
<img src="assets/modelo.png" ></a>
</p>

O segundo modelo utiliza RandomForestRegressor para estimar a umidade média das regiões, nos próximos 12 meses.
Esse modelo tem uma abordagem mais estratégica e contribui na preparação, cálculo de custos, e planejamento operacional previsto para as próximas safras.

<p align="center">
<img src="assets/modelo2.png" ></a>
</p>


<p align="center">
<img src="assets/modelo3.png" ></a>
</p>







