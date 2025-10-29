import random
    
class GA():

    def __init__(self,menu,M,N,print_gap = 10):
        self.print_gap = print_gap
        self.menu = menu
        self.M = M
        self.size_of_one = N
    
    def init_population(self,size_of_population,size_of_one):
        population = []
        
        for _ in range(size_of_population):
            single = [0]*size_of_one
            curr_weight = 0
            index = 0
            while True:
                index = random.randint(0,size_of_one-1)
                if single[index] == 0:
                    if (curr_weight + self.menu[index][0]) > self.M:
                        break
                    else:
                        curr_weight += self.menu[index][0]
                        single[index] = 1       
            population.append(single)
        return population
    
    def fitness(self,dna):
        res = [0,0]
        for i in range(len(self.menu)):
            res[0] += dna[i]*self.menu[i][0]
            res[1] += dna[i]*self.menu[i][1]
        
        if res[0]>self.M:
            res[0] = 0
            res[1] = 0
        
        return res

    def crossover1(self,left,right):
        i = random.randint(0,len(left)-1)
        return left[:i]+right[i:],left[i:]+right[:i]
    def crossover2(self, left, right):
        i = random.randint(0, len(left) - 1)
        j = random.randint(0, len(left) - 1)
        while j == i:
         j = random.randint(0, len(left) - 1)

        if i > j:
            i, j = j, i

        L = left[:i] + right[i:j] + left[j:]
        R = right[:i] + left[i:j] + right[j:]

        return L, R
    def crossover4(self,left,right):
       
        indexes = set()
        while len(indexes) < 4:
            indexes.add(random.randint(0, len(left) - 1))
    
        points = sorted(indexes)

        L = (left[:points[0]] + right[points[0]:points[1]] + left[points[1]:points[2]] + right[points[2]:points[3]] + left[points[3]:])
        R = (right[:points[0]] + left[points[0]:points[1]] + right[points[1]:points[2]] + left[points[2]:points[3]] + right[points[3]:])
    
        return L, R
    
    def mutate(self, agent, mut_prob):
        return ([a if random.random() > mut_prob else random.randint(0,1) for a in agent])

    def next_gen(self, population, mut_prob=0.1):
        new_population_size = len(population)
        new_population = []
    
        pop_fitness = [(self.fitness(individual), individual) for individual in population]
        pop_fitness.sort(reverse=True, key=lambda x: x[0][1])
        best_dna, best_fitness = pop_fitness[0][1], pop_fitness[0][0]

        fitness_values = [fit[0][1] for fit in pop_fitness]
        left_parents = random.choices([ind for _, ind in pop_fitness], weights=fitness_values, k=new_population_size)
        right_parents = random.choices([ind for _, ind in pop_fitness], weights=fitness_values, k=new_population_size)

        for i in range(new_population_size):
            function_num = random.randint(0,2)
            if function_num == 0:
                left_child, right_child = self.crossover1(left_parents[i], right_parents[i])
            elif function_num == 1:
                left_child, right_child = self.crossover2(left_parents[i], right_parents[i])
            else:
                left_child, right_child = self.crossover4(left_parents[i], right_parents[i])
            
            left_child = self.mutate(left_child, mut_prob)
            right_child = self.mutate(right_child, mut_prob)

            if self.fitness(left_child) > self.fitness(right_child):
                new_population.append(left_child)
            else:
                new_population.append(right_child)

        new_population.append(best_dna)
    
        return new_population, best_dna, best_fitness
    
    def solve(self,population_size = 700 ,num_generations = 120,mut_prob=0.01):
        population = self.init_population(population_size,self.size_of_one)
        for gen in range(num_generations):
            population, best_dna, best_fitness = self.next_gen(population,mut_prob)
            if gen % self.print_gap == 0:
                print(f"Generation: {gen} | Best Price: {best_fitness[1]}")

        print("Items useed for the solution:")
        for i in range(len(best_dna)):
            if best_dna[i] != 0:
                print(f"Item № {i+1} : [weigth/price] {self.menu[i][0]}/{self.menu[i][1]}")
        return best_dna
 
def main():
    M_N = input()
    M,N = map(int, M_N.split())

    items = {}
    it = []
    for i in range(N):
        numbers = input()
        weigth, price = map(int, numbers.split())
        pair = (weigth, price)
        it.append(pair)

    t = GA(it,M,N,10)
    t.solve()

if __name__ == "__main__":
    main()