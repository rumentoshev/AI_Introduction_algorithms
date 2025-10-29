// Rumen Toshev,SI,FN: 2MI0600038
#include<iostream>
#include<vector>
#include<queue>
#include<math.h>
#include <algorithm> 
#include <map>
#include <chrono>
#include <iomanip>

int calculate_path_from_to(int from, int to, int side) {
	int xfrom = from % side;
	int yfrom = from / side;

	int xto = to % side;
	int yto = to / side;

	return abs(xfrom - xto) + abs(yfrom - yto);
}

int calculate_manh_distance(std::vector<int> numbers, int index_of_zero, int final_index_of_zero,int side) {
	int distance = 0;
	for (int i = 0; i < numbers.size(); i++)
	{
		if (numbers[i] == 0) {
			continue;
		}
		int target_index = numbers[i] - 1;
		if (final_index_of_zero <= target_index) {
			target_index++;
		}
		distance = distance + calculate_path_from_to(i, targetindex,side);
	}
	return distance;
}

class Table {
public:
	std::vector<int> numbers;
	int side;
	int manh_dist;
	Table* parent;
	int index_of_zero;
	int final_index_of_zero;
	std::string move;

	void print_table() const {
		int index = 0;
		for (int i = 0; i < side; i++) {
			for (int j = 0; j < side; j++) {
				std::cout << numbers[index++] << " ";
			}
			std::cout << "\n";
		}
	}

	Table(std::vector<int> numbers, int side, Table* parent,int index_of_zero,int final_index_of_zero,std::string move) {
		this->numbers = numbers;
		this->side = side;
		this->parent = parent;
		this->index_ofzero = index_of_zero;
		this->final_index_of_zero = final_index_of_zero;
		this->manh_dist = calculate_manh_distance(numbers,index_of_zero,final_index_of_zero, side);
		this->move = move;
	}

	bool is_solved() const {
		return manh_dist == 0 && index_of_zero == final_index_of_zero;
	}
};

bool is_move_possible(int new_index_of_zero, int index_of_zero , int side) {

	if (new_index_of_zero<0 || new_index_of_zero >(side * side - 1)) {
		return false;
	}
	int old_x = index_of_zero % side;
	int old_y = index_of_zero / side;
	return (abs(old_x - (new_index_of_zero % side)) + abs(old_y - (new_index_of_zero / side))) == 1;
}

std::vector<Table> generate_neighbours(Table& t) {
	std::vector<Table> neighbours;

	static std::map<int, std::string> moves_for_path = { {-1,"right"},
													   {1,"left"},
													   {t.side,"up"},
													   {-t.side,"down"}};
	static std::vector<int> moves = { -1,1,t.side,-t.side };
	for (int i = 0; i < moves.size(); i++) {
		std::vector<int> temp_numbers = t.numbers;
		int new_index_of_zero = t.index_of_zero + moves[i];
		if (is_move_possible(new_index_of_zero, t.index_of_zero, t.side)) {
			std::swap(temp_numbers[t.index_of_zero], temp_numbers[new_index_of_zero]);

			Table temp_table = Table(temp_numbers, t.side, &t, new_index_of_zero, t.final_index_of_zero,moves_for_path.at(moves[i]));
			
			
			if (t.parent != nullptr) {
				if (temp_numbers != t.parent->numbers) {
					neighbours.push_back(temp_table);
				}
			}
			else
			{
				neighbours.push_back(temp_table);
			}
			
		}
	}

	return neighbours;
}
int search(Table& t, int cost, int bound,int& final_cost, std::vector<std::string>& path) {

	int f = cost + t.manh_dist;
	if (f > bound) {
		return f;
	}
	if (f == cost) {

		path.push_back(t.move);
		final_cost = cost;
		return -1;
	}

	int min_bound = INT32_MAX;
	std::vector<Table> next_tables = generate_neighbours(t);
	for (int i = 0; i < next_tables.size(); i++) {
		int result = search(next_tables[i], cost + 1,bound,final_cost,path);
		if (result == -1) {
			
			if (t.move != "")
			{
				path.push_back(t.move);
			}
			return -1;
		}
		min_bound = std::min(min_bound, result);
	}
	return min_bound;
}

bool ida_star(Table& t,int& final_cost,std::vector<std::string>& path) {
	int bound = t.manh_dist;
	while (true) {
		int result = search(t, 0, bound,final_cost,path);

		if (result == -1) {
			
			return true;
		}
		if (result == INT32_MAX) {
			return false;
		}
		bound = result;
	}
}

int get_number_of_inversions(std::vector<int>& table) {

	int inversions = 0;

	for (int i = 0; i < table.size() - 1; i++) {
		for (int j = i + 1; j < table.size(); j++)
		{
			if (table[i] != 0 && table[j] != 0) {
				if (table[i] > table[j]) {
					inversions++;
				}
			}
		}
	}

	return inversions;
}

bool is_solvable(std::vector<int>& table, int side, int zero_index,int final_index) {

	size_t inversions = get_number_of_inversions(table);
	if (side % 2 == 1) {
		return (inversions % 2 == 0);
	}
	else {
		size_t row_where_zero_is = zero_index / side;
		if (inversions == 0) {
			if ((final_index / side) == row_where_zero_is) {
				return true;
			}
		}
		return ((inversions + row_where_zero_is) % 2 == 1);
	}

	return false;
}

int main() {

	int n;
	std::cin >> n;
	int side = sqrt(n + 1);

	int empty_position_target;
	std::cin >> empty_position_target;
	if (empty_position_target == -1) {
		empty_position_target = n;
	}
	if (n % 2 == 1 && empty_position_target == (n / 2)) {
		std::cout << -1;
		return -1;
	}
	std::vector<int> table;
	int zero_index = 0;

	for (int i = 0; i < n + 1; i++) {
		int temp_num;
		std::cin >> temp_num;
		if (temp_num == 0) {
			zero_index = i;
		}
		table.push_back(temp_num);
	}


	int steps = 0;
	std::vector<std::string> path;
	if (!issolvable(table, side, zero_index, empty_position_target)) {
		std::cout << -1;
		return -1;
	}
	Table t(table, side, nullptr, zero_index, empty_position_target,"");
	auto start = std::chrono::high_resolution_clock::now();
	bool res = idastar(t, steps, path);
	auto end = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> duration = end - start;
	if (res) {
		std::cout << steps << "\n";
		for (int i = path.size() - 1; i >= 0; i--) {
			std::cout << path[i]<<"\n";
		}
		//std::cout << "Ex. time: " << std::fixed << std::setprecision(2)<< duration.count() << " s." << std::endl;
	}
	else {
		std::cout << -1;
	}
	
}


