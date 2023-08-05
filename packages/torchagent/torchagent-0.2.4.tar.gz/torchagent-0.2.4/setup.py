# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchagent', 'torchagent.agents']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'torchagent',
    'version': '0.2.4',
    'description': 'Deep-Q learning with pytorch',
    'long_description': "torchagent - A reinforcement learning library based on PyTorch\n==============================================================\nWelcome to the torchagent repository. This repository contains the sources\nfor the torchagent library.\n\n.. contents::\n\nWhat is it?\n-----------\n:code:`torchagent` is a library that implements various reinforcement learning algorithms for PyTorch.\nYou can use this library in combination with openAI Gym to implement reinforcement learning solutions.\n\nWhich algorithms are included?\n------------------------------\nCurrently the following algorithms are implemented:\n\n- Deep Q Learning \n- Double Q Learning\n\nInstallation\n------------\nYou can install the library using the following command:\n\n.. code::\n\n    pip install torchagent\n\nUsage\n-----\nThe following code shows a basic agent that uses Deep Q Learning.\n\n.. code:: python\n\n    from torchagent.memory import SequentialMemory\n    from torchagent.agents import DQNAgent\n\n    import torch\n    import torch.nn as nn\n    import torch.optim as optim\n\n    class PolicyNetwork(nn.Module):\n        def __init__(self):\n            self.linear = nn.Linear(210 * 160, 3)\n\n        def forward(self, x):\n            return self.linear(x)\n\n    policy_network = PolicyNetwork()\n    memory = SequentialMemory(20)\n    agent = DQNAgent(2, policy_network, nn.MSELoss(), optim.Adam(policy_network.parameters()), memory)\n\n    env = gym.make('Assault-v0')\n\n    for _ in range(50):\n        state = env.reset()\n\n        for t in count():\n            action = agent.act(state)\n            next_state, reward, done, _ = env.step(agent.act(state))\n\n            agent.record(state, action, next_state, reward, done)\n            agent.train()\n\n            state = next_state\n\n            if done:\n                break\n",
    'author': 'Willem Meints',
    'author_email': 'willem.meints@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wmeints/torchagent',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
