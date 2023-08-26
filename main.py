import databases
import sqlalchemy

from fastapi import FastAPI, Request

from pydantic import BaseModel, ValidationError

DATABASE_URL = 'postgresql://postgres@localhost:5432/store'

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# on each change of tables, run the following commands:
# alembic revision -m "Add a column"
# alembic upgrade head

books = sqlalchemy.Table(
    'books',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('title', sqlalchemy.String),
    sqlalchemy.Column('author', sqlalchemy.String),
    sqlalchemy.Column('reader_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('readers.id'), nullable=False, index=True),
)

readers = sqlalchemy.Table(
    'readers',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('first_name', sqlalchemy.String),
    sqlalchemy.Column('last_name', sqlalchemy.String),
)

# Not needed if using alembic
# engine = sqlalchemy.create_engine(DATABASE_URL)
# metadata.create_all(engine)

class BookCreate(BaseModel):
    title: str
    author: str
    reader_id: int

class ReaderCreate(BaseModel):
    first_name: str
    last_name: str

app = FastAPI()

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

@app.get('/books/')
async def get_all_books():
    query = books.select()
    return await database.fetch_all(query)


# @app.post('/books/')
# async def create_book(request: Request):
#     data = await request.json()
#     query = books.insert().values(**data)
#     last_record_id = await database.execute(query)
#     return {'id': last_record_id}

@app.post('/books/')
async def create_book(data: BookCreate):
    try:
        book_data = BookCreate(**data.dict())
    except ValidationError as e:
        return {'error': str(e)}

    query = books.insert().values(**book_data.dict())
    last_record_id = await database.execute(query)

    return {'id': last_record_id}

@app.get('/readers/')
async def get_all_readers():
    query = readers.select()
    return await database.fetch_all(query)


# @app.post('/readers/')
# async def create_reader(request: Request):
#     data = await request.json()
#     query = readers.insert().values(**data)
#     last_record_id = await database.execute(query)
#     return {'id': last_record_id}

@app.post('/readers/')
async def create_reader(request: ReaderCreate):
    try:
        reader_data = ReaderCreate(**request.dict())
    except ValidationError as e:
        return {'error': str(e)}
    
    query = readers.insert().values(**reader_data.dict())
    last_record_id = await database.execute(query)
    
    return {'id': last_record_id}
