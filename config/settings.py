import os
from dotenv import load_dotenv
load_dotenv()

# Theater mock Data:
"""
{
    "theater_id(int)": {
        "name[string]", seats[array]
    },
}
"""

theaters = {
    1: {"name": "Theater_A", "seats": ["A1", "A2", "A3", "B1", "B2", "B3"]},
    2: {"name": "Theater_B", "seats": ["C1", "C2", "C3", "D1", "D2", "D3"]}
}

redis_config = {
    "host": os.environ.get("redis_host", ""),
    "port": os.environ.get("redis_port", 6379)
}
