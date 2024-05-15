from pydantic import BaseModel
class Product(BaseModel):
    id : int
    name : str
    price : int
    category : str
    expiration_date : str
    description : str
    image_url : str