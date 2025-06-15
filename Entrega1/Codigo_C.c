#include <Arduino.h>
#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>  // LCD I2C

#define DHTPIN         15
#define DHTTYPE        DHT22

#define SENSOR_PH      27     // LDR simulando pH
#define FOSFORO_PIN    22     // Botão verde
#define POTASSIO_PIN   4      // Botão vermelho
#define RELE           23     // Relé bomba
#define LED            12     // LED indicador bomba

DHT dht(DHTPIN, DHTTYPE);

// LCD 16x2 no endereço padrão I2C 0x27, usando 16 colunas e 2 linhas
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(115200);
  dht.begin();
  lcd.init();         
  lcd.backlight();     // Liga o backlight do LCD

  pinMode(FOSFORO_PIN, INPUT_PULLUP);
  pinMode(POTASSIO_PIN, INPUT_PULLUP);
  pinMode(RELE, OUTPUT);
  pinMode(LED, OUTPUT);

  lcd.setCursor(0, 0);
  lcd.print("Iniciando...");
  delay(2000);
}

void loop() {
  // Otimização: float mantido por necessidade de casas decimais
  float temperatura = dht.readTemperature();    
  float umidade_solo = dht.readHumidity();      

  // Otimização: int16_t usa menos memória que int no ESP32 (2 bytes)
  int16_t ph_raw = analogRead(SENSOR_PH);
  uint8_t ph = ph_raw / 100;  // ph simplificado, otimizado para uint8_t (0–255)

  // Otimização: uso de bool ao invés de int para valores lógicos
  bool fosforo = (digitalRead(FOSFORO_PIN) == LOW);  
  bool potassio = (digitalRead(POTASSIO_PIN) == LOW);

  // Ideal para visualizar variações em tempo real
  Serial.print("Temperatura:");
  Serial.print(temperatura);
  Serial.print(",UmidadeSolo:");
  Serial.println(umidade_solo);

  Serial.printf("Temp: %.1f°C | Umidade SOLO: %.1f%% | pH: %d | Fósforo: %d | Potássio: %d\n",
                temperatura, umidade_solo, ph, fosforo, potassio);

  // === EXIBIÇÃO NO DISPLAY LCD ===
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.printf("T:%.1fC U:%.0f%%", temperatura, umidade_solo);
  lcd.setCursor(0, 1);
  lcd.printf("pH:%d F:%d P:%d", ph, fosforo, potassio);

  // === CONTROLE DA BOMBA DE ÁGUA ===
  if (umidade_solo < 60) {
    digitalWrite(RELE, HIGH);
    digitalWrite(LED, HIGH);
  } else {
    digitalWrite(RELE, LOW);
    digitalWrite(LED, LOW);
  }

  delay(2000);
}
