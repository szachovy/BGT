# Zliczanie liczby słów wszystkich dzieł Teofila Lenartowicza

from bs4 import BeautifulSoup
import requests

def accumulate(acc = 0):
    for poem in range(1, 41):
        acc += len(BeautifulSoup(requests.get("https://literat.ug.edu.pl/teofil/00{}.htm".format(poem)).text, "lxml").text.split()) - 6 if poem < 10 else len(BeautifulSoup(requests.get("https://literat.ug.edu.pl/teofil/0{}.htm".format(poem)).text, "lxml").text.split()) - 6
    return acc 
    
print(accumulate()) # autor napisał 15341 słów
