#include <SimpleDHT.h>
#include <stdlib.h>
          
// These constants are used to give names to the pins used:
const int analogInPin = A3 ;  // Analog input pin that the potentiometer is attached to

int sensorValue = 0 ;        // value read from the pot
int outputValue = 0 ;        // value output to the PWM (analog out)
int waterheight = 0 ;

int pinDHT11 = 2 ;            // DHT 11 digital input pin
SimpleDHT11 dht11 ;           // dht object declaration 

void setup() 
{
  Serial.begin(9600) ;
}

void loop() 
{
  // read the analog in value:
  byte temperature = 0 ;
  byte humidity = 0 ;
  int err = SimpleDHTErrSuccess ;

  sensorValue = analogRead(analogInPin) ;
  // map it to the range of the analog out:
  outputValue = map(sensorValue, 0, 1023, 0, 255) ;
  // map it to the sensors height
  waterheight = map (sensorValue, 0, 1023, 0 , 40) ;
  
  if ((err = dht11.read(pinDHT11, &temperature, &humidity, NULL)) != SimpleDHTErrSuccess) 
  {
    Serial.print("Read DHT11 failed, err=") ; 
    Serial.println(err) ;
    delay(1000) ;
    return EXIT_FAILURE ;
  }
  Serial.println("------------------------------------------") ;
  Serial.print("sensor = ") ;
  Serial.print(sensorValue) ;
  Serial.print("\t output = ") ;
  Serial.println(outputValue) ;
  putchar ('\t') ;
  Serial.print ("water height: ") ; 
  Serial.print (waterheight) ;
  Serial.println ("mm") ;
  Serial.print ("tempreture and humidity: ") ;
  Serial.print((int)temperature) ;                // cast the temp to int
  Serial.print(" *C, ") ; 
  Serial.print((int)humidity) ;                   // cast the humidity to int
  Serial.println(" H") ;
  Serial.println("------------------------------------------") ;
  putchar('\n') ;
  delay(2000) ;
}

