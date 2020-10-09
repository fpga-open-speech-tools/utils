/*
  Copyright 2020 Audio Logic Inc

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS 
  OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

  Tyler Davis
  Audio Logic Inc
  985 Technology Blvd
  Bozeman, MT 59718
  openspeech@flatearthinc.com
*/

// Define the GPIO connections
const byte UART_EN  = 2;
const byte PWR_EN   = 5;
const byte PWR_BTN  = 11;
const byte PWR_GOOD = 12;

// Define some global state variables
volatile boolean begin_powerdown = false;
volatile boolean begin_powerup = false;
boolean active = false;
volatile boolean time_press = false;

// Set the time to wait for force shutdown and the LED pulse duration in milliseconds
unsigned long press_duration = 5e3;
unsigned long pulse_duration = 500;




ISR(PCINT0_vect)
{
  // Execute the code on the rising edge of the interrupt
  boolean rising_edge = digitalRead(PWR_BTN) == HIGH;
  if (rising_edge)
  {
    if (!active)
      begin_powerup = true;
    else
      begin_powerdown = true;

    time_press = true;
  }
}

void powerdown()
{
  // TODO: Insert code here to communicate with the HPS

  // Pull the power enable pin high and the UART pin low
  digitalWrite(PWR_EN,HIGH);
  digitalWrite(UART_EN,LOW);

  // Reset the powerdown and active variables
  begin_powerdown = false;
  active = false;
  return;
}

void powerup()
{

  // Pull the power enable pin low and the UART pin high to enable both
  digitalWrite(PWR_EN,LOW);
  digitalWrite(UART_EN,HIGH);

  // Reset the powerup variable and set the "active" variable to true
  begin_powerup = false;
  active = true;
  return;
}

void force_powerdown()
{

  // Force the SoM off if the power button is held for a short duration
  digitalWrite(PWR_EN,LOW);
  digitalWrite(UART_EN,LOW);

  // Reset powerup/down variables
  begin_powerdown = false;
  begin_powerup = false;
  active = false;
  return;
}

void time_buttonpush()
{
  // Define the time variables and record the entry to the function
  unsigned long t0 = millis();
  unsigned long t1 = 0;

  // Wait for the power button to be released
  while(digitalRead(PWR_BTN) == HIGH);

  // Record the time when the button was released
  t1 = millis();

  // If the total time the button was held exceeds the preset duration, force 
  // the system to power down
  if (t1-t0 > press_duration)
    force_powerdown();

  // Reset the variable to check whether to time the button press
  time_press = false;
  return;
}

void setup()
{
  pinMode(UART_EN,OUTPUT);
  pinMode(PWR_EN,OUTPUT);
  
  pinMode(PWR_GOOD,INPUT);
  pinMode(PWR_BTN,INPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  // Specify the pin in the interrupt group (D11)
  PCMSK0 |= bit (PCINT3);

  // Clear and enable the interrupt group
  PCIFR  |= bit (PCIF0);
  PCICR  |= bit (PCIE0);

  digitalWrite(PWR_EN,HIGH);
  digitalWrite(UART_EN,LOW);
}

void loop()
{

  // Check whether to begin powerup or power down
  if (begin_powerdown)
    powerdown();
  if (begin_powerup)
    powerup();

  // Check to see if the button press should be timed
  if (time_press)
    time_buttonpush();

  
  // Blink the onboard LED to show the board is doing something
  digitalWrite(LED_BUILTIN, HIGH);
  delay(pulse_duration);
  digitalWrite(LED_BUILTIN, LOW);
  delay(pulse_duration);      
}
