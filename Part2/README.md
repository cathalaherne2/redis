# Choose any technology to implement this using the appropriate Redis data type


> 1 Insert the values 1 to 10 000 into the Redis instance you have on Server A.
---


The first thing I did was check out the different datatypes that are available in Redis, as I was familiar with just writing key:value pairs, but I know there is a lot more control and power I have over Data when choosing the correct data type.

I found the following [doc](https://redis.io/docs/latest/develop/data-types/) that brought me through them:

My first idea was to use "Sorted Sets"

When looking into this though, I can see it is not the correct data choice as I need both a unique strong and an associated score, which is more data than I am looking to store if I am looking only at writing 1 to 10,000

The next thing I looked at was a "LIST", when I take a look at the possible commands, I can see that both "LPUSH" and "RPUSH" would allow me to either Preappend or Append to the database the data that I am looking to write.

This script worked and I could see the data in Redis Insights:

![462581871_552641597742506_3471687155673526916_n](https://github.com/user-attachments/assets/c288c395-92a6-4a5f-9255-952b10aa237c)


>2 Read and print them in reverse order from the Redis Enterprise database in Server B.
---

When writing part 2, I found that it was actually not possible to have a LIST return its data in reverse order, and as such, I would in fact need to go back to sorted sets.

If I were to use a list, I'm sure it would be possible to reverse the output from the program in memory, but this would be done client-side rather than using Redis itself. I have included the code from this mistake in case you are interested, but I would not use it.

Once I adjusted my scripts to use a sorted set, I wrote the member and the value the same as I needed to fill both datatypes

The rest worked relatively simply 
<img width="652" alt="Screenshot 2024-12-17 at 23 53 35" src="https://github.com/user-attachments/assets/681c8de6-bb60-44d8-b5b5-9c7c43475f04" />

And I read the numbers back out from server B

![Screenshot 2024-12-17 at 23 52 26](https://github.com/user-attachments/assets/db3ff7ef-6188-4c5e-9b7e-0fa0d53eeff5)

>3 Explore the data using Redis Insight.
---
The data is all visible inside my numbers_zset in Redis Insights too

![462564269_1347816476184792_4171998284184787057_n](https://github.com/user-attachments/assets/a0cd9cca-db40-46b7-a9ce-066ac1c8be4f)

>4 What would you do to insert a lot of values (like hundreds of millions) with multiple threads and clients
and read and print those in reverse order from consumer clients?
---
(I assume that you are not looking for a code example of writing 100 million datapoints to a cache, so I will speak hypothetically)

If I wanted to insert hundreds of millions of values into a Redis cluster, the first thing I would look at is multithreading the application.

To do this, I would separate data into separate chunks so that each thread is working with its own separate data that it will be pushing.

After this, I would use Redis Pipelines to batch process multiple queries to reduce the overhead we see from making millions of network calls.


If we were seeing that there were issues with limits on the Redis side, EG not enough RAM on the server, we would look to scaling out the servers into a Redis Cluster, so that we can scale horizontally.
