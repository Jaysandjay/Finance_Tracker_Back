from django.db import models

class Category(models.model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#000000')

    def __str__(self): 
        return self.name
    
class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=250, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.type} - {self.amount} - {self.date}"
    
class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    month = models.DateField()
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('category', 'month')

    def __str__(self):
        return f"{self.category} - {self.month.strftime('%B %Y')} LIMIT: ${self.limit}"