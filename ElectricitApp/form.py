
from django import forms

class EnergyEfficiencyForm(forms.Form):
    house_size_sqft = forms.FloatField(label='House Size (Sq. Ft.)')
    appliances = forms.MultipleChoiceField(
        choices=[('fan', 'Fan'), ('tv', 'TV'), ('washing_machine', 'Washing Machine'),
                 ('ac', 'Air Conditioner'), ('lighting', 'Lighting'), ('refrigerator', 'Refrigerator'),
                 ('oven', 'Oven'), ('microwave', 'Microwave'), ('toaster', 'Toaster'),
                 ('dishwasher', 'Dishwasher'), ('coffee_maker', 'Coffee Maker'), ('computer', 'Computer')],
        label='Select Appliances (Ctrl + Click to select multiple)'
    )
