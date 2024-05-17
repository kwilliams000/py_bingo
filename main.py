'''Bingo game'''

import cmd_version as cmdv


def main()->None:
    g:cmdv.Game = cmdv.Game()
    g.play()

if __name__ == '__main__':
    main()