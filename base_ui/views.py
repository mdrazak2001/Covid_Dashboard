from django.shortcuts import render
import pandas as pd


def home(request):
    context = {}
    confirmedGlobal = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', encoding='utf-8', na_values=None)
    total_cases = confirmedGlobal[confirmedGlobal.columns[-1]].sum()

    bar_graph = confirmedGlobal[[
        'Country/Region', confirmedGlobal.columns[-1]]].groupby('Country/Region').sum()
    bar_graph = bar_graph.reset_index()
    bar_graph.columns = ['Country/Region', 'values']
    bar_graph = bar_graph.sort_values(by='values', ascending=False)
    print(bar_graph['Country/Region'].values.tolist())
    country_names = bar_graph['Country/Region'].values.tolist()
    cases = bar_graph['values'].values.tolist()

    context = {'country_names': country_names,
               'cases': cases, 'total_cases': total_cases}
    return render(request, 'base_ui/home.html', context)
