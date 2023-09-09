import requests
import time

# API usage pricing info
# https://developers.google.com/maps/documentation/places/web-service/usage-and-billing


APIKEY = "your key"
#Primary search params
lat = 33.68
long = -117.83
# in meters
radius = 15000
# defined here https://developers.google.com/maps/documentation/places/web-service/supported_types
type = "restaurant"

# nearby search with contact fields
# https://developers.google.com/maps/documentation/places/web-service/search-nearby
r0 = requests.get(f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={ lat }%2C{ long }&radius={ radius }&type={ type }&key={APIKEY}')



j0 = r0.json()


print("first results ~ " + str(j0["results"][0]))
print("get place id " + j0["results"][0]["place_id"])
print("next page token ~ " + j0["next_page_token"])


#https://developers.google.com/maps/documentation/places/web-service/details
def get_info_from_jres(j):
    print("run get details from j ~ " + str(j))
    result = None
    if "result" in j:
        result = j["result"]
    if "results" in j:
        result = j["results"]
    for p in result:
        pid = p["place_id"]
        print("Getting details for placeId " + str(pid))
        time.sleep(1)
        d = requests.get(f"https://maps.googleapis.com/maps/api/place/details/json?fields=name%2Cformatted_address%2Cformatted_phone_number%2Cwebsite&place_id={pid}&key={APIKEY}").json()
        print("Details resp ~ " + str(d))

        if ("name" in d['result'] and "website" in d['result'] and
        "formatted_phone_number" in d['result'] and "formatted_address" in d['result']):
            with open("curldout", "a+") as of:
                of.write(f"Name ~{d['result']['name']}Website ~{d['result']['website']}Number ~{d['result']['formatted_phone_number']}Address ~ {d['result']['formatted_address']}\n")

# request next page and record data
def req_np_and_rec(npt):
    print("req nextpage call")
    nr = requests.get(f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={npt}&key={APIKEY}').json()
    get_info_from_jres(nr)
    print("nextpage call res ~ " + str(nr))
    next_pg_token = nr["next_page_token"]
    print("got npt ~ " + str(next_pg_token))
    return next_pg_token

def get_first_info_and_req_next_page(j):
    print("get info and recurse nextpage")
    get_info_from_jres(j)
    npt = j["next_page_token"]
    while npt != None:
        npt = req_np_and_rec(npt)

   
if __name__ == "__main__":
    print("run main recurse scrape")
    get_first_info_and_req_next_page(j0)