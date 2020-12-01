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
from collections import Counter
from googletrans import Translator
import spacy

# -----------------

class Common_Nouns(object):
    def __init__(self):
        self.translator = Translator(service_urls=['translate.googleapis.com'])                 
        self.acc = []
        self.res = ''
        

        print('zadanie 1: 10 najczęsciej występowanych słów oraz ich liczba')
        self.most_common()
        print(self.acc[:10])
        
        print('zadanie 2: zwróc 3 najczęstsze rzeczowniki')
        self.nouns()
        print(self.res[:3])
        
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
        
        self.res = [token.lemma_ for token in doc if token.pos_ == "NOUN"]


if __name__ == '__main__':
    Common_Nouns()

# Autor Wiktor Maj
