#include <LiquidCrystal.h>

// --- DEFINIÇÕES DE PINOS ---
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Sensores e Atuadores (CONFIRMADOS NO SEU PRINT)
const int pinoTemperatura = A0;  // Sensor TMP36
const int pinoUmidade     = A2;  // Sensor YL-69
const int pinoPiezo       = 10;  // Buzzer
const int pinoMotor       = 7;   // Motor DC

// --- LIMITES ---
const int   LIMITE_IRRIGACAO   = 450;   // Limite analógico para irrigar
const float LIMITE_TEMPERATURA = 25.0;  // Limite em °C para acionar alarme

// --- FUNÇÃO DE CONVERSÃO DE TEMPERATURA (PARA TMP36) ---
float get_temperatura() {
  int leitura = analogRead(pinoTemperatura);
  float tensao = leitura * (5.0 / 1024.0);  // Converte para Volts
  return (tensao - 0.5) * 100.0; // Conversão TMP36 (500mV = 0°C, 10mV/°C)
}

// --- SETUP ---
void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  pinMode(pinoPiezo, OUTPUT);
  pinMode(pinoMotor, OUTPUT);
  lcd.noCursor();
  lcd.setCursor(0, 0);
  lcd.print("Autoirrigacao V2");
  delay(2000);
  lcd.clear();
}

// --- LOOP PRINCIPAL ---
void loop() {
  int umidadeRaw = analogRead(pinoUmidade);
  float temperatura = get_temperatura();

  // --- ATUALIZAÇÃO DO DISPLAY ---
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temperatura, 1);
  lcd.print((char)223); // Símbolo de grau
  lcd.print("C      "); // Espaços extras para limpar a linha

  lcd.setCursor(0, 1);
  lcd.print("Umidade: ");

  // --- CONTROLE DO BUZZER ---
  if (temperatura >= LIMITE_TEMPERATURA) {
    digitalWrite(pinoPiezo, HIGH);
  } else {
    digitalWrite(pinoPiezo, LOW);
  }

  // --- CONTROLE DA IRRIGAÇÃO ---
  if (umidadeRaw < LIMITE_IRRIGACAO) {
    digitalWrite(pinoMotor, HIGH);
    lcd.print("IRRIGANDO!");
  } else {
    digitalWrite(pinoMotor, LOW);
    lcd.print("OK        ");
  }

  // --- MONITOR SERIAL (opcional) ---
  Serial.print("Temp: ");
  Serial.print(temperatura);
  Serial.print(" C | Umidade: ");
  Serial.println(umidadeRaw);

  delay(500);
}
