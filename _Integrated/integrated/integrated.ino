// The integrated program for Arduino controller
//
// Created by Tribometer Group E4 Spring 2016, Section 3

#include <Encoder.h>
#include <PID_v1.h>
#include <math.h>
#include "HX711.h"
#include "arduino2.h" 
#include <AccelStepper.h>
#include <string.h>

#define MOTORREVCOUNTS 64
#define OUTREVCOUNTS 8400

#define DIR_1 8
#define PWM_1 12 // pin 4 on the mega is not working for pwm
#define BRK_1 9

// Define a stepper and the pins it will use
AccelStepper stepper(2, 11, 10);//11:step 10: dir 
long pos = 0;
int revs = 400;

// for serial communication
#define INPUT_SIZE 6
char input[INPUT_SIZE + 1];

float rpm = 0.0;

Encoder myEnc(2, 3);

volatile byte ct1 = 0;
volatile byte ct2 = 0;
volatile byte state = 1; //1 for updating ct1; 2 for updating ct2
const float sample_freq = 2000;
float Tsc = 1/sample_freq;

// pid setup
double Set_rpm, disk_input, disk_output;
double Kp=1.5, Ki=1.1, Kd=1;
double aggKp=2, aggKi=3, aggKd=1;
PID rpm_PID(&disk_input, &disk_output, &Set_rpm, Kp, Ki, Kd, DIRECT);

const GPIO_pin_t DOUT = DP69;
const GPIO_pin_t CLK = DP68;

HX711 scale(DOUT, CLK,69,68);

#define calibration_factor -7050.0 //This value is obtained using the SparkFun_HX711_Calibration sketch

void setup() {
  Serial.begin(9600);
  pinMode2(DIR_1, OUTPUT); 
  pinMode2(PWM_1, OUTPUT); 
  pinMode2(BRK_1, OUTPUT); 

  scale.set_scale(calibration_factor); 
  scale.tare();
  
  // pid setup
  Set_rpm = 50;
  rpm_PID.SetMode(AUTOMATIC);

  // motor setup
  digitalWrite2(DIR_1, LOW); //forward direction
  setupStepper();
  
  myEnc.write(0);

  cli();

  //set timer0 interrupt at 2kHz
  TCCR0A = 0;// set entire TCCR2A register to 0
  TCCR0B = 0;// same for TCCR2B
  TCNT0  = 0;//initialize counter value to 0
  // set compare match register for 2khz increments
  OCR0A = 124;// = (16*10^6) / (2000*64) - 1 (must be <256)
  // turn on CTC mode
  TCCR0A |= (1 << WGM01);
  // Set CS01 and CS00 bits for 64 prescaler
  TCCR0B |= (1 << CS01) | (1 << CS00);   
  // enable timer compare interrupt
  TIMSK0 |= (1 << OCIE0A);

  sei();
}

ISR(TIMER0_COMPA_vect){//timer0 interrupt 2kHz toggles pin 8
  if (state == 1){
    ct1 = myEnc.read();
    state = 2;
  }
  else{
    ct2 = myEnc.read();
    state = 1;
  }
  getRPM();
}

void loop() {
  while (myEnc.read() <= revs){
    disk_input = (double)rpm;
    if (Set_rpm > 70 || Set_rpm <= 15){
      rpm_PID.SetTunings(aggKp, aggKi, aggKd);
    } else {
      rpm_PID.SetTunings(Kp, Ki, Kd);
    }
    rpm_PID.Compute();
  
    cli();
    Serial.println(scale.get_units()*0.3234);
    sei();
    Serial.println(myEnc.read());
    analogWrite(PWM_1,disk_output);
  }
  Serial.println(myEnc.read());
  // stop the motor after finishing the revs
  analogWrite(PWM_1,0);

 dealWithSerial();
}

void getRPM() {
  // Speed Measurement Algorithms for Low-Resolution Incremental Encoder Equipped Drives: a Comparative Analysis 
  // RPM = 60 * dN/(Np*Tsc)
  // Np = number of pulses per revoluation
  // Tsc = time window
  // dN = number of pulses in the window
  int dN = ct2-ct1;
  float temp_rpm = fabs(60 * dN / (8400 * Tsc));
  if (temp_rpm < 1000){
    rpm = temp_rpm;
  }
}

void dealWithSerial()
{
  if (Serial.available() > 0) 
    {
      byte size = Serial.readBytes(input, INPUT_SIZE); // size of the serial input
      input[size] = '\0';
      Serial.println(input);
      if (input[0] == 'p')    // if it is a command to change position
      {
        // INPUT FORMAT: p10123 |||first bit is sign! This represents a position command to move -123
        char posStr[4];   // create a string to hold the change in position
        memset(posStr, '\0', sizeof(posStr));
        strncpy(posStr, input + 2, 4);   // copy over the values from input
        char sign = input[1];

        int value = atoi(posStr);   // the absolute value
        if (sign == '1')            // add on the sign
        {
          value = value * -1;
        }

         pos += value;
         stepper.moveTo(pos);
      } 
      // rpm command
      else if (input[0] == 'r')
      {
        rpm = updateRPM();
      }
      // revs command
      else if (input[0] == 'e'){
        
      }
      // start command
      else if (input[0] == 's'){
        
      }
    }
}

void setupStepper()
{
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(1000);
  stepper.setSpeed(500);
}

int updateRPM() {
  int rpm = 0;
  char rpmStr[4];
  // get the substring starting from index 2
  memset(rpmStr, '\0', sizeof(rpmStr));
  strncpy(rpmStr,input+2,3);
  rpm = atoi(rpmStr);
  return rpm;
}

void runStepper()
{
  // always trying to run to the new pos
  stepper.run();
}
  

