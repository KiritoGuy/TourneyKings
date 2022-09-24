import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ.get("TOKEN")
DATABASE_URL = os.environ.get("DATABASE_URL")
OWNER_IDS = [753247226880589982, 849167923066568734]
PREFIX = ["tk!", "."]
