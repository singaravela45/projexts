import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class TextEditorApp:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        master.title("Simple Python Text Editor")

        # Stores the path of the current open file (None if new file)
        self.current_file = None

        # State Variables for Settings
        self.is_word_wrap = True
        self.theme_var = tk.StringVar(value="light") # 'light' or 'dark'
        self.wrap_var = tk.BooleanVar(value=self.is_word_wrap)

        # 1. Create a ScrolledText widget for the main editing area
        # Initial wrap setting is determined by self.is_word_wrap
        self.text_area = scrolledtext.ScrolledText(
            master, 
            wrap=tk.WORD if self.is_word_wrap else tk.NONE, # Conditional wrapping
            undo=True,     # Enable undo/redo
            padx=10, 
            pady=10,
            font=("Consolas", 12)
        )
        self.text_area.pack(expand=True, fill='both')
        
        # Apply initial theme configuration
        self._apply_theme("light")

        # 2. Setup the Menu Bar
        self.setup_menu()

    def setup_menu(self):
        # Create the main menu bar
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        # --- File Menu ---
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)

        # --- Settings Menu (NEW) ---
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # Theme Sub-menu (Radio Buttons)
        theme_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="Theme", menu=theme_menu)
        
        theme_menu.add_radiobutton(
            label="Light Theme", 
            variable=self.theme_var, 
            value="light", 
            command=lambda: self._apply_theme("light")
        )
        theme_menu.add_radiobutton(
            label="Dark Theme", 
            variable=self.theme_var, 
            value="dark", 
            command=lambda: self._apply_theme("dark")
        )

        settings_menu.add_separator()

        # Word Wrap Toggle (Check Button)
        settings_menu.add_checkbutton(
            label="Word Wrap", 
            variable=self.wrap_var, 
            command=self.toggle_word_wrap
        )
        
    # --- Theme & Wrap Logic ---

    def _apply_theme(self, theme_name):
        """Applies the selected color theme to the text area."""
        if theme_name == "dark":
            # Dark theme colors
            bg_color = "#2e2e2e" # Background
            fg_color = "#ffffff" # Foreground (text color)
            select_bg = "#555555"
        else:
            # Light theme colors
            bg_color = "#ffffff" # Background
            fg_color = "#000000" # Foreground (text color)
            select_bg = "#b3d8ff"

        self.text_area.config(
            bg=bg_color, 
            fg=fg_color, 
            insertbackground=fg_color, # Color of the text cursor (blinking line)
            selectbackground=select_bg
        )

    def toggle_word_wrap(self):
        """Toggles word wrapping on and off."""
        # The wrap_var state is automatically managed by the Checkbutton in the menu.
        self.is_word_wrap = self.wrap_var.get()
        wrap_mode = tk.WORD if self.is_word_wrap else tk.NONE
        self.text_area.config(wrap=wrap_mode)

    # --- File Handling (Methods below remain the same) ---

    def new_file(self):
        """Resets the text area and prepares for a new file."""
        self.text_area.delete(1.0, tk.END) # Clear all text (from line 1, character 0 to END)
        self.current_file = None
        self.master.title("Simple Python Text Editor")

    def open_file(self):
        """Opens a file and loads its content into the text area."""
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                self.current_file = file_path
                self.master.title(f"Simple Python Text Editor - {file_path.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file: {e}")

    def save_file(self):
        """Saves the current content to the current file path. Prompts for Save As if no file is open."""
        if self.current_file:
            self._write_to_file(self.current_file)
        else:
            self.save_as_file()

    def save_as_file(self):
        """Prompts the user for a file name and path to save the content."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")]
        )
        
        if file_path:
            self._write_to_file(file_path)
            self.current_file = file_path
            self.master.title(f"Simple Python Text Editor - {file_path.split('/')[-1]}")

    def _write_to_file(self, file_path):
        """Internal function to handle the writing process."""
        try:
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("Success", f"File saved successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

    def exit_app(self):
        """Closes the application."""
        # Note: A real editor would check for unsaved changes here.
        self.master.quit()

# Main execution block
if __name__ == "__main__":
    root = tk.Tk()
    # Handle the window close event (optional, but good practice)
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit()) 
    app = TextEditorApp(root)
    root.mainloop()