import models
from config.db_config import engine,Base

def init_db():
    Base.metadata.create_all(bind=engine)

def drop_db():
    Base.metadata.drop_all(bind=engine)

# drop_db()
init_db()

# models.Base.
# # Importing library
# import qrcode

# # Data to encode
# data = "data"

# # Encoding data using make() function
# img = qrcode.make(data)

# # Saving as an image file
# img.save('MyQRCode.png')
