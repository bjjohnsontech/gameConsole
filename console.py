#! /usr/bin/python

from blessings import Terminal

term = Terminal()

keepPlaying = True
games = ['Tic-Tac-Toe',]
lowerGames = [x.lower() for x in games]
aliases = {'ttt': 'tic-tac-toe'}
def yesOrNo(input):
    while True:
        answer = raw_input(input+'(y/n)\n>>')
        if answer.lower() in ['n','no']:
            return False
        elif answer.lower() in ['y','yes']:
            return True
        else:
            print "I don't recognize that response."
            continue

if __name__ == '__main__':
    while keepPlaying:
        keepPlaying = playGame = yesOrNo('Would you like to play a game?')
        while playGame:
            print 'I am programmed to play the following games:'
            for game in games:
                print game
            play = raw_input('Which game would you like to play?\n>>')
            if aliases.has_key(play.lower()):
                play = aliases[play.lower()]
            elif play.lower() in lowerGames:
                pass
            elif play.lower() in ['q', 'quit']:
                playGame = False
                continue
            else:
                print "I don't recognize that game. If you decided not to play enter \"quit\""
                keepPlaying = False
                continue
            if play.lower() == 'tic-tac-toe':
                import ticTacToe
                game = ticTacToe.ttt()
                
            playGame = game.play()
    print 'I look forward to next time'
    
    