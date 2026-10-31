from pathlib import Path

from dotenv import load_dotenv


# Load the repository-level .env used by Docker Compose when running this API locally.
load_dotenv(Path(__file__).resolve().parents[2] / ".env", override=False)
