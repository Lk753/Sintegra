# Sintegra
# 🚀 Projeto Integrador - IoT Sintegra 
_________________________________________________________________________
## 👥 Integrantes
- Isabella Rodrigues Dalforno Maciel
- Isabella São José Guedes
- Lucas Rodrigues Sousa
- Miriã da Silva Siqueira
__________________________________________________________________________ 
## 📌 Descrição
- Sistema de monitoramento inteligente utilizando ESP8266, API, banco de dados e integração com Google Sheets.

## 🎯 Objetivo
Desenvolver um sistema capaz de:
- Coletar
- Processar
- Armazenar
- Disponibilizar dados em tempo real.

________________________________________________
## 🧩 Etapas do Projeto

 01 - Configuração
Ambiente configurado e validado

02 - Investigação de Pinos
Levantamento e análise das portas do ESP8266

03 - Modelagem do Sistema
Definição das regras e comportamento do sistema

 04 - Evidências
Registros visuais e testes realizados

05 - Atualizações
Controle de mudanças e evolução do projeto
__________________________________________________________

## 🔁 Evolução do Projeto
Ver pasta: [05_Atualizacoes](https://github.com/Lk753/Sintegra/tree/8e74015cb4571359a321730dbcd30e30fd371157/atualiza%C3%A7%C3%B5es.md)

---------
## 📸 Evidências
Ver pasta: [04_Evidencias](https://github.com/Lk753/Sintegra/tree/39dcf510adb5ebcf8d5ec3e36a9b08835b26131c/Prints.md)

## 🧠 Aprendizados
- Aprendemos a configurar o ESP8266 na IDE Arduino.
- Entendemos o funcionamento das portas GPIO.
- Tivemos contato com APIs e integração com banco de dados.
- Aprendemos a enviar dados para o Google Sheets.
___________________________________________________________________________________________________________________________________
# 🖥️ Configuração do Ambiente

## 🛠️ Ambientes de Desenvolvimento (IDEs)
   
- Utilizamos o arduino IDE para escrever, compilar e gravar o código no microcontrolador ESP8266.
- foi Utilizado o vscode para o desenvolvimento do script em Python e da interface do site.

## 🐍 Linguagens e Ferramentas de Software
   
- a Linguagem que utilizamos foi o python para criar o script que recebe os dados do ESP8266 e gerencia as integrações.
- usamos o mysql para criar o Banco de dados para armazenamento histórico dos dados.

## 📦 Instalação de Dependências e Bibliotecas

Para o Python conversar com o ESP8266, com o MySQL e com o Google Sheets, foram usadas as seguintes bibliotecas e os comandos
 
python > ESP8266
- from flask import Flask, request, jsonify
- pip install fastapi uvicorn ou pip install flask

python > MySQL
- import mysql.connector
- pip install mysql-connector-python

python > Google Sheets
- import gspread
- from datetime import datetime ( essa biblioteca Pega o horário atual do computador para registrar o momento exato em que a temperatura foi lida)
- pip install gspread google-auth

## ⚙️ Configurações realizadas
- Adição da URL do ESP8266
- Instalação do pacote
- Seleção da placa
- Configuração da porta

## 🧪 Teste realizado
<img width="520" height="347" alt="image" src="https://github.com/user-attachments/assets/211d723f-cbb8-422d-9141-ad893bd89c57" />

## ⚠️ Problemas encontrados

- Algumas portas apresentaram comportamento inesperado durante o boot.
- O pino D3 apresentou conflitos de inicialização.
- Houve dificuldades na comunicação com o banco de dados.
- Ocorreram erros de conexão Wi-Fi durante testes.
- Problemas na leitura inicial do sensor DHT11.
__________________________________________________________________________________________________________________________________

# 🔌 Investigação das Portas

| PINO | PODE USAR? | TIPO               | RESTRIÇÃO                 |
|------|------------|--------------------|---------------------------|
| D0   | SIM        | BOTÃO 1            | sem restrição             |
| D1   | SIM        | BOTÃO 2            | sem restrição             |
| D2   | SIM        | TEMPERATURA        | Usado pelo DHT11          |
| D3   | NÃO        | NÃO FOI ENCONTRADO | não utilizado             |
| D4   | SIM        | RGB VERMELHO       | PWM recomendado para RGB  |
| D5   | SIM        | BUZZER             | Compatível com buzzer PWM |
| D6   | SIM        | LED VERMELHA       | saída digital             |
| D7   | SIM        | RGB AZUL           | PWM recomendado para RGB  |
| D8   | SIM        | RGB VERDE          | PWM recomendado para RGB  |
| A0   | SIM        | POTENCIÔMETRO      | Apenas entrada analógica  |


## 🌐 Fontes utilizadas
- [O que é modelo cliente/servidor](https://www.akamai.com/pt/glossary/what-is-the-client-server-model)
- [O que é TCP/IP](https://www.techtarget.com/searchnetworking/definition/TCP-IP)
- [O que é API](https://aws.amazon.com/pt/what-is/api/)
- [O que é IoT](https://aws.amazon.com/pt/what-is/iot/)
- [Como sensores e dispositivos iot se comunicam na rede](https://blog.lyram2m.com.br/como-sensores-e-dispositivos-iot-se-comunicam-na-rede/)
- [como identificar os pinos esp8266](https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/)

## 🔍 Processo de investigação

Foram feitos diversos testes antes de realmente chegarmos em um resultado certo, não tínhamos ideia de como poderia ser feito para que começássemos a identificar os componentes. 
O primeiro componente que identificamos foi o segundo botão de acionamento e logo em seguida o led vermelho. Para encontrar ele foi feito um teste utilizando os pinos D1 para o botão e D6 para o led vermelho, para que ficasse mais fácil foi feito uma pesquisa para saber como identificar no ESP8266.

## 🚨 Problemas encontrados
- Algumas portas apresentaram comportamento inesperado durante o boot.
- O pino D3 apresentou conflitos de inicialização.
- Houve dificuldades na comunicação com o banco de dados.
- Ocorreram erros de conexão Wi-Fi durante testes.
- Problemas na leitura inicial do sensor DHT11.

## 📸 Evidências
(print/foto/teste)
__________________________________________________________________________________________________________________________________

## 🧠 Modelagem do Sistema

## 1. 🗺️ Arquitetura Geral do Sistema

  O sistema é baseado no microcontrolador ESP8266, responsável por realizar a leitura dos dados de temperatura e umidade. Esses dados são enviados para um script em Python, que atua como intermediário, realizando o armazenamento e a persistência das informações em um banco de dados MySQL e, simultaneamente, integrando e atualizando as planilhas do Google Sheets. Por fim, o Google Sheets serve como fonte de dados para um site (interface web), onde os resultados de temperatura e umidade são exibidos em tempo real para o usuário.
 
## 3. 🖥️ Modelagem de Software (Fluxograma / Máquina de Estados)

🅰️ Lógica do ESP8266 e do Software (Python, MySQL e Google Sheets)

- primeiro: o ESP8266 liga, configura os pinos dos sensores/atuadores e conecta-se á internet local.
- segundo: o sensor (DHT11) faz a leitura da temperatura e da umidade do ambiente.
- terceiro: o ESP8266 envia esses valores coletados para o script Python através de uma requisição na rede.
- quarto: o sistema aguarda um intervalo de tempo definido e repete o ciclo de leitura.
- quinto: O script Python fica rodando no computador, esperando os dados que o ESP8266 vai enviar.
- sexto: Assim que o Python recebe a temperatura e a umidade, ele confere se os dados estão corretos.
- Sétimo: O Python abre uma conexão com o banco de dados MySQL e salva o registro (com data e hora) para manter um histórico local seguro.
- Oitavo: Logo em seguida, o Python envia os mesmos dados para a API do Google Sheets, inserindo uma nova linha na planilha.
- nono: O site, que está conectado à planilha do Google Sheets, atualiza a tela automaticamente para mostrar os novos gráficos e temperaturas para quem estiver navegando.

📊 Regras definidas
 
| Condição            | Estado    | Ação            |
|---------------------|-----------|-----------------|
| Temperatura alta    | ALERTA    | Aciona buzzer   |
| Botão pressionado   | ATIVO     | Liga LED        |
| Umidade baixa       | ATENÇÃO   | Envia alerta    |
| Sensor desconectado | ERRO      | Mensagem na API |

 ## 🔄 Fluxo

Entrada → Processamento → Decisão → Ação → API

Detalhes das Etapas
- Entrada: O sensor DHT11 realiza a leitura física da temperatura e da umidade do ambiente.
- Processamento: O microcontrolador ESP8266 recebe esses sinais analógicos/digitais, converte em variáveis numéricas estruturadas e envia para o script Python através de uma requisição de rede (via Flask).
- Decisão: O script Python analisa as informações recebidas, valida os dados (carimbando com a data e hora atual) e verifica se há necessidade de disparar algum alerta ou apenas registrar o histórico.
- Ação: O Python executa um comando de inserção (INSERT) para salvar os dados recebidos no banco de dados local MySQL.
- API: O Python aciona as APIs do Google (Sheets e Drive) via gspread para enviar os dados para a planilha na nuvem, atualizando automaticamente o site integrado que exibe os gráficos para o usuário.

🧩 Variáveis

- Temperatura → Capturada pelo sensor DHT11
- Umidade → Capturada pelo sensor DHT11
- Rotação → Controle ajustado por potenciômetro
- EstadoBotao → Verifica acionamento manual
- EstadoLED → Controle visual do sistema


---

💡 Justificativas

- O ESP8266 foi escolhido por possuir Wi-Fi integrado.
- O Google Sheets foi utilizado pela facilidade de visualização dos dados.
- O DHT11 foi escolhido por ser simples e adequado para testes acadêmicos.
- LEDs e buzzer foram usados para sinalização visual e sonora..

---

📌 Melhorias realizadas

- Organização das pastas do projeto
- Correção dos pinos utilizados
- Otimização da leitura dos sensores
- Melhorias na estabilidade da conexão Wi-Fi
- Integração inicial com API e banco de dados


__________________________________________________________________________________________________________________________________

04_Evidencias/  

Aqui ficam:
Fotos
Prints
Vídeos
Sugestão:
imagem1.jpg
teste_led.png
video_link.txt
__________________________________________________________________________________________________________________________________

05_Atualizacoes/
Arquivo sugerido:   atualizacoes.md

Conteúdo essencial:
# 🔁 Atualizações do Projeto
- Pasta de [05_Atualizacoes](https://github.com/Lk753/Sintegra/tree/main/Atualiza%C3%A7%C3%B5es.md)

## v1.0
- Configuração inicial

## v1.1
- Investigação de pinos
- Identificação de erro no pino D3

## v1.2
- Alteração de pino devido a falha

## v2.0
- Definição da lógica do sistema

---
## 📌 Melhorias realizadas
Descrever mudanças importantes

## 🚨 Problemas e soluções
Explicar erros e como foram corrigidos
