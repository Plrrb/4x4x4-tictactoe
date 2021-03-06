import socket
import arcade
import argparse
import threading


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "4x4x4 Tic Tac Toe"
GRID_X = 25
GRID_Y = SCREEN_HEIGHT - 100
BACKGROUND_COLOR = arcade.color.WHITE


class TicTacToe4x4x4(arcade.Window):
    def __init__(self, width, height, title, client_socket, my_turn):
        super().__init__(width, height, title)

        self.client_socket = client_socket
        self.ttt_sound = arcade.Sound(":resources:sounds/explosion2.wav")
        self.my_turn = my_turn

        arcade.set_background_color(BACKGROUND_COLOR)

    def on_draw(self):

        arcade.start_render()
        # print("drawing")

        for i in range(4):
            self.draw_grid(250 * i + GRID_X, GRID_Y)

        # draw players
        for layer in range(4):
            for row in range(4):
                for col in range(4):
                    x, y = self.get_center(layer, row, col)
                    arcade.draw_text(
                        self.cube[layer][row][col]["symbol"],
                        x,
                        y,
                        self.cube[layer][row][col]["is_win"],
                        40,
                        font_name="comic",
                    )
        if self.game_over:
            self.draw_winner()

        # draw who the current player is
        arcade.draw_text(
            self.current_player["symbol"] + "'s Turn",
            (SCREEN_WIDTH / 2) - 56,
            SCREEN_HEIGHT - 100,
            arcade.color.BLACK,
            30,
            font_name="comic",
        )

        # draw the players score
        for i, player in enumerate(self.players):
            arcade.draw_text(
                f"{player['symbol']}'s Score: {player['score']}",
                (SCREEN_WIDTH / 2) - 130,
                GRID_Y - 250 - i * 50,
                arcade.color.BLACK,
                35,
                font_name="comic",
            )

    def check_win(self, player, input_layer, input_row, input_col):
        has_win = False

        win_color = arcade.color.RED

        for layer in self.cube:
            for row in layer:
                for col in row:
                    col["is_win"] = arcade.color.BLACK
        wins = 0
        d = 4

        # all in a row
        for i, layer in enumerate(self.cube):
            for j, row in enumerate(layer):

                if (
                    player
                    == row[0]["symbol"]
                    == row[1]["symbol"]
                    == row[2]["symbol"]
                    == row[3]["symbol"]
                ):
                    print(input_layer, input_row, input_col)
                    if input_layer == i and input_row == j:
                        if not has_win:
                            self.ttt_sound.play()
                            has_win = True
                        row[0]["is_win"] = row[1]["is_win"] = row[2]["is_win"] = row[3][
                            "is_win"
                        ] = win_color

                    wins += 1

                    print("all in row", player, i, j)

        # all in a column
        for i, layer in enumerate(self.cube):
            for col in range(d):
                if (
                    player
                    == layer[0][col]["symbol"]
                    == layer[1][col]["symbol"]
                    == layer[2][col]["symbol"]
                    == layer[3][col]["symbol"]
                ):
                    if input_layer == i and col == input_col:
                        if not has_win:
                            self.ttt_sound.play()
                            has_win = True
                        layer[0][col]["is_win"] = layer[1][col]["is_win"] = layer[2][
                            col
                        ]["is_win"] = layer[3][col]["is_win"] = win_color
                    wins += 1
                    print("all in col", player, col)

        # split layer all in row
        for i in range(d):
            for j in range(d):
                if (
                    player
                    == self.cube[0][i][j]["symbol"]
                    == self.cube[1][i][j]["symbol"]
                    == self.cube[2][i][j]["symbol"]
                    == self.cube[3][i][j]["symbol"]
                ):
                    if input_row == i and input_col == j:
                        if not has_win:
                            self.ttt_sound.play()
                            has_win = True
                        self.cube[0][i][j]["is_win"] = self.cube[1][i][j][
                            "is_win"
                        ] = self.cube[2][i][j]["is_win"] = self.cube[3][i][j][
                            "is_win"
                        ] = win_color
                    wins += 1
                    print("split layer all in row", player, i, j)

        # one layer diagonal
        for i, layer in enumerate(self.cube):
            if (
                player
                == layer[0][0]["symbol"]
                == layer[1][1]["symbol"]
                == layer[2][2]["symbol"]
                == layer[3][3]["symbol"]
            ):
                if input_layer == i and input_col == input_row:

                    if not has_win:
                        self.ttt_sound.play()
                        has_win = True
                    layer[0][0]["is_win"] = layer[1][1]["is_win"] = layer[2][2][
                        "is_win"
                    ] = layer[3][3]["is_win"] = win_color

                wins += 1

                print("one layer diagonal 1", player, i)

            if (
                player
                == layer[3][0]["symbol"]
                == layer[2][1]["symbol"]
                == layer[1][2]["symbol"]
                == layer[0][3]["symbol"]
            ):
                if input_layer == i and input_col == abs(input_row - 3):

                    if not has_win:
                        self.ttt_sound.play()
                        has_win = True

                    layer[3][0]["is_win"] = layer[2][1]["is_win"] = layer[1][2][
                        "is_win"
                    ] = layer[0][3]["is_win"] = win_color
                wins += 1

                print("one layer diagonal 2", player, i)

        # multi layer diagonal
        for i in range(d):
            if (
                player
                == self.cube[0][0][i]["symbol"]
                == self.cube[1][1][i]["symbol"]
                == self.cube[2][2][i]["symbol"]
                == self.cube[3][3][i]["symbol"]
            ):
                if input_col == input_row and input_layer == i:

                    if not has_win:
                        self.ttt_sound.play()
                        has_win = True

                    self.cube[0][0][i]["is_win"] = self.cube[1][1][i][
                        "is_win"
                    ] = self.cube[2][2][i]["is_win"] = self.cube[3][3][i][
                        "is_win"
                    ] = win_color
                wins += 1

                print("multi layer diagonal 1", player, i)

            if (
                player
                == self.cube[0][3][i]["symbol"]
                == self.cube[1][2][i]["symbol"]
                == self.cube[2][1][i]["symbol"]
                == self.cube[3][0][i]["symbol"]
            ):
                if (
                    (input_layer == 0 and input_row == 3)
                    or (input_layer == 1 and input_row == 2)
                    or (input_layer == 2 and input_row == 1)
                    or (input_layer == 3 and input_row == 0)
                    and input_col == i
                ):

                    if not has_win:
                        self.ttt_sound.play()
                        has_win = True

                    self.cube[0][3][i]["is_win"] = self.cube[1][2][i][
                        "is_win"
                    ] = self.cube[2][1][i]["is_win"] = self.cube[3][0][i][
                        "is_win"
                    ] = win_color
                wins += 1

                print("multi layer diagonal 2", player, i)

        # horizontal diagonal
        for i in range(d):
            if (
                player
                == self.cube[3][i][3]["symbol"]
                == self.cube[0][i][0]["symbol"]
                == self.cube[1][i][1]["symbol"]
                == self.cube[2][i][2]["symbol"]
            ):

                if not has_win:
                    self.ttt_sound.play()
                    has_win = True

                self.cube[3][i][3]["is_win"] = self.cube[0][i][0]["is_win"] = self.cube[
                    1
                ][i][1]["is_win"] = self.cube[2][i][2]["is_win"] = win_color
                wins += 1

                print("horizontal diagonal 1", player, i)

            if (
                player
                == self.cube[3][i][3]["symbol"]
                == self.cube[2][i][0]["symbol"]
                == self.cube[1][i][1]["symbol"]
                == self.cube[0][i][2]["symbol"]
            ):

                if not has_win:
                    self.ttt_sound.play()
                    has_win = True

                self.cube[3][i][3]["is_win"] = self.cube[2][i][0]["is_win"] = self.cube[
                    1
                ][i][1]["is_win"] = self.cube[0][i][2]["is_win"] = win_color
                wins += 1

                print("horizontal diagonal 2", player, i)

        # thru opposite corners of the cube
        if (
            player
            == self.cube[3][0][3]["symbol"]
            == self.cube[2][1][2]["symbol"]
            == self.cube[1][2][1]["symbol"]
            == self.cube[0][3][0]["symbol"]
        ):
            indices = {
                (3, 0, 3),
                (2, 1, 2),
                (1, 2, 1),
                (0, 3, 0),
            }

            if (input_layer, input_row, input_col) in indices:

                if not has_win:
                    self.ttt_sound.play()
                    has_win = True

                self.cube[3][0][3]["is_win"] = self.cube[2][1][2]["is_win"] = self.cube[
                    1
                ][2][1]["is_win"] = self.cube[0][3][0]["is_win"] = win_color
                wins += 1

            print("thru oppsite corners of the cube 1", player)

        if (
            player
            == self.cube[0][0][0]["symbol"]
            == self.cube[1][1][1]["symbol"]
            == self.cube[2][2][2]["symbol"]
            == self.cube[3][3][3]["symbol"]
        ):
            if input_layer == input_row == input_col:

                if not has_win:
                    self.ttt_sound.play()
                    has_win = True

                self.cube[0][0][0]["is_win"] = self.cube[1][1][1]["is_win"] = self.cube[
                    2
                ][2][2]["is_win"] = self.cube[3][3][3]["is_win"] = win_color
            wins += 1

            print("thru oppsite corners of the cube 2", player)

        if (
            player
            == self.cube[0][3][3]["symbol"]
            == self.cube[1][2][2]["symbol"]
            == self.cube[2][1][1]["symbol"]
            == self.cube[3][0][0]["symbol"]
        ):
            indices = {
                (0, 3, 3),
                (1, 2, 2),
                (2, 1, 1),
                (3, 0, 0),
            }

            if (input_layer, input_row, input_col) in indices:

                if not has_win:
                    self.ttt_sound.play()
                    has_win = True

                self.cube[0][3][3]["is_win"] = self.cube[1][2][2]["is_win"] = self.cube[
                    2
                ][1][1]["is_win"] = self.cube[3][0][0]["is_win"] = win_color
            wins += 1

            print("thru oppsite corners of the cube 3", player)

        if (
            player
            == self.cube[0][0][3]["symbol"]
            == self.cube[1][1][2]["symbol"]
            == self.cube[2][2][1]["symbol"]
            == self.cube[3][3][0]["symbol"]
        ):
            indices = {
                (0, 0, 3),
                (1, 1, 2),
                (2, 2, 1),
                (3, 3, 0),
            }

            if (input_layer, input_row, input_col) in indices:

                if not has_win:
                    self.ttt_sound.play()
                    has_win = True

                self.cube[0][0][3]["is_win"] = self.cube[1][1][2]["is_win"] = self.cube[
                    2
                ][2][1]["is_win"] = self.cube[3][3][0]["is_win"] = win_color
            wins += 1

            print("thru oppsite corners of the cube 4", player)

        return wins

    def setup(self):

        self.game_over = False

        self.cube = [
            [
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
            ],
            [
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
            ],
            [
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
            ],
            [
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
                [
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                    {"symbol": "", "is_win": arcade.color.BLACK},
                ],
            ],
        ]

        self.player_index = 0

        self.players = [
            {"symbol": "X", "score": 0},
            {"symbol": "O", "score": 0},
        ]

        self.current_player = self.players[self.player_index]

    def modify_cube(self, grid, row, col, symbol):
        self.cube[grid][row][col]["symbol"] = symbol

        self.current_player["score"] = self.check_win(
            self.current_player["symbol"], grid, row, col
        )

    def switch_player(self):
        self.my_turn = not self.my_turn

        self.player_index = 1 - self.player_index

        self.current_player = self.players[self.player_index]

    def recv_move(self):
        while True:
            response = self.client_socket.recv(1024).decode("ascii")

            formatted_response = eval(response)
            self.modify_cube(
                *formatted_response, self.current_player["symbol"]
            )  # this * might be a problem
            self.switch_player()

    def on_mouse_press(self, x, y, button, key_modifiers):

        if not self.my_turn:

            return

        grid = self.hit_grid(x, y)
        if grid == -1:
            return

        row, col = self.hit_square(x, y, grid)
        if row == -1 or col == -1:
            return

        if self.cube[grid][row][col]["symbol"] != "":
            return

        print(grid, row, col)

        self.modify_cube(grid, row, col, self.current_player["symbol"])

        self.client_socket.send(f"({grid},{row},{col})".encode("ascii"))
        self.switch_player()

        if self.is_cube_full():
            self.game_over = True
            return

    def draw_winner(self):
        p = sorted(self.players, key=lambda k: k["score"], reverse=True)

        best_players = []
        top_player = p[0]["score"]

        for player in p:
            if player["score"] == top_player:
                best_players.append(player)
            else:
                break

        winners = ""
        if len(best_players) == len(self.players):
            winners = "everyone loses!"
        else:
            for player in best_players:
                winners += player["symbol"] + ", "
            winners += "wins"

        arcade.draw_text(
            winners,
            SCREEN_WIDTH / 2,
            100,
            arcade.color.GOLDEN_YELLOW,
            40,
            font_name="comic",
        )

    def get_center(self, grid, row, col):
        x = grid * 250 + col * 50 + (GRID_X + 6)
        y = (GRID_Y - 54) - row * 50
        return x, y

    def hit_square(self, x, y, grid):
        gridx = 250 * grid + GRID_X
        gridy = GRID_Y

        hit_col = -1
        hit_row = -1

        for col in range(4):
            if x > gridx + col * 50 and x < gridx + (col + 1) * 50:
                hit_col = col
                break

        for row in range(4):
            if y < gridy - row * 50 and y > gridy - 50 * (row + 1):
                hit_row = row
                break

        return hit_row, hit_col

    def hit_grid(self, x, y):

        for i in range(4):
            if (
                x > 250 * i + GRID_X
                and x < 250 * i + GRID_X + 200
                and y < GRID_Y
                and y > GRID_Y - 200
            ):
                return i
        return -1

    def is_cube_full(self):
        for layer in self.cube:
            for row in layer:
                for col in row:
                    if col["symbol"] == "":
                        return False

        return True

    def draw_grid(self, x, y):
        scale = 1
        grid = 50 * (5 - 1)

        # horizontal lines
        for i in range(1, 4):
            lineX = x
            lineY = y - (50 * i)

            arcade.draw_line(lineX, lineY, lineX + grid, lineY, (1, 1, 1), scale * 5)

        # vertical lines
        for i in range(1, 4):
            lineX = x + (50 * i)
            lineY = y
            arcade.draw_line(lineX, lineY, lineX, lineY - grid, (1, 1, 1), scale * 5)
