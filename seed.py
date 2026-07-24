from app import create_app
from app.extensions import db
from app.models.user_models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    if User.query.filter_by(role=User.ROLE_ADMIN).first():
        print("Admin already exists.")
    else:
        admin = User(
            name="owner",
            email="owner@example.com",
            password=generate_password_hash("owner@123"),
            role=User.ROLE_ADMIN
        )

        db.session.add(admin)
        db.session.commit()
        print("Owner created successfully.")