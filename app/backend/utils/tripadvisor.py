import requests

class TripAdvisorClient():
    HOST = 'https://api.content.tripadvisor.com/api/v1'
    HEADERS = {
        'accept': 'application/json'
    }

    def __init__(self, api_key) -> None:
        self.api_key = api_key
    
    def locations_index(self, query, address, lang="en"):
        endpoint = '/location/search'
        queryParams = f"?key={self.api_key}&searchQuery={query}&language={lang}&address={address}"
        print(self.HOST + endpoint + queryParams)
        response = requests.get(self.HOST + endpoint + queryParams, headers=self.HEADERS)
        print(response.json())
        return response.json()["data"]
    
    def location_detail(self, location_id, lang="en"):
        endpoint = f'/location/{location_id}/details'
        queryParams = f"?key={self.api_key}&language={lang}"
        print(self.HOST + endpoint + queryParams)
        response = requests.get(self.HOST + endpoint + queryParams, headers=self.HEADERS)
        print(response.json())
        return response.json() 