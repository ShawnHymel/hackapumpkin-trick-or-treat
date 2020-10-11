import time
import board
import neopixel
import audioio
import random
from digitalio import DigitalInOut, Direction, Pull

# Parameters
fog_enable = False      # Use fog machine
cooloff_time = 5        # seconds
fog_warmup_delay = 0.1  # Time (sec) to warm ecig before releasing payload
num_pixels = 8          # Pixels in NeoPixel strip
neopixel_brightness = 0.8
neopixel_flicker_scaler = 0.3
flicker_delay_min = 0.01    # Seconds
flicker_delay_max = 0.100   # Seconds
flame_r = 226
flame_g = 121
flame_b = 35

# Pins
onboard_neopixel_pin = board.NEOPIXEL
status_led_pin = board.D13
neopixel_strip_pin = board.D9
pir_sensor_pin = board.D6
amp_shd_pin = board.D5
audio_out_pin = board.A0
fog_pin = board.A1
pump_pin = board.A2

# Onboard NeoPixel
led_rgb = neopixel.NeoPixel(onboard_neopixel_pin, 1)
led_rgb.brightness = 0.3
led_rgb[0] = (0, 0, 0)

# Status LEDs
status_led = DigitalInOut(status_led_pin)
status_led.direction = Direction.OUTPUT
status_led.value = False

# NeoPixel strip
pixels = neopixel.NeoPixel(neopixel_strip_pin, num_pixels, \
    brightness=neopixel_brightness, auto_write=False, pixel_order=neopixel.GRB)
for i in range(0, num_pixels):
    pixels[i] = (0, 0, 0)
pixels.show()

# PIR sensor
pir = DigitalInOut(pir_sensor_pin)
pir.direction = Direction.INPUT

# Audio amp shutdown control
amp_shd = DigitalInOut(amp_shd_pin)
amp_shd.direction = Direction.OUTPUT
amp_shd.value = False

# Fog (e-cig) control pin
fog = DigitalInOut(fog_pin)
fog.direction = Direction.OUTPUT
fog.value = False

# Air pump control pin
pump = DigitalInOut(pump_pin)
pump.direction = Direction.OUTPUT
pump.value = False

# Load audio file
wave_file = open("laugh.wav", "rb")
wave = audioio.WaveFile(wave_file)
audio = audioio.AudioOut(audio_out_pin)

# Globals
pir_prev_state = False

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

# Credit to mysecretstache for flicker effect
# https://codebender.cc/sketch:271084#Neopixel%20Flames.ino
def NeoFlicker():

    for i in range(0, num_pixels):

        # Set flicker vlaues
        flicker = random.randint(0, 55)
        r = flame_r - flicker
        g = flame_g - flicker
        b = flame_b - flicker
        
        # Apply brightness multiplier
        r = int(neopixel_flicker_scaler * r)
        g = int(neopixel_flicker_scaler * g)
        b = int(neopixel_flicker_scaler * b)

        # Clamp values
        r = max(min(r, 255), 0)
        g = max(min(g, 255), 0)
        b = max(min(b, 255), 0)
        
        pixels[i] = (r, g, b)
        
    pixels.show()

# Set NeoPixel strip to one color
def SetNeoColor(r, g, b):
    for i in range(0, num_pixels):
        pixels[i] = (r, g, b)
    pixels.show()
    
# Flash color
def NeoFlash(r, g, b, time_ms, num):
    for n in range(num):
        SetNeoColor(r, g, b)
        time.sleep(time_ms)
        SetNeoColor(0, 0, 0)
        time.sleep(time_ms)

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

timestamp = time.monotonic()
while True:

    # Show PIR status on onboard NeoPixel
    if ( True == pir.value ):
        led_rgb[0] = (100, 0, 0)
    else:
        led_rgb[0] = (0, 0, 0)

    # See if we're outside our "cooling off" period
    if ( time.monotonic() - timestamp >= cooloff_time ):
    
        # Show that we're armed
        status_led.value = True
    
        # Determine if PIR tripped
        pir_state = pir.value
        if (False == pir_prev_state) and (True == pir_state):
        
            # Reset cooling off timer and status LEDs
            timestamp = time.monotonic()
            status_led.value = False
        
            # --- Commence flatulence sequence ---
            # Warm up ecig resistive element
            print("Pressure is building...")
            if fog_enable:
                fog.value = True
                time.sleep(fog_warmup_delay)
            
            # Release the Kraken! Turn on onboard NeoPixel, run pump, play audio
            print("I can't hold it any longer!")
            if fog_enable:
                pump.value = True
            amp_shd.value = True
            audio.play(wave)
            
            # Flash LEDs in sequence
            SetNeoColor(0, 0, 0)
            time.sleep(0.409)
            SetNeoColor(255, 0, 0)
            time.sleep(0.081)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.08)
            SetNeoColor(255, 0, 0)
            time.sleep(0.074)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.106)
            SetNeoColor(255, 0, 0)
            time.sleep(0.077)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.097)
            SetNeoColor(255, 0, 0)
            time.sleep(0.08)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.122)
            SetNeoColor(255, 0, 0)
            time.sleep(0.053)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.104)
            SetNeoColor(255, 0, 0)
            time.sleep(0.073)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.124)
            SetNeoColor(255, 0, 0)
            time.sleep(0.113)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.126)
            SetNeoColor(64, 0, 0)
            time.sleep(0.075)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.127)
            SetNeoColor(50, 0, 0)
            time.sleep(0.093)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.130)
            SetNeoColor(32, 0, 0)
            time.sleep(0.126)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.141)
            SetNeoColor(26, 0, 0)
            time.sleep(0.094)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.155)
            SetNeoColor(18, 0, 0)
            time.sleep(0.138)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.181)
            SetNeoColor(12, 0, 0)
            time.sleep(0.128)
            
            SetNeoColor(0, 0, 0)
            time.sleep(0.189)
            
            # Fade out
            for i in range(10):
                SetNeoColor(10 - i, 0, 0)
                time.sleep(0.155)
            SetNeoColor(0, 0, 0)
            
            
            # Wait for audio file to be done
            while audio.playing:
                pass
                
            # Turn off audio amp, pump, ecig, and LEDs
            print("Aaaaahhhhh...")
            amp_shd.value = False
            if fog_enable:
                fog.value = False
                pump.value = False
            led_rgb[0] = (0, 0, 0)
            SetNeoColor(0, 0, 0)
        
        # Save state
        pir_prev_state = pir_state
    
    # Do flicker effect
    NeoFlicker()
    time.sleep(random.uniform(flicker_delay_min, flicker_delay_max))
    