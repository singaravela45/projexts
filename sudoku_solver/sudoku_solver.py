import tkinter as tk
from tkinter import messagebox

# --- Core Sudoku Solver Logic (Copied from sudoku_solver.py) ---

def is_safe(board, row, col, num):
    """Checks if placing 'num' at board[row][col] is valid according to Sudoku rules."""
    
    # 1. Check the Row
    for x in range(9):
        if board[row][x] == num:
            return False

    # 2. Check the Column
    for x in range(9):
        if board[x][col] == num:
            return False

    # 3. Check the 3x3 Box
    start_row = row - row % 3
    start_col = col - col % 3
    
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

def solve_sudoku(board):
    """Uses the backtracking algorithm to solve the Sudoku board."""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_safe(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = 0
                return False
    return True

# --- Tkinter Application Class ---

class SudokuApp:
    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")

        # Define styles for the grid
        self.entry_style = {'width': 3, 'font': ('Arial', 16), 'justify': 'center'}
        self.fixed_style = {'bg': '#D3E0F0', 'fg': 'black'} # Light blue background for fixed numbers
        self.empty_style = {'bg': 'white', 'fg': 'blue'} # White background for solved numbers

        # Store Entry widgets in a 9x9 grid
        self.entries = []
        # self.initial_board stores the board state when 'Solve' was last pressed
        self.initial_board = self.create_empty_board() 

        # Create the main frame for the Sudoku grid
        main_frame = tk.Frame(master, padx=10, pady=10)
        main_frame.pack(pady=10)

        # Build the 9x9 grid of Entry widgets
        for r in range(9):
            row_entries = []
            for c in range(9):
                # Calculate color based on 3x3 box for visual grouping
                bg_color = "#f0f0f0" if (r // 3 + c // 3) % 2 == 0 else "#ffffff"
                
                # Create the Entry widget
                entry = tk.Entry(
                    main_frame, 
                    **self.entry_style,
                    bg=bg_color,
                    # Bind a validation function to restrict input to single digits (1-9) or empty
                    validate="key", 
                    validatecommand=(master.register(self.validate_input), '%P')
                )
                
                # Place the entry in the grid layout
                # Add extra padding for 3x3 box boundaries
                entry.grid(
                    row=r, column=c, 
                    padx=(1, 5 if c % 3 == 2 and c != 8 else 1),
                    pady=(1, 5 if r % 3 == 2 and r != 8 else 1),
                    ipady=4 # Internal padding for height
                )
                row_entries.append(entry)
            self.entries.append(row_entries)

        # --- Control Buttons ---
        button_frame = tk.Frame(master, pady=10)
        button_frame.pack()

        # Solve Button
        solve_button = tk.Button(
            button_frame, 
            text="Solve Sudoku", 
            command=self.solve, 
            font=('Arial', 14, 'bold'),
            bg='#4CAF50', # Green background
            fg='white',
            activebackground='#45a049'
        )
        solve_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)
        
        # Reset Button (NEW)
        reset_button = tk.Button(
            button_frame, 
            text="Reset to Input", 
            command=self.reset_board, 
            font=('Arial', 14),
            bg='#2196F3', # Blue background
            fg='white',
            activebackground='#0b7dda'
        )
        reset_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        # Clear Button
        clear_button = tk.Button(
            button_frame, 
            text="Clear All", 
            command=self.clear_board, 
            font=('Arial', 14),
            bg='#f44336', # Red background
            fg='white',
            activebackground='#da190b'
        )
        clear_button.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)


    # --- Utility Methods ---

    def create_empty_board(self):
        """Creates a 9x9 board of zeros."""
        return [[0 for _ in range(9)] for _ in range(9)]

    def validate_input(self, P):
        """Restricts cell input to a single digit (1-9) or an empty string."""
        if P.isdigit() and len(P) <= 1 and P != '0':
            return True
        if P == "":
            return True
        return False

    def get_board_from_entries(self):
        """
        Reads the grid inputs, validates them, and returns a 9x9 list of integers.
        Initial numbers (from the start) are marked in self.initial_board.
        """
        board = self.create_empty_board()
        # IMPORTANT: We use a temporary list to store the 'initial' input 
        # for use in the reset function later.
        current_input = self.create_empty_board() 
        
        for r in range(9):
            for c in range(9):
                value = self.entries[r][c].get().strip()
                
                if value.isdigit() and 1 <= int(value) <= 9:
                    num = int(value)
                    board[r][c] = num
                    current_input[r][c] = num # Store as input for reset
                elif value == "":
                    # Empty cell is 0
                    board[r][c] = 0
                else:
                    # Invalid input found (shouldn't happen with validate_input, but safe check)
                    raise ValueError(f"Invalid input at ({r+1}, {c+1}): '{value}'")
        
        # We update self.initial_board only when reading fresh input
        self.initial_board = current_input
        return board

    def clear_board(self):
        """Clears all entries on the board."""
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)
                # Ensure the entry is editable
                self.entries[r][c].config(self.empty_style, state=tk.NORMAL)
        # Also clear the stored initial board
        self.initial_board = self.create_empty_board()
        
    def reset_board(self):
        """Resets the board to the last input state and makes all cells editable."""
        for r in range(9):
            for c in range(9):
                entry = self.entries[r][c]
                entry.config(state=tk.NORMAL) # Ensure entry is editable
                entry.delete(0, tk.END)

                num = self.initial_board[r][c]
                if num != 0:
                    entry.insert(0, str(num))
                    entry.config(self.fixed_style)
                else:
                    entry.config(self.empty_style)
                    
    def solve(self):
        """
        Main solver method. Reads input, attempts to solve, and displays the result.
        """
        try:
            # 1. Get the current board state (which also updates self.initial_board)
            board = self.get_board_from_entries()
            
            # Create a deep copy of the board for the solver, 
            # as the solver modifies the board in place
            board_to_solve = [row[:] for row in board] 

            # 2. Run the Solver
            if solve_sudoku(board_to_solve):
                # 3. Display the solution
                for r in range(9):
                    for c in range(9):
                        num = board_to_solve[r][c]
                        entry = self.entries[r][c]

                        # Clear current content and insert the solved number
                        entry.delete(0, tk.END)
                        entry.insert(0, str(num))
                        
                        # Apply styling based on whether it was an initial number
                        if self.initial_board[r][c] != 0:
                            entry.config(self.fixed_style)
                        else:
                            entry.config(self.empty_style)
                        
                        # Make all entries read-only after solving
                        entry.config(state=tk.DISABLED)

            else:
                messagebox.showerror("Error", "No valid solution exists for the given puzzle.")

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("An unexpected error occurred", str(e))

# Main execution block
if __name__ == "__main__":
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit()) 
    app = SudokuApp(root)
    root.mainloop()