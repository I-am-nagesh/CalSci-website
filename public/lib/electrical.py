def ohms_law_voltage(current, resistance):
    """Calculate voltage using Ohm's Law: V = I * R."""
    return current * resistance

def ohms_law_current(voltage, resistance):
    """Calculate current using Ohm's Law: I = V / R."""
    if resistance == 0:
        raise ValueError("Resistance cannot be zero")
    return voltage / resistance

def power(voltage, current):
    """Calculate power: P = V * I."""
    return voltage * current

def rc_time_constant(resistance, capacitance):
    """Calculate RC time constant: τ = R * C."""
    return resistance * capacitance

def rl_time_constant(inductance, resistance):
    """Calculate RL time constant: τ = L / R."""
    if resistance == 0:
        raise ValueError("Resistance cannot be zero")
    return inductance / resistance