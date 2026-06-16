from rest_framework import serializers
from .models import SalaryDetails, Payslip

class SalaryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryDetails
        fields = '__all__'

class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = '__all__'
