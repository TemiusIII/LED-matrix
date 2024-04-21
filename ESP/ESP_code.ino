#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Scheduler.h>
#include <WiFiClient.h>
#include <FastLED.h>
#include <Task.h>

#define NUM_LEDS 1024  // Amount of LEDs in strip
#define PIN_LED 12     // Digital pin

const char *ssid = "SSID of your network";
const char *password = "password of your network";
String matrix_link = "http://server hostname or ip/matrix_image";

long matrix_colors[2][NUM_LEDS];
CRGB leds[NUM_LEDS];




int i = 0;
int arr_len = 0;
int speed = 50;

String get_data(String link) {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;

    String serverPath = link;
    http.begin(client, serverPath.c_str());

    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      String payload = http.getString();
      return (payload);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    // Free resources
    http.end();
  } else {
    Serial.println("Unknown Error");
  }
  Serial.println("Nu ya huy znaet");
  return "1 1 0xff00ff";
}

int parse_next_int(String data) {
  int value = 0;
  for (; i < data.length(); ++i) {
    if (48 <= data[i] && data[i] <= 57) {
      value = value * 10 + ((int)data[i] - 48);
    } else {
      break;
    }
  }
  return value;
}

void parse_colors(bool verbose = false, bool debug = false) {
  i = 0;
  String data = get_data(matrix_link);
  if (debug)
    for (int x; x < data.length(); ++x) {
      Serial.println(data[x]);
    }

  arr_len = parse_next_int(data);
  i++;
  speed = parse_next_int(data);
  i++;
  if (verbose) {
    Serial.println(arr_len);
    Serial.println(speed);
  }
  String temp_long = "";
  int index = 0;

  int nado = 0;
  for (int k = 0; k < arr_len; k++) {
    index = 0;
    nado = 0;
    for (; i < data.length(); ++i) {
      if (data[i] == ' ') {
        matrix_colors[k][index++] = strtol(temp_long.c_str(), NULL, 16);
        nado++;
        if (debug)
          Serial.println(temp_long);
        temp_long = " ";
      } else {
        temp_long += data[i];
      }
      if (index == NUM_LEDS)
        break;
    }

    if (verbose) {
      Serial.print("Nado: ");
      Serial.println(nado);
    }
  }
  if (verbose)
    Serial.println("Parsed all!");
}



void setup() {

  Serial.begin(9600);
  FastLED.addLeds<NEOPIXEL, PIN_LED>(leds, NUM_LEDS);
  FastLED.setBrightness(10);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  parse_colors(true);
}
int cnt = 10;
int cnt2 = 0;

void loop() {
  if (++cnt2 >= 4) {
    parse_colors();
    cnt2 %= 5;
  }
  for (int k = 0; k < arr_len; ++k) {
    for (int i = 0; i < NUM_LEDS; ++i) {
      leds[i] = matrix_colors[k][i];
      if (cnt++ % 512 == 0)
        FastLED.show();
    }
    delay(speed);
  }
}
