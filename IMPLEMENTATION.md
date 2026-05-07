# Persistent Data Storage Implementation

## Overview
This implements MongoDB for persistent data storage, replacing the in-memory dictionary that was lost on server restart.

## Changes Made

### 1. **New Dependencies** (`requirements.txt`)
- Added `pymongo` - MongoDB Python driver
- Added `python-dotenv` - For environment variable management

### 2. **Database Configuration** (`src/database.py`)
- MongoDB connection management
- Connection pool setup
- Collection initialization with proper indexes
- Error handling for connection failures

### 3. **Data Models** (`src/models.py`)
- Pydantic models for validation
- Activity model with all required fields
- Registration tracking

### 4. **Updated Application** (`src/app.py`)
- Integrated MongoDB using async context manager for lifecycle management
- All activities now persisted to MongoDB
- Automatic database initialization with default activities on first run
- Added `/health` endpoint for monitoring
- Updated all endpoints to use MongoDB

### 5. **Configuration** (`.env.example`)
- MongoDB connection URL (defaults to localhost)
- Database name configuration

## Setup Instructions

### Prerequisites
- MongoDB installed and running locally, OR
- MongoDB Atlas account for cloud database

### Local MongoDB Setup
```bash
# macOS (with Homebrew)
brew services start mongodb-community

# Linux (Debian/Ubuntu)
sudo systemctl start mongod

# Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Application Setup
1. Copy `.env.example` to `.env` and modify if needed:
   ```bash
   cp .env.example .env
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python src/app.py
   ```

4. Verify database connection:
   ```bash
   curl http://localhost:8000/health
   ```

## Database Schema

### Activities Collection
```json
{
  "name": "Chess Club",
  "description": "Learn strategies and compete in chess tournaments",
  "schedule": "Fridays, 3:30 PM - 5:00 PM",
  "max_participants": 12,
  "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
}
```

### Indexes
- `activities.name` - Unique index for activity names
- `registrations.activity_name` + `registrations.email` - Unique index

## Key Features

✅ **Persistent Storage** - Data survives server restarts
✅ **Default Data** - Automatically seeds database with initial activities
✅ **Connection Management** - Proper lifecycle management with FastAPI
✅ **Error Handling** - Clear feedback when MongoDB is unavailable
✅ **Health Checks** - `/health` endpoint for monitoring
✅ **Scalability** - Ready for additional collections/features

## Migration from In-Memory Storage

The transition is automatic:
1. First run creates collections and indexes
2. Loads default activities from code
3. Subsequent runs use existing database
4. API endpoints unchanged from user perspective

## Testing

Test the endpoints:
```bash
# Get all activities
curl http://localhost:8000/activities

# Sign up for activity
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=student@mergington.edu"

# Unregister
curl -X DELETE "http://localhost:8000/activities/Chess%20Club/unregister?email=student@mergington.edu"

# Health check
curl http://localhost:8000/health
```

## Next Steps

This implementation enables:
- **Issue #9** - Role-Based Access Control (now can manage user data properly)
- **Issue #11** - Dynamic Activity Creation (database ready for admin UI)
- **Issue #14** - Admin Dashboard (data now persistent for analysis)
- **Issue #8** - User Authentication (foundation for user data)

## Notes

- All existing functionality preserved
- API endpoints remain unchanged
- Database automatically initialized on first run
- Connection pooling handled by PyMongo
