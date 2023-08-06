from leboncoin import Leboncoin
from pprint import pprint


lbc = Leboncoin()
lbc.searchFor("iphone", True)
lbc.setLimit(10)
lbc.maxPrice(2000)
lbc.setDepartement("tarn")
results = lbc.execute()


def show_ad(ad):
    print("Subject:", ad["subject"])
    print("Description:", ad["body"])
    print("Price:", ad["price"][0], "€")
    print("Url:", ad["url"])
    print("Image:", ad["images"]["urls"] or ad["images"]["small_url"], end="\n")


for ad in results["ads"]:
    show_ad(ad)
