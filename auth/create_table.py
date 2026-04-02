from auth_database import engine, Base
import models as models

Base.metadata.create_all(bind=engine)
