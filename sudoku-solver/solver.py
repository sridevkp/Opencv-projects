import time
import sys 

def idx2rowcol( idx ):
    return idx//9, idx %9

def rowcol2idx(row, col):
    return row * 9 + col

def valid(puzzle, idx):
    val = puzzle[idx]
    if val == 0 : return 0 

    row, col = idx2rowcol( idx )

    for i in range( 9 ):
        if i != col and puzzle[ rowcol2idx(row, i) ] == val : return False
    
    for i in range( 9 ):
        if i != row and puzzle[ rowcol2idx(i, col) ] == val : return False

    srow = row // 3 * 3
    scol = col // 3 * 3
    
    for i in range(srow, srow+3):
        for j in range(scol, scol+3):
            cidx = rowcol2idx(i, j)
            if cidx != idx and puzzle[cidx] == val : return False

    return True


def solve( puzzle, idx=0, debug=False ):
    if debug:
        sys.stdout.write('\033[F'*9)
        for i in range(0,81,9): sys.stdout.write( str(puzzle[ i: i+9 ])+"\n" )
        sys.stdout.flush()
        time.sleep(.1)

    if idx > 80 : return True
    if puzzle[idx] != 0 :  return solve( puzzle, idx +1, debug)
    
    for i in range(10):
        puzzle[idx] = i

        if valid( puzzle, idx ) and solve( puzzle, idx + 1, debug):
            return True
        
        puzzle[idx] = 0

    return False 

def solved( puzzle, debug=False ):
    copy = puzzle.copy()
    if debug : print("\n"*9)
    ret = solve( copy, debug=debug )
    return ret, copy

if __name__ == "__main__":
    debug=True
    puzzle = [ 
            5, 0, 0, 0, 7, 0, 0, 0, 0,
            6, 0, 0, 0, 9, 0, 0, 0, 0,
            0, 0, 8, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 6, 0, 0, 0, 3,
            4, 0, 0, 0, 0, 3, 0, 0, 0,
            7, 0, 0, 0, 2, 0, 0, 0, 6,
            0, 0, 0, 0, 0, 0, 0, 8, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 5,
            0, 0, 0, 0, 8, 0, 0, 0, 0,
            ]
    
    ret, solved_puzzle = solved(puzzle, debug=True)
    print("")
    
    
