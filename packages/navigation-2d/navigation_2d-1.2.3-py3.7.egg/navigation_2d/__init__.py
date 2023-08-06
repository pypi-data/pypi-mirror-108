from .navigation_env import NavigationEnvDefault, NavigationEnvAcc, NavigationEnvAccLidarObs, NonStationaryNavigation, RandomInitNavigationEnvAccLidarObs
#
from gym.envs import register
from .config import *

custom_envs = {}
for idx, obs_conf in enumerate(config_set):
    custom_envs['Navi-Vel-Full-Obs-Task{}-v0'.format(idx)] = dict(
                 path='navigation_2d:NavigationEnvDefault',
                 max_episode_steps=1000,
                 kwargs=dict(task_args=obs_conf))
    custom_envs['Navi-Acc-Full-Obs-Task{}-v0'.format(idx)] = dict(
                 path='navigation_2d:NavigationEnvAcc',
                 max_episode_steps=1000,
                 kwargs=dict(task_args=obs_conf))
    custom_envs['Navi-Acc-Lidar-Obs-Task{}-v0'.format(idx)] = dict(
                 path='navigation_2d:NavigationEnvAccLidarObs',
                 max_episode_steps=1000,
                 kwargs=dict(task_args=obs_conf))
    custom_envs['Random-init-Navi-Acc-Lidar-Obs-Task{}-v0'.format(idx)] = dict(
                 path='navigation_2d:RandomInitNavigationEnvAccLidarObs',
                 max_episode_steps=1000,
                 kwargs=dict(task_args=obs_conf))

custom_envs['Non-Stationary-Navigation_dyn_0-v0'] = dict(
             path='navigation_2d:NonStationaryNavigation',
             max_episode_steps=1000,
             kwargs=dict(task_args=non_sta_config_set[0]))

custom_envs['Non-Stationary-Navigation_dyn_1-v0'] = dict(
             path='navigation_2d:NonStationaryNavigation',
             max_episode_steps=1000,
             kwargs=dict(task_args=non_sta_config_set[1]))

custom_envs['Non-Stationary-Navigation_dyn_2-v0'] = dict(
             path='navigation_2d:NonStationaryNavigation',
             max_episode_steps=1000,
             kwargs=dict(task_args=non_sta_config_set[2]))

# register each env into
def register_custom_envs():
    for key, value in custom_envs.items():
        arg_dict = dict(id=key,
                        entry_point=value['path'],
                        max_episode_steps=value['max_episode_steps'],
                        kwargs=value['kwargs'])
        if 'reward_threshold' in value.keys():
            arg_dict['reward_threshold'] = value['reward_threshold']
        register(**arg_dict)

register_custom_envs()
