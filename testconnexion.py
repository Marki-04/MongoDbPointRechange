from pymongo import MongoClient

import config

client = MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=5000, tz_aware=True)
print(client.admin.command("ping"))