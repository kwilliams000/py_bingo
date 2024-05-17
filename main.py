'''Bingo game'''

import random
import timeit

class IncorrectCPUValue(Exception):
    '''Raised when the input value is outside the range 0 and 19 inclusive'''
    pass

class CPU_Board:
    def __init__(self) -> None:
        self.cpus: list = []

    def __len__(self):
        return len(self.cpus)
    
    '''def __iter__(self):
        self.num = 0
        self.length = len(self.cpus)
        return self.cpus[self.num]
    
    def __next__(self):
        if self.num > self.length:
            raise StopIteration
        else:
            self.num += 1
            return self.num'''


    def add_CPU(self, num_balls: list, board_size: int = 5):
        self.cpus.append(Board(num_balls, board_size))

class Board:
    def __init__(self, num_balls: list , board_size: int = 5) -> None:
        #self.board = list[list[dict]] = []
        self.board_size: int = board_size
        self.num_balls: list = num_balls
        self.board: list[list[dict]] = self.create_board()
        self.bingo: bool = False

    
    def create_board(self) -> list[list[dict]]:
        self.randomized_list: list[str] = self.num_balls
        random.shuffle(self.randomized_list)
        self.randomized_list = self.randomized_list[:self.board_size**2]
        row = []
        board: list[list[dict]] = []
        for number in self.randomized_list:
            row.append({'number':str(number),'checked':False})
            if len(row)%self.board_size == 0:
                board.append(row)
                row = []
        board[self.board_size//2][self.board_size//2]['number']='FREE SPACE'
        board[self.board_size//2][self.board_size//2]['checked']=True
        return board
    
    def mark_board(self, cell: str) -> None:
        for row in self.board:
            for i in row:
                if i['number'] == cell:
                    i['checked'] = True
                    return
    
    def mark_board_all(self) -> None:
        for row in self.board:
            for i in row:
                i['checked'] = True
    
    def display(self) -> None:
        row_number: str = '|'
        row_checked: str = '|'
        print('--------------------------------')
        for record in self.board:
            for cell in record:
                if len(cell['number']) == 1:
                    row_number += '  ' + cell['number'] + '  |'
                elif len(cell['number']) == 2:
                    row_number += '  ' + cell['number'] + ' |'
                else:
                    row_number += '  FS |'
                if cell['checked']:
                    row_checked += '  X  |'
                else:
                    row_checked += '     |'
            row_number += '\n'
            print(f'{row_number}{row_checked}')
            print('--------------------------------')
            row_number = '|'
            row_checked = '|'

    def calculate(self) -> None:
        def check_rows() -> bool:
            for i in range(self.board_size):
                row: list = []
                for j in range(self.board_size):
                    row.append(self.board[i][j]['checked'])
                if all(row):
                    return True
            return False
        def check_columns() -> bool:
            for k in range(self.board_size):
                col: list = []
                for l in range(self.board_size):
                    col.append(self.board[l][k]['checked'])
                if all(col):
                    return True
            return False
        def check_diagonals() -> bool:
            diag_1: list = [self.board[i][i]['checked'] for i in range(self.board_size)]
            diag_2: list = [self.board[self.board_size-1-i][i]['checked'] for i in range(self.board_size-1,-1,-1)]
                
            if all(diag_1) or all(diag_2):
                return True
            return False

        if check_rows() or check_columns() or check_diagonals():
            self.bingo = True
        else:
            self.bingo = False

    def check_bingo(self) -> bool:
        self.calculate()
        return self.bingo

    def is_bingo(self) -> bool:
        return self.check_bingo() == True
    
    def __str__(self) -> str:
        return f'{self.board}'

class Game:
    def play(self):
        #number_range: int = 25
        #balls: list = list(map(str,list(range(1,number_range+1))))
        self.num_of_cpu: int = -1
        self.game_active: bool = True
        self.board_size: int = 0
        self.cpu_boards: CPU_Board = CPU_Board()
        self.round: int = 0

        # Setup
        while self.board_size == 0:
            self.get_board_size()
            self.balls = list(map(str,list(range(1,self.generate_balls()+1))))
            self.get_num_cpu_players()
            self.player_board: Board = Board(num_balls=self.balls,board_size=self.board_size)
            random.shuffle(self.balls)
        
        print('Welcome to Bingo!\n\nYour game will now begin')

        # Actual game
        while self.game_active:
            self.round += 1
            print(f'\n----- Round {self.round} -----\n')
            print('Your board:')
            self.player_board.display()
            
            player_turn = False
            next_turn: str = input('Ready for the next ball?\n(Y - continue playing)\n(Q - quit playing)\n').lower()
            while player_turn == False:
                if next_turn not in ['y', 'q']:
                    print('Please enter "Y" to continue or "Q" to quit playing')
                elif next_turn == 'q':
                    return print('Game exited. Thanks for playing!')
                else:
                    player_turn = True
            
            next_ball: str = self.balls.pop()
            print(f'\nBall {next_ball}!')
            # update all boards with next_ball value
            self.player_board.mark_board(cell=next_ball)
            self.update_cpu_boards(next_ball=next_ball)
            
            # Exit loop if winner is found
            if self.check_winner(): continue

        print('\n\nThanks for playing!')

    def get_board_size(self) -> None:
        while self.board_size == 0:
                    change_board_size: str = input('Use default board size (5x5)? Y/N\n').lower()
                    if change_board_size not in ['y','n']:
                        print('Please enter "Y" or "N"')
                    elif change_board_size == 'n':
                        adj_board_size: int = 0
                        while adj_board_size < 0:
                            try:
                                adj_board_size: int = int(input('Please enter board width:\n'))
                            except ValueError:
                                print('Enter a board width (e.g. 5)\n')
                            else:
                                self.board_size = adj_board_size
                    else:
                        self.board_size = 5
    
    def get_num_cpu_players(self) -> None:
        while self.num_of_cpu < 0:
                try:
                    self.num_of_cpu= int(input('Please enter number of CPU players (0 - 19)\n'))
                    if self.num_of_cpu < 0 or self.num_of_cpu > 19: raise IncorrectCPUValue
                except ValueError:
                    print('You must enter a number\n')
                except IncorrectCPUValue:
                    print('You must enter a number from 0 to 19\n')
                else:
                    self.create_cpu_boards()

    def create_cpu_boards(self) -> None:
        for each in range(self.num_of_cpu):
            self.cpu_boards.add_CPU(num_balls=self.balls, board_size=self.board_size)

    def generate_balls(self) -> int:
        return (self.board_size**2) * 2 + 2*self.board_size
    
    def display_cpu_boards(self) -> None:
        for x in range(len(self.cpu_boards)):
            self.cpu_boards.cpus[x].display()
            
    def update_cpu_boards(self, next_ball) -> None:
        for x in range(len(self.cpu_boards)):
            self.cpu_boards.cpus[x].mark_board(cell=next_ball)

    def check_winner(self) -> bool:
        if self.player_board.is_bingo():
            self.game_active = False
            print('Congratulations! You win!')
            return True
        cpu_winners: list = []
        for x in range(len(self.cpu_boards)):
            if self.cpu_boards.cpus[x].is_bingo():
                cpu_winners.append(x)
        if len(cpu_winners) > 0:
            self.game_active = False
            print('Too bad, another CPU player got bingo!')
            print('The following CPU player(s) won:')
            for x in cpu_winners:
                print(f'CPU {x+1}')
                self.cpu_boards.cpus[x].display()
            return True
        return False


def main()->None:
    g:Game = Game()
    g.play()

if __name__ == '__main__':
    main()