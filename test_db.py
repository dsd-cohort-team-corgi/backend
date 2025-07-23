from sqlmodel import Session, select, text
from app.db.engine import engine
from app.models.provider import Provider
from app.models.customer import Customer
from app.models.service import Service


def seed_auth_users():
    """Create dummy users in auth.users table"""
    with Session(engine) as session:

        # check if data exists
        results = session.exec(
            text(
                f"""
                Select * from auth.users
            """
            )
        )
        # if data exists remove the data
        # deletes from services as the key is tied to auth.users
        # if results:
        #     session.exec(text("delete from services"))
        #     session.exec(text("delete from auth.users"))

        # otherwise add new data into the database for auth users to set the user_id
        users_data = [
            {
                "id": "8d4f8c52-2f84-4a10-94a7-74b72fd14c91",
                "email": "olivia.martin@example.com",
                "encrypted_password": "securepassword1",
                "created_at": "now()",
                "updated_at": "now()",
                "phone": "+1-555-101-1234",
            },
            {
                "id": "2b07e53d-e98d-42d0-a2d3-d5c0f805f0fc",
                "email": "bob.johnson@example.com",
                "encrypted_password": "dummy_password",
                "created_at": "now()",
                "updated_at": "now()",
                "phone": "+1-555-102-2345",
            },
            {
                "id": "3a0e4bd6-7a17-4ef0-a221-b3e5ed91b57d",
                "email": "liam.james@example.com",
                "encrypted_password": "securepassword2",
                "created_at": "now()",
                "updated_at": "now()",
                "phone": "+1-555-103-3456",
            },
            {
                "id": "92bcfef9-3a78-40c9-b4b5-cc4783c41f3b",
                "email": "sophia.davis@example.com",
                "encrypted_password": "securepassword3",
                "created_at": "now()",
                "updated_at": "now()",
                "phone": "+1-555-104-4567",
            },
            {
                "id": "afc55bd2-60ec-4f25-b3b7-04c37241e9bb",
                "email": "noah.brown@example.com",
                "encrypted_password": "securepassword4",
                "created_at": "now()",
                "updated_at": "now()",
                "phone": "+1-555-105-5678",
            },
            {
                "id": "c8e21ab3-3ac4-4a2c-a3f9-24bc6a5411d8",
                "email": "emma.wilson@example.com",
                "encrypted_password": "securepassword5",
                "created_at": "now()",
                "updated_at": "now()",
                "phone": "+1-555-106-6789",
            },
            {
                "id": "e00b8de7-b841-4b8f-9b3c-f51b897cad92",
                "email": "jack.thomas@example.com",
                "encrypted_password": "securepassword6",
                "created_at": "now()",
                "updated_at": "now()",
                "phone": "+1-555-107-7890",
            },
        ]

        for user in users_data:
            session.exec(
                text(
                    f"""
                INSERT INTO auth.users (id, email, encrypted_password, created_at, updated_at)
                VALUES ('{user["id"]}', '{user["email"]}', '{user["encrypted_password"]}', now(), now())
                ON CONFLICT (id) DO NOTHING;
            """
                )
            )

        session.commit()


def seed_customers():

    with Session(engine) as session:

        # Check if customers already exist
        existing_customers = session.exec(text("SELECT COUNT(*) FROM customers")).first()
        if existing_customers and existing_customers[0] > 0:
            print("Customers already exist. Skipping customer seeding.")
            return

        # Get user IDs from auth.users table
        user_results = session.exec(
            text(
                """
                    SELECT u.id FROM auth.users u 
                    LEFT JOIN providers p ON u.id = p.user_id 
                    WHERE p.user_id IS NULL 
                    LIMIT 3
                """
            )
        )
        user_ids = [row[0] for row in user_results]

        if not user_ids:
            print("No users found in auth.users table. Please run seed_auth_users() first.")
            return

        # Create customers data using the user IDs
        customers_data = [
            {
                # "email": "olivia.martin@example.com",
                "phone_number": "+1-555-101-1234",
                "first_name": "Olivia",
                "last_name": "Martin",
                "user_id": user_ids[0] if len(user_ids) > 0 else None,
            },
            {
                # "email": "bob.johnson@example.com",
                "phone_number": "+1-555-102-2345",
                "user_id": user_ids[1] if len(user_ids) > 1 else None,
                "first_name": "Bob",
                "last_name": "Johnson",
            },
            {
                # "email": "liam.james@example.com",
                "phone_number": "+1-555-103-3456",
                "user_id": user_ids[2] if len(user_ids) > 2 else None,
                "first_name": "Liam",
                "last_name": "James",
            },
        ]

        session.bulk_insert_mappings(Customer, customers_data)
        session.commit()


def seed_providers():
    with Session(engine) as session:

        # Check if providers already exist
        existing_providers = session.exec(text("SELECT COUNT(*) FROM providers")).first()
        if existing_providers and existing_providers[0] > 0:
            print("providers  already exist. Skipping providers list.")
            return

        # Get user IDs from auth.users table

        user_results = session.exec(
            text(
                """
                    SELECT u.id FROM auth.users u 
                    LEFT JOIN providers p ON u.id = p.user_id 
                    WHERE p.user_id IS NULL 
                    offset 3 LIMIT 4
                """
            )
        )
        user_ids = [row[0] for row in user_results]

        if not user_ids:
            print("No users found in auth.users table. Please run seed_auth_users() first.")
            return

        # Create customers data using the user IDs
        provider_data = [
            {
                "phone_number": "+1-555-101-1234",
                "user_id": user_ids[0] if len(user_ids) > 0 else None,
                # "email": "sophia.davis@example.com",
                "first_name": "Sophia",
                "last_name": "Davis",
            },
            {
                # "email": "noah.brown@example.com",
                "user_id": user_ids[1] if len(user_ids) > 1 else None,
                "phone_number": "+1-555-105-5678",
                "first_name": "Noah",
                "last_name": "Brown",
            },
            {
                "user_id": user_ids[2] if len(user_ids) > 2 else None,
                # "email": "emma.wilson@example.com",
                "phone_number": "+1-555-106-6789",
                "first_name": "Emma",
                "last_name": "Wilson",
            },
            {
                "user_id": user_ids[3] if len(user_ids) > 3 else None,
                # "email": "jack.thomas@example.com",
                "phone_number": "+1-555-107-7890",
                "first_name": "Jack",
                "last_name": "Thomas",
            },
        ]

        session.bulk_insert_mappings(Provider, provider_data)
        session.commit()


def seed_services():
    with Session(engine) as session:

        # Check if services already exist
        existing_services = session.exec(text("SELECT COUNT(*) FROM services")).first()
        if existing_services and existing_services[0] > 0:
            print("services  already exist. Skipping providers list.")
            return

        # Get user IDs from auth.users table
        provider_results = session.exec(text("SELECT id FROM providers"))
        # for user in user_results:
        provider_ids = [row[0] for row in provider_results]

        if not provider_ids:
            print("No users found in auth.users table. Please run seed_auth_users() first.")
            return

        # Create customers data using the user IDs
        service_data = [
            {
                "service_title": "Deep Kitchen Cleaning",
                "service_description": "Thorough kitchen cleaning including appliances and cabinets.",
                "pricing": 120.00,
                "duration": 90,
                "category": "HOUSE_CLEANING",
                "provider_id": provider_ids[0],
            },
            {
                "service_title": "Lawn Mowing & Edging",
                "service_description": "Professional lawn mowing, edging, and cleanup.",
                "pricing": 80.00,
                "duration": 60,
                "category": "LAWN_AND_GARDEN",
                "provider_id": provider_ids[0],
            },
            {
                "service_title": "TV Wall Mounting",
                "service_description": "Secure TV mounting with cable management.",
                "pricing": 100.00,
                "duration": 45,
                "category": "ASSEMBLY_AND_INSTALLATION",
                "provider_id": provider_ids[0],
            },
            {
                "service_title": "Gutter Cleaning",
                "service_description": "Clearing gutters to prevent water damage and blockages.",
                "pricing": 110.00,
                "duration": 75,
                "category": "EXTERIOR_CLEANING",
                "provider_id": provider_ids[1],
            },
            {
                "service_title": "Window Washing",
                "service_description": "Interior and exterior window cleaning for up to 2 stories.",
                "pricing": 90.00,
                "duration": 60,
                "category": "EXTERIOR_CLEANING",
                "provider_id": provider_ids[1],
            },
            {
                "service_title": "Furniture Assembly",
                "service_description": "Fast and precise assembly for all major brands.",
                "pricing": 70.00,
                "duration": 50,
                "category": "ASSEMBLY_AND_INSTALLATION",
                "provider_id": provider_ids[1],
            },
            {
                "service_title": "Home Office Setup",
                "service_description": "Furniture arrangement and cable management for your workspace.",
                "pricing": 130.00,
                "duration": 90,
                "category": "HANDYMAN_AND_REPAIRS",
                "provider_id": provider_ids[2],
            },
            {
                "service_title": "Garage Power Wash",
                "service_description": "Remove oil stains and debris from garage floors.",
                "pricing": 95.00,
                "duration": 70,
                "category": "EXTERIOR_CLEANING",
                "provider_id": provider_ids[2],
            },
            {
                "service_title": "Move-Out Cleaning",
                "service_description": "Whole-home deep cleaning service to prepare for new tenants.",
                "pricing": 180.00,
                "duration": 120,
                "category": "HOUSE_CLEANING",
                "provider_id": provider_ids[3],
            },
            {
                "service_title": "Garden Design & Planting",
                "service_description": "Custom garden design and seasonal planting service.",
                "pricing": 150.00,
                "duration": 90,
                "category": "LAWN_AND_GARDEN",
                "provider_id": provider_ids[3],
            },
        ]

        session.bulk_insert_mappings(Service, service_data)
        session.commit()


if __name__ == "__main__":
    seed_auth_users()
    seed_customers()
    seed_providers()
    seed_services()
