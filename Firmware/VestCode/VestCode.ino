//VestCode project by fisk1234ost (https://github.com/fisk1234ost)
//based on CaiVR's Custom Haptic Vest V1  (Raspi Vest Script) 
//(https://github.com/CaiVR/CaiVR-Custom-Haptic-Vest-V1/tree/main/Raspi%20Vest%20Script)

// Please include ArduinoOSCWiFi.h to use ArduinoOSC on the platform
// which can use both WiFi and Ethernet
#include <ArduinoOSCWiFi.h>
// this is also valid for other platforms which can use only WiFi
// #include <ArduinoOSC.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>


const char* ssid = "SlimeServer";
const char* pwd = "95815480";
// for ArduinoOSC
const int recv_port = 1025;

const float target_rate = 45; //hz
const unsigned long targetPeriod = (1/target_rate)*1000; // rate to period in milliseconds

Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver();
Adafruit_PWMServoDriver pwm2 = Adafruit_PWMServoDriver(0x41, Wire);
uint8_t pwm2Offset = 16;

//Motor Index Mapping (index used to send motor data to correct motor)
//;int motorMap [] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31}; //Index Mapping (index used to send motor data to correct motor)
int motorMap [] = {8,11,1,0,9,10,3,2,15,14,6,7,13,12,4,5,25,24,16,17,27,26,18,19,29,30,22,21,28,31,20,23};

bool firstPacket = true;

void setup() {

  Serial.begin(115200);
  
  pwm1.begin();
  pwm1.setOscillatorFrequency(27000000);
  pwm1.setPWMFreq(1600);  // This is the maximum PWM frequency

  pwm2.begin();
  pwm2.setOscillatorFrequency(27000000);
  pwm2.setPWMFreq(1600);  // This is the maximum PWM frequency

  Wire.setClock(400000);

  Serial.println("Program: VestCode");

  // WiFi stuff (no timeout setting for WiFi)
#if defined(ESP_PLATFORM) || defined(ARDUINO_ARCH_RP2040)
#ifdef ESP_PLATFORM
  WiFi.disconnect(true, true);  // disable wifi, erase ap info
#else
  WiFi.disconnect(true);  // disable wifi
#endif
  delay(1000);
  WiFi.mode(WIFI_STA);
#endif
  WiFi.begin(ssid, pwd);

  while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
      delay(500);
#ifdef ARDUINO_UNOR4_WIFI
      static int count = 0;
      if (count++ > 20) {
          Serial.println("WiFi connection timeout, retry");
          WiFi.begin(ssid, pwd);
          count = 0;
      }
#endif
  }
  Serial.print("WiFi connected, IP = ");
  Serial.println(WiFi.localIP());
  // subscribe osc messages
  OscWiFi.subscribe(recv_port, "/h", onOscReceived);
  Serial.println("starting server");

  pwm1.setPin(motorMap[0], 4096);
  delay(200);
  pwm1.setPin(motorMap[0], 0);
}

uint16_t floatToDuty(float e){
  return static_cast<uint16_t>(e*4096);
}

unsigned long lastStartTime;
unsigned long diff;

void onOscReceived(const OscMessage& m) {

  //flag first packet, for connection debug
  if (firstPacket) {
    Serial.println("First Packet Recieved!");
    firstPacket = false;
    lastStartTime = millis();

  } else {
    diff = millis() - lastStartTime;
    if (diff > targetPeriod) {
      /*Serial.print("OVERRUN: ");
      Serial.print(diff);
      Serial.print(" Target: ");
      Serial.println(targetPeriod);*/
    }

    lastStartTime = millis();
  }

  handle_values(m.arg<String>(0));
}


void handle_values(String args){
  const int numValues = 32;
  float rawValues[numValues];

  args.replace("[", "");
  args.replace("]", "");
  
  // Split the string by commas and convert to float
  int startIndex = 0;
  for (int i = 0; i < numValues; i++) {
    int commaIndex = args.indexOf(',', startIndex);
    if (commaIndex == -1) {
      commaIndex = args.length();
    }
    String valueStr = args.substring(startIndex, commaIndex);
    valueStr.trim(); // Remove any leading or trailing spaces
    //push value to motors
    setMotorPWM(motorMap[i], floatToDuty( valueStr.toFloat()));

    startIndex = commaIndex + 1;
  }
}

void setMotorPWM(int motorIndex, uint16_t duty) {
  Serial.println(motorIndex);
  if (motorIndex >= pwm2Offset ) {
    pwm2.setPin(motorIndex-pwm2Offset, duty);
  } else {
    pwm1.setPin(motorIndex, duty);
  }
}

void loop() {
  OscWiFi.parse(); // to receive osc
}
