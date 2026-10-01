from app.database import client, database

try:
    client.admin.command("ping")
    print("MongoDB connection successful!")
    print("Database:", database.name)
except Exception as e:
    print("MongoDB connection failed!")
    print("Error:", e)