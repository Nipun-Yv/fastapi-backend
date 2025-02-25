

# class MapInfoBot:
#     def __init__(self, tools, model_name, instruction):
#         self.model = genai.GenerativeModel(
#             model_name, 
#             tools=tools,
#             system_instruction=instruction
#         )
#         self.chat = self.model.start_chat()
    
#     def send_message(self, message):
#         # if isinstance(message, dict):
#         #     response = self.chat.send_message(
#         #         f"Function response: {message['message']}"
#         #     )
            
#         #     if message['status'] == 'success':
#         #         return message, response
#         #     else:
#         #         return None, response
            
#         response = self.chat.send_message(message)
#         print(response)
#         tool_outputs=[]
#         if(response.candidates[0].content.parts[0].function_call):
#             for i in range(len(response.candidates[0].content.parts)):
#                 if response.candidates[0].content.parts[i].function_call:
#                     call = response.candidates[0].content.parts[i].function_call
#                     result = handle_function_call(call)
#                     if result['status'] == 'success':
#                         tool_outputs.append({
#                         "function_name":call.name,
#                         "message":None,
#                         "result":result
#                         })
#                     else:
#                         tool_outputs.append({
#                         "function_name":call.name,
#                         "message":"There was an internal server error",
#                         "result":None
#                         })
#         else:
#             return response.candidates[0].content.parts[0].text # a text response to user when it can't find a function call
#         return tool_outputs

from google.generativeai import GenerativeModel
import google.generativeai as genai
from services.mapServices import get_coordinates, get_nearby_places
from services.dbCentric import fetch_hotels, fetch_events
from dotenv import load_dotenv
import os
load_dotenv()
GENAI_KEY = os.getenv("GENAI_KEY")
genai.configure(api_key=GENAI_KEY)

async def handle_function_call(call):
    function_name = call.name
    args = call.args
    
    if function_name == "render_from_location_name":
        location_name = args.get("location_name")
        coordinates = await get_coordinates(location_name, "AIzaSyDXMtvMx_eAJOvqW8KpULaW2C__wwv43Yc")
        if isinstance(coordinates, list):
            return {
                "status": "success",
                "coordinates": coordinates,
                "message": f"Successfully retrieved coordinates for {location_name}: {coordinates}"
            }
        else:
            return {
                "status": "error",
                "message": coordinates
            }
    
    elif function_name == "change_map_type":
        map_type = args.get("map_type")
        return {
            "status": "success",
            "map_type": map_type,
            "message": f"successfully retrieved the map type from the query"
        }
    
    elif function_name == "get_nearby_places":
        location = args.get("location")
        place = args.get("place")
        result = await get_nearby_places("AIzaSyDXMtvMx_eAJOvqW8KpULaW2C__wwv43Yc", location, place, 5000)
        if isinstance(result, list):
            return {
                "status": "success",
                "coordinates": result,
                "message": f"Successfully retrieved coordinates"
            }
        else:
            return {
                "status": "error",
                "message": result
            }
    
    elif function_name == "fetch_hotels":
        city = args.get("city")
        user_rating = args.get("user_rating", None)
        star_rating = args.get("star_rating", None)
        result = await fetch_hotels(city, star_rating=star_rating, user_rating=user_rating)
        return {
            "status": "success",
            "message": result
        }
    elif function_name == "fetch_events":
        city = args.get("city")
        event_type = args.get("event_type", None)
        result = await fetch_events(city,event_type=event_type)
        return {
            "status": "success",
            "message": result
        }
    else:
        return {
            "status": "error",
            "message": "Unknown function requested."
        }

# class MapInfoBot:
#     def __init__(self, tools, model_name, instruction):
#         self.model = genai.GenerativeModel(
#             model_name,
#             tools=tools,
#             system_instruction=instruction
#         )
#         self.chat = self.model.start_chat()
    
#     async def send_message(self, message):
#         response = self.chat.send_message(message)
#         print(response)
#         tool_outputs = []
        
#         if response.candidates[0].content.parts[0].function_call:
#             print("Here?")
#             for i in range(len(response.candidates[0].content.parts)):
#                 if response.candidates[0].content.parts[i].function_call:
#                     call = response.candidates[0].content.parts[i].function_call
#                     result = await handle_function_call(call)
#                     if result['status'] == 'success':
#                         tool_outputs.append({
#                             "function_name": call.name,
#                             "message": None,
#                             "result": result
#                         })
#                     else:
#                         tool_outputs.append({
#                             "function_name": call.name,
#                             "message": "There was an internal server error",
#                             "result": None
#                         })
#         else:
#             print("It's not working")
#             return response.candidates[0].content.parts[0].text  # a text response to user when it can't find a function call
        
#         return tool_outputs
    
from typing import Dict, Optional
from datetime import datetime
# class Item(BaseModel):
#     text: str
#     conversation_id: Optional[str] = None

class MapInfoBot:
    _instances: Dict[str, 'MapInfoBot'] = {}
    _last_accessed: Dict[str, datetime] = {}
    
    @classmethod
    def get_instance(cls, conversation_id: str, tools, model_name, instruction) -> 'MapInfoBot':
        # Clean up old instances first
        cls._cleanup_old_instances()
        
        # Create new instance if doesn't exist
        if conversation_id not in cls._instances:
            cls._instances[conversation_id] = cls(tools, model_name, instruction)
        
        # Update last accessed time
        cls._last_accessed[conversation_id] = datetime.now()
        return cls._instances[conversation_id]
    
    @classmethod
    def _cleanup_old_instances(cls, max_age_minutes: int = 30):
        current_time = datetime.now()
        expired_ids = [
            conv_id for conv_id, last_accessed in cls._last_accessed.items()
            if (current_time - last_accessed).total_seconds() / 60 > max_age_minutes
        ]
        for conv_id in expired_ids:
            del cls._instances[conv_id]
            del cls._last_accessed[conv_id]

    def __init__(self, tools, model_name, instruction):
        self.model = genai.GenerativeModel(
            model_name,
            tools=tools,
            system_instruction=instruction
        )
        self.chat = self.model.start_chat()

    async def send_message(self, message):
        response = self.chat.send_message(message)
        print(response)
        tool_outputs = []

        if response.candidates[0].content.parts[0].function_call:
            print("Here?")
            for i in range(len(response.candidates[0].content.parts)):
                if response.candidates[0].content.parts[i].function_call:
                    call = response.candidates[0].content.parts[i].function_call
                    result = await handle_function_call(call)
                    if result['status'] == 'success':
                        tool_outputs.append({
                            "function_name": call.name,
                            "message": None,
                            "result": result
                        })
                    else:
                        tool_outputs.append({
                            "function_name": call.name,
                            "message": "There was an internal server error",
                            "result": None
                        })
                else:
                    print("It's not working")
        if not tool_outputs:
            return response.candidates[0].content.parts[0].text
        return tool_outputs