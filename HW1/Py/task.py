import math
from typing import List


visitedTablesPath = []

def calculate_path_from_to(start: int, end: int, side: int) -> int:
    x_from, y_from = start % side, start // side
    x_to, y_to = end % side, end // side
    return abs(x_from - x_to) + abs(y_from - y_to)

def calculate_manhattan_distance(numbers: List[int], index_of_zero: int, final_index_of_zero: int, side: int) -> int:
    distance = 0
    for i in range(len(numbers)):
        if numbers[i] == 0:
            continue
        target_index = numbers[i] - 1
        if final_index_of_zero <= target_index:
            target_index += 1
        distance += calculate_path_from_to(i, target_index, side)
    return distance

class Table:
    def __init__(self, numbers: List[int], side: int, index_of_zero: int, final_index_of_zero: int, move: str):
        self.numbers = numbers
        self.side = side
        self.index_of_zero = index_of_zero
        self.final_index_of_zero = final_index_of_zero
        self.manhattan_distance = calculate_manhattan_distance(numbers, index_of_zero, final_index_of_zero, side)
        self.move = move

    def print_table(self):
        for i in range(self.side):
            print(" ".join(map(str, self.numbers[i * self.side:(i + 1) * self.side])))
        print()

def is_move_possible(new_index_of_zero: int, index_of_zero: int, side: int) -> bool:
    if new_index_of_zero < 0 or new_index_of_zero >= side * side:
        return False
    old_x, old_y = index_of_zero % side, index_of_zero // side
    return abs(old_x - (new_index_of_zero % side)) + abs(old_y - (new_index_of_zero // side)) == 1

def generate_neighbors(table: Table) -> List[Table]:
    neighbors = []
    moves_for_path = {-1: "right", 1: "left", table.side: "up", -table.side: "down"}
    moves = [-1, 1, table.side, -table.side]

    for move in moves:
        temp_numbers = table.numbers[:]
        new_index_of_zero = table.index_of_zero + move
        if is_move_possible(new_index_of_zero, table.index_of_zero, table.side):
            temp_numbers[table.index_of_zero], temp_numbers[new_index_of_zero] = temp_numbers[new_index_of_zero], temp_numbers[table.index_of_zero]
            temp_table = Table(temp_numbers, table.side, new_index_of_zero, table.final_index_of_zero, moves_for_path[move])

            if temp_table.numbers not in visitedTablesPath:
                neighbors.append(temp_table)

    return neighbors

def search(table: Table, cost: int, bound: int, final_cost: dict, path: List[str]) -> int:
    f = cost + table.manhattan_distance
    visitedTablesPath.append(table.numbers[:])
    if f > bound:
        visitedTablesPath.pop()
        return f
    if f == cost:
        path.append(table.move)
        final_cost['value'] = cost
        return -1

    min_bound = float('inf')
    for next_table in generate_neighbors(table):
        if next_table.numbers in visitedTablesPath:
            continue
        result = search(next_table, cost + 1, bound, final_cost, path)
        if result == -1:
            if table.move:
                path.append(table.move)
            return -1
        min_bound = min(min_bound, result)
    return min_bound


def ida_star(table: Table, final_cost: dict, path: List[str]) -> bool:
    bound = table.manhattan_distance
    while True:
        result = search(table, 0, bound, final_cost, path)
        if result == -1:
            return True
        if result == float('inf'):
            return False
        bound = result

def get_number_of_inversions(table: List[int]) -> int:
    inversions = 0
    for i in range(len(table) - 1):
        for j in range(i + 1, len(table)):
            if table[i] != 0 and table[j] != 0 and table[i] > table[j]:
                inversions += 1
    return inversions

def is_solvable(table: List[int], side: int, zero_index: int, final_index: int) -> bool:
    inversions = get_number_of_inversions(table)
    if side % 2 == 1:
        return inversions % 2 == 0
    else:
        row_where_zero_is = zero_index // side
        if inversions == 0:
            if final_index // 3 == row_where_zero_is:
                return True
        return (inversions + row_where_zero_is) % 2 == 1

# Main function
def main():
    N = int(input())
    side = int(math.sqrt(N + 1))

    empty_position_target = int(input())
    if empty_position_target == -1:
        empty_position_target = N
    if N % 2 == 1 and empty_position_target == (N // 2):
        print(-1)
        return

    table = []
    zero_index = 0
    for i in range(N + 1):
        temp_num = int(input())
        if temp_num == 0:
            zero_index = i
        table.append(temp_num)

    steps = {'value': 0}  # Use dictionary to store final cost
    path = []
    if not is_solvable(table, side, zero_index, empty_position_target):
        print(-1)
        return -1

    initial_table = Table(table, side, zero_index, empty_position_target, "")
    

    if ida_star(initial_table, steps, path):
        print(steps['value'])
        print("\n".join(reversed(path)))
    else:
        print(-1)

if __name__ == "__main__":
    main()
