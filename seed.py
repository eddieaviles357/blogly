from models import User, db
from app import app

# Create tables
db.drop_all()
db.create_all()

# empty table if not empty
User.query.delete()

# Add users
eduardo = User(f_name="Eduardo", l_name="Aviles",
               img_url='https://images.unsplash.com/photo-1614436163996-25cee5f54290?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1042&q=80')
eric = User(f_name="Eric", l_name="Aviles",
            img_url='https://images.unsplash.com/photo-1614436163996-25cee5f54290?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1042&q=80')
noah = User(f_name="Noah", l_name="Aviles",
            img_url='https://images.unsplash.com/photo-1614436163996-25cee5f54290?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1042&q=80')

# Add object to our session
db.session.add(eduardo)
db.session.add(eric)
db.session.add(noah)

# Commit our data
db.session.commit()
