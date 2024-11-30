from django.db import models
from django.core.exceptions import ValidationError

class Invoice(models.Model):
    id=models.AutoField(primary_key=True)
    invoice_number=models.CharField(max_length=150,unique=True)
    customer_name=models.CharField(max_length=255)
    date=models.DateField()
    
    def __str__(self) -> str:
        return f"Invoice {self.invoice_number} - {self.customer_name} Date: {self.date}"
    
class InvoiceDetail(models.Model):
    id=models.AutoField(primary_key=True)
    invoice=models.ForeignKey(Invoice,related_name="details",on_delete=models.CASCADE)
    description=models.CharField(max_length=255)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=4)
    line_total=models.DecimalField(max_digits=10,decimal_places=4)
    
    def clean(self):
        if self.quantity * self.price != self.line_total:
            raise ValidationError("Line total must be equal to quantity * price.")
    def __str__(self):
        return f"Detail for {self.invoice.invoice_number}: {self.description}"