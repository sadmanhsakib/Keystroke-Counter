import os
import dotenv

# loading the default .env file
dotenv.load_dotenv()

# getting the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
TIMEZONE = os.getenv("TIMEZONE")

if TIMEZONE is None:
    TIMEZONE = "UTC"  # default timezone