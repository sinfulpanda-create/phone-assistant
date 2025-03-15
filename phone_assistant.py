import os
import json
import requests
import sqlite3
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class PhoneModelAssistant:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.phone_api_url = os.getenv("PHONE_API_URL", "https://mock-api.example.com/new-phones")
        self.cache_expiry_hours = 24  # Cache duration in hours
        self.setup_database()

    def setup_database(self):
        """Initialize SQLite database and create cache table"""
        try:
            with sqlite3.connect('phone_cache.db') as conn:
                conn.execute('''CREATE TABLE IF NOT EXISTS api_cache (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                data TEXT NOT NULL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                             )''')
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")

    def get_cached_data(self):
        """Retrieve valid cached data from database"""
        try:
            with sqlite3.connect('phone_cache.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT data, timestamp 
                                 FROM api_cache 
                                 ORDER BY timestamp DESC 
                                 LIMIT 1''')
                result = cursor.fetchone()
                
                if result and self._is_cache_valid(result[1]):
                    return json.loads(result[0])
        except (sqlite3.Error, json.JSONDecodeError) as e:
            print(f"Cache retrieval error: {e}")
        return None

    def _is_cache_valid(self, cache_time):
        """Check if cache is still valid based on expiry time"""
        try:
            cache_datetime = datetime.fromisoformat(cache_time)
            return datetime.now() - cache_datetime < timedelta(hours=self.cache_expiry_hours)
        except (TypeError, ValueError) as e:
            print(f"Invalid timestamp: {e}")
            return False

    def store_in_cache(self, data):
        """Store new API response in cache"""
        try:
            with sqlite3.connect('phone_cache.db') as conn:
                conn.execute('''INSERT INTO api_cache (data) 
                             VALUES (?)''', (json.dumps(data),))
                conn.commit()
        except (sqlite3.Error, TypeError) as e:
            print(f"Cache storage error: {e}")

    def fetch_latest_models(self):
        """Fetch models with cache-first strategy"""
        # Try to get valid cached data first
        cached_data = self.get_cached_data()
        if cached_data:
            print("Using cached data")
            return cached_data

        # Fallback to API call if no valid cache
        try:
            response = requests.get(
                self.phone_api_url,
                timeout=10,
                headers={"User-Agent": "PhoneAssistant/1.0"}
            )
            response.raise_for_status()
            
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                self.store_in_cache(data)
                return data
                
            raise ValueError("Invalid API response format")
            
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            # Return stale cache if available
            return cached_data or None
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Data processing error: {e}")
            return cached_data or None

    def format_response(self, models):
        """Format response with cache indicator"""
        response = []
        if not models:
            return "Sorry, I couldn't find any information about new phones right now. 🫤"
            
        if self.get_cached_data() is not None:
            response.append("ℹ️ Showing cached information (updated within 24 hours)\n")
            
        response.append("📱 Latest Phone Models:\n")
        for idx, model in enumerate(models[:5], 1):
            features = [
                f"🌟 {model.get('name', 'Unnamed Model')}",
                f"Brand: {model.get('brand', 'Unknown')}",
                f"Released: {model.get('release_date', 'N/A')}",
                f"Features: {model.get('key_features', 'Not available')}"
            ]
            response.append(f"{idx}. " + "\n".join(features) + "\n")
            
        return "\n".join(response)

    # Rest of the class remains same as previous implementation

# Updated setup instructions
"""
## Updated Setup Instructions

1. Database Setup:
   - The system will automatically create 'phone_cache.db' on first run
   - Cache expires after 24 hours (adjust in CACHE_EXPIRY_HOURS)

2. Cache Management:
   - Automatic cleanup of old entries not implemented (consider adding)
   - Cache persists between sessions
   - Delete 'phone_cache.db' to clear cache

3. New Dependencies:
   - No additional dependencies needed (uses SQLite3 from standard library)
"""