# import requests
# def get_coordinates(address, api_key):
#     base_url = "https://maps.googleapis.com/maps/api/geocode/json"
#     params = {
#         "address": address,
#         "key": api_key
#     }
#     response = requests.get(base_url, params=params)
#     if response.status_code == 200:
#         results = response.json().get('results')
#         if results:
#             location = results[0]['geometry']['location']
#             return [location['lat'], location['lng']]
#         else:
#             return "No results found."
#     else:
#         return f"Error connecting to the server right now"


# def get_nearby_places(api_key: str, location: str, place: str, radius: int = 5000):

#     base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
#     location=get_coordinates(location,api_key)
#     if(isinstance(location,str)):
#         return "Could not find the place you were looking for"
#     params = {
#         "location": f"{location[0]},{location[1]}",
#         "radius": radius,
#         "type": place,
#         "key": api_key
#     }

#     response = requests.get(base_url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         coordinates = [(location[0], location[1])]  # Include specified location
#         i=0
#         for place in data.get("results", []):
#             lat = place["geometry"]["location"]["lat"]
#             lng = place["geometry"]["location"]["lng"]
#             coordinates.append([lat, lng])
#             i+=1
#             if(i==10):
#                 break
#         return coordinates
#     else:
#         return "Error connecting to the server right now"

# def fetch_hotels(city: str, star_rating: int = None, user_rating: float = None):
#     hotels = [
#         {"name": "Hotel A", "city": "Delhi", "star_rating": 4, "user_rating": 4.5},
#         {"name": "Hotel B", "city": "Gurgaon", "star_rating": 5, "user_rating": 4.8},
#         {"name": "Hotel C", "city": "Noida", "star_rating": 3, "user_rating": 3.0},
#         {"name": "Hotel D", "city": "London", "star_rating": 4, "user_rating": 4.3},
#     ]

#     filtered_hotels = [
#         hotel for hotel in hotels
#         if hotel["city"] == city
#         and (star_rating is None or hotel["star_rating"] == star_rating)
#         and (user_rating is None or hotel["user_rating"] >= user_rating)
#     ]

#     return {"hotels": filtered_hotels}
import aiohttp
from typing import List, Dict, Union, Any

async def get_coordinates(address: str, api_key: str) -> Union[List[float], str]:
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            if response.status == 200:
                results = (await response.json()).get('results')
                if results:
                    location = results[0]['geometry']['location']
                    return [location['lat'], location['lng']]
                else:
                    return "No results found."
            else:
                return "Error connecting to the server right now"

async def get_nearby_places(api_key: str, location: str, place: str, radius: int = 5000) -> Union[List[List[float]], str]:
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    location = await get_coordinates(location, api_key)
    if isinstance(location, str):
        return "Could not find the place you were looking for"
    
    params = {
        "location": f"{location[0]},{location[1]}",
        "radius": radius,
        "type": place,
        "key": api_key
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                coordinates = [(location[0], location[1])]  # Include specified location
                i = 0
                for place in data.get("results", []):
                    lat = place["geometry"]["location"]["lat"]
                    lng = place["geometry"]["location"]["lng"]
                    coordinates.append([lat, lng])
                    i += 1
                    if i == 10:
                        break
                return coordinates
            else:
                return "Error connecting to the server right now"

async def fetch_hotels(city: str, star_rating: int = None, user_rating: float = None) -> Dict[str, List[Dict[str, Any]]]:
    hotels = [
        {"name": "Hotel A", "city": "Delhi", "star_rating": 4, "user_rating": 4.5},
        {"name": "Hotel B", "city": "Gurgaon", "star_rating": 5, "user_rating": 4.8},
        {"name": "Hotel C", "city": "Noida", "star_rating": 3, "user_rating": 3.0},
        {"name": "Hotel D", "city": "London", "star_rating": 4, "user_rating": 4.3},
    ]
    
    filtered_hotels = [
        hotel for hotel in hotels
        if hotel["city"] == city
        and (star_rating is None or hotel["star_rating"] == star_rating)
        and (user_rating is None or hotel["user_rating"] >= user_rating)
    ]
    
    return {"hotels": filtered_hotels}