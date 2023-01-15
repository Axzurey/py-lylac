class WorldClock:
    timeStep: float = 1;

    @staticmethod
    def SET_TIMESTEP(step: float):
        if step < 0: raise Exception(f"A timestep of {step} is negative and as thus too low to be allowed.")
        WorldClock.timeStep = step;