import os
from dotenv import dotenv_values


env_config = dotenv_values(os.getcwd() + "/.env")
