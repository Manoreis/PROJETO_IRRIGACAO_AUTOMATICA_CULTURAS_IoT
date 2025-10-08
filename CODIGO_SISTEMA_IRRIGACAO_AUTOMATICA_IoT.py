#define BLYNK_PRINT Serial
#define BLYNK_TEMPLATE_ID "YourTemplateID"
#define BLYNK_TEMPLATE_NAME "SmartIrrigation"
#define BLYNK_AUTH_TOKEN "YourAuthToken"

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <BlynkTimer.h>

// Credenciais Wi-Fi
char ssid[] = "SEU_WIFI";
char pass[] = "SENHA_WIFI";

// Token do Blynk
char auth[] = BLYNK_AUTH_TOKEN;

// Pinos
const int sensorPin = A0;    // Sensor de umidade (YL-69)
const int bombaPin  = D1;    // Relé conectado à bomba

// Configurações
const int LIMIAR_SECO = 600; // Valores < 600 = solo seco (ajustável conforme calibração)
const unsigned long INTERVALO_LEITURA = 10000; // 10 segundos entre leituras
const unsigned long TEMPO_IRRIGACAO = 10000;  // 10 segundos de irrigação

// Estado do sistema
bool bombaLigada = false;
unsigned long tempoInicioIrrigacao = 0;

// Timer do Blynk
BlynkTimer timer;

// Função para ler sensor e decidir irrigação
void verificaUmidade() {
  int umidade = analogRead(sensorPin);
  Blynk.virtualWrite(V0, umidade); // Envia para o app
  Serial.print("Umidade do solo: ");
  Serial.println(umidade);

  unsigned long tempoAtual = millis();

  // Se a bomba NÃO está ligada
  if (!bombaLigada) {
    if (umidade < LIMIAR_SECO) {
      // Solo seco → liga bomba por 10s
      digitalWrite(bombaPin, HIGH);
      bombaLigada = true;
      tempoInicioIrrigacao = tempoAtual;
      Blynk.virtualWrite(V1, 1); // Bomba ligada
      Serial.println(">>> Solo seco! Irrigando por 10s...");
    } else {
      digitalWrite(bombaPin, LOW);
      Blynk.virtualWrite(V1, 0); // Bomba desligada
    }
  }
  // Se a bomba ESTÁ ligada, verifica se já passou o tempo
  else {
    if (tempoAtual - tempoInicioIrrigacao >= TEMPO_IRRIGACAO) {
      digitalWrite(bombaPin, LOW);
      bombaLigada = false;
      Blynk.virtualWrite(V1, 0);
      Serial.println(">>> Irrigação concluída.");
    }
    // Caso contrário, mantém ligada (não faz nada aqui)
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(bombaPin, OUTPUT);
  digitalWrite(bombaPin, LOW); // Garante que a bomba inicie desligada

  Blynk.begin(auth, ssid, pass);
  timer.setInterval(INTERVALO_LEITURA, verificaUmidade); // Lê a cada 10s
}

void loop() {
  Blynk.run();
  timer.run(); // Executa o timer sem bloquear
}
