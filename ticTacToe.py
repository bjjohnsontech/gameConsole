#! /usr/bin/python

import sqlite3
from console import yesOrNo
from blessings import Terminal
term = Terminal()
from random import randint

class ttt():
    
    def __init__(self):
        self.lines = []
        self.playing = True
        self.played = []
        self.board = []
        self.conn = sqlite3.connect('console.db')
        #print sys.argv[1]
        self.curs = self.conn.cursor()
        #self.curs.execute('DROP TABLE tictactoe')
        self.curs.execute('CREATE TABLE IF NOT EXISTS tictactoe (total integer, wins integer, losses integer)')
        self.curs.execute('SELECT * from tictactoe')
        score = self.curs.fetchone()
        if score is None:
            self.curs.execute('INSERT INTO tictactoe VALUES (0,0,0)')
            self.conn.commit()
            score = (0,0,0)
        print "I love this game, I warn you though, I've played %d games and Have never lost." % (score[0])
        print
        self.record()
        
    def record(self):
        self.curs.execute('SELECT * from tictactoe')
        score = self.curs.fetchone()
        score = [str(x) for x in score]
        print term.underline("  Total Games |  Wins  |  Losses")
        print '  ' + score[0].zfill(11) + ' |  ' + score[1].zfill(4) + '  |  ' + score[2].zfill(6)
        print
        
    def play(self):
        while self.playing:
            self.curs.execute('UPDATE tictactoe set total=total+1')
            self.conn.commit()
            self.board = [str(x) for x in range(1,10)]
            self.played = []
            if yesOrNo('Would you like to go first?'):
                print "Ok, you'll be O's"
                self.drawBoard()
            else:
                print "Ok, I'll be X's"
                self.myMove(True)
            while not self.whoWon():
                self.yourMove()
                if not self.whoWon():
                    self.myMove(False)
                else:
                    break
            self.record()
            self.playing = yesOrNo('Play again?')
        print 'Thanks for playing.'
        return
                
    def drawBoard(self):
        '''///////////////////////////////////////////
        Build the board
        ///////////////////////////////////////////'''
        board = self.board
        print term.underline('%s|%s|%s' % (board[0], board[1], board[2]))
        print term.underline('%s|%s|%s' % (board[3], board[4], board[5]))
        print '%s|%s|%s' % (board[6], board[7], board[8])
        
    def yourMove(self):
        sector = raw_input('Where will you place your O?\n>>')
        while True:
            if sector not in [str(x) for x in range(1,10)]:
                sector = raw_input('Please enter the number of the square you want to place you O in./n>>')
                continue
            elif self.board[int(sector)-1] in ['O','X']:
                sector = raw_input('That squre has already been played. Try again please.\n>>')
                continue
            else:
                break
        self.board[int(sector)-1] = 'O'
        self.played.append(int(sector))
        
    def myMove(self, first):
        x = set(['X'])
        o = set(['O'])
        move = None
        toWin = None
        toBlock = None
        prefer = []
        preferNext = []
        # I move first, play top left
        '''if first:
            move = 1
        # I move second, play center unless already played then top left'''
        if len(self.played) == 1:
            if self.played != [5]:
                move = 5
        #else: # not first or second, find rows with 2 Xs or Os
        for line in self.lines:
            if len(line) == 2: # there are 2 of something in this line
                if len(set(line) - x - o) != 0: # there's an empty square
                    if len(set(line) - x) == 1: # an empty square with 2 Xs
                        toWin = set(line) - x # find the empty square and put X there
                        toWin = int(list(toWin)[0])
                    else: # an empty square with 2 Os
                        toBlock = set(line) - o # find the empty square and put X there
                        toBlock = int(list(toBlock)[0])
            elif len(line) == 3 and len(line - o) == 3 and len(line-x) == 2: #just X and two open
                for entry in line-x:
                    preferNext.append(int(entry))
        if (len(self.played) == 3
        and self.board[4] == 'X'
        and ((self.board[0] == 'O' and self.board[8] == 'O')
            or (self.board[2] == 'O' and self.board[6] == 'O'))):
            preferNext.extend([2,4,6,8])
        if preferNext:
            prefer = [x for x in preferNext if preferNext.count(x) > 1]
        if toWin:
            move = toWin
        elif toBlock:
            move = toBlock
        while move is None and prefer:
            r = randint(0, len(prefer)-1)
            if self.board[prefer[r]-1] == str(prefer[r]):
                move = prefer[r]
            prefer.remove(prefer[r])
        while move is None and preferNext:
            r = randint(0, len(preferNext)-1)
            if self.board[preferNext[r]-1] == str(preferNext[r]):
                move = preferNext[r]
            preferNext.remove(preferNext[r])
        firstTry = [2,4,6,8]
        while move is None and firstTry:
            r = randint(0, len(firstTry)-1)
            if self.board[firstTry[r]-1] == str(firstTry[r]):
                move = firstTry[r]
            firstTry.remove(firstTry[r])
        nextTry = [1,5,3,7,9]
        while move is None and nextTry:
            r = randint(0, len(nextTry)-1)
            if self.board[nextTry[r]-1] == str(nextTry[r]):
                move = nextTry[r]
            nextTry.remove(nextTry[r])
        self.board[move-1] = 'X'
        self.played.append(move)
        print "I played %d." % (move)
        self.drawBoard()
        
            
    def whoWon(self):
        self.calcLines()
        for line in self.lines:
            if len(line) == 1: # There's a winner
                if 'X' in line: # I won
                    print 'I won... Good Game.'
                    self.curs.execute('UPDATE tictactoe set wins=wins+1')
                    self.conn.commit()
                    return True
                else: # player won
                    import time
                    print 'You won!!! (syntax Error).....'
                    time.sleep(5)
                    print 'Just kidding. Good game.'
                    self.curs.execute('UPDATE tictactoe set losses=losses+1')
                    self.conn.commit()
                    return True
        for sqr in self.board:
            if sqr not in ['X','O']:
                return False
        print 'Well, we tied. Not unexpected.'
        return True
        
    def calcLines(self):
        self.lines = []
        for line in [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]:
            self.lines.append(set([self.board[x-1] for x in line]))
        #print self.lines