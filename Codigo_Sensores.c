#include <Arduino.h>
#include <DHT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>  // LCD I2C

//Pinos
#define DHTPIN         15
#define DHTTYPE        DHT22

#define SENSOR_PH      27     // LDR simulando pH
#define FOSFORO_PIN    22     // Botão verde
#define POTASSIO_PIN   4      // Botão vermelho
#define RELE           23     // Relé bomba
#define LED            12     // LED indicador bomba

// Módulo do LCD
#define I2C_ADDR 0x27
#define LCD_COLUMNS 16
#define LCD_ROWS 2

// Pinos SCL e SDA para o ESP32
#define I2C_SDA 21  
#define I2C_SCL 22 

// Objeto para o LCD 
LiquidCrystal_I2C lcd(I2C_ADDR, LCD_COLUMNS, LCD_ROWS);

DHT dht(DHTPIN, DHTTYPE);


// Setup
void setup() {
  Serial.begin(115200);
  dht.begin();
  lcd.init();         
  lcd.backlight();   

  pinMode(FOSFORO_PIN, INPUT_PULLUP);
  pinMode(POTASSIO_PIN, INPUT_PULLUP);
  pinMode(RELE, OUTPUT);
  pinMode(LED, OUTPUT);

  Wire.begin(I2C_SDA, I2C_SCL);
    
  lcd.begin(LCD_COLUMNS, LCD_ROWS);  // Inicializa o LCD 
  lcd.backlight(); 

  lcd.setCursor(0, 0);  // Posiciona o cursor na primeira coluna da primeira linha
  lcd.print("Iniciando");  // Exibe a mensagem
  lcd.setCursor(0, 1);  
  lcd.print("Lendo dados");
  delay(2000);
}

// Loop
void loop() {
  // Otimização: float 
  float temperatura = dht.readTemperature();    
  float umidade_solo = dht.readHumidity();      

  // Otimização: int16_t usa menos memória que int no ESP32
  int16_t ph_raw = analogRead(SENSOR_PH);
  uint8_t ph = ph_raw / 100;  // otimizado para uint8_t (0–255)

  // Otimização: uso de bool ao invés de int para valores lógicos
  bool fosforo = (digitalRead(FOSFORO_PIN) == LOW);  
  bool potassio = (digitalRead(POTASSIO_PIN) == LOW);

  // Monitor Serial
  Serial.print("Temperatura:");
  Serial.print(temperatura);
  Serial.print(",UmidadeSolo:");
  Serial.println(umidade_solo);

  Serial.printf("Temp: %.1f°C | Umidade SOLO: %.1f%% | pH: %d | Fósforo: %d | Potássio: %d\n",
                temperatura, umidade_solo, ph, fosforo, potassio);

  // LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.printf("T:%.1fC U:%.0f%%", temperatura, umidade_solo);
  lcd.setCursor(0, 1);
  lcd.printf("pH:%d F:%d P:%d", ph, fosforo, potassio);

  // Bomba de água
  if (umidade_solo < 60) {
    digitalWrite(RELE, HIGH);
    digitalWrite(LED, HIGH);
  } else {
    digitalWrite(RELE, LOW);
    digitalWrite(LED, LOW);
  }

  delay(2000);
}

