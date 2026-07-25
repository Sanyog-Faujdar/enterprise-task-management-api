from app import create_app
import os
from app.extensions import db
from app.models.user_models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    owner_email = os.getenv("OWNER_EMAIL", "owner@example.com")

    owner = User.query.filter_by(email=owner_email).first()

    if owner:
        print("Admin already exists.")
    else:
        admin = User(
            name=os.getenv("OWNER_NAME","owner"),
            email=os.getenv("OWNER_EMAIL","owner@example.com"),
            password=generate_password_hash(os.getenv("OWNER_PASSWORD","owner@123")),
            role=User.ROLE_ADMIN
        )

        db.session.add(admin)
        db.session.commit()
        print("Owner created successfully.")