#!/usr/bin/env python
from django.contrib.auth.models import User
from defects.models import Product, Developer, DefectReport

# Clear existing data
DefectReport.objects.all().delete()
Developer.objects.all().delete()
Product.objects.all().delete()
User.objects.filter(username__in=['productowner', 'dev1']).delete()

# Create Product Owner
po = User.objects.create_user('productowner', 'po@test.com', 'pass123', is_staff=True)

# Create Developer
dev_user = User.objects.create_user('dev1', 'dev@test.com', 'pass123', is_staff=True)

# Create Product (Prod_1)
product = Product.objects.create(name='Prod_1', owner=po)

# Create Developer linked to product
developer = Developer.objects.create(user=dev_user, product=product)

# Defect Report 1: "Unable to search" - Status: Assigned
defect1 = DefectReport.objects.create(
    title="Unable to search",
    description="Search button unresponsive after completing an initial search",
    steps_to_reproduce="1. Complete a search\n2. Modify search criteria\n3. Click Search button",
    product=product,
    tester_id="Tester_1",
    tester_email="icyreward@gmail.com",
    status="Assigned",
    severity="Major",
    priority="High",
    assigned_developer=developer
)

# Defect Report 2: "Poor readability in dark mode" - Status: New
defect2 = DefectReport.objects.create(
    title="Poor readability in dark mode",
    description="Text unclear in dark mode due to lack of contrast with background",
    steps_to_reproduce="1. Enable dark mode\n2. Display text",
    product=product,
    tester_id="Tester_2",
    tester_email=None,
    status="New"
)

print("=" * 50)
print("DEMO SETUP COMPLETE")
print("=" * 50)
print(f"Product: {product.name} (ID: {product.id})")
print(f"Product Owner: productowner / pass123")
print(f"Developer: dev1 / pass123")
print(f"Defect 1: '{defect1.title}' - Status: {defect1.status}")
print(f"Defect 2: '{defect2.title}' - Status: {defect2.status}")
print("=" * 50)
