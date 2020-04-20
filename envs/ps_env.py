import gym
from gym import spaces
import asyncio
import websockets


initialized = False #TODO: find a way to move this into the class
_websocket = None
np_precision = np.float64

async def initialization(websocket, path):
    '''
    initialization requires the following:
    1. We get a connection
    2. We set that we're ready to go
    3. We tell the other client that we're ready to go
    '''
    #TODO: allow multithreading/multiple ongoing games?
    if not initialized: #Only allow one and ignore race conditions
      name = await websocket.recv()
      greeting = "ready"

      global _websocket = websocket
      await websocket.send(ready) #this tells the simulator that it can proceed
    

class PSEnv(gym.Env):
  '''
  Pokemon Stadium Gym Environment.  For now, just assumes a 1v1 game.
  Observation space: Dictionary
  1. HP of user (Box)
  2. HP of opponent (Box)
  3. PP (Per Move) (Box)
  PP of opponent is partially observable in some formats.  Let's ignore it for now.
  
  
  '''
  #TODO: Make this general and subclass it for various rulesets


  def __init__(self):
    super(PSEnv, self).__init__()
    self.server = websockets.serve(initialization, "localhost", 8765)
    self.num_moves = 5 #4 + 1 for struggle.  #TODO: Generalize this in the future
    self.num_observations = 6 #HP, HP, 4 PPs
    
    
    self.action_space = spaces.Discrete(num_moves) #TODO: see https://github.com/openai/gym/blob/master/gym/spaces/dict.py
    # Example for using image as input:
    self.observation_space = spaces.Box(low=0., high=1.,
                                        shape=(num_observations,), dtype=np_precision)

  def step(self, action):
    global _websocket
    await _websocket.send(str(action))
    state _websocket.recv() #this should get us the new state of the world, an observation of some sort
    #TODO: parse observation
    
    #TODO: create a new observation
    #TODO: create a new reward based off what we received
    #TODO: determine if we won the game or not
    
    return observation, reward, done, info
  def reset(self):
    observation = np.ones(shape=(num_observations,), dtype=np_precision) #we're just setting everyhing back to full HP and full PP

    return observation  # reward, done, info can't be included
  def render(self):
    pass #TODO, in the future
    
  def close (self):
    global _websocket
    _websocket = None #close the initialization
