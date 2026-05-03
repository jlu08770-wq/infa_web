from django.contrib import admin

from .models import (
    InfaModelProfile,
    InfaOpportunity,
    InfaUser,
    OpportunityApplication,
    ProfileVisit,
)


admin.site.register(InfaUser)
admin.site.register(InfaModelProfile)
admin.site.register(InfaOpportunity)
admin.site.register(ProfileVisit)
admin.site.register(OpportunityApplication)

# Register your models here.
