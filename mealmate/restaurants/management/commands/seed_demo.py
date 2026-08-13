from django.core.management.base import BaseCommand
from accounts.models import User
from restaurants.models import Restaurant, MenuItem


class Command(BaseCommand):
    help = "Seeds demo owners, restaurants and menu items so the app isn't empty on first run."

    def handle(self, *args, **options):
        if Restaurant.objects.exists():
            self.stdout.write("Demo data already present, skipping.")
            return

        owner, _ = User.objects.get_or_create(
            username='spice_owner',
            defaults={'role': 'owner', 'email': 'owner@mealmate.test'}
        )
        owner.set_password('demo1234')
        owner.role = 'owner'
        owner.save()

        r1 = Restaurant.objects.create(
            owner=owner, name="Spice Route Kitchen", cuisine="Indian",
            address="12 MG Road, Guntur", avg_prep_time=25,
            description="North Indian comfort food, cooked the way your mother would."
        )
        r2 = Restaurant.objects.create(
            owner=owner, name="Dragon Wok", cuisine="Chinese",
            address="4 Lake View, Guntur", avg_prep_time=20,
            description="Fast, fiery, and fresh wok-tossed Chinese."
        )
        r3 = Restaurant.objects.create(
            owner=owner, name="Trattoria Bella", cuisine="Italian",
            address="9 Church Street, Guntur", avg_prep_time=35,
            description="Wood-fired pizza and slow-cooked pastas."
        )

        items = [
            (r1, "Paneer Butter Masala", "main", 220, True),
            (r1, "Chicken Biryani", "main", 260, False),
            (r1, "Garlic Naan", "starter", 45, True),
            (r1, "Gulab Jamun", "dessert", 60, True),
            (r1, "Masala Chai", "beverage", 30, True),
            (r2, "Veg Hakka Noodles", "main", 180, True),
            (r2, "Chilli Chicken", "starter", 210, False),
            (r2, "Spring Rolls", "starter", 120, True),
            (r2, "Iced Lemon Tea", "beverage", 70, True),
            (r3, "Margherita Pizza", "main", 280, True),
            (r3, "Pepperoni Pizza", "main", 340, False),
            (r3, "Tiramisu", "dessert", 150, True),
            (r3, "Garlic Bread", "starter", 110, True),
        ]
        for restaurant, name, category, price, veg in items:
            MenuItem.objects.create(
                restaurant=restaurant, name=name, category=category,
                price=price, is_veg=veg, description=f"A house favorite at {restaurant.name}."
            )

        self.stdout.write(self.style.SUCCESS(
            "Seeded 3 restaurants, 13 menu items, and owner login: spice_owner / demo1234"
        ))
