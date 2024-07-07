import tkinter as tk
import tkinter.messagebox as messagebox

class DotsAndBoxes:
    def __init__(self, master, rows=5, cols=5):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.turn = 1
        self.player_scores = [0, 0]  # Player 1 and Computer scores
        self.completed_coords = []
        self.lines = []
        self.create_info_labels()
        self.draw_board()

    def draw_board(self):
        canvas_height = self.rows * 100 + 100
        canvas_width = self.cols * 100 + 100
        self.canvas = tk.Canvas(self.master, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()

        for r in range(self.rows + 1):
            for c in range(self.cols):
                self.draw_horizontal_line(r, c)
        for r in range(self.rows):
            for c in range(self.cols + 1):
                self.draw_vertical_line(r, c)
        # Draw the bottom horizontal border
        for c in range(self.cols):
            self.draw_horizontal_line(self.rows, c)
        # Draw the rightmost vertical border
        for r in range(self.rows):
            self.draw_vertical_line(r, self.cols)

    def create_info_labels(self):
        self.turn_label = tk.Label(self.master, text="Player 1's turn", font=("Arial", 20))
        self.turn_label.pack()

        self.score_label = tk.Label(self.master, text="Player 1 Score: 0   Computer Score: 0", font=("Arial", 20))
        self.score_label.pack()

    def draw_dot(self, row, col):
        x = col * 100 + 50
        y = row * 100 + 50
        dot = self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="black")

    def draw_horizontal_line(self, row, col):
        x1 = col * 100 + 50
        y1 = row * 100 + 50
        x2 = (col + 1) * 100 + 50
        y2 = y1
        line = self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=4)
        self.lines.append(line)

    def draw_vertical_line(self, row, col):
        x1 = col * 100 + 50
        y1 = row * 100 + 50
        x2 = x1
        y2 = (row + 1) * 100 + 50
        line = self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=4)
        self.lines.append(line)

    def on_click_line(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        if item in self.lines:
            self.canvas.itemconfig(item, fill="red")
            self.lines.remove(item)
            col = (event.x - 50) // 100
            row = (event.y - 50) // 100
            print(f"Clicked line: Row {row}, Column {col}")
            self.check_box_completion()
            if not self.lines:
                self.game_over()
            elif self.turn == 1:
                self.switch_turn()
                self.computer_move()
            self.update_info()

    def switch_turn(self):
        self.turn = 2 if self.turn == 1 else 1


    def update_info(self):
        current_player = "Computer" if self.turn == 2 else "Player 1"
        self.turn_label.config(text=f"{current_player}'s turn")
        self.score_label.config(text=f"Player 1 Score: {self.player_scores[0]}   Computer Score: {self.player_scores[1]}")


    def check_box_completion(self):
        # Iterate over each box
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.completed_coords:
                    continue
                # Check the right line of the box
                right_line = self.canvas.find_closest((c + 1) * 100, r * 100 + 50)[0]
                # Check the bottom line of the box
                bottom_line = self.canvas.find_closest(c * 100 + 50, (r + 1) * 100)[0]
                # Check the right line of the box below
                bottom_right_line = self.canvas.find_closest((c + 1) * 100, (r + 1) * 100 + 50)[0]
                # Check the bottom line of the box to the right
                right_bottom_line = self.canvas.find_closest(c * 100 + 100, r * 100 + 100)[0]

                # Check if all surrounding lines are clicked
                if right_line not in self.lines and bottom_line not in self.lines and bottom_right_line not in self.lines and right_bottom_line not in self.lines:
                    print(f"Box [{r},{c}] is complete")
                    self.completed_coords.append((r, c))
                    self.player_scores[self.turn - 1] += 1


    def check_box_completion_for_minMax(self, lines):
        # Iterate over each box
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.completed_coords:
                    continue
                # Check the right line of the box
                right_line = self.canvas.find_closest((c + 1) * 100, r * 100 + 50)[0]
                # Check the bottom line of the box
                bottom_line = self.canvas.find_closest(c * 100 + 50, (r + 1) * 100)[0]
                # Check the right line of the box below
                bottom_right_line = self.canvas.find_closest((c + 1) * 100, (r + 1) * 100 + 50)[0]
                # Check the bottom line of the box to the right
                right_bottom_line = self.canvas.find_closest(c * 100 + 100, r * 100 + 100)[0]

                # Check if all surrounding lines are clicked
                if right_line not in lines and bottom_line not in lines and bottom_right_line not in lines and right_bottom_line not in lines:
                    print(f"Box [{r},{c}] is complete")
                    self.completed_coords.append((r, c))
                    self.player_scores[self.turn - 1] += 1


    def evaluate_move(self, line):
        # Simulate the effect of the move and evaluate the resulting game state
        self.canvas.itemconfig(line, fill="red")
        lines_left = self.lines.copy()
        lines_left.remove(line)
        col = (self.canvas.coords(line)[0] - 50) // 100
        row = (self.canvas.coords(line)[1] - 50) // 100

        # Store the previous state of completed boxes and scores
        prev_completed_coords = self.completed_coords.copy()
        prev_player_scores = self.player_scores.copy()

        self.check_box_completion_for_minMax(lines=lines_left)
        score_change = self.player_scores[1] - prev_player_scores[1]
        self.canvas.itemconfig(line, fill="gray")
        self.completed_coords = prev_completed_coords
        self.player_scores = prev_player_scores
        return score_change

    def minimax(self, depth, is_maximizing):
        if depth == 0 or not self.lines:
            return 0  # Base case: return the score

        if is_maximizing:
            best_score = float("-inf")
            for line in self.lines:
                score = self.evaluate_move(line)
                best_score = max(best_score, score + self.minimax(depth - 1, False))
                # Undo the move before evaluating the next one
                self.undo_last_move()
            return best_score
        else:
            best_score = float("inf")
            for line in self.lines:
                score = self.evaluate_move(line)
                best_score = min(best_score, score + self.minimax(depth - 1, True))
                # Undo the move before evaluating the next one
                self.undo_last_move()
            return best_score

    def undo_last_move(self):
        # Undo the last move by restoring the previous state
        self.canvas.itemconfig(self.lines[-1], fill="gray")
        if(len(self.completed_coords)>0):
            self.completed_coords.pop()
            self.player_scores[1] -= 1  # Adjust the score accordingly

    def computer_move(self):
        if self.turn == 2:
            best_score = float("-inf")
            best_line = None
            for line in self.lines:
                score = self.evaluate_move(line) + self.minimax(1, True)
                if score > best_score:
                    best_score = score
                    best_line = line

            # Make the best move
            self.canvas.itemconfig(best_line, fill="red")
            self.lines.remove(best_line)
            col = (self.canvas.coords(best_line)[0] - 50) // 100
            row = (self.canvas.coords(best_line)[1] - 50) // 100
            print(f"Computer selected line: Row {row}, Column {col}")
            self.check_box_completion()
            self.update_info()
            if not self.lines:
                self.game_over()
            elif self.turn == 2:
                self.switch_turn()


    def game_over(self):
        # Determine the winner
        winner = "Player 1" if self.player_scores[0] > self.player_scores[1] else "Computer" if self.player_scores[1] > self.player_scores[0] else "It's a tie"
        # Display game over message
        messagebox.showinfo("Game Over", f"The game is over!\n{winner} wins!")

root = tk.Tk()
root.title("Dots and Boxes")

game = DotsAndBoxes(root)

game.canvas.bind("<Button-1>", game.on_click_line)

root.mainloop()

