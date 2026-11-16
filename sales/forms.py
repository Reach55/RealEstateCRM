from django import forms

from .models import Sale
from properties.models import Property


class SalePropertyChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, property_obj):
        location = property_obj.district or property_obj.city or property_obj.location
        return (
            f'{property_obj.house_id} · {property_obj.title} · '
            f'{location} · ${property_obj.price:,.0f}'
        )


class SaleForm(forms.ModelForm):
    property = SalePropertyChoiceField(
        queryset=Property.objects.none(),
        label='Sale property',
        empty_label='Choose an available property',
        help_text='Available sale listings across the team portfolio.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available = Property.objects.filter(
            listing_type='SALE',
            status='AVAILABLE',
        )
        if self.instance.pk and self.instance.property_id:
            available = available | Property.objects.filter(pk=self.instance.property_id)
        self.fields['property'].queryset = available.select_related('agent').order_by('pk').distinct()
        self.available_properties = self.fields['property'].queryset

    class Meta:
        model = Sale
        fields = [
            'property',
            'customer',
            'agent',
            'selling_price',
            'sale_date',
            'payment_status',
            'notes',
        ]

        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
