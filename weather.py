import requests
# url = "https://api.openweathermap.org/data/2.5/weather?lat=55.0415&lon=82.9346&appid=aead30913ed30e6fc7731ae288a4b48c"
# url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&ru&units=metric&appid=aead30913ed30e6fc7731ae288a4b48c"

class WeatherGet():
    def __init__(self, url=None, city=None, param=None, token=None):
        self._url = url
        self._city = city
        self._param = param
        self._token = token
        self._resresult = ''

    def get__temp_api(self):
        res = ''
        res__json = ''
        code = ''
        url = self._url + f"q={self._city}" + self._param + f"&appid={self._token}"
        res = requests.get(url)
        if res.status_code == 200:
            res__json = res.json()
            self._resresult = res__json
            return res__json
        else:
            code = res.status_code
            return code
    
    def set__url(self, url):
        self._url = url
    
    def set__city(self, city):
        self._city = city
    
    def set__param(self, param):
        self._param = param
    
    def set__token(self, token):
        self._token = token


