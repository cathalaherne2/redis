# Choose any technology to implement this using the appropriate Redis data type

First thing I did was check out the different datatypes that are available in Redis, as I was familiar with just writing key:value pairs, but I know there is a lot more control and power I have over Data when choosing the correct data type.

I found the following [doc](https://redis.io/docs/latest/develop/data-types/) that brought me through them:

My first idea was to use "Sorted Sets"

When looking into this though, I can see its not the correct data choice as I need both a unique strong and an associated score, which is more data than i am looking to store if I am looking only at writing 1 to 10,000

Next thing I looked at was a "LIST", when I take a look at the possible commands, I can see that both "LPUSH" and "RPUSH" would allow me to either Preappend or Append to the database the data that I am looking to write.

This script worked and I could see the data in redis insights:

![462581871_552641597742506_3471687155673526916_n](https://github.com/user-attachments/assets/c288c395-92a6-4a5f-9255-952b10aa237c)


When writing part 2, I found that it was actually not possible to have a LIST return its data in reverse order, and as such, I would infact need to go back to sorted sets.

If I was to use a list, im sure it would be possible to reverse the output from the program in memory, but this would be done client side rather than using redis itself. I have included the code from this mistake incase you are interested, but I would not use it.

Once I adjusted my scripts to use a sorted set, I wrote the member and the value the same as I needed to fill both datatypes

The rest worked relatively simply 
<img width="652" alt="Screenshot 2024-12-17 at 23 53 35" src="https://github.com/user-attachments/assets/681c8de6-bb60-44d8-b5b5-9c7c43475f04" />

And I read the numbers back out from server B

![Screenshot 2024-12-17 at 23 52 26](https://github.com/user-attachments/assets/db3ff7ef-6188-4c5e-9b7e-0fa0d53eeff5)

> Explore the data using Redis Insight.

The data is all visible inside my numbers_zset in redis insights too

![462564269_1347816476184792_4171998284184787057_n](https://github.com/user-attachments/assets/a0cd9cca-db40-46b7-a9ce-066ac1c8be4f)

