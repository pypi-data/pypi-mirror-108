import json
import os
#  from pathlib import Path

# import requests
from cloudscraper import create_scraper


# noinspection PyTypeChecker,PyPep8Naming
class Leboncoin:
    def __init__(self):
        self.requests = create_scraper()
        self.headers = {
            "Referer": "https://www.leboncoin.fr/",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        }

        self._payload = {
            "limit": 35,
            "limit_alu": 3,
            "filters": {
                "enums": {
                    "ad_type": ["offer"]
                },
                "ranges": {
                    "price": {
                        "min": 0,
                    }
                },
                "location": {

                },
                "keywords": {

                },
                "category": {

                }
            }
        }

        current_path = os.path.dirname(os.path.realpath(__file__))
        with open(current_path + "/Ressources/regions.json", "r") as json_file:
            self.region_data = json.load(json_file)
        with open(current_path + "/Ressources/departements.json", "r") as json_file:
            self.dept_data = json.load(json_file)

    def setLimit(self, limit):
        self._payload["limit"] = int(limit)

    def maxPrice(self, price):
        self._payload["filters"]["ranges"]["price"]["max"] = int(price)

    def minPrice(self, price):
        self._payload["filters"]["ranges"]["price"]["min"] = int(price)

    def setRegion(self, region_name):
        for region in self.region_data:
            if region["channel"] == region_name:
                self._payload["filters"]["location"]["locations"] = [{
                    "locationType": "region",
                    "region_id": region["id"],
                    "label": region["name"]
                }]

    def setDepartement(self, dept_name):
        for dept in self.dept_data:
            if dept["channel"].lower() == dept_name:
                self._payload["filters"]["location"]["locations"] = [{
                    "country_id": "FR",
                    "department_id": str(dept["id"]),
                    "locationType": "department",
                    "region_id": dept["region_id"]
                }]

    def setLocation(self, lat: float, lng: float, radius: int):
        """ Radius (in kilometers) must be >= 10
        """
        assert lat and lng and radius
        assert radius >= 10, "Radius must be >= 10"
        self._payload["filters"]["location"]['area'] = {}
        self._payload["filters"]["location"]['area']['lat'] = float(lat)
        self._payload["filters"]["location"]['area']['lng'] = float(lng)
        self._payload["filters"]["location"]['area']['radius'] = int(radius * 1000)  # radius in API is in meters

    def _get_category(self, query):
        url = f"https://api.leboncoin.fr/api/parrot/v1/complete?q={query.replace(' ', '%20')}"
        r = self.requests.get(url, headers=self.headers)

        if r:
            return str(r.json()[0]["cat_id"])
        else:
            # No category returned
            return None

    def searchFor(self, query, autoCatgory=True):
        self._payload["filters"]["keywords"]["text"] = query
        if autoCatgory:
            category = self._get_category(query)
            if category:
                self._payload["filters"]["category"]["id"] = str(category)

    def setCategory(self, query):
        self._payload["filters"]["category"]["id"] = self._get_category(query)

    def execute(self):
        r = self.requests.post(
            url="https://api.leboncoin.fr/finder/search",
            data=json.dumps(self._payload),
            headers=self.headers
        )

        return r.json()
