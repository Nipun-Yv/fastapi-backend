system_instruction="""You are chatbot that has access to functions that you supply a 
place name which the user gives to you in natural language, you parse it and send the location_name
as a parameter into render_from_location_name or change the map type using change_map_type or fetch coordinates
to places near a given location using get_nearby_places, any other queries are not supported by you except 
these functions may give you an error response if they are not able to find the location at which point
you may ask the user to try again. Allowed map types are satellite,terrain,road and hybrid try to match the best possible
type to the user's description of the theme or type he wants, if and only if the description is very vague should you
ask the user to try again. You may refer https://developers.google.com/maps/documentation/javascript/place-types to see
the list of allowed place types that you may pass as the place parameter in the get_nearby_places function"""

tools=[
    {
            "function_declarations": [
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
# from google.generativeai import GenerativeModel
# import google.generativeai as genai
# from .mapServices import get_coordinates, get_weather, get_population

# genai.configure(api_key="AIzaSyCdiv_GOKtLgzQPr18xwC6A2earUwW0USg")

# def handle_function_call(call):
#     function_name = call.name
#     args = call.args
    
#     try:
#         if function_name == "render_from_location_name":
#             coordinates = get_coordinates(args["location_name"], "YOUR_API_KEY")
#             if isinstance(coordinates, tuple):
#                 lat, lng = coordinates
#                 return {
#                     "name": function_name,
#                     "response": {
#                         "latitude": lat,
#                         "longitude": lng,
#                         "status": "success"
#                     }
#                 }
        
#         elif function_name == "get_weather_info":
#             weather_data = get_weather(args["lat"], args["lng"])
#             return {
#                 "name": function_name,
#                 "response": {
#                     "temperature": weather_data["temp"],
#                     "conditions": weather_data["conditions"],
#                     "status": "success"
#                 }
#             }
            
#         elif function_name == "get_population_data":
#             population = get_population(args["location_name"])
#             return {
#                 "name": function_name,
#                 "response": {
#                     "population": population,
#                     "status": "success"
#                 }
#             }
            
#     except Exception as e:
#         return {
#             "name": function_name,
#             "response": {
#                 "error": str(e),
#                 "status": "error"
#             }
#         }

# class MapInfoBot:
#     def __init__(self, tools, model_name, instruction):
#         self.model = genai.GenerativeModel(
#             model_name, 
#             tools=tools,
#             system_instruction=instruction
#         )
#         self.chat = self.model.start_chat()
    
#     def process_function_calls(self, response):
#         # Get all function calls from the response
#         if not hasattr(response.candidates[0].content.parts[0], 'function_calls'):
#             return None, response
            
#         function_calls = response.candidates[0].content.parts[0].function_calls
        
#         # Handle each function call and collect responses
#         tool_outputs = []
#         results = {}
        
#         for call in function_calls:
#             function_result = handle_function_call(call)
#             tool_outputs.append(function_result)
            
#             # Store results for return
#             if function_result['response'].get('status') == 'success':
#                 results[call.name] = function_result['response']
        
#         # Send all function responses back to the model
#         if tool_outputs:
#             response = self.chat.send_message(
#                 None,
#                 tool_outputs=tool_outputs
#             )
            
#         return results, response
    
#     def send_message(self, message):
#         response = self.chat.send_message(message)
#         return self.process_function_calls(response)

# # Example usage
# tools = [
#     {
#         "name": "render_from_location_name",
#         "description": "Get coordinates for a location",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "location_name": {"type": "string"}
#             },
#             "required": ["location_name"]
#         }
#     },
#     {
#         "name": "get_weather_info",
#         "description": "Get weather information for coordinates",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "lat": {"type": "number"},
#                 "lng": {"type": "number"}
#             },
#             "required": ["lat", "lng"]
#         }
#     },
#     {
#         "name": "get_population_data",
#         "description": "Get population data for a location",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "location_name": {"type": "string"}
#             },
#             "required": ["location_name"]
#         }
#     }
# ]

# # Example of how to use it
# bot = MapInfoBot(tools, "gemini-pro", "You are a helpful location assistant")
# results, response = bot.send_message("What's the weather and population in New York?")