from bs4 import BeautifulSoup
import requests

def accumulate(acc = []):
    acc += [len(BeautifulSoup(requests.get("https://literat.ug.edu.pl/teofil/00{}.htm".format(poem)).text, "lxml").text.split()) - 6 if poem < 10 else len(BeautifulSoup(requests.get("https://literat.ug.edu.pl/teofil/0{}.htm".format(poem)).text, "lxml").text.split()) - 6 for poem in range(1, 41)]
    return sum(acc)
    
print(accumulate())
