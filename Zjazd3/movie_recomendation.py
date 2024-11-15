import argparse
import json
import numpy as np

#pobieranie danych z terminala, używając parsowania (argparse) sprawdzamy czy dane zostaly podane oraz
# walidujemy dane
def build_arg_parser():
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--person1', dest='person1', required=True,
            help='First user')
    # Ustawienie required na False, ponieważ nie jest konieczne porównywanie sie do jednej osoby
    parser.add_argument('--person2', dest='person2', required=False,
            help='Second user')
    parser.add_argument("--score-type", dest="score_type", required=True,
            choices=['Euclidean', 'Pearson'], help='Similarity metric to be used')
    return parser

#Obliczanie odległości euklidesowej
def euclidean_score(dataset, person1, person2):
    #Sprawdzenie czy obie osoby istnieją w zbiorze danych
    if person1 not in dataset:
        raise TypeError('Cannot find ' + person1 + ' in the dataset')

    if person2 not in dataset:
        raise TypeError('Cannot find ' + person2 + ' in the dataset')

    #Szukanie filmów, które istnieją u obu osób
    common_movies = {}

    for item in dataset[person1]:
        if item in dataset[person2]:
            common_movies[item] = 1

    # Jeżeli nie znaleniono żadnego wspólnego filmu zwracamy 0 jako odległość euklidesową
    if len(common_movies) == 0:
        return 0

    #lista kwadratów różnic
    squared_diff = []

    # Obliczamy różnicę między ocenami dwóch użytkowników, a następnie podnosimy tę różnicę do kwadratu
    for item in dataset[person1]:
        if item in dataset[person2]:
            squared_diff.append(np.square(dataset[person1][item] - dataset[person2][item]))

    # Podstawiamy obliczone dane do wzoru na odległość euklidesową
    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


# Obliczanie współczynnika korelacji Pearsona
def pearson_score(dataset, person1, person2):
    #Sprawdzenie czy osoby istnieją w zbiorze danych
    if person1 not in dataset:
        raise TypeError('Cannot find ' + person1 + ' in the dataset')

    if person2 not in dataset:
        raise TypeError('Cannot find ' + person2 + ' in the dataset')

    # Lista wspólnie ocenionych filmów
    common_movies = {}

    #Szukanie wspólnych filmów
    for item in dataset[person1]:
        if item in dataset[person2]:
            common_movies[item] = 1

    #
    num_ratings = len(common_movies)

    # Zwrócenie 0 jako wspólczynnik korelacji, jeżeli osoby nie mają wspólnie ocenionych filmów
    if num_ratings == 0:
        return 0

    # Obliczamy sumy ocen dla wspólnych filmów
    person1_sum = np.sum([dataset[person1][item] for item in common_movies])
    person2_sum = np.sum([dataset[person2][item] for item in common_movies])

    # Obliczamy sumy kwadratów ocen dla wspólnych filmów
    person1_squared_sum = np.sum([np.square(dataset[person1][item]) for item in common_movies])
    person2_squared_sum = np.sum([np.square(dataset[person2][item]) for item in common_movies])

    # Obliczamy sumę iloczynów ocen dla wspólnych filmów
    sum_of_products = np.sum([dataset[person1][item] * dataset[person2][item] for item in common_movies])

    # Obliczanie składników do wzoru korelacji Pearsona
    # Sxy: suma iloczynów ocen użytkowników, skorygowana o średnią ocen
    Sxy = sum_of_products - (person1_sum * person2_sum / num_ratings)
    #Sxx: suma kwadratów ocen person1, skorygowana o średnią ocen person1
    Sxx = person1_squared_sum - np.square(person1_sum) / num_ratings
    #Syy: suma kwadratów ocen person2, skorygowana o średnią ocen person2
    Syy = person2_squared_sum - np.square(person2_sum) / num_ratings

    #Obliczanie współczynnika korelacji Pearsona
    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)

# Funkcja porównująca jedną osobę do wszystkich innych użytkowników w zbiorze danych
def compare_to_top_n(dataset, person, score_type, n=3, threshold=0.1):
    # Sprawdź, czy wybrana osoba znajduje się w zbiorze danych
    if person not in dataset:
        print("Dostępne osoby w zbiorze:", list(dataset.keys()))
        raise TypeError(f'Cannot find {person} in the dataset')

    # Słownik do przechowywania wyników porównań
    similarity_scores = {}

    for other_person in dataset:
        if other_person == person:
            continue

        if score_type == "Euclidean":
            score = euclidean_score(dataset, person, other_person)
        elif score_type == "Pearson":
            score = pearson_score(dataset, person, other_person)
        else:
            raise ValueError("Invalid score_type. Choose 'Euclidean' or 'Pearson'.")

        similarity_scores[other_person] = score

    # Sortowanie wyników (od najlepszych do najgorszych dla Euclidean, odwrotnie dla Pearson)
    sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=(score_type == "Pearson"))

    # Wybieranie do N najlepiej dopasowanych osób z filtrowaniem
    best_score = sorted_scores[0][1]
    top_matches = [sorted_scores[0]]  # Zawsze uwzględniamy najlepszego

    for other_person, score in sorted_scores[1:]:
        if abs(score - best_score) <= threshold and len(top_matches) < n:
            top_matches.append((other_person, score))
        if len(top_matches) >= n:
            break

    return [person for person, score in top_matches]


# Funkcja do rekomendowania filmów na podstawie wyników podobieństwa
def recommended_movies(dataset, person1, person2, score_type):
    recommended_movies = set()
    non_common_movies = {}
    good_rate = 10
    bad_rate = 1
    rate_change = 0

    # Przechodzimy przez filmy oceniane przez osobę2, które nie zostały ocenione przez osobę1
    for item in dataset[person2]:
       if item not in dataset[person1]:
           non_common_movies[item] = 1

    if score_type == "Euclidean":
        # Przechodzimy przez wszystkie filmy, zaczynając od "dobrych" ocen
        while len(recommended_movies) < 5:
            for item in non_common_movies:
                # Jeśli ocena jest większa lub równa good_rate - rate_change, dodajemy film do listy
                if dataset[person2][item] >= good_rate - rate_change:
                    recommended_movies.add(item)
                if len(recommended_movies) == 5:
                    break

            # Jeśli lista nie jest pełna po przejściu przez wszystkie filmy, zmniejszamy rate_change
            if len(recommended_movies) < 5:
                rate_change += 1  # Zmniejszamy good_rate o 1

    else:
        # Przechodzimy przez wszystkie filmy, zaczynając od "złych" ocen
        while len(recommended_movies) < 5:
            for item in non_common_movies:
                # Jeśli ocena jest mniejsza lub równa bad_rate - rate_change, dodajemy film do listy
                if dataset[person2][item] <= bad_rate + rate_change:
                    recommended_movies.add(item)
                if len(recommended_movies) == 5:
                    break

            # Jeśli lista nie jest pełna po przejściu przez wszystkie filmy, zmniejszamy rate_change
            if len(recommended_movies) < 5:
                rate_change += 1  # Zmieniamy wartość bad_rate (zwiększamy ją)

    return recommended_movies

# Funkcja do rekomendowania filmów, które nie są zalecane
def not_recommended_movies(dataset, person1, person2,score_type):
    not_recommended_movies = set()
    non_common_movies = {}
    good_rate = 10
    bad_rate = 1
    rate_change = 0

    for item in dataset[person2]:
        if item not in dataset[person1]:
            non_common_movies[item] = 1

    if score_type == "Pearson":
        # Przechodzimy przez wszystkie filmy, zaczynając od "dobrych" ocen
        while len(not_recommended_movies) < 5:
            for item in non_common_movies:
                # Jeśli ocena jest większa lub równa good_rate - rate_change, dodajemy film do listy
                if dataset[person2][item] >= good_rate - rate_change:
                    not_recommended_movies.add(item)
                if len(not_recommended_movies) == 5:
                    break

            # Jeśli lista nie jest pełna po przejściu przez wszystkie filmy, zmniejszamy rate_change
            if len(not_recommended_movies) < 5:
                rate_change += 1  # Zmniejszamy good_rate o 1

    else:
        # Przechodzimy przez wszystkie filmy, zaczynając od "złych" ocen
        while len(not_recommended_movies) < 5:
            for item in non_common_movies:
                # Jeśli ocena jest mniejsza lub równa bad_rate - rate_change, dodajemy film do listy
                if dataset[person2][item] <= bad_rate + rate_change:
                    not_recommended_movies.add(item)
                if len(not_recommended_movies) == 5:
                    break

            # Jeśli lista nie jest pełna po przejściu przez wszystkie filmy, zmniejszamy rate_change
            if len(not_recommended_movies) < 5:
                rate_change += 1  # Zmieniamy wartość bad_rate (zwiększamy ją)

    return not_recommended_movies


if __name__=='__main__':
    #Przypisywanie pobranych danych od użytkownika do zmiennych
    args = build_arg_parser().parse_args()
    person1 = args.person1
    person2 = args.person2
    score_type = args.score_type

    #Zbiór danych, który używamy
    ratings_file = 'ratings.json'

    # Otwieranie i wczytywanie danych z pliku JSON
    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    # Gdy porównujemy person1 do wszystkich
    if person2 is None:
        # Porównywanie person1 do 3 najbardziej dopasowanych uzytkowników
        similarity_scores = compare_to_top_n(data, person1, score_type, n=3, threshold=0.1)
        # Wyświetlenie ich
        print("Top matches:", similarity_scores)

        all_recommended = set()
        all_not_recommended = set()

        # Zbiór filmów na podstawie Euclidean
        if score_type == "Euclidean":
            for match in similarity_scores:
                all_recommended.update(recommended_movies(data, person1, match, score_type))
                all_not_recommended.update(not_recommended_movies(data, person1, match, score_type))

            print("\nRecommended movies from top matches (Euclidean):")
            print(set(list(all_recommended)[:5]))
            print("\nNot recommended movies from top matches (Euclidean):")
            print(set(list(all_not_recommended)[:5]))

        # Zbiór filmów na podstawie Pearson
        elif score_type == "Pearson":
            for match in similarity_scores:
                all_not_recommended.update(recommended_movies(data, person1, match, score_type))
                all_recommended.update(not_recommended_movies(data, person1, match, score_type))

            print("\nRecommended movies from top matches (Pearson):")
            print(set(list(all_recommended)[:5]))
            print("\nNot recommended movies from top matches (Pearson):")
            print(set(list(all_not_recommended)[:5]))

    #Gdy porównujemy konkretne dwie osoby
    else:
        if score_type == 'Euclidean':
            print("\nEuclidean score:")
            score = euclidean_score(data, person1, person2)
            print(score)

        else:
            print("\nPearson score:")
            print(pearson_score(data, person1, person2))

