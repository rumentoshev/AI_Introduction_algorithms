// Rumen Toshev,SI,FN: 2MI0600038
#include<iostream>
#include<vector>
#include<queue>
#include<math.h>
#include <algorithm> 
#include <map>
#include <chrono>
#include <iomanip>

int calculatepathfromto(int from, int to, int side) {
	int xfrom = from % side;
	int yfrom = from / side;

	int xto = to % side;
	int yto = to / side;

	return abs(xfrom - xto) + abs(yfrom - yto);
}

int calculatemanhdistance(std::vector<int> numbers, int indexofzero, int finalindexofzero,int side) {
	int distance = 0;
	for (int i = 0; i < numbers.size(); i++)
	{
		if (numbers[i] == 0) {
			continue;
		}
		int targetindex = numbers[i] - 1;
		if (finalindexofzero <= targetindex) {
			targetindex++;
		}
		distance = distance + calculatepathfromto(i, targetindex,side);
	}
	return distance;
}

class Table {
public:
	std::vector<int> numbers;
	int side;
	int manhdist;
	Table* parent;
	int indexofzero;
	int finalindexofzero;
	std::string move;

	void printtable() const {
		int index = 0;
		for (int i = 0; i < side; i++) {
			for (int j = 0; j < side; j++) {
				std::cout << numbers[index++] << " ";
			}
			std::cout << "\n";
		}
	}

	Table(std::vector<int> numbers, int side, Table* parent,int indexofzero,int finalindexofzero,std::string move) {
		this->numbers = numbers;
		this->side = side;
		this->parent = parent;
		this->indexofzero = indexofzero;
		this->finalindexofzero = finalindexofzero;
		this->manhdist = calculatemanhdistance(numbers,indexofzero,finalindexofzero, side);
		this->move = move;
	}

	bool issolved() const {
		return manhdist == 0 && indexofzero == finalindexofzero;
	}
};

bool ismovepossible(int newindexofzere, int indexofzero , int side) {

	if (newindexofzere<0 || newindexofzere >(side * side - 1)) {
		return false;
	}
	int oldx = indexofzero % side;
	int oldy = indexofzero / side;
	return (abs(oldx - (newindexofzere % side)) + abs(oldy - (newindexofzere / side))) == 1;
}

std::vector<Table> generateneighbours(Table& t) {
	std::vector<Table> neighbours;

	static std::map<int, std::string> movesforpath = { {-1,"right"},
													   {1,"left"},
													   {t.side,"up"},
													   {-t.side,"down"}};
	static std::vector<int> moves = { -1,1,t.side,-t.side };
	for (int i = 0; i < moves.size(); i++) {
		std::vector<int> tempnumbers = t.numbers;
		int newindexofzero = t.indexofzero + moves[i];
		if (ismovepossible(newindexofzero, t.indexofzero, t.side)) {
			std::swap(tempnumbers[t.indexofzero], tempnumbers[newindexofzero]);

			Table temptable = Table(tempnumbers, t.side, &t, newindexofzero, t.finalindexofzero,movesforpath.at(moves[i]));
			
			
			if (t.parent != nullptr) {
				if (tempnumbers != t.parent->numbers) {
					neighbours.push_back(temptable);
				}
			}
			else
			{
				neighbours.push_back(temptable);
			}
			
		}
	}

	return neighbours;
}
int search(Table& t, int cost, int bound,int& finalcost, std::vector<std::string>& path) {

	int f = cost + t.manhdist;
	if (f > bound) {
		return f;
	}
	if (f == cost) {

		path.push_back(t.move);
		finalcost = cost;
		return -1;
	}

	int minbound = INT32_MAX;
	std::vector<Table> nexttables = generateneighbours(t);
	for (int i = 0; i < nexttables.size(); i++) {
		int result = search(nexttables[i], cost + 1,bound,finalcost,path);
		if (result == -1) {
			
			if (t.move != "")
			{
				path.push_back(t.move);
			}
			return -1;
		}
		minbound = std::min(minbound, result);
	}
	return minbound;
}

bool idastar(Table& t,int& finalcost,std::vector<std::string>& path) {
	int bound = t.manhdist;
	while (true) {
		int result = search(t, 0, bound,finalcost,path);

		if (result == -1) {
			
			return true;
		}
		if (result == INT32_MAX) {
			return false;
		}
		bound = result;
	}
}

int getnumberofinversions(std::vector<int>& table) {

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

bool issolvable(std::vector<int>& table, int side, int zeroindex,int finalindex) {

	size_t inversions = getnumberofinversions(table);
	if (side % 2 == 1) {
		return (inversions % 2 == 0);
	}
	else {
		size_t rowwherezerois = zeroindex / side;
		if (inversions == 0) {
			if ((finalindex / side) == rowwherezerois) {
				return true;
			}
		}
		return ((inversions + rowwherezerois) % 2 == 1);
	}

	return false;
}

int main() {

	int n;
	std::cin >> n;
	int side = sqrt(n + 1);

	int emptypositiontarget;
	std::cin >> emptypositiontarget;
	if (emptypositiontarget == -1) {
		emptypositiontarget = n;
	}
	if (n % 2 == 1 && emptypositiontarget == (n / 2)) {
		std::cout << -1;
		return -1;
	}
	std::vector<int> table;
	int zeroindex = 0;

	for (int i = 0; i < n + 1; i++) {
		int temp_num;
		std::cin >> temp_num;
		if (temp_num == 0) {
			zeroindex = i;
		}
		table.push_back(temp_num);
	}


	int steps = 0;
	std::vector<std::string> path;
	if (!issolvable(table, side, zeroindex, emptypositiontarget)) {
		std::cout << -1;
		return -1;
	}
	Table t(table, side, nullptr, zeroindex, emptypositiontarget,"");
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


