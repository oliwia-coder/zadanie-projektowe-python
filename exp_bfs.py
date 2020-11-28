

import random
import heapq

from team import Team

from gen_test_case import load_test_case

nominal_pq_size = 10000000000
max_pq_size = 2 * nominal_pq_size
max_iteration = 100000000000000000


def bfs(pq, group_size, team_size, hate_list):
    # best_so_far = Team(solution=[1] * team_size, group_size=group_size,
    # hate_list = hate_list)
    best_so_far = pq[0][0]

    i = 0
    while len(pq) > 0 and i < max_iteration:
        t, ind = heapq.heappop(pq)
        if best_so_far.fitness < t.fitness:
            best_so_far = t

        if (ind < team_size):
            for new_group in range(1, group_size + 1):
                sol = list(t.solution)
                sol[ind] = new_group
                new_team = Team(sol, group_size, hate_list)
                heapq.heappush(pq, (new_team, ind + 1))

        if len(pq) > max_pq_size:
            print("Przepelnienie")
            pq = heapq.nsmallest(nominal_pq_size, pq)

        i += 1

        if i % 100000 == 0:
            print(f'Best {i:05}: {best_so_far} {len(pq)}')

    return best_so_far


if __name__ == '__main__':
    test_case_filename = 'test_case_1.json'
    test_case = load_test_case(test_case_filename)

    # Ustalenie jednego seed aby wyniki byly powtarzalne
    random.seed(test_case['seed'])

    pq = [(Team.random(
        team_size=test_case['team_size'],
        group_size=test_case['group_size'],
        hate_list=test_case['hate_list']),
           0)
    ]

    best = bfs(
        pq=pq,
        team_size=test_case['team_size'],
        group_size=test_case['group_size'],
        hate_list=test_case['hate_list']
    )

    print(f'Najlepszy znaleziony podzial {best}')
