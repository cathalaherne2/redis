# redis
hiring exercise for the Redis team


# Part 0: ensure authentication

step 0 was straightfoward, downloading SSH key, adjusting its permissions to ``chmod 400`` and SSHing with the command: ``ssh -i techChallengeKey-1.pem azureuser@123.45.67.89``

<img width="1506" alt="Screenshot 2024-12-17 at 19 46 06" src="https://github.com/user-attachments/assets/a6b40286-6e3d-47e5-b051-50a0359fa0cb" />

to confirm for any later OS differences, I confirmed the OS I was running was Red Hat 9.4 

<img width="730" alt="Screenshot 2024-12-17 at 19 47 16" src="https://github.com/user-attachments/assets/15339d3e-209e-4dfe-9512-73510d6003ef" />

# Part 1: Installing Redis community edition

>Install standalone Redis Community Edition on Server A.

First thing I did was to update yum to ensure I am resolving any dependancies correctly. I then checked the [redis website](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-linux/) and saw the following commands:

```
sudo yum install redis
sudo systemctl enable redis
sudo systemctl start redis
```
I ran these commands and so redis was installed and is enabled as a systemctl process and will restart if I shut down the machine


>  Change the default port from default 6379 to something else

To do this I edited the file with

```
sudo nano /etc/redis/redis.conf
```



