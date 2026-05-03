from rest_framework import serializers
from .models import (
    InfaUser,
    InfaModelProfile,
    InfaOpportunity,
    ProfileVisit,
    OpportunityApplication,
)


# =====================================================
# User Serializer
# Converts InfaUser model data <-> JSON format
# Used for API requests & responses
# =====================================================
class InfaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfaUser          # Model to serialize
        fields = '__all__'        # Include all fields from the model


# =====================================================
# Model Profile Serializer
# Handles serialization for model profiles
# Used when creating, updating, or viewing model details
# =====================================================
class InfaModelProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_location = serializers.CharField(source='user.location', read_only=True)
    avatar_url = serializers.CharField(source='user.avatar_url', read_only=True)

    class Meta:
        model = InfaModelProfile  # Model being serialized
        fields = '__all__'        # Serialize all fields


# =====================================================
# Opportunity Serializer
# Converts opportunity data for API communication
# Used by organizers to post opportunities
# =====================================================
class InfaOpportunitySerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.name', read_only=True)

    class Meta:
        model = InfaOpportunity   # Opportunity model
        fields = '__all__'        # Include all fields


# =====================================================
# Profile Visit Serializer
# Tracks profile visits between users
# Useful for analytics (who viewed whose profile)
# =====================================================
class ProfileVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileVisit      # Profile visit tracking model
        fields = '__all__'        # Serialize all fields


class OpportunityApplicationSerializer(serializers.ModelSerializer):
    opportunity_title = serializers.CharField(source='opportunity.title', read_only=True)
    model_name = serializers.CharField(source='model_profile.user.name', read_only=True)

    class Meta:
        model = OpportunityApplication
        fields = '__all__'
