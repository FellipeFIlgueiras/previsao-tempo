from datetime import date

import json
import requests

API_KEY = ""
API_LOCATION_URL = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
API_FORECAST_URL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"
API_FORECAST_DAYS = 5
API_LANGUAGE = "pt-br"

DIAS_SEMANA = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]


def get_localizacao():
    """
    Busca a região baseada no IP.
    :return: JSON com os dados da localização.
    """
    response = requests.get('http://www.geoplugin.net/json.gp')
    if response.status_code != 200:
        print('Não foi possível obter a localização!')
        return None
    else:
        return json.loads(response.text)


def get_latitude_longitude(localizacao):
    """
    Busca a latitude e longidade de uma localização.
    :param localizacao: JSON com os dados da localização.
    :return: A latitude e longitude da local.
    """
    try:
        latitude = localizacao['geoplugin_latitude']
        longitude = localizacao['geoplugin_longitude']
    except:
        return None
    return latitude, longitude


def get_dados_localizacao(latitude, longitude):
    """
    Busca o nome da cidade, estado e o código da localização baseada na latitude e longitude.
    :param latitude: Latitude da localização.
    :param longitude: Longitude da localização.
    :return: Código da localização, cidade e estado.
    """
    localizacao_url = f"{API_LOCATION_URL}?apikey={API_KEY}&q={latitude},{longitude}&language={API_LANGUAGE}"
    response = requests.get(localizacao_url)
    if response.status_code != 200:
        print('Erro ao obter código!')
        return None
    else:
        try:
            response_json = json.loads(response.text)
            codigo_localizacao = response_json['Key']
            cidade = response_json['ParentCity']['LocalizedName']
            estado = response_json['AdministrativeArea']['ID']
            return codigo_localizacao, cidade, estado
        except:
            return None


def get_clima(codigo_localizacao):
    """
    Consulta os dados do clima.
    :param codigo_localizacao: Código que corresponde a localização.
    :return: JSON com os dados do clima.
    """
    clima_url = f"{API_FORECAST_URL}{codigo_localizacao}?apikey={API_KEY}&language={API_LANGUAGE}&metric=true"
    response = requests.get(clima_url)
    if response.status_code != 200:
        print('Erro ao obter o clima!')
        return None
    else:
        try:
            response_json = json.loads(response.text)
            return response_json
        except:
            return None


def mostrar_clima(clima_json, cidade, estado):
    """
    Mostra ao usuário as informações de clima.
    :param clima_json: Informações do clima para os dias.
    :param cidade: Nome da cidade.
    :param estado: Nome do estado.
    :return: None caso aconteça alguma exception.
    """
    try:
        for day in range(0, API_FORECAST_DAYS):
            texto_clima = clima_json['DailyForecasts'][day]['Day']['IconPhrase']
            temperatura_minima = clima_json['DailyForecasts'][day]['Temperature']['Minimum']['Value']
            temperatura_maxima = clima_json['DailyForecasts'][day]['Temperature']['Maximum']['Value']
            temperatura_unidade = clima_json['DailyForecasts'][day]['Temperature']['Minimum']['Unit']
            dia_semana_int = int(date.fromtimestamp(clima_json['DailyForecasts'][day]['EpochDate']).strftime("%w"))
            dia_semana_txt = DIAS_SEMANA[dia_semana_int]

            print(f"Local: {cidade}, {estado}\n"
                  f"{dia_semana_txt}\n"
                  f"Condição: {texto_clima}\n"
                  f"Temperatura mínima: {temperatura_minima}º{temperatura_unidade}\n"
                  f"Temperatura máxima: {temperatura_maxima}º{temperatura_unidade}\n"
                  f"================================================================")
    except:
        print(clima_json)
        return None


def obter_clima():
    """
    Cria as chamadas para a obtenção do clima.
    """
    try:
        localizacao = get_localizacao()
        latitude, longitude = get_latitude_longitude(localizacao)
        codigo_localizacao, cidade, estado = get_dados_localizacao(latitude, longitude)
        clima_atual = get_clima(codigo_localizacao)
        mostrar_clima(clima_atual, cidade, estado)
    except:
        print("Não foi possível obter o clima atual, entre em contato com o suporte.")


if __name__ == '__main__':
    obter_clima()
