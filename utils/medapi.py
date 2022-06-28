import aiohttp


class MedApi:
    url = config.API_URL
    token = config.API_TOKEN
    
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
