"""
Database configuration and connection management for MongoDB
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# Load environment variables
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "mergington_school")

# Global database client
client = None
db = None


def connect_to_mongo():
    """
    Connect to MongoDB and initialize collections
    """
    global client, db
    
    try:
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        # Verify connection
        client.admin.command('ping')
        db = client[DATABASE_NAME]
        
        # Initialize collections with schema validation if needed
        create_collections()
        
        print(f"✓ Connected to MongoDB at {MONGODB_URL}")
        return db
    except ServerSelectionTimeoutError:
        print(f"✗ Failed to connect to MongoDB at {MONGODB_URL}")
        print("  Make sure MongoDB is running locally, or update MONGODB_URL in .env")
        raise


def create_collections():
    """
    Create collections and set up indexes
    """
    if "activities" not in db.list_collection_names():
        db.create_collection("activities")
        db["activities"].create_index("name", unique=True)
        print("✓ Created 'activities' collection")
    
    if "registrations" not in db.list_collection_names():
        db.create_collection("registrations")
        db["registrations"].create_index([("activity_name", 1), ("email", 1)], unique=True)
        print("✓ Created 'registrations' collection")


def get_db():
    """
    Get database instance
    """
    global db
    if db is None:
        connect_to_mongo()
    return db


def close_mongo():
    """
    Close MongoDB connection
    """
    global client
    if client:
        client.close()
        print("✓ Disconnected from MongoDB")
