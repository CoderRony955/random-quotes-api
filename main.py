from fastapi import FastAPI
from pydantic import BaseModel
import connect_db
import logging
import random

app = FastAPI()

cur = connect_db.connect.cursor()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode='w',
    filename='api.log',
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


class quote(BaseModel):
    type: str
    quote: str
    author: str


@app.get('/')
async def all_quotes():
    cur.execute("""
                        SELECT * FROM public."random quotes"
                        """)
    query = cur.fetchall()
    return {'quotes': query}


@app.get('/quote/{id}')
async def get_quote_by_id(id: int):
    cur.execute("""
                SELECT * from public."random quotes" WHERE id = %s
                """, (str(id),))
    quote_by_id = cur.fetchone()
    if quote_by_id:
        return {'status': 'successfully found', 'quote': quote_by_id}
    return {'status': f'quote not found by id {id}'}


@app.post('/post')
async def add_quote(quotes: quote):
    cur.execute("""
            INSERT INTO public."random quotes" (id, type, quote, author)
            VALUES (%s, %s, %s, %s) RETURNING *
        """, (
        random.randint(0, 10000),
        quotes.type,
        quotes.quote,
        quotes.author
    ))
    data = cur.fetchone()
    connect_db.connect.commit()
    return {'status': "quote successfully added", "quote": data}


@app.delete('/rmquote/{id}')
async def del_quote(id: int):
    cur.execute("""
                DELETE FROM public."random quotes" WHERE id = %s RETURNING *
                """, (id,))
    removed_quote = cur.fetchone()
    connect_db.connect.commit()
    if removed_quote:
        return {'status': f'quote with id {id} was successfully removed', 'quote': removed_quote}
    return {
        'status': f'quote with id {id} was not found'
    }


@app.put('/update/{id}')
async def update_qoute(id: int, quote: quote):
    cur.execute("""
                UPDATE public."random quotes" 
                SET type = %s, quote = %s, author = %s
                WHERE id = %s RETURNING *
                """, (quote.type, quote.quote, quote.author, id))
    new_quote = cur.fetchone()
    connect_db.connect.commit()
    if new_quote:
        return {'status': 'quote updated successfully', 'updated quote': new_quote}
    return {'status': f'quote with id {id} was not found'}
