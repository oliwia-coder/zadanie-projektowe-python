

import random
import heapq



from typing import List

class Team:
    """
    'Chromoson' w problemie druzynowym
    
    Informacja jest zakodowana w tablicy. Kazda indeks tablicy to numer osoby,
        a wartosc to numer grupy
    
    Metoda _fitness oblicza score, i zapisuje je pod polem 'fitness'
    
    hate_list jest to lista par osob, ktore sie nie lubia
    """ 
    def __init__(
            self,
            solution: List[int],
            group_size: int,
            hate_list: List[tuple],
            ):
        self.solution = solution
        self.hate_list = hate_list

        self.team_size = len(solution)
        self.group_size = group_size
        self._fitness()

    def _fitness(self):
        """
        Fitness zapisuje liczbe przeciwną do liczby par z hate_list,
            które należą do tej samej grupy
        """
        score = 0
        for person1, person2 in self.hate_list:
            if self.solution[person1-1] == self.solution[person2-1]:
                score -= 1
        self.fitness = score

    def mutate(self, k: int=1):
        """
        Zwraca nowy chromosom, z losowo zmutowanymi k genami
        """
        new_solution = list(self.solution)  # kopiujemy istniejace rozwiazanie
        indices = random.sample(range(self.team_size), k)  # wybieramy losowo k indeksow
        for i in indices:
            act_group = self.solution[i]   # zapisujemy aktualna grupe
            # Losujemy nowa grupe z przedziału <1, group_size - 1> 
            #   czyli o jeden mniejszy niż normalnie. Gdy wylosowana grupa
            #   będzie większa-równa act_group to wtedy zwiększamy 
            #   numer grupy o 1. Taki trick pozwala na losowanie liczby z
            #   ze zbioru {1, ..., act_num-1} U {act_num+1, ..., group_size}
            #   czyli z pominieciem act_group
            new_group = random.randint(1, self.group_size-1)
            if new_group >= act_group:
                new_group += 1
            new_solution[i] = new_group
        return Team(new_solution, self.group_size, self.hate_list)
    
    def mutate_swap(self):
        """
        Zamieniamy ze soba dwa losowe indeksy
        """
        new_solution = list(self.solution)
        k1, k2 = random.sample(range(self.team_size), 2)
        new_solution[k1], new_solution[k2] = new_solution[k2], new_solution[k1]
        return Team(new_solution, self.group_size, self.hate_list)
        
    def crossover(self, team: 'Team'):
        """
        Robimy krzyzowke z innym chromosomem
        Wybieramy losowo indeks k i robimy krzyzowke do k indeksu
        """
        # Szukamy podzialu bez pierwszego i ostatniego elementu
        i = random.randint(1, self.team_size - 1)
        new_solution_1 = self.solution[:i] + team.solution[i:]
        new_solution_2 = team.solution[:i] + self.solution[i:]
        return [
            Team(new_solution_1, self.group_size, self.hate_list),
            Team(new_solution_2, self.group_size, self.hate_list),
        ]
    

    def __str__(self):
        return f'Team({self.solution}, score={self.fitness})'

    def __repr__(self):
        return str(self.solution)
    
    def __eq__(self, team):
        return self.solution == team.solution
    
    def __hash__(self):
        return str(self).__hash__()
    
    def __gt__(self, team):
        return self.fitness > team.fitness

    @staticmethod
    def random(group_size, team_size, hate_list):
        """
        Metoda statyczna do utworzenia losowego rozwiazania
        """
        rand_solution = [random.randint(1, group_size) for i in range(team_size)]
        return Team(rand_solution, group_size, hate_list)


class TeamPopulation:
    """
    Klasa do trzymania i operowania na populacji
    """
    def __init__(self, pop_num, rand_team_gen, pop=None):
        self.pop_num = pop_num

        if pop is None:
            self.pop = {rand_team_gen() for i in range(2 * self.pop_num)}
        else:
            self.pop = pop
            
    def best(self, k):
        """
        Zwraca k najlepszych rozwiazan z populacji
        """
        return heapq.nlargest(k, self.pop, lambda x: x.fitness)

    def select(self):
        """
        Wybiera self.pop_num najlepszych rozwiazan z populacji
        """
        self.pop = set(self.best(self.pop_num))
        
    def mutate(self):
        """
        Generator zmutowanych obiektow
        """
        # Mutujemy po jednym genie
        yield from self.mutate_pos(1)
        # Mutujemy dwa geny
        yield from self.mutate_pos(2)
        # Losowo zamieniamy dwie pozycje
        yield from self.mutate_swap()
        # Krzyzujemy ze soba 
        yield from self.crossover()

    def mutate_pos(self, k=1):
        """
        Mutujemy k genow dla kazdego chromosomu
        """
        for team in self.pop:
            yield team.mutate(k)
        
    
    def mutate_swap(self):
        """
        Zamieniamy losowo dwa geny w kazdym chromosomie
        """
        for team in self.pop:
           yield team.mutate_swap()
    
    def crossover(self):
        """
        Dzielimy populacje na dwie losowe listy i wykonujemy krzyzowke parami
        """
        
        pop = list(self.pop)  # Wykonujemy kopie aby zachowac kolejnosc w orginalnym solution
        random.shuffle(pop)  # Mieszamy populacje aby byla roznorodnosc w krzyzowce
        pop_a = pop[:self.pop_num//2]
        pop_b = pop[self.pop_num//2:]
             
        for t1, t2 in zip(pop_a, pop_b):
            yield from t1.crossover(t2)
            
    
    def update(self, new_pop):
        """
        Rozszerzamy populacje o nowe przypadki
        """
        self.pop.update(new_pop)

    def __str__(self):
        return f'TeamPopulation({self.pop_num})'


class TeamSolver:
    def __init__(self, pop_size, team_size, group_size, hate_list, steps):
        self.pop_size = pop_size
        self.team_size = team_size
        self.group_size = group_size
        self.hate_list = hate_list
        self.steps = steps

        # Funkcja do generowania randomowych chromosomow o zadanych parametrach
        rand_team_gen = lambda: Team.random(group_size, team_size, hate_list)
        self.population = TeamPopulation(self.pop_size, rand_team_gen)

    def step(self):
        """
        Jeden krok algorytmu genetycznego
        
        1. Wybieramy najlepsza populacje
        2. Tworzymy nowe mutacje i krzyzowki
        3. Rozszerzamy populacje
        """
        self.population.select()
        
        # Zapisujemy nowa popluacje do osobnej tablicy
        next_pop = list(self.population.mutate())
        
        self.population.update(next_pop)
        
    def best_solution(self):
        """
        Zwraca najlepsze rozwiazanie
        """
        return self.population.best(1)[0]
        
    @property
    def solve(self):
        """
        Funkcja wykonuje kolejne kroki algorytmu genetycznego i 
            zwraca najlepsze rozwiazanie
        Jesli znalezlismy optymalne to zwraca wynik od razu
        """
        stats = []
        for i in range(self.steps):
            best_so_far = self.best_solution()
            print(f'Step {i}. Best so far {best_so_far}')
            
            stats.append((i, best_so_far.fitness))
            
            # Jesli juz znalezlismy optymalne rozwiazanie
            if best_so_far.fitness == 0:
                return best_so_far
            else:
                self.step()
        
        best_so_far = self.best_solution()
        return best_so_far, stats






