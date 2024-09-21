from time import time, time_ns
import numpy as np
from random import randint

class BoardModulator:
    def __init__(self, 
                 intensity,
                 frequency, 
                 distance, 
                 num_motors: int,
                 modulation_offset: float | int = randint(0, 32),
                 motor_min: float = 0,
                 motor_max: float = 1,
                 ):
        """Handles modulation across time for waveform definitions

        Args:
            frequency (int, optional): [Hz] frequency that the modulation will occur at. Defaults to 10.
            mod_dist (float, optional): percent of the incoming signal to modulate (keep some active signal). Defaults to 1.0.
        """
        self.distance = distance
        self.frequency = frequency # is prescaled to hz (vrc_handler.py: get_mod_freq)
        self.intensity = intensity
        self.motor_min = motor_min
        self.motor_max = motor_max
        self.num_motors = num_motors
        
        self.modulation_offset = modulation_offset
        
        self.omega = 2*np.pi / frequency()
    
    def sin_interp(self, raw: float | np.ndarray[np.float64], time_s: float = None, just_sin = False) -> float | list[float]:        
        self.omega = 2*np.pi * self.frequency()
        if not time_s:
            time_s = time()
        #find value to scale by
        mult = np.sin(self.omega* time_s)
        return raw * (1 - (self.distance()) * (1 - (mult+1)*0.5))
    
    def float_to_int16(self, raw: list[float]):
        int_array = [int(0)] * self.num_motors
        for index, element in enumerate(raw):
            scaled_val = (element * (self.motor_max - self.motor_min) + self.motor_min) * self.intensity()
            int_array[index] = int(scaled_val * 4095)
            
        return int_array
    
def _time_functions():
    def test_freq(): 
        return 1
    def test_intensity(): 
        return 1
    def test_mod(): 
        return 1
    
    mod = BoardModulator(
        frequency=test_freq,
        intensity=test_intensity,
        distance = test_mod
    )
    
    # Time Function
    # Measure time for 1000 calls with a single float
    total= 0
    start_time = time()
    raw_signal = 0.5
    for _ in range(100000): 
        mod.sin_interp(raw_signal, start_time, True)
        total += time() - start_time
        start_time = time()
        
    print(f"Average Call Time for Single Float: {(total/100):.6f} ms") # dividing by 100 rather than 100k -> ms

    total= 0
    raw_signal = np.array([0.5] * 32)
    start_time = time()
    for _ in range(100000): 
        mod.sin_interp(raw_signal, start_time, True)
        total += time() - start_time
        start_time = time()
        
    print(f"Average Call Time for 32 Floats: {(total/100):.6f} ms")


    
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    _time_functions()
    
    # Example functions for frequency, distance, and intensity
    def frequency_func():
        return 1

    def distance_func():
        return 0

    def intensity_func():
        return 1.0 

    # Plot Function
    frequencies = [frequency_func, lambda: 5, lambda: 10]  # Example frequency functions
    mod_dists = [distance_func, lambda: 0.2, lambda: 0.4]   # Example distance functions
    raw_signal = 1.0
    time_s = np.linspace(0, 2, 1000)  # 2 seconds, 1000 samples

    plt.figure(figsize=(12, 8))
    y_limits = (0, 1.5)  # Set y-axis limits

    for i, frequency in enumerate(frequencies):
        plt.subplot(3, 1, i + 1)
        for mod_dist in mod_dists:
            mod = BoardModulator(intensity=intensity_func, frequency=frequency, distance=mod_dist)
            modulated_signal = [mod.sin_interp(raw_signal, t, True) for t in time_s]
            plt.plot(time_s, modulated_signal, label=f"Mod Dist: {mod_dist()}")

        plt.title(f"Frequency: {frequency()} Hz")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.ylim(y_limits)
        plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1), borderaxespad=0.)


    plt.tight_layout()
    plt.show()