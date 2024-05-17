from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas
import db

app = FastAPI()

@app.get("/products")
def get_products():
    mysql_db = mysql.connector.connect(host=db.host_name, port=db.port_number, user=db.user_name, password=db.password_db, database=db.database_name)
    cursor = mysql_db.cursor()
    cursor.execute("SELECT * FROM products")
    result = cursor.fetchall()
    mysql_db.close()
    cursor.close()
    return {"products": result}

@app.get("/products/{id}")
def get_products_by_id(int: id):
    mysql_db = mysql.connector.connect(host=db.host_name, port=db.port_number, user=db.user_name, password=db.password_db, database=db.database_name)
    cursor = mysql_db.cursor()
    cursor.execute(f"SELECT * FROM products WHERE id = {id}")
    result = cursor.fetchone()
    mysql_db.close()
    cursor.close()

    if result:
        return {"product": result}
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products")
def create_products(product:schemas.Product):
    mysql_db = mysql.connector.connect(host=db.host_name, port=db.port_number, user=db.user_name, password=db.password_db, database=db.database_name)
    cursor = mysql_db.cursor()

    cursor.execute("SELECT id FROM products WHERE id = %s", (product.id,))
    existing_product = cursor.fetchone()
    if existing_product:
        mysql_db.close()
        cursor.close()
        raise HTTPException(status_code=400, detail="ID already exist")


    id = product.id
    name = product.name
    price = product.price
    category = product.category
    expiration_date = product.expiration_date
    description = product.description
    image_url = product.image_url

    sql = "INSERT INTO products (id, name, price, category, expiration_date, description, image_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (id, name, price, category, expiration_date, description, image_url)
    cursor.execute(sql, val)
    mysql_db.commit()
    mysql_db.close()
    cursor.close()
    return {"message": "Product added successfully"}


@app.put("/products/{id}")
def change_products(id:int, product:schemas.Product):
    mysql_db = mysql.connector.connect(host=db.host_name, port=db.port_number, user=db.user_name, password=db.password_db, database=db.database_name)
    cursor = mysql_db.cursor()

    name = product.name
    price = product.price
    category = product.category
    expiration_date = product.expiration_date
    description = product.description
    image_url = product.image_url

    cursor = mysql_db.cursor()
    sql = "UPDATE products set name=%s, price=%s, category=%s, expiration_date=%s, description=%s, image_url=%s where id=%s"
    val = (id, name, price, category, expiration_date, description, image_url)
    cursor.execute(sql, val)
    mysql_db.commit()
    mysql_db.close()
    cursor.close()
    return {"message": "Product modified successfully"}

@app.delete("/products/{id}")
def delete_products(id : int):
    mysql_db = mysql.connector.connect(host=db.host_name, port=db.port_number, user=db.user_name, password=db.password_db, database=db.database_name)
    cursor = mysql_db.cursor()

    cursor.execute("SELECT id FROM products WHERE id = %s", (id,))
    existing_product = cursor.fetchone()
    if not existing_product:
        mysql_db.close()
        cursor.close()
        raise HTTPException(status_code=404, detail="Product not found")

    cursor.execute(f"DELETE FROM products WHERE id = {id}")
    mysql_db.commit()
    mysql_db.close()
    cursor.close()
    return {"message": "Product deleted successfully"}

