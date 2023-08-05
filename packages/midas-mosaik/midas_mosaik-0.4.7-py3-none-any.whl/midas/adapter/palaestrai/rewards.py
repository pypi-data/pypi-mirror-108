from palaestrai.environment.reward import Reward
from palaestrai.agent.reward_information import RewardInformation
from palaestrai.types import Discrete


class GridHealthReward(Reward):
    def __init__(self, **params):
        self.grid_health_sensor = params.get(
            "grid_health", "Powergrid-0.Grid-0.health"
        )
        self.ext_grid_sensor = params.get(
            "ext_grid", "Powergrid-0.0-ext_grid-0.p_mw"
        )

    def __call__(self, state, *args, **kwargs):

        rewards = []
        for sensor in state:
            if self.grid_health_sensor == sensor.sensor_id:
                system_health_reward = RewardInformation(
                    sensor.sensor_value, Discrete(2), "grid_health_reward"
                )
                rewards.append(system_health_reward)
            elif self.ext_grid_sensor in sensor.sensor_id:
                reward = abs(sensor.sensor_value)
                external_grid_penalty_reward = RewardInformation(
                    reward, Discrete(1000), "external_grid_penalty_reward"
                )
                rewards.append(external_grid_penalty_reward)
        return rewards
