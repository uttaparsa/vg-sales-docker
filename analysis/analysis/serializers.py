from rest_framework import serializers


class SalesComparisonByGameSerializer(serializers.Serializer):
    game1 = serializers.CharField(min_length=2, max_length=256)
    game2 = serializers.CharField(min_length=2, max_length=256)


class TwoPublisherSerialzier(serializers.Serializer):
    publisher1 = serializers.CharField(min_length=2, max_length=256)
    publisher2 = serializers.CharField(min_length=2, max_length=256)


class YearSerializer(serializers.Serializer):
    year = serializers.IntegerField(min_value=1, max_value=2100)


class YearRangeSerializer(serializers.Serializer):
    start_year = serializers.IntegerField(min_value=1970, max_value=2100)
    end_year = serializers.IntegerField(min_value=1971, max_value=2100)
