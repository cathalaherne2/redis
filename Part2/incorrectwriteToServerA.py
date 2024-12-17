import time
import os
import redis

# Retrieve Redis password from environment variable
redis_password = os.getenv("REDIS_PASSWORD")


# Check if the password is set
if not redis_password:
    raise ValueError("Redis password is not set in environment variables!")
# Redis Server A Configuration
server_a = redis.Redis(host='4.234.124.79', port=6123, db=0, password=redis_password)

# Insert values into Redis List
list_name = 'my_numbers'
server_a.delete(list_name)  # Clear the list if it already exists

for i in range(1, 10001):
    server_a.rpush(list_name, i)  # Append values to the list

print("Inserted values 1 to 10,000 into Server A.")
