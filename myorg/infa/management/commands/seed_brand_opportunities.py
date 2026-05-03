from datetime import date

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from infa.models import InfaModelProfile, InfaOpportunity, InfaUser


DEFAULT_PASSWORD = "brandconnect123"


BRAND_DATA = [
    {
        "name": "Zara Casting Desk",
        "email": "zara@infa.demo",
        "location": "Mumbai, India",
        "bio": "International fashion retailer scouting verified editorial and commercial talent.",
        "avatar_url": "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?auto=format&fit=crop&w=900&q=80",
        "cover_image_url": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=1800&q=80",
        "opportunities": [
            {
                "title": "Zara Monsoon Lookbook 2026",
                "description": "Female models for a clean, modern monsoon lookbook with studio and lifestyle frames for India launch assets.",
                "type": "paid",
                "budget": 95000,
                "category": "Fashion",
                "location": "Mumbai",
                "start_date": date(2026, 5, 4),
                "end_date": date(2026, 5, 6),
                "featured": True,
                "image_url": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "title": "Zara Denim Street Edit",
                "description": "Fresh streetwear editorial campaign focused on confident urban portraits and movement-led styling.",
                "type": "paid",
                "budget": 78000,
                "category": "Commercial",
                "location": "Delhi",
                "start_date": date(2026, 5, 18),
                "end_date": date(2026, 5, 19),
                "featured": False,
                "image_url": "https://images.unsplash.com/photo-1521119989659-a83eee488004?auto=format&fit=crop&w=1200&q=80",
            },
        ],
    },
    {
        "name": "H&M Campaign Team",
        "email": "hm@infa.demo",
        "location": "Bengaluru, India",
        "bio": "Regional casting team for H&M digital campaigns and sustainability-led fashion stories.",
        "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=900&q=80",
        "cover_image_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=1800&q=80",
        "opportunities": [
            {
                "title": "H&M Summer Essentials Campaign",
                "description": "Seeking women with natural, expressive presence for a bright commercial campaign across ecommerce and social formats.",
                "type": "paid",
                "budget": 88000,
                "category": "Commercial",
                "location": "Bengaluru",
                "start_date": date(2026, 5, 10),
                "end_date": date(2026, 5, 12),
                "featured": True,
                "image_url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1200&q=80",
            },
            {
                "title": "H&M Conscious Edit Collaboration",
                "description": "Collaborative content shoot for eco-conscious styling stories with portrait and short-form video output.",
                "type": "collaboration",
                "budget": 35000,
                "category": "Lifestyle",
                "location": "Pune",
                "start_date": date(2026, 5, 22),
                "end_date": date(2026, 5, 23),
                "featured": False,
                "image_url": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=1200&q=80",
            },
        ],
    },
    {
        "name": "Vogue India Editorial",
        "email": "vogueindia@infa.demo",
        "location": "New Delhi, India",
        "bio": "Editorial casting desk for fashion stories, interviews, and special digital issues.",
        "avatar_url": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=900&q=80",
        "cover_image_url": "https://images.unsplash.com/photo-1521119989659-a83eee488004?auto=format&fit=crop&w=1800&q=80",
        "opportunities": [
            {
                "title": "Vogue India Modern Heritage Editorial",
                "description": "Editorial feature blending Indian textiles with contemporary portrait direction for a premium print and digital story.",
                "type": "paid",
                "budget": 120000,
                "category": "Editorial",
                "location": "Jaipur",
                "start_date": date(2026, 5, 14),
                "end_date": date(2026, 5, 16),
                "featured": True,
                "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=1200&q=80",
            }
        ],
    },
    {
        "name": "Lakme Fashion Week Team",
        "email": "lakme@infa.demo",
        "location": "Mumbai, India",
        "bio": "Runway and backstage casting team sourcing poised, camera-ready models for fashion week events.",
        "avatar_url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=900&q=80",
        "cover_image_url": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=1800&q=80",
        "opportunities": [
            {
                "title": "Lakme Fashion Week Runway Casting",
                "description": "Runway opportunity for female models with strong walk, polished portfolio, and backstage adaptability.",
                "type": "paid",
                "budget": 110000,
                "category": "Runway",
                "location": "Mumbai",
                "start_date": date(2026, 6, 2),
                "end_date": date(2026, 6, 5),
                "featured": True,
                "image_url": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=1200&q=80",
            }
        ],
    },
    {
        "name": "Tanishq Brand Studio",
        "email": "tanishq@infa.demo",
        "location": "Hyderabad, India",
        "bio": "Luxury jewellery brand team producing bridal, festive, and premium portrait campaigns.",
        "avatar_url": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=900&q=80",
        "cover_image_url": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=1800&q=80",
        "opportunities": [
            {
                "title": "Tanishq Festive Jewellery Campaign",
                "description": "Female talent for elegant portrait-led campaign work featuring festive styling and premium close-up beauty shots.",
                "type": "paid",
                "budget": 130000,
                "category": "Luxury",
                "location": "Hyderabad",
                "start_date": date(2026, 5, 28),
                "end_date": date(2026, 5, 30),
                "featured": True,
                "image_url": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=1200&q=80",
            }
        ],
    },
    {
        "name": "Nykaa Fashion Studio",
        "email": "nykaa@infa.demo",
        "location": "Gurugram, India",
        "bio": "Fashion marketplace creative team creating beauty, fashion, and campaign-led catalog imagery.",
        "avatar_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=900&q=80",
        "cover_image_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=1800&q=80",
        "opportunities": [
            {
                "title": "Nykaa Fashion Creator Campaign",
                "description": "Beauty-forward fashion shoot for ecommerce hero banners, reels, and seasonal style edits.",
                "type": "paid",
                "budget": 67000,
                "category": "Beauty",
                "location": "Gurugram",
                "start_date": date(2026, 5, 20),
                "end_date": date(2026, 5, 21),
                "featured": False,
                "image_url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1200&q=80",
            }
        ],
    },
]


MODEL_DATA = [
    {
        "name": "Bhavneet Kaur",
        "email": "bhavneet@infa.demo",
        "location": "Delhi, India",
        "bio": "Commercial and lifestyle model with a bright editorial presence.",
        "age": 22,
        "gender": "Female",
        "category": "Lifestyle",
        "experience": "Comfortable with outdoor lifestyle, fashion lookbooks, reels, and brand social content.",
        "height_cm": 165,
        "instagram_handle": "bhavneet.infa",
        "image": "/static/infa/profile-images/bhavneet.jpeg",
        "featured": True,
    },
    {
        "name": "Hardik Sahu",
        "email": "hardik@infa.demo",
        "location": "Mumbai, India",
        "bio": "Male commercial model for fashion, cafe, and urban lifestyle campaigns.",
        "age": 23,
        "gender": "Male",
        "category": "Commercial",
        "experience": "Available for menswear, accessories, lifestyle reels, and brand catalogue assignments.",
        "height_cm": 178,
        "instagram_handle": "hardik.infa",
        "image": "/static/infa/profile-images/hardik-sahu.jpeg",
        "featured": True,
    },
    {
        "name": "Harshita Sharma",
        "email": "harshita@infa.demo",
        "location": "Jaipur, India",
        "bio": "Traditional and festive fashion talent with expressive portrait work.",
        "age": 21,
        "gender": "Female",
        "category": "Ethnic",
        "experience": "Works well for ethnic wear, jewellery, festive catalogues, and creator-led campaigns.",
        "height_cm": 162,
        "instagram_handle": "harshita.infa",
        "image": "/static/infa/profile-images/harshita.jpeg",
        "featured": False,
    },
    {
        "name": "Radhika Mehra",
        "email": "radhika@infa.demo",
        "location": "Pune, India",
        "bio": "Editorial model with clean styling, soft movement, and outdoor shoot experience.",
        "age": 20,
        "gender": "Female",
        "category": "Editorial",
        "experience": "Best suited for editorial fashion, resort wear, beauty portraits, and premium lookbooks.",
        "height_cm": 168,
        "instagram_handle": "radhika.infa",
        "image": "/static/infa/profile-images/radhika.jpeg",
        "featured": True,
    },
    {
        "name": "Reshma Khan",
        "email": "reshma@infa.demo",
        "location": "Bengaluru, India",
        "bio": "Beauty and portrait model with dramatic lighting and close-up campaign experience.",
        "age": 24,
        "gender": "Female",
        "category": "Beauty",
        "experience": "Experienced in makeup, skincare, jewellery, mood-led portraits, and short-form content.",
        "height_cm": 166,
        "instagram_handle": "reshma.infa",
        "image": "/static/infa/profile-images/reshma.jpeg",
        "featured": False,
    },
    {
        "name": "Shalini Verma",
        "email": "shalini@infa.demo",
        "location": "Chandigarh, India",
        "bio": "Fresh fashion and ethnic model with natural camera presence.",
        "age": 19,
        "gender": "Female",
        "category": "Fashion",
        "experience": "Available for fashion catalogues, festive campaigns, outdoor portraits, and social shoots.",
        "height_cm": 164,
        "instagram_handle": "shalini.infa",
        "image": "/static/infa/profile-images/shalini.jpeg",
        "featured": False,
    },
]


class Command(BaseCommand):
    help = "Seed verified organizer accounts and featured brand opportunities."

    def handle(self, *args, **options):
        organizers_created = 0
        opportunities_created = 0
        models_created = 0

        for brand in BRAND_DATA:
            organizer_defaults = {
                "name": brand["name"],
                "password": make_password(DEFAULT_PASSWORD),
                "role": "organizer",
                "verified": True,
                "location": brand["location"],
                "bio": brand["bio"],
                "avatar_url": brand["avatar_url"],
                "cover_image_url": brand["cover_image_url"],
            }
            organizer, created = InfaUser.objects.update_or_create(
                email=brand["email"],
                defaults=organizer_defaults,
            )
            if created:
                organizers_created += 1

            for opportunity in brand["opportunities"]:
                _, opportunity_created = InfaOpportunity.objects.update_or_create(
                    organizer=organizer,
                    title=opportunity["title"],
                    defaults={
                        "description": opportunity["description"],
                        "type": opportunity["type"],
                        "budget": opportunity["budget"],
                        "status": "open",
                        "category": opportunity["category"],
                        "location": opportunity["location"],
                        "start_date": opportunity["start_date"],
                        "end_date": opportunity["end_date"],
                        "image_url": opportunity["image_url"],
                        "featured": opportunity["featured"],
                    },
                )
                if opportunity_created:
                    opportunities_created += 1

        for model in MODEL_DATA:
            user, created = InfaUser.objects.update_or_create(
                email=model["email"],
                defaults={
                    "name": model["name"],
                    "password": make_password(DEFAULT_PASSWORD),
                    "role": "model",
                    "verified": True,
                    "location": model["location"],
                    "bio": model["bio"],
                    "avatar_url": model["image"],
                    "cover_image_url": model["image"],
                },
            )
            if created:
                models_created += 1

            InfaModelProfile.objects.update_or_create(
                user=user,
                defaults={
                    "age": model["age"],
                    "gender": model["gender"],
                    "category": model["category"],
                    "experience": model["experience"],
                    "height_cm": model["height_cm"],
                    "portfolio_image_url": model["image"],
                    "gallery_image_1_url": model["image"],
                    "gallery_image_2_url": model["image"],
                    "gallery_image_3_url": model["image"],
                    "instagram_handle": model["instagram_handle"],
                    "featured": model["featured"],
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete. Organizers created: {organizers_created}, opportunities created: {opportunities_created}. "
            f"Models created: {models_created}. Demo password: {DEFAULT_PASSWORD}"
        ))
