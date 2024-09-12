from time import time
import numpy as np
from random import randint

class BoardModulator:
    def __init__(self, 
                 frequency:int = 10, 
                 modulation_dist:float = 0.2, 
                 modulation_offset: float | int = randint(0, 32),
                 motor_min: float = 0,
                 motor_max: float = 1,
                 vrc_percentage: float = 1,
                 ):
        """Handles modulation across time for waveform definitions

        Args:
            frequency (int, optional): [Hz] frequency that the modulation will occur at. Defaults to 10.
            mod_dist (float, optional): percent of the incoming signal to modulate (keep some active signal). Defaults to 1.0.
        """
        self.modulation_dist = modulation_dist
        self.frequency = frequency
        
        self.motor_min = motor_min
        self.motor_max = motor_max
        self.vrc_percentage = vrc_percentage
        
        self.modulation_offset = modulation_offset
        
        self.omega = 2*np.pi * frequency
        
    
    def sin_interp(self, raw: float | np.ndarray[np.float64], time_s: float = time(), just_sin = False) -> float | list[float]:        
        #find value to scale by
        return raw * (1 - (self.modulation_dist) * (1 - (np.sin(self.omega * time_s)+1)*0.5))
    
    def float_to_int16(self, raw: list[float]):
        int_array = [int(0)] * 32
        for index, element in enumerate(raw):
            scaled_val = (element * (self.motor_max - self.motor_min) + self.motor_min) * self.vrc_percentage
            print(scaled_val)
            int_array[index] = int(scaled_val * 4096)
            
        return int_array
    
    
    def set_mod_amount(self, var: float):
        self.mod_dist = var
        
    def set_mod_frequency(self, freq: int):
        self.frequency = freq
        self.omega = np.pi * freq
    
def _time_functions():
    mod = BoardModulator()
    
    # Time Function
    # Measure time for 1000 calls with a single float
    total= 0
    start_time = time()
    raw_signal = 0.5
    for _ in range(100000): 
        mod.sin_interp(raw_signal, start_time, True)
        total += time() - start_time
        start_time = time()
        
    print(f"Average Call Time for Single Float: {(total/100):.6f} ms")

    total= 0
    start_time = time()
    raw_signal = np.array([0.5] * 32)
    for _ in range(100000): 
        mod.sin_interp(raw_signal, start_time, True)
        total += time() - start_time
        start_time = time()
        
    print(f"Average Call Time for 32 Floats: {(total/100):.6f} ms")
    
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    _time_functions()
    
    # Plot Function
    frequencies = [5, 10, 20]
    mod_dists = [0.2, 0.5, 1.0]
    raw_signal = 1.0
    time_s = np.linspace(0, 2, 1000)  # 2 seconds, 1000 samples

    plt.figure(figsize=(12, 8))
    y_limits = (0, 1.5)  # Set y-axis limits

    for i, frequency in enumerate(frequencies):
        plt.subplot(3, 1, i + 1)
        for mod_dist in mod_dists:
            mod = BoardModulator(frequency=frequency, modulation_dist=mod_dist)
            modulated_signal = [mod.sin_interp(raw_signal, t, True) for t in time_s]
            plt.plot(time_s, modulated_signal, label=f"Mod Dist: {mod_dist}")

        plt.title(f"Frequency: {frequency} Hz")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.ylim(y_limits)
        plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1), borderaxespad=0.)


    plt.tight_layout()
    plt.show()