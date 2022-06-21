import csv
import datetime
from unicodedata import name
from django.shortcuts import render, redirect
from django.template import context
import pandas as pd
import json
import base_ui.views as v
import plotly.graph_objects as go
import plotly.offline as opy
import plotly.express as px

confirmedGlobal = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', encoding='utf-8', na_values=None)


def countryInsights(request, country_index):
    if request.method == 'POST':
        country_idx = request.POST['test']
        # print(country_idx)
        return redirect('country_graph', country_idx)
    context = {}
    total_cases = confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    bar_graph = confirmedGlobal[[
        'Country/Region', confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    bar_graph = bar_graph.reset_index()
    bar_graph.columns = ['Country/Region', 'values']
    countries_display = bar_graph['Country/Region'].values.tolist()
    bar_graph = bar_graph.sort_values(by='values', ascending=False)
    country_names = bar_graph['Country/Region'].values.tolist()
    # country get request top affected covid wise sorted
    country = country_names[int(country_index)]  # country is found
    row = confirmedGlobal[confirmedGlobal['Country/Region'] == country]
    # The appropriate row of the country and its cases on each day is gotten hold of
    # print(row)

    country_map = country_mapping(country_names)

    ''' Now we make a csv type data format so that plotly
    can plot it, it hase 2 columns date & covid cases  '''

    '''Data is a dict lookup where we see total cases till
        ystdy & we deduct that from todays total count sum
        to get cases on curr day '''

    data_csv = get_data_csv(row, bar_graph)
    # print(data_csv)

    fig = go.Figure(
        [go.Scatter(x=data_csv['date'], y=data_csv['cases'])])

    fig.update_layout(
        title="Tracking the Covid Timeline",
        xaxis_title="TimeLine",
        yaxis_title="Cases",
        legend_title="Legend Title",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        hovermode="x",
    )
    fig.update_traces(mode="markers+lines")
    div = opy.plot(fig, auto_open=False, output_type='div')
    context['fig'] = div
    context['country_map'] = country_map
    context['country'] = country
    context['countries_display'] = countries_display
    return render(request, 'data_insights/country.html', context)


def country_mapping(country_names):
    country_map = {}
    i = 0
    for c in country_names:
        country_map[c] = i
        i = i + 1
    return country_map


def get_data_csv(row, bar_graph):
    data = []
    data_csv =  pd.DataFrame(columns=['date', 'cases'])
    for i, col in enumerate(row):
        cases = list(row[col])[0]
        # print(i, row[col])
        t = {}
        if i > 3 and cases != 0:
            new_cases = 0
            if len(data_csv) > 1:
                # todays cases = cases sum till todays count - ystdy total count
                new_cases = cases - (data[-1])['cases']
            datetime_obj = datetime.datetime.strptime(str(col), "%m/%d/%y")
            t['date'] = datetime_obj
            t['cases'] = cases
            data_csv.loc[0] = [datetime_obj, new_cases]
            data_csv.index = data_csv.index + 1
        data.append(t)
    return data_csv


def versus(request, country_index1, country_index2):

    if request.method == 'POST':
        country_idx1 = request.POST['test1']
        country_idx2 = request.POST['test2']
        # print(country_idx1)
        return redirect('versus', country_idx1, country_idx2)

    context = {}
    bar_graph = confirmedGlobal[[
        'Country/Region', confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    bar_graph = bar_graph.reset_index()
    bar_graph.columns = ['Country/Region', 'values']
    countries_display = bar_graph['Country/Region'].values.tolist()
    context['countries_display'] = countries_display
    bar_graph = bar_graph.sort_values(by='values', ascending=False)
    country_names = bar_graph['Country/Region'].values.tolist()

    country1 = country_names[int(country_index1)]
    country2 = country_names[int(country_index2)]

    country_map = country_mapping(country_names)

    row1 = confirmedGlobal[confirmedGlobal['Country/Region'] == country1]
    row2 = confirmedGlobal[confirmedGlobal['Country/Region'] == country2]

    d1 = get_data_csv(row1, bar_graph)
    d2 = get_data_csv(row2, bar_graph)

    fig = px.line(markers=True)
    fig.add_scatter(x=d1['date'], y=d1['cases'], name=country1)
    fig.add_scatter(x=d2['date'], y=d2['cases'], name=country2)
    fig.update_traces(mode="markers+lines")
    fig.update_layout(
        title="Tracking the Covid Timeline",
        xaxis_title="TimeLine",
        yaxis_title="Cases",
        legend_title="Legend Title",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        ),
        hovermode="x",
    )
    div = opy.plot(fig, auto_open=False, output_type='div')
    context['fig'] = div
    context['country1'] = country1
    context['country2'] = country2
    context['country_map'] = country_map
    context['countries_display'] = countries_display

    return render(request, 'data_insights/countries.html', context)
