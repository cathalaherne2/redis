import os
import redis

# Redis Server A Configuration
redis_host = "4.234.124.79"
redis_port = 6123
redis_password = os.getenv("REDIS_PASSWORD")  # Fetch password from ENV variable

# ZSET name
zset_name = "my_numbers_zset"

try:
    # Connect to Redis Server A
    server_a = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

    # Clean up old ZSET data
    server_a.delete(zset_name)
    print(f"Old ZSET '{zset_name}' removed from Server A.")

    # Insert 10,000 numbers into the ZSET
    print("Inserting 10,000 numbers into ZSET...")
    pipeline = server_a.pipeline()
    for i in range(1, 10001):
        pipeline.zadd(zset_name, {i: i})  # Score and member are the same
    pipeline.execute()
    print("Insertion complete.")

except Exception as e:
    print(f"Error writing to Server A: {e}")

