from django.shortcuts import render
import pandas as pd
import json


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
    # print(bar_graph['Country/Region'].values.tolist())
    country_names = bar_graph['Country/Region'].values.tolist()
    cases = bar_graph['values'].values.tolist()
    heat_map_jsondata = heat_map(bar_graph, country_names)
    heat_map_jsondata = json.dumps(heat_map_jsondata)
    # print(len(heat_map_jsondata))
    context = {'country_names': country_names,
               'cases': cases, 'total_cases': total_cases, 'heat_map_jsondata': heat_map_jsondata}
    return render(request, 'base_ui/home.html', context)


# format of data for passing into heat map
data = pd.read_json(
    "https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json")


def heat_map(bar_graph, country_names):
    heat_map = []
    for country in country_names:
        try:
            df = data[data['name'] == country]
            temp = {}
            temp['code3'] = list(df['code3'].values)[0]
            temp['name'] = country
            # temp['value'] = int(int(bar_graph[bar_graph['Country/Region']
            #                                   == country]['values'].sum()))
            # Or
            tdf = bar_graph[bar_graph['Country/Region'] == country]
            temp['value'] = int(list(tdf['values'].values)[0])
            temp['code'] = list(df['code'].values)[0]
            heat_map.append(temp)
        except:
            pass

    """Few prominent country names differed in sample data of heat_map & our
    bar_graph csv names so now have to filter them & add to our heat_map json  """

    From = ['US', 'Russia', 'Iran', 'Slovakia', 'Korea, South', 'Venezuela', 'Egypt', 'North Macedonia', 'Kyrgyzstan', 'Kosovo', 'Laos', 'Congo (Kinshasa)', 'Syria', 'Bahamas', 'Congo (Brazzaville)', 'Brunei',
            'Gambia', 'Yemen', 'Burma', 'Greenland', 'Saint Vincent and the Grenadines', 'Saint Kitts and Nevis', 'Micronesia']
    # 'Eritrea' not in to json file
    To = ['United States', 'Russian Federation', 'Iran, Islamic Rep.', 'Slovak Republic', 'Korea, Rep.',
          'Venezuela, RB', 'Egypt, Arab Rep.', 'Macedonia, FYR', 'Kyrgyz Republic', 'Lao PDR', 'Congo, Dem. Rep.', 'Syrian Arab Republic',
          'Bahamas, The', 'Congo, Rep.', 'Brunei Darussalam', 'Gambia, The', 'Yemen, Rep.', 'Myanmar', 'Greenland', 'St. Vincent and the Grenadines', 'St. Kitts and Nevis', 'Micronesia, Fed. Sts.']

    for i, missing_country in enumerate(To):
        try:
            df = data[data['name'] == missing_country]
            temp = {}
            temp['code3'] = list(df['code3'].values)[0]
            temp['name'] = missing_country
            tdf = bar_graph[bar_graph['Country/Region'] == From[i]]
            temp['value'] = int(list(tdf['values'].values)[0])
            temp['code'] = list(df['code'].values)[0]
            # print(df)
            # print(temp)
            heat_map.append(temp)
        except Exception as e:
            print(e)
    # print(heat_map)
    return heat_map
