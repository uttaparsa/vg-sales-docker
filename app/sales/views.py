from django.shortcuts import render

# Create your views here.
import pandas as pd
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sales import serializers

df = pd.read_csv('vgsales.csv')


class RankView(APIView):

    def get(self, request, rank, *args, **kwargs):
        return Response(df.loc[df['Rank'] == rank].to_dict(orient='records')[0], status=status.HTTP_200_OK)


class NameView(APIView):

    @extend_schema(parameters=[serializers.NameSerializer])
    def get(self, request, *args, **kwargs):
        serializer = serializers.NameSerializer(
            data=request.GET
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        return Response(df[df['Name'].str.contains(validated_data['name'])].fillna('').to_dict(orient='records'),
                        status=status.HTTP_200_OK)


class FiveBestSellersBasedOnYearAndPlatform(APIView):

    @extend_schema(parameters=[serializers.YearSerializer, serializers.PlatformSerializer])
    def get(self, request, *args, **kwargs):
        serializers.YearSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        serializers.PlatformSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        return Response(
            df.loc[(df['Year'] == int(request.GET['year'])) & (df['Platform'] == request.GET['platform'])]
                .fillna('').sort_values(by=['Global_Sales'], ascending=False).to_dict(orient='records'),
            status=status.HTTP_200_OK)


class AmericanSellsMoreThanBritish(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            df.loc[df['NA_Sales'] < df['EU_Sales']][['Rank']].fillna('').to_dict(orient='records'),
            status=status.HTTP_200_OK)
