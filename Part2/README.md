# Choose any technology to implement this using the appropriate Redis data type

First thing I did was check out the different datatypes that are available in Redis, as I was familiar with just writing key:value pairs, but I know there is a lot more control and power I have over Data when choosing the correct data type.

I found the following [doc](https://redis.io/docs/latest/develop/data-types/) that brought me through them:

My first idea was to use "Sorted Sets"

When looking into this though, I can see its not the correct data choice as I need both a unique strong and an associated score, which is more data than i am looking to store if I am looking only at writing 1 to 10,000

Next thing I looked at was a "LIST", when I take a look at the possible commands, I can see that both "LPUSH" and "RPUSH" would allow me to either Preappend or Append to the database the data that I am looking to write.

One thing that I am expecting is that because I have old data in the database from challenge A, and because I am using the same setup from part A, I may have some mixed up data. I dont want to delete this data right now, but will do this if I need to.

This script worked and I could see the data in redis insights:

![462581871_552641597742506_3471687155673526916_n](https://github.com/user-attachments/assets/c288c395-92a6-4a5f-9255-952b10aa237c)

