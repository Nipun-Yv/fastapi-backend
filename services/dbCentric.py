from dotenv import load_dotenv
import os

load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")
import asyncpg


# async def fetch_hotels(city: str, star_rating: int = None, user_rating: float = None):
#     query = """
#     SELECT * FROM hotel_data
#     WHERE city = $1
#     """
#     params = [city]

#     if star_rating is not None:
#         query += " AND hotel_star = $2"
#         params.append(star_rating)

#     if user_rating is not None:
#         query += f" AND user_rating >= ${len(params) + 1}"
#         params.append(user_rating)

#     conn = await asyncpg.connect(CONNECTION_STRING)
#     try:
#         records = await conn.fetch(query, *params)
#         hotels = [dict(record) for record in records]
#         return {"hotels": hotels[:10]}
#     finally:
#         await conn.close()

# async def fetch_hotels(city: str, star_rating: int = None, user_rating: float = None):
#     query = """
#     SELECT hotel_star, user_rating, city, location, name, images[1] AS image
#     FROM hotel_data
#     WHERE city = $1
#     """
#     params = [city]

#     if star_rating is not None:
#         query += " AND hotel_star = $2"
#         params.append(star_rating)

#     if user_rating is not None:
#         query += f" AND user_rating >= ${len(params) + 1}"
#         params.append(user_rating)

#     conn = await asyncpg.connect(CONNECTION_STRING)
#     try:
#         records = await conn.fetch(query, *params)
#         hotels = [
#             {
#                 **dict(record),
#                 "image": f"https://{record.image}" if record.image else None
#             }
#             for record in records
#         ]
#         return {"hotels": hotels[:10]}
#     finally:
#         await conn.close()
async def fetch_hotels(city: str, star_rating: int = None, user_rating: float = None):
    query = """
    SELECT hotel_star, user_rating, city, location, name, 
           CONCAT('https:', (REGEXP_MATCHES(images, '//[^,}]+'))[1]) AS image
    FROM hotel_data
    WHERE city = $1
    """
    params = [city]

    if star_rating is not None:
        query += f" AND hotel_star = ${len(params) + 1}"
        params.append(star_rating)

    if user_rating is not None:
        query += f" AND user_rating >= ${len(params) + 1}"
        params.append(user_rating)

    conn = await asyncpg.connect(CONNECTION_STRING)
    try:
        records = await conn.fetch(query, *params)
        hotels = [dict(record) for record in records]
        return {"hotels": hotels[:10]}
    finally:
        await conn.close()

async def fetch_events(city: str, event_type: str = None):
    query = """
    SELECT id, name,location, city, type, description, image, start_date,end_date
           
    FROM events
    WHERE city = $1
    """
    params = [city]

    if event_type is not None:
        query += f" AND type = ${len(params) + 1}"
        params.append(event_type)


    conn = await asyncpg.connect(CONNECTION_STRING)
    try:
        records = await conn.fetch(query, *params)
        events = [dict(record) for record in records]
        return {"events": events[:10]}
    finally:
        await conn.close()