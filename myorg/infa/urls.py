from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', InfaUserViewSet)
router.register(r'profiles', ModelProfileViewSet)
router.register(r'opportunities', OpportunityViewSet)
router.register(r'visits', ProfileVisitViewSet)
router.register(r'applications', OpportunityApplicationViewSet)

urlpatterns = [
    path('', landing_page, name='home'),
    path('signup/', signup_page, name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('discover/', model_gallery_page, name='model-gallery'),
    path('models/<int:pk>/', model_detail_page, name='model-detail'),
    path('opportunity-board/', opportunities_page, name='opportunity-board'),
    path('organizer/requests/', organizer_requests_page, name='organizer-requests'),
    path('dashboard/applications/', applications_page, name='applications-page'),
    path('profiles/<int:pk>/edit/', edit_profile_page, name='profile-edit'),

    # Counts
    path('users/count/', UserCountViewSet.as_view({'get': 'list'})),
    path('visits/count/<int:model_id>/', ModelVisitCountViewSet.as_view({'get': 'list'})),

    # Filters
    path('profiles/category/<str:category>/', ProfilesByCategoryViewSet.as_view({'get': 'list'})),
    path('opportunities/open/', OpenOpportunityViewSet.as_view({'get': 'list'})),
    path('opportunities/organizer/<int:organizer_id>/', OpportunitiesByOrganizerViewSet.as_view({'get': 'list'})),
    path('visits/model/<int:model_id>/', ModelVisitViewSet.as_view({'get': 'list'})),
    path('applications/model/<int:model_id>/', ApplicationsByModelViewSet.as_view({'get': 'list'})),
    path('applications/opportunity/<int:opportunity_id>/', ApplicationsByOpportunityViewSet.as_view({'get': 'list'})),

    path('api/', include(router.urls)),
    path('', include(router.urls)),
]
