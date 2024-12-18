# Azure Managed Redis

>1. Using your account, create a Redis database on Azure Managed Redis and connect with Redis Insight.
---
I did not have an Azure account before this, so I created an account and searched for "Azure Cache for Redis" in the resources section

Once this was done, I used the default settings provided other than changing the Cache SKU to Azure Managed Redis and selected the "Balanced" type so that I could get the normal experience
![Screenshot 2024-12-18 at 00 32 39](https://github.com/user-attachments/assets/2576ec13-05ad-4228-973c-a9ab9bb43a22)

Once this resource was created, I searched for authentication, found the access key and tried to use it, but was getting a connection error.

After doing some digging, I found it is because Azure Managed Redis uses TLS by default, and so my connections would fail automatically.

Once this setting was passed, I was authenticated and everything worked right away.

>2 . Using Redis Insight, create a Hash with your firstname and lastname. Use “user:1” for the key.
---
I created a hash and added my user to this hash:
![462636476_961892702472359_5091078148899457578_n](https://github.com/user-attachments/assets/9835904d-c592-44cc-9b7a-779233beb46a)

> Explore some of the high-level differences between Elasticache and AMR. What would you say about those in 3 sentences or 10 lines maximum?
---
Pricing: Azure Managed Redis has adopted a consumption-based pricing model meaning that users will pay per operation rather than Elasitcache where we are provisioning instances and are paying for reserved capacity.

Scalability: Azure Managed Redis scales resources automatically, meaning that bursts of traffic are handled seamlessly, with no application degradation. Elasticache requires using autoscaling and can be slower to react to sudden bursts of traffic.

Overall, Azure Managed Redis is best for unpredictable workloads where we need flexibility


Final question I was asked in my interview was:

> how do Redis PubSub and Redis Steams differ regarding data loss around a restart?
---
Reids pub/Sub operates in a "fire and forget" model similar to something like Kenesis streams in AWS(not the same but, the same in this behaviour) and as such if a client is not online to receive the message, it will be lost.

Redis streams operate as a store for these messages and will wait for a consumer to read this information before it is lost. If the Redis streams server is set to store data to its local disk, it will also retain this information after a server restart
