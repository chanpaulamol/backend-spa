from django.urls import path
from . import views

urlpatterns = [
    # Supplier URLs
    path('suppliers/', views.SupplierListCreateView.as_view(), name='supplier-list'),
    path('suppliers/<int:pk>/',
         views.SupplierRetrieveUpdateDestroyView.as_view(), name='supplier-detail'),

    # AHP Calculation URLs
    path('ahp/', views.AHPcalculationListCreateView.as_view(),
         name='ahp-calculation-list'),
    path('ahp/<int:pk>/', views.AHPcalculationRetrieveUpdateDestroyView.as_view(),
         name='ahp-calculation-detail'),

    # Criteria URLs
    path('criteria/', views.CriteriaListCreateView.as_view(), name='criteria-list'),
    path('criteria/<int:pk>/',
         views.CriteriaRetrieveUpdateDestroyView.as_view(), name='criteria-detail'),

    # Weights URLs
    path('weights/', views.WeightsListCreateView.as_view(), name='weights-list'),
    path('weights/<int:pk>/',
         views.WeightsRetrieveUpdateDestroyView.as_view(), name='weights-detail'),

    # Benefit and Cost URLs
    path('benefitcost/', views.BenefitCostListCreateView.as_view(),
         name='benefitcost-list'),
    path('benefitcost/<int:pk>/',
         views.BenefitCostRetrieveUpdateDestroyView.as_view(), name='benefitcost-detail'),
]
