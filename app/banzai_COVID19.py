import io
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class BanzaiCOVID19():
    def __init__(self):
        self.global_confirmed_deaths_path = ""
        self.global_confirmed_cases_path = ""
        self.brazil_cases_path = ""
        self.brazil_deaths_path = ""
        self.countries_population_path = ""
        self.countries_lookup_path = ""

    #Get global data
    #datasource from
    #https://github.com/CSSEGISandData/COVID-19.git
    def get_global_cases(self):
        global_cases = pd.read_csv(self.global_confirmed_cases_path)
        # grouping by country at first (laziness)
        global_cases = global_cases.groupby(["Country/Region"], as_index=False).sum()
        # removing lat and long, the groupby summed the values...
        global_cases = global_cases.drop(["Lat", "Long"], axis=1)

        # transposing the columns to rows
        global_cases = global_cases.transpose()
        # making the top row as columns
        new_header = global_cases.iloc[0]
        global_cases.columns = new_header.str.lower()
        # removing the first row from dataframe
        global_cases = global_cases[1:]
        # converting the main time series index to datetime
        global_cases.index = pd.to_datetime(global_cases.index)
        global_cases.index = global_cases.index.rename("date")
        return global_cases

    def get_global_deaths(self):
        global_deaths = pd.read_csv(self.global_confirmed_deaths_path)
        # grouping by country at first (laziness)
        global_deaths = global_deaths.groupby(["Country/Region"], as_index=False).sum()
        # removing lat and long, the groupby summed the values...
        global_deaths = global_deaths.drop(["Lat", "Long"], axis=1)

        # transposing the columns to rows
        global_deaths = global_deaths.transpose()
        # making the top row as columns
        new_header = global_deaths.iloc[0]
        global_deaths.columns = new_header.str.lower()
        # removing the first row from dataframe
        global_deaths = global_deaths[1:]
        # converting the main time series index to datetime
        global_deaths.index = pd.to_datetime(global_deaths.index)
        global_deaths.index = global_deaths.index.rename("date")
        return global_deaths


    def get_brazil_cases(self):
        brazil_raw_cases = pd.read_csv(self.brazil_cases_path)
        brazilian_states = brazil_raw_cases.state.unique()
        brazil_cases = pd.DataFrame()
        i = 0
        for state in brazilian_states:
            state_deaths = brazil_raw_cases[brazil_raw_cases.state == state]
            # grouping by date if any state has more than one death information by day
            state_deaths = state_deaths.groupby(["date"], as_index=False).max()
            state_deaths = state_deaths.set_index("date")
            state_deaths.index = pd.to_datetime(state_deaths.index)
            state_deaths = state_deaths[["deaths"]]
            state_deaths = state_deaths.rename(columns={"deaths": state.lower()})
            if i == 0:
                brazil_cases = state_deaths
            else:
                brazil_cases = brazil_cases.join(state_deaths)
            i += 1
        return brazil_cases

    def get_brazil_deaths(self):
        brazil_raw_deaths = pd.read_csv(self.brazil_cases_path)
        brazilian_states = brazil_raw_deaths.state.unique()
        brazil_deaths = pd.DataFrame()
        i = 0
        for state in brazilian_states:
            state_deaths = brazil_raw_deaths[brazil_raw_deaths.state == state]
            # grouping by date if any state has more than one death information by day
            state_deaths = state_deaths.groupby(["date"], as_index=False).max()
            state_deaths = state_deaths.set_index("date")
            state_deaths.index = pd.to_datetime(state_deaths.index)
            state_deaths = state_deaths[["deaths"]]
            state_deaths = state_deaths.rename(columns={"deaths": state.lower()})
            if i == 0:
                brazil_deaths = state_deaths
            else:
                brazil_deaths = brazil_deaths.join(state_deaths)
            i += 1
        return brazil_deaths


    def get_countries_population(self):
        countries_population = pd.read_csv(self.countries_population_path)
        countries_lookup = pd.read_csv(self.countries_lookup_path)


        countries_lookup = countries_lookup[["Country_Code", "Country_Region"]]
        countries_lookup = countries_lookup.drop_duplicates()
        countries_lookup.index = countries_lookup.Country_Code

        countries_population = countries_population[countries_population.Year==2016]
        countries_population.index = countries_population.Country_Code
        countries_merge = countries_population.join(countries_lookup, lsuffix='_left', rsuffix='_right')
        result = countries_merge.groupby("Country_Region").sum()
        result.index = result.index.str.lower()
        return result

    def merge_global_brazil_cases(self, sp_cases, global_cases):
        result = global_cases.join(sp_cases)
        return result

    def merge_global_brazil_deaths(self, sp_deaths, global_deaths):
        result = global_deaths.join(sp_deaths)
        return result

    def get_timeless_comparison_cases(self, cases_count, cases):
        # creating a dataframe with all first date cases
        df_first_cases = pd.DataFrame(columns=["country", "event_date"])
        for label in cases.columns:
            event_date = cases[cases[label] > cases_count].index.min()
            # print(label,first_case_date)
            df_first_cases = df_first_cases.append(
                {"country": label,
                 "event_date": cases[cases[label] > cases_count].index.min()},
                ignore_index=True
            )
        df_timeless = pd.DataFrame(index=range(0, cases.shape[0]))
        df_timeless_item = pd.DataFrame()
        df_timeless.index.values
        column_names = []
        for index, row in df_first_cases.iterrows():
            df_timeless_item = cases[[row["country"]]][cases.index >= row["event_date"]]
            df_timeless_item.index = range(0, df_timeless_item.shape[0])
            df_timeless = pd.concat(
                [df_timeless, df_timeless_item],
                ignore_index=True, axis=1
            )
            column_names.append(row["country"])

        df_timeless.columns = column_names
        return df_timeless

    def get_timeless_comparison_deaths(self, deaths_count, deaths):
        # creating a dataframe with all first date cases
        df_first_cases = pd.DataFrame(columns=["country", "event_date"])
        for label in deaths.columns:
            event_date = deaths[deaths[label] > deaths_count].index.min()
            # print(label,first_case_date)
            df_first_cases = df_first_cases.append(
                {"country": label,
                 "event_date": deaths[deaths[label] >= deaths_count].index.min()},
                ignore_index=True
            )
        df_timeless = pd.DataFrame(index=range(0, deaths.shape[0]))
        df_timeless_item = pd.DataFrame()
        df_timeless.index.values
        column_names = []
        for index, row in df_first_cases.iterrows():
            df_timeless_item = deaths[[row["country"]]][deaths.index >= row["event_date"]]
            df_timeless_item.index = range(0, df_timeless_item.shape[0])
            df_timeless = pd.concat(
                [df_timeless, df_timeless_item],
                ignore_index=True, axis=1
            )
            column_names.append(row["country"])

        df_timeless.columns = column_names
        return df_timeless

    def consider_population(self, time_series, ratio):

        result = pd.DataFrame(index=time_series.index)

        countries_population = self.get_countries_population()
        for place in time_series.columns:
            try:
                population = countries_population[countries_population.index==place].Value[0]
                item = time_series[[place]].div((population/ratio))
                result = pd.concat([result, item], axis=1)
            except:
                result = result

        return result


    def plot_comparison_cases(self, cases, countries_array, max_days):
        plt.close('all')
        plt.title("COVID-19 Cases")
        plt.text(max_days - 2, 0.01, 'by Banzai',
                verticalalignment='bottom',
                horizontalalignment='right',
                color='black', fontsize=5)
        cases[countries_array][cases.index<=max_days].plot()
        plt.show()

    def plot_comparison_deaths(self, deaths, countries_array, max_days):
        plt.close('all')
        deaths[countries_array][deaths.index<=max_days].plot()
        plt.title("COVID-19 Deaths")
        plt.text(max_days - 2, 0.01, 'by Banzai',
                verticalalignment='bottom',
                 horizontalalignment='right',
                color='black', fontsize=5)
        plt.show()

    def plot_cases(self, countries, start_cases, count_days):
        confirmed = self.get_global_cases()
        sp_cases = self.get_brazil_cases()
        cases = self.merge_global_brazil_cases(sp_cases, confirmed)
        timeless_cases = self.get_timeless_comparison_cases(start_cases, cases)
        self.plot_comparison_cases(timeless_cases, countries, count_days)

    def plot_deaths(self, countries, start_deaths, count_days):
        deaths = self.get_global_deaths()
        sp_deaths = self.get_brazil_deaths()
        deaths = self.merge_global_brazil_deaths(sp_deaths, deaths)
        timeless_cases = self.get_timeless_comparison_deaths(start_deaths, deaths)
        self.plot_comparison_deaths(timeless_cases, countries, count_days)

    def get_filtered_dataframe(self, countries, start_deaths, count_days, death_rate):
        deaths = self.get_global_deaths()
        sp_deaths = self.get_brazil_deaths()
        deaths = self.merge_global_brazil_deaths(sp_deaths, deaths)
        timeless_deaths = self.get_timeless_comparison_deaths(start_deaths, deaths)
        timeless_deaths = timeless_deaths[countries]
        timeless_deaths = timeless_deaths[timeless_deaths.index <= int(count_days)]
        if death_rate:
            timeless_deaths = self.consider_population(timeless_deaths, 100000)
        return timeless_deaths

    def get_figure_plot_deaths(self, countries, start_deaths, count_days, log, death_rate):
        timeless_cases = self.get_filtered_dataframe(countries, start_deaths, count_days, death_rate)
        if death_rate:
            y_title = "Deaths per 100 000 people"
        else:
            y_title = "Total Deaths"

        fig = Figure()
        ax = fig.add_subplot(1,1,1)
        count_days = int(count_days)
        end_xticks = count_days + 2
        xticks = range(0, end_xticks)

        if count_days < 20:
            xticks = range(0, end_xticks)
        elif count_days < 40:
            xticks = range(0, end_xticks, 2)
        elif count_days < 60:
            xticks = range(0, end_xticks, 8)
        elif count_days < 100:
            xticks = range(0, end_xticks, 12)

        ax.set_ylabel(y_title)
        ax.set_xlabel("days after 1st death")
        if log:
            ax.set_title("COVID-19 Total Deaths (logarithmic) ")
            ax.text((count_days - 2), 2, 'by Banzai',
                    verticalalignment='bottom',
                    horizontalalignment='right',
                    color='black', fontsize=5)
            timeless_cases.plot(ax=ax, logy=True, xticks=xticks)
        else:
            ax.set_title("COVID-19 Total Deaths (linear)")
            ax.text((count_days - 2), 0.01, 'by Banzai',
                    verticalalignment='bottom',
                    horizontalalignment='right',
                    color='black', fontsize=5)
            timeless_cases.plot(ax=ax, xticks=xticks)

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return output

    def get_json_deaths(self, countries, start_deaths, count_days, log, death_rate):
        timeless_cases = self.get_filtered_dataframe(countries, start_deaths, count_days, death_rate)
        timeless_cases.reset_index(level=0, inplace=True)
        for label in timeless_cases.columns:
            timeless_cases[label] = pd.to_numeric(timeless_cases[label])
        return timeless_cases.to_json(orient="split")

    def get_json_gviz_deaths(self, countries, start_deaths, count_days, log, death_rate):
        timeless_cases = self.get_filtered_dataframe(countries, start_deaths, count_days, death_rate)
        timeless_cases.reset_index(level=0, inplace=True)
        timeless_cases = timeless_cases.rename(columns={"index":"days"})
        timeless_cases = timeless_cases.fillna("null")
        #gviz definition as dictionary
        table_columns = []
        table_rows = []


        for label in timeless_cases.columns:
            table_columns.append({"id": label,"label":label,"type":"number"})


        for index, row in timeless_cases.iterrows():
            row_cels = []
            for item in row:
                row_cels.append({"v":item})
            c = {"c": row_cels}
            table_rows.append(c)

        result = {
            "cols": table_columns,
            "rows": table_rows
        }
        return result
