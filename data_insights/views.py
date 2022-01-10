from django.shortcuts import render
from django.template import context
import pandas as pd
import json
import base_ui.views as v

confirmedGlobal = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', encoding='utf-8', na_values=None)


def countryInsights(request, country_index):
    context = {}
    total_cases = confirmedGlobal[confirmedGlobal.columns[-1]].sum()
    bar_graph = confirmedGlobal[[
        'Country/Region', confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    bar_graph = bar_graph.reset_index()
    bar_graph.columns = ['Country/Region', 'values']
    bar_graph = bar_graph.sort_values(by='values', ascending=False)
    country_names = bar_graph['Country/Region'].values.tolist()
    cases = bar_graph['values'].values.tolist()
    print(country_names[int(country_index)])

    return render(request, 'data_insights/country.html', context)
