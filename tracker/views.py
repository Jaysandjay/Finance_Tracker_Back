from rest_framework import viewsets, views
from rest_framework.response import Response
from datetime import date
from django.db.models import Sum
from .models import *
from .serializers import *


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        qs = Transaction.objects.all()
        month = self.request.query_params.get('month')
        type = self.request.query_params.get('type')
        min_amount = self.request.query_params.get('min_amount')
        max_amount = self.request.query_params.get('max_amount')

        if month:
            year, m = month.split('-')
            qs = qs.filter(date__year=year, date__month=m)
        
        if type:
            qs = qs.filter(type=type)
        
        if min_amount:
            qs = qs.filter(amount__gte=min_amount)

        if max_amount:
            qs = qs.filter(amount__lte=max_amount)
        
        return qs


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    qs = Budget.objects.all()


class MonthlySummaryView(views.APIView):
    def get(self, request):
        month = request.query_params.get('month')
        if month:
            year, m = month.split('-')
        else:
            today = date.today()
            year, m = today.year, today.month

        transactions = Transaction.objects.filter(date__year=year, date__month=m)
        total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

        by_category = (
            transactions.filter(type='expense')
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        return Response({
            'month': f"{year}-{m}",
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net': total_income - total_expenses,
            'by_category': list(by_category)
        })
        