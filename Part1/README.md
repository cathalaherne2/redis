# redis
Hiring Exercise for the Redis team

---
## Part 0: ensure authentication

step 0 was straightfoward, downloading SSH key, adjusting its permissions to ``chmod 400`` and SSHing with the command: ``ssh -i techChallengeKey-1.pem azureuser@123.45.67.89``

<img width="1506" alt="Screenshot 2024-12-17 at 19 46 06" src="https://github.com/user-attachments/assets/a6b40286-6e3d-47e5-b051-50a0359fa0cb" />

to confirm for any later OS differences, I confirmed the OS I was running was Red Hat 9.4 

<img width="730" alt="Screenshot 2024-12-17 at 19 47 16" src="https://github.com/user-attachments/assets/15339d3e-209e-4dfe-9512-73510d6003ef" />

## Part 1: Installing Redis community edition

>Install standalone Redis Community Edition on Server A.
---
First thing I did was to update yum to ensure I am resolving any dependancies correctly. I then checked the [redis website](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/) and saw the following commands:

```
sudo yum install redis
sudo systemctl enable redis
sudo systemctl start redis
```
I ran these commands and so redis was installed and is enabled as a systemctl process and will restart if I shut down the machine

## Part 2: Modify the config as needed

>  Change the default port from default 6379 to something else
---
To do this I edited the file with

```
sudo nano /etc/redis/redis.conf
```

<img width="811" alt="Screenshot 2024-12-17 at 20 00 40" src="https://github.com/user-attachments/assets/d7b6dfbc-4506-4161-8808-9a3b39c8d9ee" />

While skimming the config I noticed a section on replication. My guess is I will have to come back to this later

<img width="805" alt="Screenshot 2024-12-17 at 20 01 51" src="https://github.com/user-attachments/assets/b919331e-b91d-41ab-a24f-27250187da0f" />


I found the line "requirepass" and edited the password to a 30 character string based on the advice of the config file


<img width="809" alt="Screenshot 2024-12-17 at 20 07 35" src="https://github.com/user-attachments/assets/747496d6-f0b3-423b-8907-b3e20023116b" />

I then commented out the config line `` #bind 127.0.0.1 -::1`` to allow communication from the public internet

I then found the protected mode line and changed it to "no"

<img width="296" alt="Screenshot 2024-12-17 at 20 18 55" src="https://github.com/user-attachments/assets/908d097f-0ac6-41d7-8a85-c5dd26ff41e8" />


then I faced some sort of issue:

<img width="1431" alt="Screenshot 2024-12-17 at 20 20 48" src="https://github.com/user-attachments/assets/0fa3b1e1-d34f-4158-ad3a-01cf9fefd69d" />

My inital guess is that I have malformed the config file somehow, and so the process is not restarting. I will take a look for some startup logs and see what the issue is

I found the following details with no real information:

<img width="1417" alt="Screenshot 2024-12-17 at 20 23 47" src="https://github.com/user-attachments/assets/98eac318-fa4a-4fe5-a5f0-d5b2f9586de2" />

and so I had a look at the redis troubleshooting docs [here](https://redis.io/docs/latest/operate/oss_and_stack/management/troubleshooting/)

While I dont think I have a memory issue, I tried the command anyways:

<img width="1172" alt="Screenshot 2024-12-17 at 20 24 45" src="https://github.com/user-attachments/assets/1168b4dc-a533-49d2-873b-23a0fe39aad4" />

As I expected, it looks like a config issue on line 2055, but this is not super useful as there are 2054 lines in the redis config file according to Nano 

<img width="630" alt="Screenshot 2024-12-17 at 20 25 40" src="https://github.com/user-attachments/assets/acba69e0-7a66-4ac9-9faa-f52f8fdaa7e1" />

Doing some digging into the logs, I see that there was a permission denied error when starting up on port 6123.

My two guesses at this point was that it was either 1) an issue with RHEL and how it enforces security policies (this affected a customer I worked with recently) or 2) there is another process already bound to port 6123, so I tried to remove SELinux permissions for a second to see if that fixed the issue:

<img width="917" alt="Screenshot 2024-12-17 at 20 32 08" src="https://github.com/user-attachments/assets/b4fe72a8-7d6c-48d8-bd46-7c5b9dbb2db0" />

sure enough, I was able to restart redis afterwards, so I googled how to resolve this permenantly, and found the command:

```
sudo semanage port -a -t redis_port_t -p tcp 6123
```

to bind it correctly.

<img width="1352" alt="Screenshot 2024-12-17 at 20 34 53" src="https://github.com/user-attachments/assets/c0940d3b-1e1b-4f3c-9f3d-d63ddd90fae3" />

this worked, and I was able to test redis connecting with a [redis ping](https://redis.io/docs/latest/commands/ping/)

I tried to connect with redis insight but was unable to connect from there, I tried to connect from my other VM and found that the connection would timeout, leading me to think there was a firewall issue. 

I fixed this by adding a rule to allow 6123 communication (initally on the wrong server!) and both my redis insights + second machine could connect.

<img width="1512" alt="Screenshot 2024-12-17 at 20 54 22" src="https://github.com/user-attachments/assets/1bc4a084-850f-494b-a09c-f592f902eaef" />

## Part 3: Installing Redis software (redis Enterprise) on server B

>Download and install Redis Software (Redis Enterprise, latest version for RHEL 9) on Server B.
---
while I could download the software from the console, i was looking for a command I could use to install it via the CLI

![Screenshot 2024-12-17 at 20 59 27](https://github.com/user-attachments/assets/19446990-70ef-479c-9ab2-009ffda21efb)

I couldnt seem to find a command, so instead I fell back to scp. Im sure there is a way to do this if I searched harder, but SCP works just fine too, and so I used that

<img width="575" alt="Screenshot 2024-12-17 at 21 06 34" src="https://github.com/user-attachments/assets/f4fc15d3-a63e-4871-bc52-cb596d0f69c2" />

I followed the install instructions [here](https://redis.io/docs/latest/operate/rs/installing-upgrading/quickstarts/redis-enterprise-software-quickstart/#install-redis-enterprise-software) to get everything up and running

I faced an issue with systemd-resolve running on port 53, so I followed the instructions above for how to resolve this issue:

<img width="1240" alt="Screenshot 2024-12-17 at 21 24 00" src="https://github.com/user-attachments/assets/e146de47-d1a3-4ebc-a5d3-76a1c9c12ef9" />

this didnt seem to fix the issue, so I am going to try and stop the process entirely:

<img width="1109" alt="Screenshot 2024-12-17 at 21 25 26" src="https://github.com/user-attachments/assets/7d760866-f508-408a-8d17-c82e527ff02d" />

this worked and I was able to install redis

>step 4: setup Redis enterprise on that server
---
<img width="1232" alt="Screenshot 2024-12-17 at 21 28 00" src="https://github.com/user-attachments/assets/ae155116-5db1-450f-a893-c524fe162660" />

I Created a cluster from scratch within the UI and see the following prompt:
![Screenshot 2024-12-17 at 21 30 35](https://github.com/user-attachments/assets/a07338f5-9e3e-42f3-9427-dd1cd884821d)

I set a FQDN on my /etc/hosts directory to set my domain name as something that would resolve locally

I left the rest of this as default:

![Screenshot 2024-12-17 at 21 44 45](https://github.com/user-attachments/assets/d5e0c9be-9a91-48b3-9429-6cf093cfd75a)

I am now authenticated and installed

>step 5: create a redis database on the enterprise cluster:
---
this was relatively simple, I have the database a name of "redistest" the only other step I did was to ensure there was a password on the Database so that I could secure the cluster.

![Screenshot 2024-12-17 at 21 30 35](https://github.com/user-attachments/assets/69175a42-a8c1-4ef1-8b98-d0a6e0d9fca3)

one thing I can see that I think I missed a step on earlier is "(using no DNS option)" but I have set my FQDN as it looked like I had to, but now I have a DNS name to connect to. I will use the IP to connect to from now on though.

<img width="1283" alt="Screenshot 2024-12-17 at 21 54 50" src="https://github.com/user-attachments/assets/aff6a8e7-179a-4bea-b075-eed2855e6a57" />

> Find and use memtier-benchmark
---
I hadnt heard of this tool previously, so I googled the instructions and read the [following](https://redis.io/blog/memtier_benchmark-a-high-throughput-benchmarking-tool-for-redis-memcached/)
and found the [following link](https://redis.io/docs/latest/operate/rs/clusters/optimize/memtier-benchmark/) 

I had the test run with the following command

``` bash
/opt/redislabs/bin/memtier_benchmark -s $DB_HOST -p $DB_PORT -a $DB_PASSWORD -t 4 -R --ratio=1:1

```
<img width="1311" alt="Screenshot 2024-12-17 at 22 02 48" src="https://github.com/user-attachments/assets/130df564-3fa4-49fb-ad0c-f9e2042bf6df" />

I received the following performance results:

<img width="1349" alt="Screenshot 2024-12-17 at 22 05 16" src="https://github.com/user-attachments/assets/3d9c0ea3-bb91-415f-9c17-13b248cdebce" />

After this test was run, I used redis insights to confirm that this data is stored inside server A:

![462642827_874084291261529_2762838153478665611_n](https://github.com/user-attachments/assets/04e25b00-0697-4b70-8249-968251d06f4d)

> step 7: Congure the Redis Enterprise database with the “Replica Of geo-distributed Redis” feature
---
I created a database named "geo-replica-db"

and I used the "replica of" parameter to set the redis url of "redis://:<password>@4.234.124.79:6123"

![Screenshot 2024-12-17 at 22 19 48](https://github.com/user-attachments/assets/0640d0d0-0866-464e-8431-4a5502753d76)

I then confirmed that the sync was working both from the UI side:

![Screenshot 2024-12-17 at 22 28 05](https://github.com/user-attachments/assets/75e9dc79-efdc-4e01-b056-07c867dd6129)

And also from the CLI side:

![Screenshot 2024-12-17 at 22 27 41](https://github.com/user-attachments/assets/5ee2592c-3d86-481e-8ab0-6955022bcba5)


