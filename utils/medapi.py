import aiohttp


class MedApi:
    url = 'https://sandbox-healthservice.priaid.ch'
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InNlbWVub2xlZ292aWNoQHlhbmRleC5ydSIsInJvbGUiOiJVc2VyIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc2lkIjoiMTA1NjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3ZlcnNpb24iOiIyMDAiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xpbWl0IjoiOTk5OTk5OTk5IiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwIjoiUHJlbWl1bSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbGFuZ3VhZ2UiOiJlbi1nYiIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvZXhwaXJhdGlvbiI6IjIwOTktMTItMzEiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL21lbWJlcnNoaXBzdGFydCI6IjIwMjItMDQtMTIiLCJpc3MiOiJodHRwczovL3NhbmRib3gtYXV0aHNlcnZpY2UucHJpYWlkLmNoIiwiYXVkIjoiaHR0cHM6Ly9oZWFsdGhzZXJ2aWNlLnByaWFpZC5jaCIsImV4cCI6MTY1MDU1MTY2OCwibmJmIjoxNjUwNTQ0NDY4fQ.TaIklQsOQ5SbNlJYVHHPphGVJ2PLJC1gSznAG783WjE'

    async def get_body_locations(self, language: str):
        # {{host}}/body/locations?token={{token}}&language=ru-ru
        params = {'token': self.token, "language": language}
        resp = await self.get_request(path='body/locations', params=params)
        return resp


    async def get_body_sublocations(self, language: str, location_id: int):
        # {{host}}/body/locations?token={{token}}&language=ru-ru
        params = {'token': self.token, "language": language}
        resp = await self.get_request(path=f'body/locations/{location_id}', params=params)
        return resp

    async def get_symptoms(self, language: str, location_id: int, gender: str):
        # {{host}}/symptoms/6/man?language=ru-ru&token={{token}}
        params = {'token': self.token, "language": language}
        resp = await self.get_request(path=f'symptoms/{location_id}/{gender}', params=params)
        return resp

    async def get_request(self, path: str, params: dict = {}, return_json: bool = True):
        header = {}
        # if token:
        header['Authorization'] = self.token
        request_url = f'{self.url}/{path}'
        async with aiohttp.request('GET', request_url, headers=header, params=params) as response:
            return await response.json() if return_json else response

    async def post_request(self, 
                           path: str, 
                           data: dict = None, 
                           params: dict = {}, 
                           return_json: bool = True):
        header = {}
        # if token:
        header['Authorization'] = self.token
        request_url = f'{self.url}/{path}'
        async with aiohttp.request('POST', request_url, headers=header, params=params, json=data) as response:
            return await response.json() if return_json else response


api = MedApi()