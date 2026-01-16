"""
Management command to create test data for the auction application.
Creates 5 test users, 1 admin user, and 10+ auction items.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random
from typing import List

from api.models import User, Item, Bid, Question, Answer


class Command(BaseCommand):
    help = 'Creates test data for the auction application'

    def handle(self, *args, **options) -> None:
        self.stdout.write("Creating test data...")

        # Create admin superuser
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@auctionhub.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f"Created admin user: admin / admin123"))

        # Create 5 test users
        test_users: List[User] = []
        user_data = [
            {'username': 'alice', 'email': 'alice@example.com', 'password': 'alice123'},
            {'username': 'bob', 'email': 'bob@example.com', 'password': 'bob123'},
            {'username': 'charlie', 'email': 'charlie@example.com', 'password': 'charlie123'},
            {'username': 'diana', 'email': 'diana@example.com', 'password': 'diana123'},
            {'username': 'eve', 'email': 'eve@example.com', 'password': 'eve123'},
        ]

        for data in user_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={'email': data['email']}
            )
            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {data['username']} / {data['password']}"))
            test_users.append(user)

        # Create 12 auction items
        items_data = [
            {
                'title': 'Vintage Leather Armchair',
                'description': 'Beautiful vintage leather armchair from the 1960s. In excellent condition with minor patina that adds to its character. Perfect for a study or living room.',
                'starting_price': Decimal('150.00'),
                'days_until_end': 5,
            },
            {
                'title': 'Antique Oak Writing Desk',
                'description': 'Stunning antique oak writing desk with multiple drawers and original brass handles. Dates back to the early 1900s. Some surface wear consistent with age.',
                'starting_price': Decimal('350.00'),
                'days_until_end': 7,
            },
            {
                'title': 'Vintage Vinyl Record Collection',
                'description': 'Collection of 50+ vinyl records from the 70s and 80s. Includes rock, jazz, and classical. All in playable condition. Great for collectors!',
                'starting_price': Decimal('75.00'),
                'days_until_end': 3,
            },
            {
                'title': 'Professional DSLR Camera',
                'description': 'Nikon D850 professional camera body. Low shutter count (under 10,000). Comes with original box and accessories. Perfect working condition.',
                'starting_price': Decimal('1200.00'),
                'days_until_end': 10,
            },
            {
                'title': 'Handmade Persian Rug',
                'description': 'Authentic handmade Persian rug, 8x10 feet. Wool with intricate traditional patterns in deep reds and blues. Made in Isfahan.',
                'starting_price': Decimal('800.00'),
                'days_until_end': 14,
            },
            {
                'title': 'Rare Comic Book Collection',
                'description': 'First edition Spider-Man and X-Men comics from the 1960s. Professionally graded and slabbed. A must-have for serious collectors.',
                'starting_price': Decimal('500.00'),
                'days_until_end': 6,
            },
            {
                'title': 'Mechanical Watch - Swiss Made',
                'description': 'Luxury Swiss mechanical watch with sapphire crystal and genuine leather band. Automatic movement, 42mm case diameter. Barely worn.',
                'starting_price': Decimal('450.00'),
                'days_until_end': 8,
            },
            {
                'title': 'Vintage Tea Set - Fine China',
                'description': 'Complete 12-piece vintage English bone china tea set. Includes teapot, sugar bowl, creamer, and 8 cups with saucers. Floral pattern with gold trim.',
                'starting_price': Decimal('120.00'),
                'days_until_end': 4,
            },
            {
                'title': 'Artist Oil Painting - Original',
                'description': 'Original oil painting on canvas, contemporary abstract style. Size 24x36 inches. Signed by the artist. Gallery worthy piece.',
                'starting_price': Decimal('250.00'),
                'days_until_end': 12,
            },
            {
                'title': 'Retro Gaming Console Bundle',
                'description': 'Nintendo NES console with 15 classic games including Mario, Zelda, and Metroid. All tested and working. Controllers included.',
                'starting_price': Decimal('180.00'),
                'days_until_end': 5,
            },
            {
                'title': 'Antique Brass Telescope',
                'description': 'Beautiful antique brass telescope on wooden tripod. Fully functional optics. A great decorative piece that actually works!',
                'starting_price': Decimal('200.00'),
                'days_until_end': 9,
            },
            {
                'title': 'Designer Handbag - Authentic',
                'description': 'Authentic Louis Vuitton Neverfull MM in Damier Ebene. Comes with dust bag and original receipt. Excellent pre-owned condition.',
                'starting_price': Decimal('700.00'),
                'days_until_end': 7,
            },
        ]

        created_items: List[Item] = []
        for i, data in enumerate(items_data):
            owner = test_users[i % len(test_users)]
            item, created = Item.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'starting_price': data['starting_price'],
                    'end_datetime': timezone.now() + timedelta(days=data['days_until_end']),
                    'owner': owner,
                }
            )
            if created:
                self.stdout.write(f"Created item: {data['title']}")
            created_items.append(item)

        # Create some bids on items
        for item in created_items[:6]:  # Add bids to first 6 items
            bidders = [u for u in test_users if u != item.owner]
            num_bids = random.randint(1, 4)
            current_price = item.starting_price
            
            for _ in range(num_bids):
                bidder = random.choice(bidders)
                bid_amount = current_price + Decimal(random.randint(5, 50))
                Bid.objects.get_or_create(
                    item=item,
                    bidder=bidder,
                    amount=bid_amount,
                )
                current_price = bid_amount

        # Create some questions and answers
        for item in created_items[:4]:  # Add Q&A to first 4 items
            askers = [u for u in test_users if u != item.owner]
            
            questions = [
                "Is this item still available for viewing before the auction ends?",
                "Can you provide more details about the condition?",
                "Do you offer shipping, or is this pickup only?",
            ]
            
            for q_text in random.sample(questions, k=random.randint(1, 2)):
                question, created = Question.objects.get_or_create(
                    item=item,
                    asker=random.choice(askers),
                    text=q_text,
                )
                
                if created and random.random() > 0.3:  # 70% chance of answer
                    Answer.objects.get_or_create(
                        question=question,
                        responder=item.owner,
                        text="Yes, absolutely! Please feel free to contact me for more information or to arrange a viewing.",
                    )

        self.stdout.write(self.style.SUCCESS("Test data creation completed!"))
        self.stdout.write("\nTest User Credentials:")
        self.stdout.write("=" * 40)
        self.stdout.write("Admin: admin / admin123")
        for data in user_data:
            self.stdout.write(f"{data['username']}: {data['username']} / {data['password']}")
