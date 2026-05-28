#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include "DHT.h" // Importa a biblioteca do sensor de temperatura

// --- CONFIGURAÇÃO DO HARDWARE ---
#define DHTPIN D2          // Pino onde você vai ligar o sinal do Sensor DHT (Pino D2)
#define DHTTYPE DHT11      // Se o seu sensor for o azul use DHT11, se for o branco mude para DHT22
#define BUZZER_PIN D5      // Pino onde você vai ligar o positivo do Buzzer (Pino D5)

DHT dht(DHTPIN, DHTTYPE);

// --- CONFIGURAÇÃO DO WIFI ---
const char* ssid     = "Cyber-Projeto";  
const char* password = "Senai@122";   

// --- CONFIGURAÇÃO DA API ---
String servidor = "http://10.106.208.16:8000/temperatura";
const char* token_secreto = "arduinoplayboyzin";

// --- FUNÇÃO PARA O BUZZER ---
void apitarBuzzer(int vezes) {
  for (int i = 0; i < vezes; i++) {
    tone(BUZZER_PIN, 2700); // Frequência para o som ficar mais alto
    delay(150);             
    noTone(BUZZER_PIN);     
    delay(100);             
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Inicialização do Hardware
  pinMode(BUZZER_PIN, OUTPUT);
  dht.begin(); 

  Serial.println("\n--- INICIANDO CONEXÃO WIFI ---");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ Wi-Fi conectado com sucesso!");
  
  // Apita duas vezes rápido para avisar que conectou
  apitarBuzzer(2);

  // Registro de boot do sistema
  enviarDadosParaAPI("ESP8266_SISTEMA", 0); 
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    
    // --- CAPTURA DA TEMPERATURA ATUAL DO AMBIENTE ---
    float valorTemperatura = dht.readTemperature(); 

    // Verifica se o sensor está bem conectado ou falhou
    if (isnan(valorTemperatura)) {
      Serial.println("❌ Erro ao ler o sensor DHT! Verifique os cabos.");
    } else {
      String sensorID = "ESP8266_Senai";

      // Apita assim que capturar a temperatura com sucesso
      apitarBuzzer(1); 

      // Envia a temperatura real para a API
      enviarDadosParaAPI(sensorID, valorTemperatura);
    }

  } else {
    Serial.println("❌ WiFi desconectado. Tentando reconectar...");
    WiFi.begin(ssid, password);
  }

  delay(20000); // Aguarda 20 segundos para a próxima leitura
}

// --- FUNÇÃO DE ENVIO PARA A API ---
void enviarDadosParaAPI(String sensor, float valor) {
  WiFiClient client;
  HTTPClient http;

  String urlEnvio = servidor + "?sensor=" + sensor + "&temperatura=" + String(valor) + "&token=" + String(token_secreto);

  Serial.print("\n[IoT] Enviando para: ");
  Serial.println(urlEnvio);

  http.begin(client, urlEnvio);
  int httpResponseCode = http.GET();

  if (httpResponseCode > 0) {
    Serial.print("[API] Código de Resposta HTTP: ");
    Serial.println(httpResponseCode); 
    
    if (httpResponseCode == 200) {
      Serial.println("✅ Sucesso: Dados salvos no Banco e no Sheets!");
    } else if (httpResponseCode == 401) {
      Serial.println("❌ Erro de Segurança: Token rejeitado!");
    }
  } else {
    Serial.print("❌ Erro de rede. Código: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}