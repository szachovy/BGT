#Big Data 03
#Temat: pobieranie danych; webscrapping; analiza słów
#Ćwiczenia 03  30.11.2020
#Termin nadsyłania prac

#Który autor jest największy?
#Napisz skrypt, który automatycznie pobierze wszystkie dzieła dwóch wybranych autorów (z poprzednich ćwiczeń). Wybrana postać musi być autorem przynajmniej 10 publikacji.
#- Użyc Hadoop z dowolnym API
#- Ile słow napisał autor?
#- Jakie jest 10 najpopularniejszy słów autora?
#- Jakie są 3 najpopulurniszej rzeczowniki? (np. przez https://www.wordsapi.com/  np. przez sprawdzenie z listą rzeczwoników - to znalezienia)
#- W nagłówku programu w postaci komentarza należy zawrzeć: podsumowanie zadania + autorów rozwiązanie.
#- Udokumentować source code (metody) (JDOC, doxystring)
#Proszę użyć dobrych praktyk programistycznych (np. object oriented; SOLID; DRY, np.)
#Zadanie należy rozwiązać w parach z zastosowaniem dowolnej technologii.
#Należy wybrać autora, którego dzieła nie są chronione prawami autorskimi.
#- użyć repo z poprzenidch ćwiczen
#- Porównać czas egzekucji ćwiczenia 02 i ćwiczenia 03; wyniki pomiarów wrzucić na repozytorium

#Szymon Zimorowic
from bs4 import BeautifulSoup
import requests
from collections import Counter
from googletrans import Translator
import spacy
import timeit


# -----------------

class Common_Nouns(object):
    def __init__(self):
        start = timeit.timeit()
        self.translator = Translator(service_urls=['translate.googleapis.com'])                 
        self.acc = []
        self.res = ''
        

        print('zadanie 1: 10 najczęsciej występowanych słów oraz ich liczba')
        self.most_common()
        print(self.acc[:10])
        
        print('zadanie 2: zwróc 3 najczęstsze rzeczowniki')
        self.nouns()
        print(self.res.text)
        end = timeit.timeit()
        print('time elapsed:', end - start)
        
    def most_common(self, acc=[]):
        for poem in range(1, 71):
            req = requests.get("https://literat.ug.edu.pl/roxolan/00{}.htm".format(poem)) if poem < 10 else requests.get("https://literat.ug.edu.pl/roxolan/0{}.htm".format(poem))
            text = BeautifulSoup(req.content, "lxml").text.split()
            self.acc += text[2:len(text)-2]
            
        self.acc = Counter(self.acc).most_common(100)

    
    def nouns(self):
        for word in range(100):
            translated_text = self.translator.translate(self.acc[word][0], dest="en")
            if len(translated_text.text) > 2:
                self.res += translated_text.text + ' '

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.res)

        #print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
        #print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
        
        self.res = [token.lemma_ for token in doc if token.pos_ == "NOUN"][:3]
        self.res = self.translator.translate(','.join(self.res), dest="pl")

if __name__ == '__main__':
    Common_Nouns()

# Autor Wiktor Maj
