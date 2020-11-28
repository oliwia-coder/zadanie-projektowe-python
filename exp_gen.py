

import random

from team import TeamSolver

from gen_test_case import load_test_case

if __name__ == '__main__':
    test_case_filename = 'test_case_1.json'
    test_case = load_test_case(test_case_filename)

    random.seed(test_case['seed'])  # Ustalenie jednego seed aby wyniki byly powtarzalne

    ts = TeamSolver(
        pop_size=test_case['population_size'],
        team_size=test_case['team_size'],
        group_size=test_case['group_size'],
        hate_list=test_case['hate_list'],
        steps=test_case['steps']
    )

    best = ts.solve

    print(f'Najlepszy znaleziony podzial {best}')


import matplotlib.pyplot as plt


# 1 wykres to group_size =3 i przechodzi team_size od 6...10
# 1 wykres dodaje czas działania alg genetycznego

# 1 wykres to group_size =4 i przechodzi team_size od 6...10
# 1 wykres dodaje czas działania alg genetycznego

s = [6, 7, 8, 9, 10]
v = [70, 120, 500, 1200, 2600]
v2 = [80, 130, 600, 1500, 3000]
plt.plot(s, v, label='Wersja_4')
plt.plot(s, v, label='Wersja_5')

plt.title('TEST CASE 1')
plt.ylabel('Czas dzialania [s]')
plt.xlabel('Rozmiar druzyny')
plt.legend()

# plt.show()
plt.savefig('test_case_diag_1.jpg', dpi=300)


