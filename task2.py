#Big Data 02
#Temat: pobieranie danych; webscrapping; analiza słów
#Ćwiczenia 02 23.11.2020
#Termin nadsyłania prac

#Który autor jest największy?
#Napisz skrypt, który automatycznie pobierze wszystkie dzieła danego autora. Wybrana postać musi być autorem przynajmniej 10 publikacji. Wybierz autora innego niż użyłeś w pierwszy zadaniu.
#- Jakie jest 10 najpopularniejszy słów autora?
#- Jakie są 3 najpopulurniszej rzeczowniki? (np. przez https://www.wordsapi.com/  np. przez sprawdzenie z listą rzeczwoników - to znalezienia)
#- W nagłówku programu w postaci komentarza należy zawrzeć: podsumowanie zadania + autorów rozwiązanie.
#Proszę użyć dobrych praktyk programistycznych (np. object oriented; SOLID; DRY, np.)
#Zadanie należy rozwiązać w parach z zastosowaniem dowolnej technologii.
#Należy wybrać autora, którego dzieła nie są chronione prawami autorskimi.

from bs4 import BeautifulSoup
import requests
from collections import Counter

def most_common(acc = []):
    for poem in range(1, 71):
        req = requests.get("https://literat.ug.edu.pl/roxolan/00{}.htm".format(poem)) if poem < 10 else requests.get("https://literat.ug.edu.pl/roxolan/0{}.htm".format(poem))
        text = BeautifulSoup(req.content, "lxml").text.split()
        acc += text[2:len(text)-2]
    
    return Counter(acc).most_common(10)
    
print(most_common())

# Autor Wiktor Maj
