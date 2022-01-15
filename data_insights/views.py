import csv
import datetime
from django.shortcuts import render, redirect
from django.template import context
import pandas as pd
import json
import base_ui.views as v
import plotly.graph_objects as go
import plotly.offline as opy

confirmedGlobal = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', encoding='utf-8', na_values=None)


def countryInsights(request, country_index):
    if request.method == 'POST':
        country_idx = request.POST['test']
        print(country_idx)
        return redirect('country_graph', country_idx)
    context = {}
    total_cases = confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    bar_graph = confirmedGlobal[[
        'Country/Region', confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    bar_graph = bar_graph.reset_index()
    bar_graph.columns = ['Country/Region', 'values']
    countries_display = bar_graph['Country/Region'].values.tolist()
    context['countries_display'] = countries_display
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

    data = []
    data_csv = bar_graph
    data_csv.reset_index()
    data_csv.columns = ['date', 'cases']
    data_csv = data_csv.drop(range(0, 196))

    for i, col in enumerate(row):
        cases = list(row[col])[0]
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

    # print(data_csv)
    fig = go.Figure([go.Scatter(x=data_csv['date'], y=data_csv['cases'])])
    div = opy.plot(fig, auto_open=False, output_type='div')
    context['fig'] = div
    context['country_map'] = country_map
    context['country'] = country
    return render(request, 'data_insights/country.html', context)


def country_mapping(country_names):
    country_map = {}
    i = 0
    for c in country_names:
        country_map[c] = i
        i = i + 1
    return country_map
