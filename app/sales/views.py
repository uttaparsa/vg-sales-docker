from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sales import serializers

df = pd.read_csv('vgsales.csv')
df = df.dropna()
df[['Year']] = df[['Year']].astype(int)


class RankView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, rank, *args, **kwargs):
        return Response(df.loc[df['Rank'] == rank].to_dict(orient='records')[0], status=status.HTTP_200_OK)


class NameView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[serializers.NameSerializer])
    def get(self, request, *args, **kwargs):
        serializer = serializers.NameSerializer(
            data=request.GET
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        return Response(df[df['Name'].str.contains(validated_data['name'])].to_dict(orient='records'),
                        status=status.HTTP_200_OK)


class FiveBestSellersBasedOnYearAndPlatform(APIView):
    permission_classes = [IsAuthenticated]

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
                .sort_values(by=['Global_Sales'], ascending=False).to_dict(orient='records'),
            status=status.HTTP_200_OK)


class AmericanSellsMoreThanBritish(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(
            df.loc[df['NA_Sales'] < df['EU_Sales']][['Rank']].to_dict(orient='records'),
            status=status.HTTP_200_OK)


class TopNRanksByPlatform(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[serializers.NSerializer, serializers.PlatformSerializer])
    def get(self, request, *args, **kwargs):
        serializers.NSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        serializers.PlatformSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        return Response(
            df.loc[df['Platform'] == request.GET['platform']]
                .sort_values(by=['Rank'], ascending=True)[:int(request.GET['N'])]
                .to_dict(orient='records'),
            status=status.HTTP_200_OK)


class TopNRanksByYear(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[serializers.NSerializer, serializers.YearSerializer])
    def get(self, request, *args, **kwargs):
        serializers.NSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        serializers.YearSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        return Response(
            df.loc[df['Year'] == int(request.GET['year'])]
                .sort_values(by=['Rank'], ascending=True)[:int(request.GET['N'])]
                .to_dict(orient='records'),
            status=status.HTTP_200_OK)


class TopNRanksByGenre(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(parameters=[serializers.NSerializer, serializers.GenreSerializer])
    def get(self, request, *args, **kwargs):
        serializers.NSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        serializers.GenreSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        return Response(
            df.loc[df['Genre'] == request.GET['genre']]
                .sort_values(by=['Rank'], ascending=True)[:int(request.GET['N'])]
                .to_dict(orient='records'),
            status=status.HTTP_200_OK)