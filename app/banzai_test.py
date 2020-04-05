from banzai_COVID19 import BanzaiCOVID19 #my analysis class
import yaml


try:
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    analysis = BanzaiCOVID19()
    analysis.global_confirmed_deaths_path = config["files"]["covid19_deaths_global"]
    analysis.global_confirmed_cases_path = config["files"]["covid19_cases_global"]
    analysis.brazil_cases_path = config["files"]["covid19_cases_brazil"]
    analysis.brazil_deaths_path = config["files"]["covid19_cases_brazil"]

    countries = ["brazil", "italy", "spain", "sao paulo", "portugal"]
    img = analysis.get_figure_plot_deaths(countries, 1, 16, True)

except Exception as e:
    print('error', e)
