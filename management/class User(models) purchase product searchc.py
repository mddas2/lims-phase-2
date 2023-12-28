class User(models.Model)
    name
    id

class Product(models.Model):
    name = models.Charfifeld
    price = 

class PurchaseProuct(models.Model):
    user = models.Foreign with User
    product = models.Foreign with Product
    other...

make a orm query so that it print like

product_name      purchased count      total price