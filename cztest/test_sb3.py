import pytest
import gymnasium as gym
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import SubprocVecEnv
from datetime import datetime

class MimicClass():
    test_int: int
    test_float: float
    test_string: str = "test_string............"
    def __init__(self):
        self.test_int = 323234
        self.test_float = 2.335235

def test_TestClass():
    test_obj1 = MimicClass()
    test_obj2 = MimicClass()
    print(test_obj1.test_float, test_obj2.test_float)
    print(test_obj1.test_int, test_obj2.test_int)
    print(test_obj1.test_string, test_obj2.test_string)
    test_obj1.test_int = 1
    assert test_obj1.test_int != test_obj2.test_int
    test_obj2.test_float = 0.332
    assert test_obj1.test_float != test_obj2.test_float
    test_obj2.test_string = "234asfasdfasfas"

    #test_string is not shared for all instances from MimicClass, it's also instance variables
    #assert test_obj1.test_string == test_obj2.test_string

    assert test_obj1.test_string != test_obj2.test_string

    print(test_obj1.test_float, test_obj2.test_float)
    print(test_obj1.test_int, test_obj2.test_int)
    print(test_obj1.test_string, test_obj2.test_string)

    #This is right, because test_string is initted from class level, so could be access through class
    assert MimicClass.test_string == test_obj1.test_string

    #print(MimicClass.test_int) #this is wrong because test_int is not initted in class level, so can't be used as class variables.



def test_SB3_framework():
    env = gym.make("CartPole-v1", render_mode="rgb_array")

    model = A2C("MlpPolicy", env, verbose=1)
    #model.learn(total_timesteps=100_000) #100_000 will make the model last forever, total_reward == 500
    model.learn(total_timesteps=50_000)

    #vec_env = model.get_env()
    env = gym.make("CartPole-v1", render_mode="human")
    obs, info = env.reset()
    total_reward = 0.0
    for i in range(1000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        env.render()
        # VecEnv resets automatically
        if terminated or truncated:
           print(f"done happened, reset it now, terminated:{terminated,} truncated:{truncated}, total_reward:{total_reward}!!!")
           total_reward = 0.0
           obs, info = env.reset()


def test_vecenv_SB3_framework():
    num_envs = 10
    num_envs = 20
    num_envs = 30
    num_envs = 140
    #num_envs = 2
    env_name = 'CartPole-v1'
    env_fns = [lambda: gym.make(env_name) for i in range(num_envs)]
    # Create vectorized env 
    env = SubprocVecEnv(env_fns)

    model = A2C("MlpPolicy", env, verbose=1)
    #model.learn(total_timesteps=100_000) #100_000 will make the model last forever, total_reward == 500
    #model.learn(total_timesteps=50_000)
    #total_timesteps=50_000*60
    total_timesteps=50_000*5
    total_timesteps=50_000*50
    #total_timesteps=50_000*100
    start_time = datetime.now()
    model.learn(total_timesteps=total_timesteps)
    stop_time = datetime.now()
    print(f"{total_timesteps/(stop_time-start_time).total_seconds()} time steps per second")

    #vec_env = model.get_env()
    env = gym.make("CartPole-v1", render_mode="human")
    obs, info = env.reset()
    total_reward = 0.0
    for i in range(1000):
        action, _state = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        env.render()
        # VecEnv resets automatically
        if terminated or truncated:
           print(f"done happened, reset it now, terminated:{terminated,} truncated:{truncated}, total_reward:{total_reward}!!!")
           total_reward = 0.0
           obs, info = env.reset()
    env.close()

