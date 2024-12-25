from machine import ADC, Pin
import time

# Configuration
MIC_PIN = 0  # ADC pin connected to the microphone
KNOCK_THRESHOLD = 300  # Adjust based on microphone sensitivity
DEBOUNCE_TIME = 100  # Minimum time between knocks in milliseconds
PATTERN_TIMEOUT = 2000  # Time to wait for a pattern in milliseconds

# Initialize ADC
mic = ADC(MIC_PIN)

def detect_knocks():
    knock_times = []
    start_time = time.ticks_ms()

    print("Listening for knocks...")

    while True:
        # Read microphone value
        mic_value = mic.read()

        if mic_value > KNOCK_THRESHOLD:
            current_time = time.ticks_ms()
            if not knock_times or time.ticks_diff(current_time, knock_times[-1]) > DEBOUNCE_TIME:
                knock_times.append(current_time)
                print("Knock detected!")

        # Check if pattern timeout is reached
        if knock_times and time.ticks_diff(time.ticks_ms(), knock_times[-1]) > PATTERN_TIMEOUT:
            break

    return knock_times

def analyze_pattern(knock_times):
    # Calculate intervals between knocks
    intervals = [
        time.ticks_diff(knock_times[i], knock_times[i - 1])
        for i in range(1, len(knock_times))
    ]
    print("Knock pattern detected:", intervals)
    return intervals

def main():
    while True:
        knock_times = detect_knocks()
        if len(knock_times) > 1:
            pattern = analyze_pattern(knock_times)
            # Example: Check for a specific pattern
            if len(pattern) == 2 and pattern[0] < 500 and pattern[1] < 500:
                print("Double knock pattern recognized!")
            else:
                print("Unknown pattern.")
        else:
            print("Single knock or noise detected.")

        time.sleep(1)

if __name__ == "__main__":
    main()

