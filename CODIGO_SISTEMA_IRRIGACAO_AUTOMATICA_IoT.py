#define BLYNK_TEMPLATE_ID "YourTemplateID"
#define BLYNK_TEMPLATE_NAME "SmartIrrigation"
#define BLYNK_AUTH_TOKEN "YourAuthToken"

#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

char ssid[] = "SEU_WIFI";        // Nome da rede Wi-Fi
char pass[] = "SENHA_WIFI";      // Senha do Wi-Fi
char auth[] = BLYNK_AUTH_TOKEN;  // Token gerado no app Blynk

int sensorPin = A0;              // Pino analógico para sensor de umidade
int bombaPin = D1;               // Pino digital ligado ao relé da bomba
int limiteSeco = 600;            // Limite de umidade (ajustável)

void setup() {
  Serial.begin(115200);
  pinMode(bombaPin, OUTPUT);
  digitalWrite(bombaPin, LOW);  // bomba desligada inicialmente
  Blynk.begin(auth, ssid, pass);
}

void loop() {
  Blynk.run();
  
  int umidade = analogRead(sensorPin);
  Serial.print("Umidade do Solo: ");
  Serial.println(umidade);

  Blynk.virtualWrite(V0, umidade); // Envia o valor lido para o app

  if (umidade > limiteSeco) {
    digitalWrite(bombaPin, HIGH);  // Liga a bomba
    Blynk.virtualWrite(V1, 1);     // Informa bomba ligada
  } else {
    digitalWrite(bombaPin, LOW);   // Desliga a bomba
    Blynk.virtualWrite(V1, 0);     // Informa bomba desligada
  }

  delay(2000); // Tempo de espera entre leituras (pode ser substituído por timer)
}
