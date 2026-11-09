from getpass import getpass

from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password


def create_teacher():
    db = SessionLocal()

    try:
        email = input("Enter teacher email: ").strip().lower()

        existing_user = db.query(User).filter(
            User.email == email
        ).first()

        if existing_user:
            if existing_user.role == "teacher":
                print("Teacher already exists.")
            else:
                print("This email belongs to a student.")
            return

        name = input("Enter teacher name: ").strip()
        phone = input("Enter teacher phone: ").strip()
        password = getpass("Enter teacher password: ")

        if len(password) < 8:
            print("Password must be at least 8 characters.")
            return

        teacher = User(
            name=name,
            email=email,
            phone=phone,
            password_hash=hash_password(password),
            role="teacher",
            status="active"
        )

        db.add(teacher)
        db.commit()

        print("Teacher created successfully!")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_teacher()