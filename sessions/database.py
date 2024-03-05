from dotenv import load_dotenv

from controllers.DatabaseController import DatabaseController

load_dotenv()

db = DatabaseController()

db.create_pool()
