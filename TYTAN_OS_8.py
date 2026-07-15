import tkinter as tk
from tkinter import colorchooser, messagebox, simpledialog, filedialog
import time
import os
import random


# Kod z TYTAN OS
class MiniWindows:
    def __init__(self, root):
        self.root = root
        self.root.title("Tytan OS")
        self.root.geometry("800x600")

        self.color = "#FFFFFF"
        self.lock_screen_color = "#FFFFFF"
        self.windows = []
        self.logged_in = False
        self.pen_size = 5
        self.eraser_size = 20
        self.password = "tytan"

        self.show_loading_screen()

    def show_loading_screen(self):
        self.loading_screen = tk.Frame(self.root, bg="black")
        self.loading_screen.pack(fill=tk.BOTH, expand=True)

        self.loading_label = tk.Label(self.loading_screen, text="Ładowanie... 0%", fg="white", bg="black", font=("Arial", 24))
        self.loading_label.pack(expand=True)

        self.progress = 0
        self.update_loading_screen()

    def update_loading_screen(self):
        self.progress += 1
        self.loading_label.config(text=f"Ładowanie... {self.progress * 2}%")
        if self.progress < 50:
            self.root.after(140, self.update_loading_screen)
        else:
            self.hide_loading_screen()
            self.show_login_screen()

    def hide_loading_screen(self):
        self.loading_screen.pack_forget()

    def show_login_screen(self):
        self.login_screen = tk.Frame(self.root, bg="black")
        self.login_screen.pack(fill=tk.BOTH, expand=True)

        login_label = tk.Label(self.login_screen, text="Logowanie", fg="white", bg="black", font=("Arial", 24))
        login_label.pack(pady=20)

        user_label = tk.Label(self.login_screen, text="Użytkownik: tytan", fg="white", bg="black", font=("Arial", 14))
        user_label.pack(pady=5)

        self.password_entry = tk.Entry(self.login_screen, show='*', font=("Arial", 14))
        self.password_entry.pack(pady=10)
        self.password_entry.bind('<Return>', lambda event: self.login())

        login_button = tk.Button(self.login_screen, text="Zaloguj", command=self.login, font=("Arial", 14))
        login_button.pack(pady=20)

    def login(self):
        password = self.password_entry.get()
        if password == self.password:
            self.logged_in = True
            self.login_screen.pack_forget()
            self.create_taskbar()
            self.create_desktop()
            self.update_clock()
        else:
            messagebox.showerror("Błąd", "Niepoprawne hasło!")

    def create_taskbar(self):
        taskbar = tk.Frame(self.root, bg="gray", height=40)
        taskbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.clock_label = tk.Label(taskbar, text="", bg="gray", fg="white")
        self.clock_label.pack(side=tk.RIGHT, padx=10)

        self.taskbar_frame = tk.Frame(taskbar, bg="gray")
        self.taskbar_frame.pack(side=tk.LEFT, padx=10)

        # Menu button on taskbar
        menu_button = tk.Button(self.taskbar_frame, text="Menu", command=self.show_start_menu)
        menu_button.pack(side=tk.LEFT, padx=5)

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def create_desktop(self):
        self.desktop_frame = tk.Frame(self.root, bg=self.color)
        self.desktop_frame.pack(fill=tk.BOTH, expand=True)

        # Add draggable icons to the desktop
        self.create_draggable_icon("Notatnik", self.open_notepad, 50, 50)
        self.create_draggable_icon("Ustawienia", self.open_settings, 200, 50)
        self.create_draggable_icon("Zegar", self.open_clock, 350, 50)
        self.create_draggable_icon("Kalkulator", self.open_calculator, 500, 50)
        self.create_draggable_icon("Paint", self.open_paint, 650, 50)
        self.create_draggable_icon("Zarządca plików", self.open_file_manager, 800, 50)
        self.create_draggable_icon("Geometry Dash", self.start_geometry_dash, 50, 150)

    def create_draggable_icon(self, text, command, x, y):
        icon = tk.Button(self.desktop_frame, text=text)
        icon.place(x=x, y=y)
        icon.bind("<Button-1>", self.start_drag)
        icon.bind("<B1-Motion>", self.drag)
        icon.bind("<Double-1>", lambda event: command())

    def start_drag(self, event):
        widget = event.widget
        widget._drag_data = {"x": event.x, "y": event.y}

    def drag(self, event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_data["x"] + event.x
        y = widget.winfo_y() - widget._drag_data["y"] + event.y
        widget.place(x=x, y=y)

    def show_start_menu(self):
        start_menu = tk.Toplevel(self.root)
        start_menu.title("Menu Start")
        start_menu.geometry("250x400+10+350")
        start_menu.config(bg="gray")
        
        menu_frame = tk.Frame(start_menu, bg="gray")
        menu_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(menu_frame, text="Programy", bg="gray", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(menu_frame, text="Notatnik", command=self.open_notepad).pack(fill=tk.X, pady=2)
        tk.Button(menu_frame, text="Kalkulator", command=self.open_calculator).pack(fill=tk.X, pady=2)
        tk.Button(menu_frame, text="Zegar", command=self.open_clock).pack(fill=tk.X, pady=2)
        tk.Button(menu_frame, text="Paint", command=self.open_paint).pack(fill=tk.X, pady=2)
        tk.Button(menu_frame, text="Zarządca plików", command=self.open_file_manager).pack(fill=tk.X, pady=2)
        
        tk.Label(menu_frame, text="System", bg="gray", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(menu_frame, text="Ustawienia", command=self.open_settings).pack(fill=tk.X, pady=2)
        tk.Button(menu_frame, text="Wyloguj", command=self.logout).pack(fill=tk.X, pady=2)
        tk.Button(menu_frame, text="Uruchom ponownie", command=self.restart).pack(fill=tk.X, pady=2)
        tk.Button(menu_frame, text="Wyłącz", command=self.shutdown).pack(fill=tk.X, pady=2)
        
        tk.Button(menu_frame, text="Zamknij", command=start_menu.destroy).pack(pady=10)

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Ustawienia")
        settings_window.geometry("300x400+10+100")

        tk.Label(settings_window, text="Ustawienia", font=("Arial", 16)).pack(pady=10)

        tk.Button(settings_window, text="Zmień kolor tapety", command=self.change_wallpaper_color).pack(fill=tk.X, pady=5)
        tk.Button(settings_window, text="Zmień kolor tapety logowania", command=self.change_login_screen_color).pack(fill=tk.X, pady=5)
        tk.Button(settings_window, text="Zmiana motywu", command=self.change_theme).pack(fill=tk.X, pady=5)
        tk.Button(settings_window, text="Informacje o sprzęcie", command=self.show_system_info).pack(fill=tk.X, pady=5)
        tk.Button(settings_window, text="Zamknij", command=settings_window.destroy).pack(pady=10)

    def change_wallpaper_color(self):
        color_code = colorchooser.askcolor(title="Wybierz kolor tapety")
        if color_code and color_code[1] != "#000000":
            self.color = color_code[1]
            self.desktop_frame.config(bg=self.color)
            messagebox.showinfo("Informacja", f"Kolor tapety został zmieniony na {self.color}")

    def change_login_screen_color(self):
        color_code = colorchooser.askcolor(title="Wybierz kolor tapety logowania")
        if color_code and color_code[1] != "#000000":
            self.lock_screen_color = color_code[1]
            messagebox.showinfo("Informacja", f"Kolor tapety logowania został zmieniony na {self.lock_screen_color}")

    def change_theme(self):
        theme = simpledialog.askstring("Wybierz motyw", "Wybierz motyw (ciemny/jasny):")
        if theme.lower() in ["ciemny", "jasny"]:
            if theme.lower() == "ciemny":
                self.root.config(bg="black")
                self.desktop_frame.config(bg="black")
            else:
                self.root.config(bg="white")
                self.desktop_frame.config(bg="white")
            messagebox.showinfo("Informacja", f"Motyw został zmieniony na {theme}")
        else:
            messagebox.showerror("Błąd", "Niepoprawny motyw!")

    def show_system_info(self):
        system_info = f"System: Tytan OS\nWersja: 1.0\nProcesor: {os.cpu_count()} rdzeni\nPamięć: {self.get_memory_info()}"
        messagebox.showinfo("Informacje o systemie", system_info)

    def get_memory_info(self):
        # Placeholder for memory info function
        return "8GB"

    def logout(self):
        if messagebox.askokcancel("Wyloguj", "Czy na pewno chcesz się wylogować?"):
            self.logged_in = False
            self.desktop_frame.pack_forget()
            self.taskbar_frame.pack_forget()
            self.show_login_screen()

    def restart(self):
        if messagebox.askokcancel("Uruchom ponownie", "Czy na pewno chcesz uruchomić ponownie?"):
            self.logged_in = False
            self.desktop_frame.pack_forget()
            self.taskbar_frame.pack_forget()
            self.show_loading_screen()

    def shutdown(self):
        if messagebox.askokcancel("Wyłącz", "Czy na pewno chcesz wyłączyć?"):
            self.root.destroy()

    def open_notepad(self):
        notepad = tk.Toplevel(self.root)
        notepad.title("Notatnik")
        notepad.geometry("600x400")

        text_area = tk.Text(notepad)
        text_area.pack(fill=tk.BOTH, expand=True)

        menu_bar = tk.Menu(notepad)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Nowy", command=lambda: text_area.delete(1.0, tk.END))
        file_menu.add_command(label="Otwórz", command=lambda: self.open_file(text_area))
        file_menu.add_command(label="Zapisz", command=lambda: self.save_file(text_area))
        file_menu.add_command(label="Zamknij", command=notepad.destroy)
        menu_bar.add_cascade(label="Plik", menu=file_menu)

        notepad.config(menu=menu_bar)

    def open_file(self, text_area):
        file_path = filedialog.askopenfilename(filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, file.read())

    def save_file(self, text_area):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(text_area.get(1.0, tk.END))

    def open_calculator(self):
        calc = tk.Toplevel(self.root)
        calc.title("Kalkulator")
        calc.geometry("300x400")

        self.calc_entry = tk.Entry(calc, width=16, font=("Arial", 24), bd=10, insertwidth=4, bg="powder blue", justify="right")
        self.calc_entry.grid(row=0, column=0, columnspan=4)

        button_texts = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        buttons = []
        for text in button_texts:
            button = tk.Button(calc, padx=16, pady=16, bd=8, fg="black", font=("Arial", 20, 'bold'), text=text, command=lambda t=text: self.on_calc_button_click(t))
            buttons.append(button)

        row = 1
        col = 0
        for button in buttons:
            button.grid(row=row, column=col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def on_calc_button_click(self, char):
        if char == 'C':
            self.calc_entry.delete(0, tk.END)
        elif char == '=':
            try:
                result = str(eval(self.calc_entry.get()))
                self.calc_entry.delete(0, tk.END)
                self.calc_entry.insert(0, result)
            except:
                self.calc_entry.delete(0, tk.END)
                self.calc_entry.insert(0, "Error")
        else:
            self.calc_entry.insert(tk.END, char)

    def open_clock(self):
        clock_window = tk.Toplevel(self.root)
        clock_window.title("Zegar")
        clock_window.geometry("200x100")

        self.clock_label = tk.Label(clock_window, text="", font=("Arial", 24))
        self.clock_label.pack(expand=True)

        self.update_clock_label(clock_window)

    def update_clock_label(self, window):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        if window.winfo_exists():
            window.after(1000, self.update_clock_label, window)

    def open_file_manager(self):
        file_manager = tk.Toplevel(self.root)
        file_manager.title("Zarządca plików")
        file_manager.geometry("600x400")

        self.file_list = tk.Listbox(file_manager)
        self.file_list.pack(fill=tk.BOTH, expand=True)
        self.update_file_list(".")
        self.file_list.bind("<Double-1>", self.open_selected_file)

    def update_file_list(self, directory):
        self.file_list.delete(0, tk.END)
        for file_name in os.listdir(directory):
            self.file_list.insert(tk.END, file_name)

    def open_selected_file(self, event):
        selection = self.file_list.curselection()
        if selection:
            file_name = self.file_list.get(selection[0])
            if os.path.isfile(file_name):
                os.startfile(file_name)
            elif os.path.isdir(file_name):
                self.update_file_list(file_name)

    def open_paint(self):
        paint = tk.Toplevel(self.root)
        paint.title("Paint")
        paint.geometry("800x600")

        self.canvas = tk.Canvas(paint, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.old_x = None
        self.old_y = None
        self.pen_color = "black"
        self.eraser_on = False

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        menu_bar = tk.Menu(paint)
        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="Kolor pędzla", command=self.choose_color)
        tools_menu.add_command(label="Gumka", command=self.use_eraser)
        tools_menu.add_command(label="Zapisz", command=self.save_drawing)
        tools_menu.add_command(label="Wyczyść", command=self.clear_canvas)
        menu_bar.add_cascade(label="Narzędzia", menu=tools_menu)

        paint.config(menu=menu_bar)

    def choose_color(self):
        self.pen_color = colorchooser.askcolor()[1]
        self.eraser_on = False

    def use_eraser(self):
        self.eraser_on = True

    def save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Pliki PNG", "*.png"), ("Wszystkie pliki", "*.*")])
        if file_path:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            self.canvas.postscript(file=file_path + ".eps")
            from PIL import Image
            img = Image.open(file_path + ".eps")
            img.save(file_path, "png")
            os.remove(file_path + ".eps")

    def clear_canvas(self):
        self.canvas.delete("all")

    def paint(self, event):
        self.line_width = self.eraser_size if self.eraser_on else self.pen_size
        paint_color = "white" if self.eraser_on else self.pen_color
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill=paint_color, capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def start_geometry_dash(self):
        self.root.withdraw()  # Ukrywa główne okno systemu
        geometry_dash_app(self.root)  # Uruchamia grę Geometry Dash


# Kod gry Geometry Dash
def geometry_dash_app(root):
    # Ustawienia gry
    game_root = tk.Toplevel(root)
    game_root.title("Geometry Dash - Uproszczona Wersja")
    game_root.geometry("800x600")
    game_canvas = tk.Canvas(game_root, width=800, height=600, bg="lightblue")
    game_canvas.pack()

    player = game_canvas.create_rectangle(50, 500, 100, 550, fill="cyan")
    player_y = 500
    player_dy = 0
    game_over = False
    points = 0
    points_text = game_canvas.create_text(700, 30, text=f"Punkty: {points}", font=("Arial", 18), fill="white")

    # Funkcja skoku
    def jump(event):
        nonlocal player_dy
        if player_y >= 500:
            player_dy = -20

    # Funkcja do rysowania gracza
    def move_player():
        nonlocal player_y, player_dy
        player_dy += 1
        player_y += player_dy
        if player_y > 500:
            player_y = 500
        game_canvas.coords(player, 50, player_y, 100, player_y + 50)

    # Obsługa przeszkód
    obstacles = []
    def create_obstacle():
        x = 800
        obstacle = game_canvas.create_rectangle(x, 500, x + 70, 550, fill="red")
        obstacles.append(obstacle)

    def move_obstacles():
        for obstacle in obstacles:
            x1, y1, x2, y2 = game_canvas.coords(obstacle)
            game_canvas.coords(obstacle, x1 - 5, y1, x2 - 5, y2)

    # Sprawdzenie kolizji
    def check_collision():
        nonlocal game_over
        player_bbox = game_canvas.bbox(player)
        for obstacle in obstacles:
            obstacle_bbox = game_canvas.bbox(obstacle)
            if player_bbox[2] > obstacle_bbox[0] and player_bbox[0] < obstacle_bbox[2]:
                if player_bbox[1] + 50 > 500:
                    game_over = True

    # Funkcja startowa gry
    def start_game():
        nonlocal game_over, points
        game_over = False
        points = 0
        obstacles.clear()
        create_obstacle()
        while not game_over:
            move_player()
            move_obstacles()
            check_collision()
            game_canvas.update()
            game_canvas.after(30)  # Zmniejszenie szybkości gry

        if game_over:
            game_canvas.create_text(400, 300, text="Koniec Gry!", font=("Arial", 30), fill="white")

    game_root.bind("<space>", jump)
    start_game()

# Uruchomienie systemu TYTAN OS
if __name__ == "__main__":
    root = tk.Tk()
    app = MiniWindows(root)
    root.mainloop()
