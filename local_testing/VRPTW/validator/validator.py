from validator.IOModule import IOModule
from validator.environment import VRPEnvironment
import validator.tools as tools

import numpy as np

State = dict[str, np.ndarray]
Action = list[list[int]]
Info = dict[str, str]

EPOCH_TLIM = 5

class Validator(IOModule):
    def __init__(self):
        self.observations: list[tuple[State, int, bool, Info]] = list()
        self.score: int = None

        static_instance = tools.read_vrplib(f'instances/instance')
        self.env = VRPEnvironment(instance=static_instance, epoch_tlim=EPOCH_TLIM, is_static=False)
        obs, info = self.env.reset()
        self.observations = [(obs, None, False, info)]

    def _score(self) -> dict[str, int]:
        return {"score": -self.score}

    def obtain_data(self) -> tuple[State, int, bool, Info]:
        """
        returns:
        Current state:                      State
        The reward:                         int
        Is done:                            bool
        Info (errors and problem info):     Info
        """
        if len(self.observations) == 0:
            return None
        
        return self.observations.pop(0)

    def push_data(self, solution: Action):
        obs = self.env.step(solution=solution)
        self.observations.append(obs)
        self.score = obs[1]

        super().push_data()