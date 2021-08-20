import arcade
import socket
import argparse

from tictactoe_4x4x4 import TicTacToe4x4x4


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "4x4x4 Tic Tac Toe"
GRID_X = 25
GRID_Y = SCREEN_HEIGHT - 100
BACKGROUND_COLOR = arcade.color.WHITE


def main():
    """Main method"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="its the port number", required=True)
    parser.add_argument("--ip", help="its the ipaddress")
    args = parser.parse_args()

    # create a socket object
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connection to hostname on the port.
    clientsocket.connect((args.ip, int(args.port)))

    game = TicTacToe4x4x4(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, clientsocket)
    game.setup(1, "client")
    arcade.run()


if __name__ == "__main__":
    main()
