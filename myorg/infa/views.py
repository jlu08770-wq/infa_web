from collections import Counter

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .forms import InfaModelProfileForm, InfaUserForm, LoginForm, SignupForm
from .models import (
    InfaModelProfile,
    InfaOpportunity,
    InfaUser,
    OpportunityApplication,
    ProfileVisit,
)
from .serializers import (
    InfaModelProfileSerializer,
    InfaOpportunitySerializer,
    InfaUserSerializer,
    OpportunityApplicationSerializer,
    ProfileVisitSerializer,
)


DEFAULT_AVATAR = (
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330"
    "?auto=format&fit=crop&w=800&q=80"
)
DEFAULT_COVER = (
    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f"
    "?auto=format&fit=crop&w=1600&q=80"
)
DEFAULT_PORTFOLIO = (
    "https://images.unsplash.com/photo-1524504388940-b1c1722653e1"
    "?auto=format&fit=crop&w=1200&q=80"
)


def _profiles_queryset():
    return InfaModelProfile.objects.select_related('user').annotate(
        visit_count=Count('user__model_visits', distinct=True),
        application_count=Count('applications', distinct=True),
    )


def _opportunities_queryset():
    return InfaOpportunity.objects.select_related('organizer').annotate(
        application_count=Count('applications', distinct=True)
    )


def _applications_queryset():
    return OpportunityApplication.objects.select_related(
        'opportunity',
        'opportunity__organizer',
        'model_profile',
        'model_profile__user',
    )


def _current_user(request):
    user_id = request.session.get('infa_user_id')
    if not user_id:
        return None
    return InfaUser.objects.filter(pk=user_id).first()


def _current_profile(request):
    user = _current_user(request)
    if not user or user.role != 'model':
        return None
    return InfaModelProfile.objects.select_related('user').filter(user=user).first()


def _password_matches(raw_password, stored_password):
    if not stored_password:
        return False
    if stored_password == raw_password:
        return True
    try:
        return check_password(raw_password, stored_password)
    except ValueError:
        return False


def _selected_profile(request):
    profile_id = request.GET.get('profile')
    current_user = _current_user(request)
    current_profile = _current_profile(request)

    if current_profile:
        queryset = InfaModelProfile.objects.select_related('user').filter(user=current_profile.user)
        if profile_id:
            return queryset.filter(pk=profile_id).first()
        return current_profile

    if current_user and current_user.role == 'admin' and profile_id:
        return InfaModelProfile.objects.select_related('user').filter(pk=profile_id).first()

    return None


def _selected_organizer(request):
    organizer_id = request.GET.get('organizer')
    current_user = _current_user(request)

    if current_user and current_user.role == 'organizer':
        return current_user

    if current_user and current_user.role == 'admin' and organizer_id:
        queryset = InfaUser.objects.filter(role='organizer').order_by('name')
        return queryset.filter(pk=organizer_id).first()

    return None


def _build_querystring(request, **updates):
    params = request.GET.copy()
    for key, value in updates.items():
        if value in (None, ''):
            params.pop(key, None)
        else:
            params[key] = value
    query = params.urlencode()
    return f'?{query}' if query else ''


def signup_page(request):
    if _current_user(request):
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['infa_user_id'] = user.pk
            messages.success(request, 'Your account has been created successfully.')
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login_page(request):
    if _current_user(request):
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            password = form.cleaned_data['password']
            user = InfaUser.objects.filter(email__iexact=email).first()

            if user and _password_matches(password, user.password):
                if user.password == password:
                    user.password = make_password(password)
                    user.save(update_fields=['password'])
                request.session['infa_user_id'] = user.pk
                messages.success(request, f'Welcome back, {user.name}.')
                return redirect('home')

            form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_page(request):
    request.session.pop('infa_user_id', None)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def landing_page(request):
    context = {
        'total_models': InfaModelProfile.objects.count(),
        'total_opportunities': InfaOpportunity.objects.filter(status='open').count(),
        'total_applications': OpportunityApplication.objects.count(),
        'featured_profiles': _profiles_queryset().filter(featured=True)[:3],
    }
    return render(request, 'home.html', context)


def model_gallery_page(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    profiles = _profiles_queryset().order_by('-featured', '-visit_count', 'user__name')
    if query:
        profiles = profiles.filter(
            Q(user__name__icontains=query)
            | Q(user__location__icontains=query)
            | Q(category__icontains=query)
            | Q(gender__icontains=query)
        )
    if category:
        profiles = profiles.filter(category__iexact=category)

    context = {
        'profiles': profiles,
        'query': query,
        'selected_category': category,
        'categories': InfaModelProfile.objects.order_by('category')
        .values_list('category', flat=True)
        .distinct(),
        'default_avatar': DEFAULT_AVATAR,
    }
    return render(request, 'model_gallery.html', context)


def model_detail_page(request, pk):
    profile = get_object_or_404(_profiles_queryset(), pk=pk)
    organizer = _selected_organizer(request)

    if organizer:
        ProfileVisit.objects.get_or_create(model=profile.user, organizer=organizer)

    similar_profiles = _profiles_queryset().exclude(pk=profile.pk).filter(
        category__iexact=profile.category
    )[:4]
    matching_opportunities = _opportunities_queryset().filter(status='open').filter(
        Q(category__iexact=profile.category) | Q(category='')
    )[:4]

    context = {
        'profile': profile,
        'organizer': organizer,
        'similar_profiles': similar_profiles,
        'matching_opportunities': matching_opportunities,
        'default_avatar': DEFAULT_AVATAR,
        'default_cover': DEFAULT_COVER,
        'default_portfolio': DEFAULT_PORTFOLIO,
        'querystring': _build_querystring(
            request,
            organizer=organizer.pk if organizer else None,
        ),
    }
    return render(request, 'model_detail.html', context)


def opportunities_page(request):
    active_profile = _selected_profile(request)

    if request.method == 'POST':
        opportunity = get_object_or_404(
            InfaOpportunity,
            pk=request.POST.get('opportunity_id'),
            status='open',
        )
        if not active_profile:
            messages.error(request, 'Create a model profile first to apply for opportunities.')
        else:
            _, created = OpportunityApplication.objects.get_or_create(
                opportunity=opportunity,
                model_profile=active_profile,
            )
            if created:
                messages.success(request, f'Applied to "{opportunity.title}".')
            else:
                messages.info(request, f'You already applied to "{opportunity.title}".')
        return redirect(reverse('opportunity-board') + _build_querystring(
            request,
            profile=active_profile.pk if active_profile else None,
        ))

    query = request.GET.get('q', '').strip()
    opportunity_type = request.GET.get('type', '').strip()
    category = request.GET.get('category', '').strip()

    opportunities = _opportunities_queryset().filter(status='open').order_by(
        '-featured',
        '-id',
    )
    if query:
        opportunities = opportunities.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(location__icontains=query)
            | Q(organizer__name__icontains=query)
        )
    if opportunity_type:
        opportunities = opportunities.filter(type=opportunity_type)
    if category:
        opportunities = opportunities.filter(category__iexact=category)

    applied_ids = set()
    if active_profile:
        applied_ids = set(
            active_profile.applications.values_list('opportunity_id', flat=True)
        )

    context = {
        'opportunities': opportunities,
        'active_profile': active_profile,
        'applied_ids': applied_ids,
        'query': query,
        'selected_type': opportunity_type,
        'selected_category': category,
        'categories': InfaOpportunity.objects.exclude(category='')
        .order_by('category')
        .values_list('category', flat=True)
        .distinct(),
        'querystring': _build_querystring(
            request,
            profile=active_profile.pk if active_profile else None,
        ),
    }
    return render(request, 'opportunity_board.html', context)


def organizer_requests_page(request):
    organizer = _selected_organizer(request)
    opportunities = _opportunities_queryset().order_by('-featured', '-id')
    if organizer:
        opportunities = opportunities.filter(organizer=organizer)

    context = {
        'organizer': organizer,
        'opportunities': opportunities,
        'total_requests': opportunities.count(),
        'active_requests': opportunities.filter(status='open').count(),
        'featured_requests': opportunities.filter(featured=True).count(),
    }
    return render(request, 'organizer_requests.html', context)


def applications_page(request):
    active_profile = _selected_profile(request)
    applications = _applications_queryset().order_by('-applied_on', '-id')
    if active_profile:
        applications = applications.filter(model_profile=active_profile)
    else:
        applications = applications.none()

    counts = Counter(applications.values_list('status', flat=True))
    context = {
        'active_profile': active_profile,
        'applications': applications,
        'total_applications': applications.count(),
        'under_review_count': counts.get('under_review', 0),
        'hired_count': counts.get('hired', 0),
        'applied_count': counts.get('applied', 0),
    }
    return render(request, 'applications.html', context)


def edit_profile_page(request, pk):
    profile = get_object_or_404(InfaModelProfile.objects.select_related('user'), pk=pk)
    current_user = _current_user(request)

    if not current_user:
        messages.error(request, 'Please sign in to edit a profile.')
        return redirect('login')

    if current_user.role != 'admin' and profile.user_id != current_user.pk:
        messages.error(request, 'You can only edit your own profile.')
        return redirect('model-detail', pk=profile.pk)

    if request.method == 'POST':
        user_form = InfaUserForm(request.POST, instance=profile.user)
        profile_form = InfaModelProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile-edit', pk=profile.pk)
    else:
        user_form = InfaUserForm(instance=profile.user)
        profile_form = InfaModelProfileForm(instance=profile)

    context = {
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
        'default_avatar': DEFAULT_AVATAR,
        'default_cover': DEFAULT_COVER,
    }
    return render(request, 'profile_edit.html', context)


# =====================================================
# USER CRUD
# =====================================================
class InfaUserViewSet(viewsets.ModelViewSet):
    queryset = InfaUser.objects.all()
    serializer_class = InfaUserSerializer


# =====================================================
# Count Total Users
# =====================================================
class UserCountViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    def list(self, request):
        total = InfaUser.objects.count()
        return Response({'total_users': total})


# =====================================================
# MODEL PROFILE CRUD
# =====================================================
class ModelProfileViewSet(viewsets.ModelViewSet):
    queryset = InfaModelProfile.objects.select_related('user').all()
    serializer_class = InfaModelProfileSerializer


# =====================================================
# Profiles by Category
# =====================================================
class ProfilesByCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = InfaModelProfileSerializer

    def get_queryset(self):
        category = self.kwargs.get('category')
        return InfaModelProfile.objects.filter(category=category)


# =====================================================
# OPPORTUNITY CRUD
# =====================================================
class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = InfaOpportunity.objects.select_related('organizer').all()
    serializer_class = InfaOpportunitySerializer


# =====================================================
# Open Opportunities
# =====================================================
class OpenOpportunityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = InfaOpportunitySerializer

    def get_queryset(self):
        return InfaOpportunity.objects.filter(status='open')


# =====================================================
# Opportunities by Organizer
# =====================================================
class OpportunitiesByOrganizerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = InfaOpportunitySerializer

    def get_queryset(self):
        organizer_id = self.kwargs.get('organizer_id')
        return InfaOpportunity.objects.filter(organizer_id=organizer_id)


# =====================================================
# PROFILE VISIT CRUD
# =====================================================
class ProfileVisitViewSet(viewsets.ModelViewSet):
    queryset = ProfileVisit.objects.select_related('model', 'organizer').all()
    serializer_class = ProfileVisitSerializer


# =====================================================
# Visits for a Model
# =====================================================
class ModelVisitViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProfileVisitSerializer

    def get_queryset(self):
        model_id = self.kwargs.get('model_id')
        return ProfileVisit.objects.filter(model_id=model_id)


# =====================================================
# Count Visits per Model
# =====================================================
class ModelVisitCountViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ProfileVisitSerializer

    def list(self, request, *args, **kwargs):
        model_id = self.kwargs.get('model_id')
        total = ProfileVisit.objects.filter(model_id=model_id).count()
        return Response({'total_visits': total})


# =====================================================
# APPLICATION CRUD
# =====================================================
class OpportunityApplicationViewSet(viewsets.ModelViewSet):
    queryset = OpportunityApplication.objects.select_related(
        'opportunity',
        'model_profile',
        'model_profile__user',
    ).all()
    serializer_class = OpportunityApplicationSerializer


class ApplicationsByModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = OpportunityApplicationSerializer

    def get_queryset(self):
        model_id = self.kwargs.get('model_id')
        return OpportunityApplication.objects.filter(model_profile_id=model_id)


class ApplicationsByOpportunityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = OpportunityApplicationSerializer

    def get_queryset(self):
        opportunity_id = self.kwargs.get('opportunity_id')
        return OpportunityApplication.objects.filter(opportunity_id=opportunity_id)
