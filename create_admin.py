"""
Quick script to create an admin user
Run this with: python3 manage.py shell < create_admin.py
Or run: python3 create_admin.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cityservicehub_project.settings')
django.setup()

from core.models import Users

# Create admin user
admin_email = "admin@cityservicehub.com"
admin_password = "admin123"
admin_name = "Admin User"
admin_phone = "1234567890"
admin_address = "Admin Address"

# Check if admin already exists
if Users.objects.filter(email=admin_email).exists():
    print(f"Admin user with email {admin_email} already exists!")
    print("You can login with:")
    print(f"Email: {admin_email}")
    print(f"Password: {admin_password}")
else:
    admin_user = Users.objects.create(
        name=admin_name,
        email=admin_email,
        phone=admin_phone,
        password=admin_password,
        adress=admin_address,
        status="user",  # Status doesn't matter, email contains "admin"
        gender="male"
    )
    print("✅ Admin user created successfully!")
    print("\nLogin credentials:")
    print(f"Email: {admin_email}")
    print(f"Password: {admin_password}")
    print(f"\nAccess admin dashboard at: http://127.0.0.1:8000/admin-dashboard/")



