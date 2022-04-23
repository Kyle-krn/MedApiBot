import aiohttp


class MedApi:
    url = 'https://sandbox-healthservice.priaid.ch'
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InNlbWVub2xlZ292aWNoQHlhbmRleC5ydSIsInJvbGUiOiJVc2VyIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc2lkIjoiMTA1NjMiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3ZlcnNpb24iOiIyMDAiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xpbWl0IjoiOTk5OTk5OTk5IiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwIjoiUHJlbWl1bSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbGFuZ3VhZ2UiOiJlbi1nYiIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvZXhwaXJhdGlvbiI6IjIwOTktMTItMzEiLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL21lbWJlcnNoaXBzdGFydCI6IjIwMjItMDQtMTIiLCJpc3MiOiJodHRwczovL3NhbmRib3gtYXV0aHNlcnZpY2UucHJpYWlkLmNoIiwiYXVkIjoiaHR0cHM6Ly9oZWFsdGhzZXJ2aWNlLnByaWFpZC5jaCIsImV4cCI6MTY1MDY0NjU4MiwibmJmIjoxNjUwNjM5MzgyfQ.95uPAq6bcdJSGavoIhjIFOq76bLevqMX_SopIIIotFU'

    async def get_body_locations(self, language: str):
        # {{host}}/body/locations?token={{token}}&language=ru-ru
        params = {'token': self.token, "language": language}
        resp = await self.get_request(path='body/locations', params=params)
        return resp


    async def get_body_sublocations(self, language: str, location_id: int):
        # {{host}}/body/locations?token={{token}}&language=ru-ru
        params = {"language": language}
        resp = await self.get_request(path=f'body/locations/{location_id}', params=params)
        return resp

    async def get_symptoms(self, language: str, location_id: int, gender: str):
        # {{host}}/symptoms/6/man?language=ru-ru&token={{token}}
        params = {"language": language}
        resp = await self.get_request(path=f'symptoms/{location_id}/{gender}', params=params)
        return resp

    async def get_diagnosis(self, language: str, male: bool, symptoms: list, year_of_birth: int):
        params = {'language': language, 
                  'gender': 'male' if male else 'female',
                  'symptoms' : str(symptoms),
                  'year_of_birth': year_of_birth
                  }
        resp = await self.get_request(path=f'diagnosis', params=params)
        return resp

    async def get_request(self, path: str, params: dict = {}, return_json: bool = True):
        while True:
            header = {}
            params['token'] = self.token
            request_url = f'{self.url}/{path}'
            async with aiohttp.request('GET', request_url, headers=header, params=params) as response:
                resp = await response.json() if return_json else response
                if resp == 'Invalid token':
                    await self.get_token()
                else:
                    return resp

    async def get_token(self):
        headers = {'Authorization': 'Bearer semenolegovich@yandex.ru:E1XZwmzECKefVcDAMoR26Q=='}
        async with aiohttp.request('POST', 'https://sandbox-authservice.priaid.ch/login', headers=headers) as response:
            resp = await response.json()
            token = resp['Token']
            self.token = token


api = MedApi()