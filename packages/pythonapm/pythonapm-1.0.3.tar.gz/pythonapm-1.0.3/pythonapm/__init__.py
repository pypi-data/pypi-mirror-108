
import os
from .agentfactory import get_agent

name = "pythonapm"

version = "1.0.3"

installed_path = os.path.dirname(__file__)

agent = get_agent()