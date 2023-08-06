
import requests
from googletrans import Translator

def get_chuck_norries_joke():
    try:
        result = None
        response = requests.get("https://api.chucknorris.io/jokes/random")

        if response.ok:
            result = response.json()['value']
        return result
    except Exception as e:
        print(e)
      
def translate_joke(text):
    translator = Translator()
    return translator.translate(text, 'es').text

