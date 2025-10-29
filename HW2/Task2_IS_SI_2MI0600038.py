import random
import time

def show(soln, nr):
	for i in range(nr):
		row = ['-'] * nr
		for col in range(nr):
			if soln[col] == nr - 1 - i:
				row[col] = '*'
		print(' '.join(row))


def generate_table(N):
     
    board = [0] * N
    row_index = 0
    for i in range(N//2):
        board[i] = row_index
        board[i + (N//2)] = row_index+1
        row_index +=2
    if N % 2 == 1:
        board[N-1] = N - 1

    return board

def calc_conflicts(table,N,ld_conf,rd_conf,row_conf):
    num_of_diagonals = N*2-1
    for col in range(N):
        for row in range(N):
             if table[col] == row:
                  ld_conf[col+row] += 1
                  rd_conf[(N - 1 - col) + row] += 1
                  row_conf[row] += 1

def get_conf(ld_conf,rd_conf,row_conf,table,N):
    conflicts = [0] * N
    
    for i in range(N):
        conflicts[i] = row_conf[table[i]] + ld_conf[table[i] + i] + rd_conf[(N - 1 - i) + table[i]] - 3
    
    return conflicts

def gen_standart_table(N):
    res = []
    for i in range(N):
        res.append(N - 1 -i)
    
    return res

def get_col_conf(ld_conf,rd_conf,row_conf,table,N,col):
    conflicts = [0] * N
    min = N+1
    for row in range(N):
        if row != table[col]:
            conflicts[row] = row_conf[row] + ld_conf[row + col] + rd_conf[(N - 1 - col) + row]
            if conflicts[row] <= min:
                min = conflicts[row]
        else:
            conflicts[row] = N*2
    
    return [min,conflicts]

def update_conflicts(row_conf,left_diagonals_conf,right_diagonals_conf,random_col,table,new_row,N):
    row_conf[table[random_col]] -= 1
    row_conf[new_row] += 1
    left_diagonals_conf[random_col + table[random_col]] -= 1
    left_diagonals_conf[random_col + new_row] += 1
    right_diagonals_conf[(N - 1 - random_col) + table[random_col]] -= 1
    right_diagonals_conf[(N - 1 - random_col) + new_row] += 1

def min_conf_alg(N,max_steps,table,left_diagonals_conf,right_diagonals_conf,row_conf):
    
    for step in range(max_steps):

        conflicts = get_conf(left_diagonals_conf,right_diagonals_conf,row_conf,table,N)
        check = sum(conflicts)
        if check == 0:
            return table
        
        if check<(N//4):
            conflicted_columns = [i for i in range(N) if conflicts[i] > 0]
            random_col = random.choice(conflicted_columns)
        else:
            random_col = random.randint(0, N-1)
            while conflicts[random_col] == 0: 
                random_col = random.randint(0, N-1)
        
        conf_in_col = get_col_conf(left_diagonals_conf,right_diagonals_conf,row_conf,table,N,random_col)
        min_conflict_count = min(conf_in_col[1])

        #preventing loop (example with 6)
        if conf_in_col[1][0] != 0 and ((sum(conf_in_col[1])-(2*N))+1)//(min_conflict_count+1) == N-1:
            random_col = random.randint(0, N-1)
            conf_in_col = get_col_conf(left_diagonals_conf,right_diagonals_conf,row_conf,table,N,random_col)
    
        min_conflict_count = min(conf_in_col[1])
        new_row = random.choice([i for i in range(N) if conf_in_col[1][i] == min_conflict_count])
        
        update_conflicts(row_conf,left_diagonals_conf,right_diagonals_conf,random_col,table,new_row,N)
        table[random_col] = new_row

    return False

def main():
    N = int(input())
    
    if N == 2 or N == 3:
        print(-1)
        return
    if N == 1:
        print([0])
        return
    
    left_diagonals_conf = [0] * (N*2 - 1)
    right_diagonals_conf = [0] * (N*2 - 1)
    row_conf = [0] * N

    table = generate_table(N)
    calc_conflicts(table,N,left_diagonals_conf,right_diagonals_conf,row_conf)
    
    start = time.time()
    res = min_conf_alg(N,20000,table,left_diagonals_conf,right_diagonals_conf,row_conf)
    end = time.time()

    if res != False:
        if N < 100:
            show(res,N)
        else:
            print(round(end - start,2))
    else:
        print(-1)

             
if __name__ == "__main__":
    main()

