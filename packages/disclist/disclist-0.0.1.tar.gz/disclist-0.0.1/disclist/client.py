from typing import Union, Dict
from .errors import *

import aiohttp
import requests

class Client:
    def __init__(self,  token : str = None, sync : bool = True):
        """
        The Client of DiscList to authenticate to all endpoints.

        Parameters
        ----------
        token :class:`str`
            The token of your bot to authenticate to endpoints
            that require a token.
        sync :class:`bool`
            Whether if functions should be async or not.
            If this is ``True``, it will use aiohttp,
            else it will use requests to authenticate to
            endpoints.
        """
        self.sync = sync
        self.token = token
        self.base_url = "https://disclist.noxitb.repl.co/api"

    #def _get_adapter(self):
        #if self.sync:
            #return requests.session()
        #else:
            #return aiohttp.ClientSession()

    def post_stats(self, server_count : int) -> Union[aiohttp.ClientResponse, requests.Response]:
        """
        Updates the stats of your bot.

        Paramaters
        ----------
        server_count :class:`int`
            The number of servers that your bot
            is in.
        """
        server_count = str(server_count)

        if self.sync:
            async def _post_stats():
                async with aiohttp.ClientSession() as session:
                    async with session.post(f"{self.base_url}/bots/stats", headers={"serverCount": server_count, "Authorization": self.token}) as response:
                        if response.status == 401:
                            raise BotTokenRequired()
                        elif response.status == 404:
                            raise InvalidToken()

                        return response
        else:
            def _post_stats():
                response = requests.post(f"{self.base_url}/bots/stats", headers={"serverCount": server_count, "Authorization": self.token})
                if response.status_code == 401:
                    raise BotTokenRequired()
                elif response.status_code == 404:
                    raise InvalidToken()

                return response

        return _post_stats()

    def has_voted(self, user_id : int) -> bool:
        """
        Checks if the user has voted your
        bot or not.

        Paramaters
        ----------
        user_id :class:`int`
            The user id of the user you want
            to check.
        """
        user_id = str(user_id)

        if self.sync:
            async def _has_voted():
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/check/{user_id}", headers={"Authorization": self.token}) as response:
                        if response.status == 401:
                            raise Unauthorized(f"You must enter a user id.")
                        elif response.status == 403:
                            raise BotTokenRequired()
                        elif response.status == 404:
                            raise InvalidToken()

                        js = await response.json()
                        return js['voted']
        else:
            def _has_voted():
                response = requests.get(f"{self.base_url}/check/{user_id}", headers={"Authorization": self.token})

                if response.status_code == 401:
                    raise Unauthorized(f"You must enter a user id.")
                elif response.status_code == 403:
                    raise BotTokenRequired()
                elif response.status_code == 404:
                    raise InvalidToken()

                js = response.json()
                return js['voted']

        return _has_voted()

    def search(self, bot_id : int) -> Dict[str, Union[str, list]]:
        """
        Checks if the user has voted your
        bot or not.

        Paramaters
        ----------
        bot_id :class:`int`
            The bot id to search for.
        """
        user_id = str(bot_id)

        if self.sync:
            async def _has_voted():
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/bots/{bot_id}") as response:
                        if response.status_code == 404:
                            raise NotFound("You entered an invalid Bot ID.")

                        js = await response.json()
                        return js
        else:
            def _has_voted():
                response = requests.get(f"{self.base_url}/bots/{bot_id}")

                if response.status_code == 404:
                    raise NotFound("You entered an invalid Bot ID.")

                js = response.json()
                return js

        return _has_voted()