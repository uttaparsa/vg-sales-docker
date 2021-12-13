from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from analysis import serializers

df = pd.read_csv('vgsales.csv')
df = df.dropna()
df[['Year']] = df[['Year']].astype(int)


@extend_schema(parameters=[serializers.YearRangeSerializer, serializers.TwoPublisherSerialzier])
class PublishersSalesComparisonByYearsPeriod(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializers.YearRangeSerializer(
            data=request.GET
        ).is_valid(raise_exception=True)

        serializers.TwoPublisherSerialzier(
            data=request.GET
        ).is_valid(raise_exception=True)

        start_year = int(request.GET['start_year'])
        end_year = int(request.GET['end_year'])

        publisher1 = request.GET['publisher1']
        publisher2 = request.GET['publisher2']

        fig = self.create_figure(start_year, end_year, publisher1, publisher2)
        output = io.BytesIO()
        fig.savefig(output, format='png')
        return HttpResponse(output.getvalue(), content_type="image/png")

    def create_figure(self, start_year, end_year, publisher1, publisher2):
        plt.clf()
        publisher1_data = \
            df[df['Publisher'].str.contains("Ubisoft") & (df['Year'] >= start_year) & (df['Year'] <= end_year)].groupby(
                ['Year'])[
                'Global_Sales'].agg('sum').to_dict()
        publisher2_data = \
            df[df['Publisher'].str.contains("Nintendo") & (df['Year'] >= start_year) & (
                    df['Year'] <= end_year)].groupby(['Year'])[
                'Global_Sales'].agg('sum').to_dict()

        # Create a dataframe using the two lists
        df_publisher_sales = pd.DataFrame(
            {'Years': publisher1_data.keys(),
             publisher1: publisher1_data.values(),
             publisher2: publisher2_data.values()})

        ax = plt.gca()

        # use plot() method on the dataframe
        df_publisher_sales.plot(x='Years', y=publisher1, ax=ax)
        df_publisher_sales.plot(x='Years', y=publisher2, ax=ax)

        return ax.get_figure()


@extend_schema(parameters=[serializers.YearRangeSerializer])
class TotalSalesByYearsPeriod(APIView):
    permission_classes = [IsAuthenticated]

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


@extend_schema(parameters=[serializers.SalesComparisonByGameSerializer])
class SalesComparisonByGame(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        game1 = request.GET['game1']
        game2 = request.GET['game2']
        fig = self.create_figure(game1, game2)
        output = io.BytesIO()
        fig.savefig(output, format='png')
        return HttpResponse(output.getvalue(), content_type="image/png")

    def create_figure(self, first_game_name, second_game_name):
        barWidth = 0.1
        fig, ax = plt.subplots(figsize=(12, 8))

        first_game = df[df['Name'].str.contains(first_game_name)][0:1]
        second_game = df[df['Name'].str.contains(second_game_name)][0:1]
        games_data = pd.concat([first_game, second_game], ignore_index=True)

        NA = games_data[0:2]['NA_Sales']
        EU = games_data[0:2]['EU_Sales']
        JP = games_data[0:2]['JP_Sales']
        Other = games_data[0:2]['Other_Sales']
        Global = games_data[0:2]['Global_Sales']

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
                   [games_data.iloc[0]['Name'], games_data.iloc[1]['Name']])

        plt.legend()
        return fig


@extend_schema(parameters=[serializers.YearRangeSerializer])
class CategorySalesByYear(APIView):
    permission_classes = [IsAuthenticated]

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
        data = df.loc[(df['Year'] >= start_year) & (df['Year'] <= end_year)].groupby(['Genre'])['Global_Sales'].agg(
            'sum').to_dict()
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
