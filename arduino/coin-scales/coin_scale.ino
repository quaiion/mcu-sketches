#include "HX711.h"
#include "GyverTimers.h"

HX711 wt_chip;

enum PINS {
  HX_DT = 8,                            // in pin, connected to DT of HX711
  HX_SCK = 9,                           // in pin, connected to SCK of HX711
  BEP_PWM = 11,                         // out pin, conected to the beeper
  AWT_BUT = 2                           // in pin, connected to the button
};

const unsigned AWT_BUT_INT = digitalPinToInterrupt(AWT_BUT);

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

const unsigned NLEDS = 6;
const unsigned LED_PINS[6] = {3, 4, 5, 6, 7, 10};
int leds_lit = 0;

bool overload_beeping = false;

inline void beep() {
  tone(BEP_PWM, 1500, 100);
}

inline void overload_beep() {
  tone(BEP_PWM, 500);
  overload_beeping = true;
}

inline void stop_overload_beep() {
  noTone(BEP_PWM);
  overload_beeping = false;
}

volatile bool weight_changed = false;
volatile bool pulse_beeping = false;
volatile bool beep_pulse_up = false;

inline void pulse_beep() {
  tone(BEP_PWM, 500);
  beep_pulse_up = true;
}

inline void stop_pulse_beep() {
  noTone(BEP_PWM);
  beep_pulse_up = false;
}

const unsigned TIM1_ROUNDS = 20;
unsigned tim1_ctr = 0;

ISR(TIMER1_A) {
  if (!pulse_beeping) {
    if (tim1_ctr < TIM1_ROUNDS) {
      if (weight_changed) {
        tim1_ctr = 0;
        weight_changed = false;
      } else {
        tim1_ctr += 1;
      }
    } else {
      pulse_beeping = true;
    }
  } else if (weight_changed) {
    pulse_beeping = false;
    weight_changed = false;
    tim1_ctr = 0;
  }
}

const unsigned TIM0_ROUNDS = 15;
unsigned tim0_ctr = 0;

ISR(TIMER0_A) {
  if (tim0_ctr >= TIM0_ROUNDS) {
    if (!overload_beeping) {
      if (beep_pulse_up) {
        stop_pulse_beep();
      } else if (pulse_beeping) {
        pulse_beep();
      }
    }
    tim0_ctr = 0;
  } else {
    tim0_ctr += 1;
  }
}

#define FIFTEENMILSEC 15000
#define HALFSEC 500000

void setup() {
  pinMode(BEP_PWM, OUTPUT);

  pinMode(AWT_BUT, INPUT);
  attachInterrupt(AWT_BUT_INT, stop_wait, RISING);

  wt_chip.begin(HX_DT, HX_SCK);
  wt_chip.set_average_mode();

  beep();
  wait_button();
  wt_chip.tare();

  beep();
  wait_button();
  wt_chip.calibrate_scale(1, 10);       // 1 coin exactly

  for (int i = 0; i < NLEDS; ++i) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW);
  }

  Timer0.setPeriod(FIFTEENMILSEC);
  Timer1.setPeriod(HALFSEC);

  noInterrupts();
  Timer0.enableISR(CHANNEL_A);
  Timer1.enableISR(CHANNEL_A);
  detachInterrupt(AWT_BUT_INT);         // for safe int replacemet
  attachInterrupt(AWT_BUT_INT, recalibrate, RISING);
  interrupts();

  beep();
}

void loop() {
  float weight = wt_chip.get_units();
  
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
