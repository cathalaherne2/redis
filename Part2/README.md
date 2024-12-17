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

