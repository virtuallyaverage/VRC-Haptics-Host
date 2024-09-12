
# checks disabled
class BoardMask:
    def __init__(self, 
                 num_motors: int = 32,
                 init_value: bool = True,
                 ) -> None:
        
        self.num_motors = num_motors
        self.mask = [init_value] * num_motors
        
    def get_mask(self):
        return self.mask
    
    def set_mask(self, index: int, value: bool):
        if (index > self.num_motors or index < 0):
            raise IndexError(f"Mask index out of range: {index}")
        
        if type(value) is not bool:
            raise TypeError(f"Wrong type for mask: {type(value)}")
        
        self.mask[index] = value
        
    def allTo(self, value: bool):
        self.mask = [value] * self.num_motors