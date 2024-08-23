from time import time
import numpy as np

class Modulation:
    def __init__(self, frequency:int = 10, mod_dist:float = 1.0):
        """Handles modulation across time for waveform definitions

        Args:
            frequency (int, optional): [Hz] frequency that the modulation will occur at. Defaults to 10.
            mod_dist (float, optional): percent of the incoming signal to modulate (keep some active signal). Defaults to 1.0.
        """
        self.mod_dist = mod_dist
        self.frequency = frequency
        
        self.omega = np.pi * frequency
        
    
    def sin_interp(self, raw:float | list[float]) -> float:
        time_s = time()
        
        #find value to scale by
        sin_result = (np.sin(self.omega * time_s)+1)*0.5
        #return scaled values according to mod_dist
        # Check if raw is a list and convert to numpy array if necessary
        if isinstance(raw, list):
            raw = np.array(raw)
        return raw * (1 - (self.mod_dist) * (1 - sin_result))
        
        if isinstance(raw, list):
            for index, element in enumerate(raw):
                raw[index] = element * (1 - (self.mod_dist*element) * (1 - sin_result))
            return raw
        
        elif isinstance(raw, float):
            return raw * (1 - (self.mod_dist*raw) * (1 - sin_result))
        
        else:
            raise NotImplementedError
    
    def set_mod_amount(self, var: float):
        self.mod_dist = var
        
    def set_mod_frequency(self, freq: int):
        self.frequency = freq
        self.omega = np.pi * freq
    
def _time_functions():
    mod = Modulation()
    
    # Time Function
    # Measure time for 1000 calls with a single float
    total= 0
    start_time = time()
    raw_signal = 0.5
    for _ in range(100000): 
        mod.sin_interp(raw_signal, 0.5)
        total += time() - start_time
        start_time = time()
        
    print(f"Average Call Time for Single Float: {(total/100):.6f} ms")

    total= 0
    start_time = time()
    raw_signal = [0.5] * 32
    for _ in range(100000): 
        mod.sin_interp(raw_signal, 0.5)
        total += time() - start_time
        start_time = time()
        
    print(f"Average Call Time for Single Float: {(total/100):.6f} ms")
    
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import timeit
    
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
            mod = Modulation(frequency=frequency, mod_dist=mod_dist)
            modulated_signal = [mod.sin_interp(raw_signal, t) for t in time_s]
            plt.plot(time_s, modulated_signal, label=f"Mod Dist: {mod_dist}")

        plt.title(f"Frequency: {frequency} Hz")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.ylim(y_limits)
        plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1), borderaxespad=0.)


    plt.tight_layout()
    plt.show()