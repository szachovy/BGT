#Big Data 06			
#Temat:ML; silinik rekomendacji			
#Ćwiczenia 06  14.12.2026			
#Termin nadsyłania prac		21.12.2020	do13;00
#			
#Który autor jest największy?			
#1. Wykorzystać BigData; Hadoop; Spark;Storm; etc.			
#- uzpełnij ankietę (samodzielnie)		do 14.12.2020	
#- zbuduj silnik rekomendacji filmów;			
#- zaproponuj 5 filmów interesujących dla prowadzącego, których nie oglądał			
#- Podać obsada; średnią ocen; zarys fabuły;			
#			
#Dodać dokumentację do kodu źródłowego (np. Python -> docstring; Java -> Jdoc; Kotlina -> Kdoc; C++ -> doxgen, etc.)			
#Rozwiazanie poprzedź komentarzem zawierający opis problem, autora, instrukcję użycia, (opcjonalnie: refenerencje)			
#Rozwiązanie umieść w repozytoriach obu partnerów (użytym podczas pierwszy ćwiczeń)			
#Dodać zrzut ekranu (wideo, etc.) z wywołaniem trzech przykładowych scenariuszy; wkomituj do repozytorium			

%pyspark
import pandas as pd
from surprise import KNNWithMeans, Dataset, Reader
from surprise.model_selection import GridSearchCV
from bs4 import BeautifulSoup
import requests

class MovieData():
    def __init__(self, path):
        self.df = self.load_data(path)

    def check_if_exists(self, person, movie):
        if person not in self.df.osoba.values:
            print("Tej osoby nie ma w bazie")
            return False

        if movie not in self.df.film.values:
            print("Tego filmu nie ma w bazie")
            return False
        return True

    @staticmethod
    def load_data(path):
        '''
        first column: People
        other columns: Tuple (Movie, Ocena)
        I'm changing it here so that it becomes (Person, Movie, Rating)
        '''
        data = pd.read_csv(path, header=None)
        rows_count = data.shape[0]
        temp_rows = []
        for row in range(rows_count):
            osoba = data.iloc[row, 0]
            filmy = data.iloc[row, 1::2]
            oceny = data.iloc[row, 2::2]

            number_of_rated_movies = len(filmy)
            filmy = [film for film in filmy]
            oceny = [ocena for ocena in oceny]
            for i in range(number_of_rated_movies):
                temp_rows.append({'osoba': osoba, 'film': filmy[i], 'ocena': oceny[i]})

        df = pd.DataFrame(temp_rows, columns=['osoba', 'film', 'ocena'])
        return df

    def amount_of_ratings(self, title):
        '''
        Returns amount of ratings based on movie title as a key
        '''
        try:
            return self.df['film'].value_counts()[title]
        except(KeyError):
            raise KeyError('Ten film nie istnieje w bazie !!!')

class MoviePredictions:
    def __init__(self, data):
        self.data = data
        self.algo = self.calculate_recomendations(data.df)


    def calculate_recomendations(self, df):
        reader = Reader(rating_scale=(1,10))
        data = Dataset.load_from_df(df[['osoba', 'film', 'ocena']], reader)
        algo = GridSearchCV(KNNWithMeans, refit=True, cv=3, measures=["rmse", "mae"], param_grid={
            "sim_options": {
                "name": ["msd", "cosine"],
                "min_support": [3, 4, 5],
                "user_based": [False, True],
            }
        })
        algo.fit(data)
        return algo


    def predict(self, person, movie):
        if self.data.check_if_exists(person, movie):
            prediction = self.algo.predict(person, movie)
            return prediction.est



def calculate_recommended_movie_based_on_user_ratings(df, movie_title):
    # 1. Get data set with (rating, amount of ratings)
    avg_ratings = df.groupby('film')['ocena'].mean()
    amount_of_ratings = df.groupby('film')['ocena'].count()
    df_ratings = pd.DataFrame({"rating": avg_ratings, "amount of ratings": amount_of_ratings})

    # 2. Get user rating correlation for a specified movie
    df_ = df.loc[:, ['osoba', 'film', 'ocena']]
    osoba_film_matrix = pd.pivot_table(df_, columns='film', index='osoba', values='ocena')

    movie_watched = osoba_film_matrix[movie_title]
    li = []
    for i, col in enumerate(osoba_film_matrix.columns):
        li.append(movie_watched.corr(osoba_film_matrix.iloc[:, i]))
    li = pd.Series(li)

    # Step 3 - Return dataframe
    df = pd.DataFrame({'movie':pd.Series(osoba_film_matrix.columns), 'correlation': li, 'amount of ratings': pd.Series(amount_of_ratings)})
    recomendation_set = df[df['amount of ratings'] >= 2].sort_values(by=['correlation', 'amount of ratings'],
                                                                     ascending=False)
    recomended_movies = recomendation_set['movie'].values
    print(recomended_movies)

def calulate_correlation(df):

    # Step 1 - Create correlation table (Person, movie)
    df = df.loc[:, ['osoba', 'film', 'ocena']]
    osoba_film_matrix = pd.pivot_table(df, columns='film', index ='osoba', values ='ocena')

    # Step 2 - perfom corelation
    li = []
    for i, col in enumerate(osoba_film_matrix.columns):
        li.append(osoba_film_matrix[col].corr(osoba_film_matrix.iloc[:, i]))
    li = pd.Series(li)

    # Step 3 - Return dataframe
    number_of_ratings = [amount_of_ratings(df, movie_name) for movie_name in osoba_film_matrix.columns]
    df = pd.DataFrame({'movie': osoba_film_matrix.columns, 'correlation': li, 'number of ratings': number_of_ratings})

    recomendation_set = df[df['number of ratings'] >= 2].sort_values(by=['correlation', 'number of ratings'], ascending=False)
    recomended_movies = recomendation_set['movie'].values

    print(recomended_movies)

class MovieScrapper:
    '''
    Podstawowy Web Scrapper do filmweba utworzony (19.12.2020).
    '''
    def __init__(self, movie_title):
        '''
        Creates Movie MetaData object based on movie title requested from: filmweb.pl
        '''
        self.html = self.get_html(movie_title)

    @staticmethod
    def get_html(movie_title):
        # Change space to plus sign (Filmweb requires this)
        movie_title = movie_title.replace(' ', '+')
        url = "https://www.filmweb.pl/search?q={}".format(movie_title)
        film_previes_html = requests.get(url).content

        # Get correct movie link from the list
        soup = BeautifulSoup(film_previes_html, 'html.parser')
        movie_link = soup.find('a', {"class": "filmPreview__link"})['href']

        #request the correct movie
        url = "https://www.filmweb.pl{}".format(movie_link)
        movie_html = requests.get(url).content
        return movie_html

    def genre(self):
        pass

    def story_line(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        story_line = soup.find('div', {"class": "filmPosterSection__plot"})
        return story_line.contents[0]

    def average_score(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        score = soup.find('span', {"class": "filmRating__rateValue"}).contents[0]
        return score


    def actors(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        actors = soup.find('div', {"class": "crs__wrapper"}).find_all('div', {"class": "crs__item"})
        actor_list = []
        for actor in actors: #type: BeautifulSoup
            try:
                actor_name = actor.find('span').find('a').contents[0]
                actor_list.append(actor_name)
            except(AttributeError):
                '''
                Sometimes web page renders differently with more junk, instead of writting
                more exact web scrapper I'm silently ignoring error thus doing nothing with
                invalid data
                '''
        return actor_list

def prowadzacy_widzial_film(movies_to_recommend):
    widziane_filmy_prowadzacy = movie_data.df[movie_data.df['osoba'] == 'Paweł Czapiewski']['film']
    widziane_filmy_prowadzacy = [film for film in widziane_filmy_prowadzacy]
    for movie in movies_to_recommend:
        if movie in widziane_filmy_prowadzacy:
            raise AssertionError('Brak spełnienia zadania: Musibyć film nieznany')

if __name__ == '__main__':
    '''
    1. Load data from CSV
    2. Find Cartesian logic in there (Colaborative filtering)
    3. Zaproponuj 5 filmów dla prowadząceg
    '''
    movie_data = MovieData("Oceny_Filmow_BGT.csv")
    movie_predictions = MoviePredictions(movie_data)

    movies_to_recommend = [
        'Django',
        'Breaking Bad',
        'Taken',
        'Jackie Brown',
        'Toy Story'
    ]
    prowadzacy_widzial_film(movies_to_recommend)

    # Polecenie 5 filmów prowadzącemu
    prowadzacy = "Paweł Czapiewski"
    for movie in movies_to_recommend:
        ocena_filmu_dla_prowadzacego = movie_predictions.predict(prowadzacy, movie)
        dane_filmu = MovieScrapper(movie)

        print("\nFILM: {}".format(movie))
        print("OCENA DOPASOWANIA: {}".format(ocena_filmu_dla_prowadzacego))
        print("\n-- METADANE FILMU --")
        print("OBSADA: {}".format(dane_filmu.actors()))
        print("OCENA: {}".format(dane_filmu.average_score()))
        print("FABULA: {}".format(dane_filmu.story_line()))

# Autorzy Wiktor Maj, Robert Mielewczyk
