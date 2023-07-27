from django.urls import path
from .views import (
    RegistrationView,
    LoginView,
    SupplierListCreateView,
    SupplierRetrieveUpdateDestroyView,
    RankingListView,
    RankingListCreateView,
    RankingDeleteAllView
)
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('suppliers/', SupplierListCreateView.as_view(),
         name='supplier-list-create'),
    path('suppliers/<int:pk>/', SupplierRetrieveUpdateDestroyView.as_view(),
         name='supplier-retrieve-update-destroy'),
    path('ahp/rankings/', RankingListView.as_view(), name='ranking-list'),
    path('ahp/save/', RankingListCreateView.as_view(), name='ranking-create'),
    path('ahp/delete-all/', RankingDeleteAllView.as_view(),
         name='ranking-delete-all')
]
