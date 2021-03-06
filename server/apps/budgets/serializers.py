from rest_framework import serializers

from .models import Transaction, BudgetThroughModel


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = []


class BudgetThroughModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetThroughModel
        exclude = ['created']

    def validate(self, attrs):
        if attrs['amount'] > attrs['transaction'].amount:
            raise serializers.ValidationError(
                {'amount': 'This transaction does not have that much.'})
        return attrs
 
