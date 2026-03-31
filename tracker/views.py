from rest_framework import viewsets
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
 

    