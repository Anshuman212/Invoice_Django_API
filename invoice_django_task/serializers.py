from rest_framework import serializers
from .models import Invoice,InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=InvoiceDetail
        fields=['description','quantity','price','line_total']
    
class InvoiceSerializer(serializers.ModelSerializer):
    details=InvoiceDetailSerializer(many=True)
    class Meta:
        model=Invoice
        fields=['invoice_number','customer_name','date','details']
    
    def validate(self, data):
        details_data=data.get('details',[])
        if not details_data:
            raise serializers.ValidationError("Atleast one invoice should be included")
        
        total_sum=0
        for detail in details_data:
            price=detail['price']
            quantity=detail['quantity']
            if not price or not quantity:
                if not quantity:
                    raise serializers.ValidationError("No invoice without quantity")
                else:
                    raise serializers.ValidationError("No invoice without price")
            else:
                if price<0:
                    raise serializers.ValidationError("Price shoudl be greater than 0")
                elif quantity<0:
                    raise serializers.ValidationError("Quantity should be greater than 0")
            total_sum+=detail['line_total']
            
        if total_sum<=0:
            raise serializers.ValidationError("Total Sum should be greater than 0")
        
        return data
    
    def validate_line_total(self,value):
        
        quantity=self.initial_data.get('quantity')
        price=self.initial_data.get('price')
        if quantity and price:
            expected_line_total=quantity*price
            if value!=expected_line_total:
                raise serializers.ValidationError("Line total should be equal to quantity * price")
        
        return value
        
    
    def create(self,data_dictionary):
        data_for_details=data_dictionary.pop("details")
        new_invoice_create=Invoice.objects.create(**data_dictionary)
        for detail in data_for_details:
            InvoiceDetail.objects.create(invoice=new_invoice_create,**detail)
        return new_invoice_create

    def update(self,obj_instance,data_dictionay):
        data_for_details=data_dictionay.pop("details")
        obj_instance.invoice_number=data_dictionay.get('invoice_number',obj_instance.invoice_number)
        obj_instance.customer_name=data_dictionay.get('customer_name',obj_instance.customer_name)
        obj_instance.date=data_dictionay.get('date',obj_instance.date)
        obj_instance.save()
        
        for detail_data in data_for_details:
            #first let's find if there is a detail with same description
            #yes update no add
            description_to_check=detail_data.get('description')
            description_check=obj_instance.details.filter(description=description_to_check).first()
            if description_check:
                description_check.quantity=detail_data.get('quantity',description_check.quantity)
                description_check.price=detail_data.get('price',description_check.price)
                description_check.line_total=detail_data.get('line_total',description_check.line_total)
                description_check.save()
            else:
                InvoiceDetail.objects.create(invoice=obj_instance,**detail_data)
        
        return obj_instance
    