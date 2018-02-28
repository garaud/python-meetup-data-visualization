# coding: utf-8

import numpy as np
import pandas as pd
# from sklearn.datasets.samples_generator import make_blobs
# from sklearn.datasets import samples_generator

from faker import Faker


SEED = 7331
np.random.seed(SEED)

SIZE = 2000
COLUMNS = ['id', 'name', 'sex', 'age', 'income', 'workin_hour', 'contract']
SEX = ['F', 'M']
# CDI, CDD, unemployement
CONTRACT = [1, 2, 3]
# min/max age values
AGE_RANGE = [18, 68]
# min/max weekly working hours
WORKIN_HOUR = [0, 60]
# income
INCOME = [0, 10000]


def make_id(fake):
    """make a random ID with 2 letters, 2 digits, 2 letters
    """
    content = '??##??'
    content = fake.lexify(content)
    return fake.numerify(content).upper()


def law_age():
    size = SIZE * 2
    data = 30 + np.random.lognormal(size=SIZE) * 7
    data = data.clip(min=AGE_RANGE[0], max=AGE_RANGE[1])
    data = np.random.choice(data, size=SIZE, replace=False)
    assert data.shape[0] == SIZE
    return data.astype(np.int)

def income_gen(contract):
    if contract == 1:
        a = 1600 + np.random.lognormal() * 200
    elif contract == 2:
        a = 1500 - np.random.lognormal() * 300
    else:
        a = 700 - np.random.lognormal() * 100
    a = np.clip(a, a_min=INCOME[0], a_max=INCOME[1])
    return np.round(a, 2)


def workin_hour_gen(contract):
    if contract == 1:
        a = 40 + np.random.normal() * 6
    elif contract == 2:
        a = 25 + np.random.normal() * 4
    else:
        a = 7 + np.random.normal() * 5
    a = np.clip(a, a_min=WORKIN_HOUR[0], a_max=WORKIN_HOUR[1])
    return np.round(a, 1)


def main(locale='fr_FR'):
    # locale fr
    fake = Faker(locale)

    def namegen(sex):
        if sex == 'F':
            return fake.name_female()
        return fake.name_male()

    ids = [make_id(fake) for _ in range(SIZE)]
    sex = np.random.choice(SEX, size=SIZE)
    names = [namegen(x) for x in sex]
    ages = law_age()
    contracts = np.random.choice(CONTRACT, size=SIZE)
    incomes = [income_gen(c) for c in contracts]
    workin_hours = [workin_hour_gen(c) for c in contracts]


    df = pd.DataFrame({'id': ids,
                       'sex': sex,
                       'name': names,
                       'age': ages,
                       'workin_hour': workin_hours,
                       'income': incomes,
                       'contract': contracts})
    return df[COLUMNS]


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Générateur de données')
    parser.add_argument('-s', '--save', action='store_true',
                        help='Sauvegarde les données dans un fichier CSV.')
    parser.add_argument('-l', '--locale', type=str, default='fr_FR',
                        help='Indique la locale. fr par défaut.')
    args = parser.parse_args()

    datasets = main(args.locale)
    print("Generation de données")
    print("Sample:")
    print(datasets.head())
    if args.save:
        datasets.to_csv('data.csv', index=False)
        print("Fichier 'data.csv' généré avec {} lignes".format(SIZE))
