from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('transactions', TransactionViewSet, basename='transaction')
router.register('budgets', BudgetViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', MonthlySummaryView.as_view())
]