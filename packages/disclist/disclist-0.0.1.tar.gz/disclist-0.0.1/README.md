# Guides:
Here are guides of how to use this Python Wrapper.

## Initiating your Client:
```py
from disclist import Client

client = Client(token="...", sync=True) # sync is a kwarg to set if functions need to be async or not. Defaults to True.
```

## Posting Stats:
```py
# If you set sync to True, it will not need to be awaited
# Else, it needs to.
# You can check it using `client.sync` or see the kwarg you set
# if you are unsure.

# For synchronous:
client.post_stats(server_count=1) # Set your server count to 1.

# For asynchronous:
await client.post_stats(server_count=1) # Set your server count to 1.
```

## For checking if user has voted or not:
```py
# For synchronous:
has_voted = client.has_voted(user_id=1234567890)

# For asynchronous:
has_voted = await client.has_voted(user_id=1234567890)

print(has_voted) # True/False
```

## For searching a bot using it's ID:
```py
# For synchronous:
result = client.search(bot_id=1234567890)

# For asynchronous:
result = await client.search(bot_id=1234567890)

print(result) # {'...': ...}, Returns a dict.
```

# Where should I ask help?
Join our [discord](https://discord.gg/nZPaZbzYsb) to ask for help!

# License:
MIT