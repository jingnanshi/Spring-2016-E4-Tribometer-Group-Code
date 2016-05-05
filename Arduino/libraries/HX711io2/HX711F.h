// based on bogde HX711 https://github.com/bogde/HX711
// NEED arduino2.h to work: http://www.codeproject.com/Articles/732646/Fast-digital-I-O-for-Arduino

#ifndef HX711F_h
#define HX711F_h

#if ARDUINO >= 100
#include "Arduino.h"
#include "arduino2.h"
#else
#include "WProgram.h"
#include "arduino2.h"
#endif

class HX711F
{
	private:
		GPIO_pin_t PD_SCK;	// Power Down and Serial Clock Input Pin
		GPIO_pin_t DOUT;		// Serial Data Output Pin
        byte PD_SCK_byte;
        byte DOUT_byte;
		byte GAIN;		// amplification factor
		long OFFSET;	// used for tare weight
		float SCALE;	// used to return weight in grams, kg, ounces, whatever

	public:
		// define clock and data pin, channel, and gain factor
		// channel selection is made by passing the appropriate gain: 128 or 64 for channel A, 32 for channel B
		// gain: 128 or 64 for channel A; channel B works with 32 gain factor only
		HX711F(GPIO_pin_t dout, GPIO_pin_t pd_sck, byte dout_byte, byte pd_sck_byte, byte gain = 128);

		virtual ~HX711F();

		// check if HX711F is ready
		// from the datasheet: When output data is not ready for retrieval, digital output pin DOUT is high. Serial clock
		// input PD_SCK should be low. When DOUT goes to low, it indicates data is ready for retrieval.
		bool is_ready();

		// set the gain factor; takes effect only after a call to read()
		// channel A can be set for a 128 or 64 gain; channel B has a fixed 32 gain
		// depending on the parameter, the channel is also set to either A or B
		void set_gain(byte gain = 128);
    
        uint8_t shiftIn2(GPIO_pin_t dataPin, GPIO_pin_t clockPin, uint8_t bitOrder);
    
		// waits for the chip to be ready and returns a reading
		long read();

		// returns an average reading; times = how many times to read
		long read_average(byte times = 10);

		// returns (read_average() - OFFSET), that is the current value without the tare weight; times = how many readings to do
		double get_value(byte times = 1);

		// returns get_value() divided by SCALE, that is the raw value divided by a value obtained via calibration
		// times = how many readings to do
		float get_units(byte times = 1);

		// set the OFFSET value for tare weight; times = how many times to read the tare value
		void tare(byte times = 10);

		// set the SCALE value; this value is used to convert the raw data to "human readable" data (measure units)
		void set_scale(float scale = 1.f);

		// get the current SCALE
		float get_scale();

		// set OFFSET, the value that's subtracted from the actual reading (tare weight)
		void set_offset(long offset = 0);

		// get the current OFFSET
		long get_offset();

		// puts the chip into power down mode
		void power_down();

		// wakes up the chip after power down mode
		void power_up();
};

#endif /* HX711F_h */
