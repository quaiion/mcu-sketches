#include "HX711.h"
#include <avr/io.h>
#include <avr/interrupt.h>

HX711 wt_chip;

enum PINS {
  HX_DT = 8,                            // in pin, connected to DT of HX711
  HX_SCK = 9,                           // in pin, connected to SCK of HX711
  BEP_PWM = 11,                         // out pin, conected to the beeper
  AWT_BUT = 2                           // in pin, connected to the button
};

const int AWT_BUT_INT = digitalPinToInterrupt(AWT_BUT);

volatile bool await;

void wait_button() {
  await = true;
  while(await) {
    delay(200);
  }
}

void stop_wait() {
  await = false;
}

void recalibrate() {
  wt_chip.tare();                       // maybe no wrapper needed
}

const int NLEDS = 6;
const int LED_PINS[6] = {3, 4, 5, 6, 7, 10};
int leds_lit = 0;

bool overload_beeping = false;

inline void beep() {
  tone(BEP_PWM, 1500, 500);
}

inline void overload_beep() {
  tone(BEP_PWM, 3000);
  overload_beeping = true;
}

inline void stop_overload_beep() {
  noTone(BEP_PWM);
  overload_beeping = false;
}

volatile bool weight_changed = false;
volatile bool pulse_beeping = false;
volatile bool beep_pulse_up = false;

ISR(TIM1_COMPA_vect) {
  pulse_beeping = !weight_changed;      // start beeping if weight didn't change
  weight_changed = false;
}

ISR(TIM0_OVF_vect) {
  if (!overload_beeping) {
    if (beep_pulse_up) {
      noTone(BEP_PWM);
      beep_pulse_up = false;
    } else if (pulse_beeping) {
      tone(BEP_PWM, 3000);
      beep_pulse_up = true;
    }
  }
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);

  pinMode(AWT_BUT, INPUT);
  attachInterrupt(AWT_BUT_INT, stop_wait, RISING);

  wt_chip.begin(HX_DT, HX_SCK);
  wt_chip.set_average_mode();

  beep();
  digitalWrite(LED_BUILTIN, HIGH);
  wait_button();
  wt_chip.tare();
  digitalWrite(LED_BUILTIN, LOW);

  beep();
  digitalWrite(LED_BUILTIN, HIGH);
  wait_button();
  wt_chip.calibrate_scale(1, 10);       // 1 coin exactly
  digitalWrite(LED_BUILTIN, LOW);

  for (int i = 0; i < NLEDS; ++i) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW);
  }

  noInterrupts();

  detachInterrupt(AWT_BUT_INT);         // for safe int replacemet
  attachInterrupt(AWT_BUT_INT, recalibrate, RISING);

  TCCR1A = 0;                           // preparing timer
  TCCR1B = 0;
  OCR1A = 62500;                        // interrupt every 4s
  TCCR1B |= (1 << WGM12);               // going "comapare" mode
  TCCR1B |= (1 << CS10);                // frequency adjustment (1024 divisor)
  TCCR1B |= (1 << CS12);
  TIMSK1 |= (1 << OCIE1A);

  TCCR0A = 0;                           // again for another timer
  TCCR0B = 0;
  TIMSK0 = (1 << TOIE0);                // interrupt upon overflow
  TCCR0B |= (1 << CS10);
  TCCR0B |= (1 << CS12);

  interrupts();
}

void loop() {
  float weight = wt_chip.get_units(10);
  
  if (weight > (float)NLEDS + 0.5) {
    if (!overload_beeping) {
      overload_beep();
    }
  } else if (overload_beeping) {
      stop_overload_beep();
  }

  if (weight > (float)leds_lit + 0.5) {
    weight_changed = true;
    while (weight > (float)leds_lit + 0.5 && leds_lit < NLEDS) {
      digitalWrite(LED_PINS[leds_lit], HIGH);
      leds_lit += 1;
    }
  } else if (weight < (float)leds_lit - 0.5) {
    weight_changed = true;
    while (weight < (float)leds_lit - 0.5 && leds_lit > 0) {
      digitalWrite(LED_PINS[leds_lit - 1], LOW);
      leds_lit -= 1;
    }
  }
}
