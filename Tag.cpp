/*
The tag node is responsible for performing two-way ranging with nearby anchors and transmitting distance 
measurements to the host system. The firmware configures the DW3000 UWB transceiver, initializes the OLED display,
and interfaces with the MakerFab AT command firmware over UART.
ESP32-S3 UWB Tag Firmware
MakerFab MaUWB ESP32S3 + DW3000

Dependencies:
- Wire
- Adafruit_GFX
- Adafruit_BusIO
- SPI
- Adafruit_SSD1306
*/

// =====================================================
// USER CONFIG
// =====================================================

#define UWB_INDEX 0
#define TAG
#define UWB_TAG_COUNT 64

// =====================================================
// INCLUDES
// =====================================================

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>

#define SERIAL_LOG Serial
#define SERIAL_AT mySerial2

HardwareSerial SERIAL_AT(2);

// ESP32-S3 Pins
#define RESET    16
#define IO_RXD2  18
#define IO_TXD2  17

#define I2C_SDA 39
#define I2C_SCL 38

Adafruit_SSD1306 display(128, 64, &Wire, -1);

String response = "";

// =====================================================
// SETUP
// =====================================================

void setup()
{
    pinMode(RESET, OUTPUT);
    digitalWrite(RESET, HIGH);

    SERIAL_LOG.begin(115200);
    SERIAL_LOG.println(F("ESP32-S3 UWB Tag"));

    SERIAL_AT.begin(115200, SERIAL_8N1, IO_RXD2, IO_TXD2);

    Wire.begin(I2C_SDA, I2C_SCL);

    delay(1000);

    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
    {
        SERIAL_LOG.println(F("SSD1306 allocation failed"));
        while (true);
    }

    display.clearDisplay();

    logoShow();

    sendData("AT?", 2000, true);
    sendData("AT+RESTORE", 5000, true);

    sendData(configCmd(), 2000, true);
    sendData(capCmd(), 2000, true);

    sendData("AT+SETRPT=1", 2000, true);
    sendData("AT+SAVE", 2000, true);
    sendData("AT+RESTART", 2000, true);
}

// =====================================================
// LOOP
// =====================================================

void loop()
{
    while (SERIAL_LOG.available() > 0)
    {
        SERIAL_AT.write(SERIAL_LOG.read());
        yield();
    }

    while (SERIAL_AT.available() > 0)
    {
        char c = SERIAL_AT.read();

        if (c == '\r')
            continue;

        if (c == '\n')
        {
            SERIAL_LOG.println(response);
            response = "";
        }
        else
        {
            response += c;
        }
    }
}

// =====================================================
// OLED DISPLAY
// =====================================================

void logoShow()
{
    display.clearDisplay();

    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);

    display.setCursor(0, 0);
    display.println(F("MaUWB DW3000"));

    display.setCursor(0, 20);

    display.setTextSize(2);

    String temp = "";
    temp += "T";
    temp += UWB_INDEX;
    temp += " 6.8M";

    display.println(temp);

    display.setCursor(0, 40);

    temp = "Total: ";
    temp += UWB_TAG_COUNT;

    display.println(temp);

    display.display();

    delay(2000);
}

// =====================================================
// SERIAL COMMAND HELPER
// =====================================================

String sendData(String command, const int timeout, bool debug)
{
    String response = "";

    SERIAL_LOG.println(command);
    SERIAL_AT.println(command);

    long startTime = millis();

    while ((startTime + timeout) > millis())
    {
        while (SERIAL_AT.available())
        {
            response += (char)SERIAL_AT.read();
        }
    }

    if (debug)
    {
        SERIAL_LOG.println(response);
    }

    return response;
}

// =====================================================
// UWB CONFIGURATION
// =====================================================

String configCmd()
{
    String temp = "AT+SETCFG=";

    temp += UWB_INDEX;

    // Device role:
    // 0 = Tag
    // 1 = Anchor
    temp += ",0";

    // Frequency: 6.8 Mbps
    temp += ",1";

    // Range filter enabled
    temp += ",1";

    return temp;
}

String capCmd()
{
    String temp = "AT+SETCAP=";

    temp += UWB_TAG_COUNT;

    // Time slot
    temp += ",10";

    // Extended mode
    temp += ",1";

    return temp;
}
