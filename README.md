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

# Entregar

Desafios e Requisitos da FASE 4:

Incorporar Scikit-learn: utilize a biblioteca Scikit-learn para aprimorar a inteligência do sistema de irrigação automatizado. Você pode criar um modelo preditivo que, com base nos dados coletados, sugira ações futuras de irrigação. Por exemplo, com base no histórico de umidade e nutrientes, o sistema pode prever a necessidade de irrigação em horários específicos do dia.
Implementar Streamlit: aprimore o dashboard do projeto utilizando Streamlit, criando uma interface interativa onde os dados do sistema de irrigação podem ser visualizados em tempo real. Isso pode incluir gráficos da variação da umidade do solo, níveis de nutrientes, além de insights gerados pelo modelo de Machine Learning.
Adicionar display LCD no Wokwi: use um display LCD conectado ao ESP32 no Wokwi, barramento I2C (pinos SDA e SCL), para mostrar as principais métricas em tempo real, umidade, níveis de nutrientes e status da irrigação. Esse display deve ser utilizado para exibir informações críticas diretamente no sistema físico.
Monitoramento com Serial Plotter: implemente o uso do Serial Plotter para monitorar uma ou mais variáveis do seu projeto (por exemplo, umidade). O gráfico do Serial Plotter deve apresentar as mudanças em tempo real, ajudando na análise visual do comportamento do sistema.
Otimização de Memória no ESP32: revise e otimize o uso das variáveis no código C/C++ do ESP32. Realize otimizações quando utilizar tipos de dados inteiros, floats e chars para economizar memória, garantindo que o sistema rode de maneira mais eficiente. Além disso, comente no código as modificações feitas para justificar as escolhas de otimização. 
Entregáveis da FASE 4:

a) Herança da Fase 3: copie (função Fork) do repositório da Fase 3 e renomeie como FASE 4. Esse repositório tem que estar no template Github do tutor Lucas. Caso não esteja desde a Fase 3, precisa adequar o seu projeto da FarmTech Solutions agora na Fase 4, sob pena de redução de nota;

b) Código C/C++ otimizado: apresente um código revisado e otimizado no ESP32 que gerencie os sensores e exiba os dados no display LCD;

c) Banco de dados: aprimore o seu banco de dados, revisando o modelo de negócio da sua FarmTech Solutions;

d) Código Python com Scikit-learn e Streamlit: apresente o código Python responsável pela modelagem preditiva usando Scikit-learn e a interface interativa com Streamlit.

e) Integração do Serial Plotter: faça a demonstração do uso do Serial Plotter usando prints da sua tela do Wokwi para monitoramento de variáveis e poste no REDME, e explique os prints inseridos;

f) Documentação e atualização no GitHub: atualize de forma geral o repositório GitHub com a documentação do README explicando as melhorias implementadas, além das imagens e/ou prints;

g) Vídeo: grave um vídeo de até 5 minutos demonstrando o funcionamento do sistema atualizado, poste no Youtube de forma “não listada” e coloque o link no seu GitHub, dentro do README.
