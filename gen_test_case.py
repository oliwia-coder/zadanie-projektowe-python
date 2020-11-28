

import random        
import json


def generate_hate_list(team_size, group_size, n):
    hate_list = set()
    while len(hate_list) < n:
        x1 = random.randint(1, team_size)
        x2 = random.randint(1, team_size)
        if x1 == x2:
            continue  # Nie mozna dodac pary (x, x)
        if x1 > x2:
            x1, x2 = x2, x1  # x1 zawsze mniejsze od x2
        hate_list.add((x1, x2))
    
    return hate_list

def create_test_case(name, 
                     team_size,
                     group_size,
                     hate_list_size,
                     population_size,
                     seed,
                     steps):
    hate_list = list(generate_hate_list(team_size, group_size, hate_list_size))
    config = {
        'team_size': team_size,
        'group_size': group_size,
        'hate_list': hate_list,
        'population_size': population_size,
        'steps': steps,
        'seed': seed
    }
    with open(f'{name}.json', 'w') as f:
        json.dump(config, f)

def load_test_case(filename):
    with open(filename) as f:
        config = json.load(f)  
    config['hate_list'] = set((x, y) for (x, y) in config['hate_list'] )
    print(config['hate_list'])
    return config


if __name__ == '__main__':
    create_test_case(
        name = 'test_case_1',
        team_size = 20,
        group_size = 3,
        hate_list_size = 90,
        population_size=10000,
        seed=1,
        steps=100)

