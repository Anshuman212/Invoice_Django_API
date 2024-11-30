from rest_framework.test import APITestCase
from rest_framework import status
from invoice_django_task.models import InvoiceDetail,Invoice
from django.urls import reverse

class InvoiceAPITestCase(APITestCase):
    
    def setUp(self):
        self.url = reverse('invoices-list')
        self.invoice_data = {
            "invoice_number": "INV025",
            "customer_name": "Joe Doremon",
            "date": "2024-12-01",
            "details": [
                {
                    "description": "Product Key",
                    "quantity": 5,
                    "price": 500.000,
                    "line_total": 2500.00
                },
                {
                    "description": "Product Lock",
                    "quantity": 5,
                    "price": 70.00,
                    "line_total": 350.00
                }
            ]
        }
    
    def test_create_invoice(self):
        response=self.client.post(self.url,self.invoice_data,format='json')
        print(response)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        #ensuring that invoice is created
        invoice=Invoice.objects.get(invoice_number="INV025")
        self.assertEqual(invoice.customer_name,"Joe Doremon")
        self.assertEqual(invoice.details.count(),2)
        
    def test_update_invoice(self):
        self.invoice_data['invoice_number']="INV026"
        self.invoice_data['customer_name']="Jackie Chang"
        response=self.client.post(self.url,self.invoice_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        invoice=Invoice.objects.get(invoice_number='INV026')
        updated_data = {
            "invoice_number": "INV026",
            "customer_name": "Jackie Chang",
            "date": "2024-12-01",
            "details": [
                {
                    "description": "Product Lock",
                    "quantity": 3,
                    "price": 50.00,
                    "line_total": 150.00
                },
                {
                    "description": "Product Key",
                    "quantity": 2,
                    "price": 75.00,
                    "line_total": 150.00
                }
            ]
        }
        
        response=self.client.put(reverse('invoices-detail',kwargs={'pk':invoice.pk}),updated_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        updated_invoice=Invoice.objects.get(invoice_number='INV026')
        self.assertEqual(updated_invoice.customer_name,"Jackie Chang")
        self.assertEqual(updated_invoice.details.count(),2)
    
    def test_invalid_invoice_data(self):
        invalid_data = {
                "invoice_number": "INV012",
                "customer_name": "Jane Doe",
                "date": "2024-11-12",
                "details": [
                {
                    "description": "Product A",
                    "quantity": -2,
                    "price": 50.00,
                    "line_total": 100.00
                }
            ]
        }
        response=self.client.post(self.url,invalid_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        