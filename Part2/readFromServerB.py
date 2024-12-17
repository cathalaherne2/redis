import os
import redis

# Redis Server B Configuration
redis_host = "10.240.0.4"       
redis_port = 13127               
redis_password = os.getenv("REDIS_PASSWORD")  # Fetch password from ENV variable

# ZSET name
zset_name = "my_numbers_zset"

try:
    # Connect to Redis Server B
    server_b = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

    # Fetch data in reverse order using ZREVRANGE
    print("Reading all numbers in reverse order from Server B...")
    reversed_numbers = server_b.zrevrange(zset_name, 0, -1, withscores=False)

    # Print all values
    print(f"Total numbers retrieved: {len(reversed_numbers)}")
    for index, value in enumerate(reversed_numbers):
        print(f"{index + 1}: {int(value.decode('utf-8'))}")

except Exception as e:
    print(f"Error reading from Server B: {e}")

