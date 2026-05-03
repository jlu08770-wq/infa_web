from django.db import models


WOMEN_PORTRAIT_FALLBACKS = [
    "/static/infa/profile-images/bhavneet.jpeg",
    "/static/infa/profile-images/hardik-sahu.jpeg",
    "/static/infa/profile-images/harshita.jpeg",
    "/static/infa/profile-images/radhika.jpeg",
    "/static/infa/profile-images/reshma.jpeg",
    "/static/infa/profile-images/shalini.jpeg",
]

WOMEN_COVER_FALLBACKS = [
    "/static/infa/profile-images/bhavneet.jpeg",
    "/static/infa/profile-images/radhika.jpeg",
    "/static/infa/profile-images/reshma.jpeg",
    "/static/infa/profile-images/shalini.jpeg",
]


# =====================================================
# Users Table
# Stores all users of the platform (Models, Organizers, Admins)
# =====================================================
class InfaUser(models.Model):

    # Role choices for user type
    ROLE_CHOICES = [
        ('model', 'Model'),
        ('organizer', 'Organizer'),
        ('admin', 'Admin'),
    ]

    name = models.CharField(max_length=100)              # Full name of user
    email = models.EmailField(unique=True)               # Unique email for login
    password = models.CharField(max_length=100)          # Hashed password (recommended)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # User role
    verified = models.BooleanField(default=False)        # Verification status
    location = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)
    cover_image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def _image_seed(self, slot):
        base = self.pk or self.email or self.name or 'guest'
        safe = str(base).replace('@', '-').replace(' ', '-').replace('.', '-').lower()
        return f"infa-{safe}-{slot}"

    def _fallback_index(self, slot, total):
        base = f"{self.pk or self.email or self.name or 'guest'}-{slot}"
        return sum(ord(char) for char in str(base)) % total

    @property
    def resolved_avatar_url(self):
        return self.avatar_url or WOMEN_PORTRAIT_FALLBACKS[
            self._fallback_index('avatar', len(WOMEN_PORTRAIT_FALLBACKS))
        ]

    @property
    def resolved_cover_image_url(self):
        return self.cover_image_url or WOMEN_COVER_FALLBACKS[
            self._fallback_index('cover', len(WOMEN_COVER_FALLBACKS))
        ]


# =====================================================
# Model Profile Table
# Stores additional details for users with role = "model"
# =====================================================
class InfaModelProfile(models.Model):

    user = models.ForeignKey(InfaUser, on_delete=models.CASCADE)
    # If user is deleted, profile is also deleted

    age = models.IntegerField()              # Model's age
    gender = models.CharField(max_length=20) # Gender
    category = models.CharField(max_length=50)  # Category (e.g., Fashion, Actor)
    experience = models.TextField()          # Experience description
    height_cm = models.PositiveIntegerField(null=True, blank=True)
    portfolio_image_url = models.URLField(blank=True)
    gallery_image_1_url = models.URLField(blank=True)
    gallery_image_2_url = models.URLField(blank=True)
    gallery_image_3_url = models.URLField(blank=True)
    instagram_handle = models.CharField(max_length=80, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} Profile"

    def _gallery_seed(self, slot):
        base = self.pk or self.user_id or self.user.name or 'profile'
        safe = str(base).replace(' ', '-').lower()
        return f"infa-profile-{safe}-{slot}"

    def _gallery_fallback(self, slot):
        return WOMEN_PORTRAIT_FALLBACKS[
            (sum(ord(char) for char in self._gallery_seed(slot)) % len(WOMEN_PORTRAIT_FALLBACKS))
        ]

    @property
    def resolved_portfolio_image_url(self):
        return self.portfolio_image_url or self._gallery_fallback('portfolio')

    @property
    def resolved_primary_image_url(self):
        return self.portfolio_image_url or self.gallery_image_1_url or self.user.avatar_url or self.resolved_portfolio_image_url

    @property
    def resolved_cover_image_url(self):
        return self.gallery_image_1_url or self.gallery_image_2_url or self.user.cover_image_url or self.resolved_primary_image_url

    @property
    def resolved_gallery_images(self):
        return [
            self.resolved_primary_image_url,
            self.gallery_image_1_url or self._gallery_fallback('gallery-1'),
            self.gallery_image_2_url or self._gallery_fallback('gallery-2'),
            self.gallery_image_3_url or self._gallery_fallback('gallery-3'),
        ]


# =====================================================
# Opportunities Table
# Stores opportunities posted by organizers
# =====================================================
class InfaOpportunity(models.Model):

    # Opportunity type choices
    TYPE_CHOICES = [
        ('paid', 'Paid'),
        ('collaboration', 'Collaboration'),
    ]

    # Opportunity status choices
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    organizer = models.ForeignKey(
        InfaUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'organizer'}
    )
    # Only users with role "organizer" can create opportunities

    title = models.CharField(max_length=100)       # Opportunity title
    description = models.TextField()               # Detailed description
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)  # Paid or collaboration
    budget = models.IntegerField()                 # Budget amount
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    category = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    image_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# =====================================================
# Profile Visit Table
# Tracks when an organizer visits a model's profile
# =====================================================
class ProfileVisit(models.Model):

    visit_date = models.DateTimeField(auto_now_add=True)
    # Automatically stores date & time of visit

    model = models.ForeignKey(
        InfaUser,
        on_delete=models.CASCADE,
        related_name='model_visits',
        limit_choices_to={'role': 'model'}
    )
    # Only users with role "model" can be visited

    organizer = models.ForeignKey(
        InfaUser,
        on_delete=models.CASCADE,
        related_name='organizer_visits',
        limit_choices_to={'role': 'organizer'}
    )
    # Only organizers can visit profiles

    def __str__(self):
        return f"{self.organizer.name} visited {self.model.name}"


class OpportunityApplication(models.Model):

    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    opportunity = models.ForeignKey(
        InfaOpportunity,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    model_profile = models.ForeignKey(
        InfaModelProfile,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    cover_note = models.TextField(blank=True)
    applied_on = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('opportunity', 'model_profile')

    def __str__(self):
        return f"{self.model_profile.user.name} -> {self.opportunity.title}"
