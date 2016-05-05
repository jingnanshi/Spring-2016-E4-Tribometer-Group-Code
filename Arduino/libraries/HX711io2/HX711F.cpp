#include "arduino2.h" 
#include <Arduino.h>
#include <HX711F.h>

HX711F::HX711F(GPIO_pin_t dout, GPIO_pin_t pd_sck,byte dout_byte, byte pd_sck_byte, byte gain) {
	PD_SCK = pd_sck;
	DOUT = dout;
    PD_SCK_byte = pd_sck_byte;
    DOUT_byte = dout_byte;

	pinMode2f(PD_SCK, OUTPUT);
	pinMode2f(DOUT, INPUT);

	set_gain(gain);
}

HX711F::~HX711F() {

}

bool HX711F::is_ready() {
	return digitalRead2f(DOUT) == LOW;
}

void HX711F::set_gain(byte gain) {
	switch (gain) {
		case 128:		// channel A, gain factor 128
			GAIN = 1;
			break;
		case 64:		// channel A, gain factor 64
			GAIN = 3;
			break;
		case 32:		// channel B, gain factor 32
			GAIN = 2;
			break;
	}

	digitalWrite2f(PD_SCK, LOW);
	read();
}

// custom shiftIn function for faster digital read and write
uint8_t HX711F::shiftIn2(GPIO_pin_t dataPin, GPIO_pin_t clockPin, uint8_t bitOrder) {
    uint8_t value = 0;
    uint8_t i;
    
    for (i = 0; i < 8; ++i) {
        digitalWrite2f(clockPin, HIGH);
        if (bitOrder == LSBFIRST)
            value |= digitalRead2f(dataPin) << i;
        else
            value |= digitalRead2f(dataPin) << (7 - i);
        digitalWrite2f(clockPin, LOW);
    }
    return value;
}

long HX711F::read() {
	// wait for the chip to become ready
	while (!is_ready());

    unsigned long value = 0;
    byte data[3] = { 0 };
    byte filler = 0x00;

	// pulse the clock pin 24 times to read the data
    data[2] = shiftIn2(DOUT, PD_SCK, MSBFIRST);
    data[1] = shiftIn2(DOUT, PD_SCK, MSBFIRST);
    data[0] = shiftIn2(DOUT, PD_SCK, MSBFIRST);

	// set the channel and the gain factor for the next reading using the clock pin
	for (unsigned int i = 0; i < GAIN; i++) {
		digitalWrite2f(PD_SCK, HIGH);
		digitalWrite2f(PD_SCK, LOW);
	}

    // Datasheet indicates the value is returned as a two's complement value
    // Flip all the bits
    data[2] = ~data[2];
    data[1] = ~data[1];
    data[0] = ~data[0];

    // Replicate the most significant bit to pad out a 32-bit signed integer
    if ( data[2] & 0x80 ) {
        filler = 0xFF;
    } else if ((0x7F == data[2]) && (0xFF == data[1]) && (0xFF == data[0])) {
        filler = 0xFF;
    } else {
        filler = 0x00;
    }

    // Construct a 32-bit signed integer
    value = ( static_cast<unsigned long>(filler) << 24
            | static_cast<unsigned long>(data[2]) << 16
            | static_cast<unsigned long>(data[1]) << 8
            | static_cast<unsigned long>(data[0]) );

    // ... and add 1
    return static_cast<long>(++value);
}

long HX711F::read_average(byte times) {
	long sum = 0;
	for (byte i = 0; i < times; i++) {
		sum += read();
	}
	return sum / times;
}

double HX711F::get_value(byte times) {
	return read_average(times) - OFFSET;
}

float HX711F::get_units(byte times) {
	return get_value(times) / SCALE;
}

void HX711F::tare(byte times) {
	double sum = read_average(times);
	set_offset(sum);
}

void HX711F::set_scale(float scale) {
	SCALE = scale;
}

float HX711F::get_scale() {
	return SCALE;
}

void HX711F::set_offset(long offset) {
	OFFSET = offset;
}

long HX711F::get_offset() {
	return OFFSET;
}

void HX711F::power_down() {
	digitalWrite2f(PD_SCK, LOW);
	digitalWrite2f(PD_SCK, HIGH);
}

void HX711F::power_up() {
	digitalWrite2f(PD_SCK, LOW);
}
