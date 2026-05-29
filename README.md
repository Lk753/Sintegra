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
Ver pasta: [04_Evidencias]Prints.md/Evidências

## 🧠 Aprendizados
- Aprendemos a configurar o ESP8266 na IDE Arduino.
- Entendemos o funcionamento das portas GPIO.
- Tivemos contato com APIs e integração com banco de dados.
- Aprendemos a enviar dados para o Google Sheets.
___________________________________________________________________________________________________________________________________

01_Configuracao/
Arquivo sugerido:  configuracao.md

Conteúdo esperado:

# 🖥️ Configuração do Ambiente

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

02_Investigacao_Pinos/  
Arquivo sugerido:  investigacao.md

Conteúdo esperado:

# 🔌 Investigação das Portas

## 🌐 Fontes utilizadas
- [O que é modelo cliente/servidor](https://www.akamai.com/pt/glossary/what-is-the-client-server-model)
- [O que é TCP/IP](https://www.techtarget.com/searchnetworking/definition/TCP-IP)
- [O que é API](https://aws.amazon.com/pt/what-is/api/)
- [O que é IoT](https://aws.amazon.com/pt/what-is/iot/)
- [Como sensores e dispositivos iot se comunicam na rede](https://blog.lyram2m.com.br/como-sensores-e-dispositivos-iot-se-comunicam-na-rede/)
- [como identificar os pinos esp8266](https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/)

## 🔍 Processo de investigação


## 📊 Tabela de resultados
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

## 🚨 Problemas encontrados
- Algumas portas apresentaram comportamento inesperado durante o boot.
- O pino D3 apresentou conflitos de inicialização.
- Houve dificuldades na comunicação com o banco de dados.
- Ocorreram erros de conexão Wi-Fi durante testes.
- Problemas na leitura inicial do sensor DHT11.

## 📸 Evidências
(print/foto/teste)
__________________________________________________________________________________________________________________________________

03_Modelagem_Sistema/  
Arquivo sugerido:   modelagem.md

Conteúdo esperado:

🧠 Modelagem do Sistema

📊 Regras definidas
 
| Condição            | Estado    | Ação            |
|---------------------|-----------|-----------------|
| Temperatura alta    | ALERTA    | Aciona buzzer   |
| Botão pressionado   | ATIVO     | Liga LED        |
| Umidade baixa       | ATENÇÃO   | Envia alerta    |
| Sensor desconectado | ERRO      | Mensagem na API |

 🔄 Fluxo

Entrada → Processamento → Decisão → Ação → API

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
