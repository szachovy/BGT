# Big Data 01
# Temat: pobieranie danych; webscrapping; analiza słów
# Ćwiczenia 01 20.11.2020
# Termin nadsyłania prac

# Który autor jest największy?
# Napisz skrypt, który automatycznie pobierze wszystkie dzieła danego autora. Wybrana postać musi być autorem przynajmniej 10 publikacji.
# Napisz skrypt, który odpowied na pytanie: "Ile słów napisał autor w ciągu swojego życia?".
# W nagłówku programu w postaci komentarza należy zawrzeć: podsumowanie zadania + autorów rozwiązanie.
# Zadanie należy rozwiązać w parach z zastosowaniem dowolnej technologii.
# Należy wybrać autora, którego dzieła nie są chronione prawami autorskimi.

#Teofil Lenartowicz
from bs4 import BeautifulSoup
import requests

def accumulate(acc = []):
    acc += [len(BeautifulSoup(requests.get("https://literat.ug.edu.pl/teofil/00{}.htm".format(poem)).text, "lxml").text.split()) - 6 if poem < 10 else len(BeautifulSoup(requests.get("https://literat.ug.edu.pl/teofil/0{}.htm".format(poem)).text, "lxml").text.split()) - 6 for poem in range(1, 41)]
    return sum(acc)
    
print(accumulate()) # 15341

# Autor Wiktor Maj
