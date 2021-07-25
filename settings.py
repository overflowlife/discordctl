# coding:UTF-8 cp65001

import os
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path=join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

PREFIX=os.getenv("PREFIX")
DBG=os.getenv("DBG")
TOKEN=os.getenv("TOKEN")
