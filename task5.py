
# Big Data 05		
# Temat: pobieranie danych; webscrapping; analiza słów		
# Ćwiczenia 05  07.12.2020		
# Termin nadsyłania prac		10.12.2020
		
# Który autor jest największy?		
# Napisz skrypt, MapReduce, Spark z dowolnym API		
# 1. Zmodyfikować program aby dostarczał inforamcje o ilość słow w każdej z katerogii		
# tiny 1; 2-4 small; 5-9 medium; >10 big;		
# 2. Rozpoznał język tekstu (ang. vs pl) - analizy częstości występowania liter		
# 3. Dokonaj analizy zachorowań na Covia w wybranym regionie;		
# - wartość: max; min; odchylenei standardowe; wariancja;		
# - gdzie się warto się przenieść?		
		
# Przynajmiej jeden z plików ma być wczytany z HDFS.		
		
# - Udokumentować source code (metody) (JDOC, doxystring)		
# - Proszę użyć dobrych praktyk programistycznych (np. object oriented; SOLID; DRY, np.)		
# - Zadanie należy rozwiązać w parach z zastosowaniem dowolnej technologii.		
# - użyć repo z poprzenidch ćwiczen		
# - Proszę wkomitować przykładowy wynik działa programu (video, zrzut ekranu, log, etc.)		

from bs4 import BeautifulSoup
import requests
from collections import Counter
import time
from langdetect import detect

# -----------------

class Common_Nouns(object):
    def __init__(self):
             
        self.acc = []
        self.most_common()

        
    def most_common(self, acc=[]):
        for poem in range(1, 71):
            req = requests.get("https://literat.ug.edu.pl/roxolan/00{}.htm".format(poem)) if poem < 10 else requests.get("https://literat.ug.edu.pl/roxolan/0{}.htm".format(poem))
            text = BeautifulSoup(req.content, "lxml").text.split()
            self.acc += text[2:len(text)-2]

        
        container = []
        container += [len(word) for word in self.acc]
        
        print('slowa jednoliterowe: ', len([val for val in container if val == 1]))
        print('slowa w przedziale od 2 do 4 liter: ', len([val for val in container if (val >= 2 and val <= 4)]))
        print('slowa w przedziale od 5 do 9 liter: ', len([val for val in container if (val >= 5 and val <= 9)]))
        print('slowa wieksze niz 10 liter: ', len([val for val in container if val >= 10]))
        

        
        lang = detect(str(self.acc))
        print('jezyk uzywany przez autora:', lang)
        text = [letter for letter in "".join(self.acc)]
        print('ile jakich liter podczas calej tworczosci:', Counter(text))

start = time.time()
Common_Nouns()
end = time.time()
print('czas trwania:', end-start)

# Autor Wiktor Maj
