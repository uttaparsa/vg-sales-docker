from rest_framework import serializers


class NameSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)


class PlatformSerializer(serializers.Serializer):
    platform = serializers.CharField(max_length=256)


class YearSerializer(serializers.Serializer):
    year = serializers.IntegerField(min_value=1, max_value=2100)

class YearRangeSerializer(serializers.Serializer):
    start_year = serializers.IntegerField(min_value=1970, max_value=2100)
    end_year = serializers.IntegerField(min_value=1971, max_value=2100)

class CountSerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=1, max_value=16500)
