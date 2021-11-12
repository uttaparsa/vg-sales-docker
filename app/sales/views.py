from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sales import serializers

df = pd.read_csv('vgsales.csv')
df = df.dropna()
df[['Year']] = df[['Year']].astype(int)


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
        return Response(df[df['Name'].str.contains(validated_data['name'])].to_dict(orient='records'),
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
                .sort_values(by=['Global_Sales'], ascending=False).to_dict(orient='records'),
            status=status.HTTP_200_OK)


class AmericanSellsMoreThanBritish(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            df.loc[df['NA_Sales'] < df['EU_Sales']][['Rank']].to_dict(orient='records'),
            status=status.HTTP_200_OK)


@extend_schema(parameters=[serializers.YearRangeSerializer])
class SalesByYearsPeriod(APIView):
    def get(self, request, *args, **kwargs):
        start_year = int(request.GET['start_year'])
        end_year = int(request.GET['end_year'])
        serializers.YearRangeSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        fig = self.create_figure(start_year, end_year)
        output = io.BytesIO()
        fig.savefig(output, format='png')
        return HttpResponse(output.getvalue(), content_type="image/png")

    def create_figure(self, start_year, end_year):
        data = df.loc[(df['Year'] >= start_year) & (df['Year'] <= end_year)].groupby(['Year'])['Global_Sales'].agg(
            'sum').to_dict()
        years = list(data.keys())
        sales = list(data.values())

        fig = plt.figure(figsize=(10, 5))

        # creating the bar plot
        plt.bar(years, sales, color='maroon',
                width=0.4)

        plt.xlabel("Year")
        plt.ylabel("Total Sells")
        plt.title("Total sells in each year")
        return fig


class SalesComparisonByGame(APIView):
    def get(self, request, *args, **kwargs):
        fig = self.create_figure()
        output = io.BytesIO()
        fig.savefig(output, format='png')
        return HttpResponse(output.getvalue(), content_type="image/png")

    def create_figure(self):
        barWidth = 0.1
        fig, ax = plt.subplots(figsize=(12, 8))

        NA = df[1:3]['NA_Sales']
        EU = df[1:3]['EU_Sales']
        JP = df[1:3]['JP_Sales']
        Other = df[1:3]['Other_Sales']
        Global = df[1:3]['Global_Sales']

        # Set position of bar on X axis
        br1 = np.arange(len(NA))
        br2 = [x + barWidth for x in br1]
        br3 = [x + barWidth for x in br2]
        br4 = [x + barWidth for x in br3]
        br5 = [x + barWidth for x in br4]

        # Make the plot
        plt.bar(br1, NA, color='r', width=barWidth,
                edgecolor='grey', label='NA')
        plt.bar(br2, EU, color='g', width=barWidth,
                edgecolor='grey', label='EU')
        plt.bar(br3, JP, color='b', width=barWidth,
                edgecolor='grey', label='JP')
        plt.bar(br4, Other, color='c', width=barWidth,
                edgecolor='grey', label='Other')
        plt.bar(br5, Global, color='m', width=barWidth,
                edgecolor='grey', label='Global')

        # Adding Xticks
        plt.xlabel('Game', fontweight='bold', fontsize=15)
        plt.ylabel('Sales', fontweight='bold', fontsize=15)
        plt.xticks([r + barWidth for r in range(len(NA))],
                   [df.iloc[1]['Name'], df.iloc[2]['Name']])
        plt.legend()
        return fig

@extend_schema(parameters=[serializers.YearRangeSerializer])
class CategorySalesByYear(APIView):
    def get(self, request, *args, **kwargs):
        start_year = int(request.GET['start_year'])
        end_year = int(request.GET['end_year'])
        serializers.YearRangeSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        fig = self.create_figure(start_year, end_year)
        output = io.BytesIO()
        fig.savefig(output, format='png')
        return HttpResponse(output.getvalue(), content_type="image/png")

    def create_figure(self, start_year, end_year):
        data = df.loc[(df['Year'] >= start_year) & (df['Year'] <= end_year)].groupby(['Genre'])['Global_Sales'].agg('sum').to_dict()
        categories = list(data.keys())
        sales = list(data.values())

        fig = plt.figure(figsize=(15, 8))

        # creating the bar plot
        plt.bar(categories, sales, color='c',
                width=0.4)

        plt.xlabel("Category")
        plt.ylabel("Total Sells")
        plt.title(f"{start_year} to {end_year}")
        return fig
