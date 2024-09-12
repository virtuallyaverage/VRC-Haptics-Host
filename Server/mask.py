class maskSetup: #mask depricated
    def __init__(self):
        pass
    
    def update_mask():
        """Update the motor_mask variable according to new parameters
        """
        #default to all motors off
        global motor_mask
        set_mask(False)
        
        if vrc.motors_enabled:
            if(vrc.checks_enabled):
                #set each group of indices to the value of the parent collider;
                motor_mask = set_mask_list(motor_mask, motor_groups["Spine"], vrc.spine_triggered)
                motor_mask = set_mask_list(motor_mask, motor_groups["Hip"], vrc.hip_triggered)
                motor_mask = set_mask_list(motor_mask, motor_groups["Chest"], vrc.chest_triggered)
            
            else:
                set_mask(True)
    
    
    def set_mask_list(mask, indices:list, switch_to: bool):
        """sets the boolean mask input to the switch_to conditions at indices locations

        Args:
            mask (list[bool]): list of boolean values to modify
            indices (list[int]): list of indices to modify on the mask
            switch_to (bool): boolean values to switch to

        Returns:
            list[bool]: the modified mask
        """
        for i in indices:
            mask[i] = switch_to
        return mask

        
    def apply_mask(in_list, mask):
        """Apply a mask to a list. for index i in boolean mask, mask[i] = float(0.0)

        Args:
            in_list (list[float]): the list to filter
            mask (list[bool]): The mask to apply

        Returns:
            _type_: modified list with mask applied
        """
        for index, mask_val in enumerate(mask):
            if not mask_val:
                in_list[index] = float(0.0)
                
        return in_list
            
    def set_mask(r_input: bool):
        """Set the motor_mask to a consistent boolean value

        Args:
            input (bool): the bool value to set the whole list to
        """
        global motor_mask
        motor_mask = [r_input] * total_motors