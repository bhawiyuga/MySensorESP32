#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Replace with your network credentials
const char* ssid = "MyWifi";
const char* password = "KepoBanget12345";

// Replace with your server URL
const char* serverName = "https://owsgip.itc.utwente.nl/v1.1/Observations";

// Example sensor reading function
float getSensorResult() {
    // Replace with your actual sensor code
    return 40.4;  // Example sensor result
}

void setup() {
    Serial.begin(115200);

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
}

void loop() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;

        // Specify content-type header
        http.begin(serverName);
        http.addHeader("Content-Type", "application/json");

        // Prepare JSON payload
        StaticJsonDocument<200> jsonDoc;
        jsonDoc["result"] = getSensorResult();
        jsonDoc["Datastream"]["@iot.id"] = "8f6da310-b02f-4c24-9688-7fe09d63041b";

        String requestBody;
        serializeJson(jsonDoc, requestBody);

        // Send POST request
        int httpResponseCode = http.POST(requestBody);

        // Check the returning code
        if (httpResponseCode > 0) {
            String response = http.getString();  // Get the response to the request
            Serial.println(httpResponseCode);    // Print return code
            Serial.println(response);            // Print response
        } else {
            Serial.print("Error on sending POST: ");
            Serial.println(httpResponseCode);
        }

        // Free resources
        http.end();
    } else {
        Serial.println("Error in WiFi connection");
    }

    // Wait before sending the next request
    delay(60000);  // Send a request every 60 seconds
}