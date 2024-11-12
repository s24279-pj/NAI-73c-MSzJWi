import argparse
import json
import numpy as np

#pobieranie danych z terminala, używając parsowania (argparse) sprawdzamy czy dane zostaly podane oraz
# walidujemy dane
def build_arg_parser():
    parser = argparse.ArgumentParser(description='Compute similarity score')
    parser.add_argument('--person1', dest='person1', required=True,
            help='First user')
    parser.add_argument('--person2', dest='person2', required=True,
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