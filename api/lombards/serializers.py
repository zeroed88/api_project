from lombards.models import PercentQuery, Filial, GoldMark
from rest_framework import serializers

class PercentQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentQuery
        fields = (
            'percent',
            'lastName',
            'user',
            'ip',
            'zalogNumber',
            'relizDate'
            )
        extra_kwargs = {'ip': {'write_only': True}}



class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = (
            'name',
            'address',
            'phone',
            'shop',
            'image',
            'long',
            'lat',
            'daysInterval',
            'workTime'
        )

class GoldMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldMark
        fields = ('name', 'mark', 'price')
