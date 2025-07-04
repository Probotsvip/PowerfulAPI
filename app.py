import os
import logging
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "flaks-music-api-secret-key-2025")
CORS(app)

# MongoDB configuration
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://jaydipmore74:xCpTm5OPAfRKYnif@cluster0.5jo18.mongodb.net/?retryWrites=true&w=majority")
client = MongoClient(MONGO_URI)
db = client.flaks_music_api

# Collections
api_keys_collection = db.api_keys
usage_stats_collection = db.usage_stats
admin_users_collection = db.admin_users

# Initialize admin user if not exists
admin_user = admin_users_collection.find_one({"username": "admin"})
if not admin_user:
    admin_users_collection.insert_one({
        "username": "admin",
        "password": "admin123",  # Change this in production
        "created_at": datetime.utcnow()
    })

# Import routes
from routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
