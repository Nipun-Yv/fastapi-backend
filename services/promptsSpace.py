system_instruction="""You are a hotel/event booking assistant(chatbot) named Aura, you are able to fetch hotels
based on parameters passed by the user regarding the start_rating, user_rating and city(limited to only certain cities) passed on by the user
which you send as parameters to the fetch_hotels function which will send back hotel data that you are to display to the user.
You are also able to fetch events like concerts, theatres,sport-events based on parameters passed by the user regarding the 
city, event_type which will send back event details that you are to display to the user.

You also have access to these functions:
You can supply a place name which the user gives to you in natural language, you parse it and send the location_name
as a parameter into render_from_location_name also you can change the map type using change_map_type or fetch coordinates
of places near a given location using get_nearby_places, any other queries are not supported by you except 
these, functions may give you an error response if they are not able to find the location at which point
you may ask the user to try again. Allowed map types are satellite,terrain,road and hybrid try to match the best possible
type to the user's description of the theme or type he wants, if and only if the description is very vague should you
ask the user to try again. You may refer https://developers.google.com/maps/documentation/javascript/place-types to see
the list of allowed place types that you may pass as the place parameter in the get_nearby_places function

You are only able to help with fetching and finding hotels and are supposed to respond with a message about your limitations
for unrelated queries"""
tools=[
    {
            "function_declarations": [
                {
                    "name": "fetch_hotels",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            "city": {
                            "type": "STRING",
                            "enum": ["Delhi", "Gurgaon", "Noida", "London"],
                            "description": "The city name that you are to extract from the user query"
                        },
                        "star_rating": {
                            "type": "INTEGER",
                            "description": "The hotel star rating used to classify hotels based on luxury"
                        },
                        "user_rating":{
                            "type":"NUMBER",
                            "description":"The user rating threshold, that is to be considered(greater than threshold value)"
                        }
                    },
                    "required": ["city"]
                    },
                    "description": (
                        "Accepts the city name(limited to certain cities),and user rating and star rating(which are not mandatory) and retrieves hotel data"
                    ),
                },
                {
                    "name": "fetch_events",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            "city": {
                            "type": "STRING",
                            "enum": ["Delhi", "London"],
                            "description": "The city name that you are to extract from the user query"
                        },
                        "event_type": {
                            "type": "STRING",
                            "enum":["concert","theatre","sport-event"],
                            "description": "The event type you are to fetch, only specific values are allowed"
                        },
                    },
                    "required": ["city"]
                    },
                    "description": (
                        "Accepts the city name(limited to certain cities),and event type(which is not mandatory) and retrieves event data"
                    ),
                },
                {
                    "name": "render_from_location_name",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            "location_name": {
                            "type": "STRING",
                            "description": "The location or address that the user wants to render on the map"
                        }
                    },
                    "required": ["location_name"]
                    },
                    "description": (
                        "Accepts a location or a address as an input and supplies the relevant information to my organisation to render it"
                    ),
                },
                {
                    "name": "change_map_type",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            "map_type": {
                            "type": "STRING",
                            "enum": ["satellite", "terrain", "hybrid", "roadmap"],
                            "description": "specification of only one of four map types: satellite, terrain, hybrid, roadmap"
                        }
                    },
                    "required": ["map_type"]
                    },
                    "description": (
                        "Accepts only one of four map types supplied by matching the best possible map type to the user's description"
                    ),
                },
                {
                    "name": "get_nearby_places",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            "location": {
                            "type": "STRING",
                            "description": "the location near which certain types of places are to be located(to be parsed from user query)"
                        },
                        "place": {
                            "type": "STRING",
                            "description": "the (type of) places that are to be located near the specific location, types of places are limited"
                        }
                    },
                    "required": ["location","place"]
                    },
                    "description": (
                        "Accepts a location and types of places to be found near that location"
                    ),
                },
            ]
        }
]