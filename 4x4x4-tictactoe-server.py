import socket
import arcade
import argparse
import threading

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
    args = parser.parse_args()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostname(), int(args.port)))
    server_socket.listen(5)

    print("waiting for client connection")
    client_socket, addr = server_socket.accept()
    print("client connected from", addr)

    game = TicTacToe4x4x4(
        SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, client_socket, my_turn=True
    )

    recv_thread = threading.Thread(target=game.recv_move, daemon=True)

    game.setup()
    recv_thread.start()
    arcade.run()


if __name__ == "__main__":
    main()
