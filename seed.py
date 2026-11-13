
from getpass import getpass

from app.database import SessionLocal
from app.models.user import User
from app.security import hash_password


def create_user(db, role):
    print(f"\n--- Create {role.title()} Account ---")

    email = input(f"Enter {role} email: ").strip().lower()

    if not email:
        print("Email cannot be empty.")
        return

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        if existing_user.role == role:
            print(f"{role.title()} already exists.")
        else:
            print("This email belongs to another role.")
        return

    name = input(f"Enter {role} name: ").strip()
    phone = input(f"Enter {role} phone: ").strip()
    password = getpass(f"Enter {role} password: ")

    if not name or not phone:
        print("Name and phone cannot be empty.")
        return

    if len(password) < 8:
        print("Password must be at least 8 characters.")
        return

    user = User(
        name=name,
        email=email,
        phone=phone,
        password_hash=hash_password(password),
        role=role,
        status="active"
    )

    db.add(user)
    db.commit()

    print(f"{role.title()} created successfully!")


def main():
    db = SessionLocal()

    try:
        create_user(db, "teacher")
        create_user(db, "student")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    main()
