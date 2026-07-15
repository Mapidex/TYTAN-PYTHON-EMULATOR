import tkinter as tk
from tkinter import colorchooser, messagebox, simpledialog, filedialog
import time
import os
import sys

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
        self.passwords = {"tytan": "tytan", "admin": "admin"}

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

        user_label = tk.Label(self.login_screen, text="Wybierz użytkownika", fg="white", bg="black", font=("Arial", 14))
        user_label.pack(pady=5)

        self.user_var = tk.StringVar(self.root)
        self.user_var.set("tytan")  # Default user
        users_menu = tk.OptionMenu(self.login_screen, self.user_var, *self.passwords.keys())
        users_menu.pack(pady=5)

        self.password_entry = tk.Entry(self.login_screen, show='*', font=("Arial", 14))
        self.password_entry.pack(pady=10)
        self.password_entry.bind('<Return>', lambda event: self.login())

        login_button = tk.Button(self.login_screen, text="Zaloguj", command=self.login, font=("Arial", 14))
        login_button.pack(pady=20)

    def login(self):
        selected_user = self.user_var.get()
        password = self.password_entry.get()
        if self.passwords.get(selected_user) == password:
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

        self.taskbar_frame = tk.Frame(taskbar, bg="gray")
        self.taskbar_frame.pack(side=tk.LEFT, padx=10)

        # Menu button on taskbar
        menu_button = tk.Button(self.taskbar_frame, text="▲", command=self.show_start_menu)
        menu_button.pack(side=tk.LEFT, padx=5)

        # Volume button
        volume_button = tk.Button(taskbar, text="🔊", command=self.show_volume_slider)
        volume_button.pack(side=tk.RIGHT, padx=5)

        self.clock_label = tk.Label(taskbar, text="", bg="gray", fg="white")
        self.clock_label.pack(side=tk.RIGHT, padx=10)

    def show_volume_slider(self):
        slider_window = tk.Toplevel(self.root)
        slider_window.title("Regulacja głośności")
        slider_window.geometry("200x100")
        volume_slider = tk.Scale(slider_window, from_=0, to=100, orient=tk.HORIZONTAL)
        volume_slider.set(50)
        volume_slider.pack(fill=tk.BOTH, expand=True)

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
        if theme.lower() == "ciemny":
            self.desktop_frame.config(bg="black")
        elif theme.lower() == "jasny":
            self.desktop_frame.config(bg="white")

    def show_system_info(self):
        info_window = tk.Toplevel(self.root)
        info_window.title("Informacje o systemie")
        info_window.geometry("300x200+10+200")

        system_info = f"""
        Procesor: {os.cpu_count()} rdzeni
        Pamięć: {round(os.getloadavg()[0], 2)} MB
        System: {sys.platform.capitalize()}
        """
        tk.Label(info_window, text="Informacje o systemie", font=("Arial", 16)).pack(pady=10)
        tk.Label(info_window, text=system_info, font=("Arial", 12)).pack(pady=10)
        tk.Button(info_window, text="Zamknij", command=info_window.destroy).pack(pady=10)

    def logout(self):
        self.logged_in = False
        self.desktop_frame.pack_forget()
        self.create_taskbar()
        self.show_login_screen()

    def restart(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def shutdown(self):
        self.root.quit()

    def open_notepad(self):
        notepad_window = tk.Toplevel(self.root)
        notepad_window.title("Notatnik")
        notepad_window.geometry("600x400")

        text_area = tk.Text(notepad_window)
        text_area.pack(fill=tk.BOTH, expand=True)

        menu_bar = tk.Menu(notepad_window)
        notepad_window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Plik", menu=file_menu)
        file_menu.add_command(label="Otwórz", command=lambda: self.open_file(text_area))
        file_menu.add_command(label="Zapisz", command=lambda: self.save_file(text_area.get("1.0", "end-1c")))
        file_menu.add_command(label="Zamknij", command=notepad_window.destroy)

    def open_file(self, text_area):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                text_area.delete("1.0", tk.END)
                text_area.insert("1.0", text)

    def open_calculator(self):
        calc_window = tk.Toplevel(self.root)
        calc_window.title("Kalkulator")
        calc_window.geometry("300x400")

        def calculate():
            try:
                result = eval(entry.get())
                result_var.set(result)
            except Exception as e:
                result_var.set("Błąd")

        entry = tk.Entry(calc_window, font=("Arial", 20))
        entry.pack(pady=10)

        result_var = tk.StringVar()
        result_var.set("0")
        result_label = tk.Label(calc_window, textvariable=result_var, font=("Arial", 20))
        result_label.pack(pady=10)

        buttons_frame = tk.Frame(calc_window)
        buttons_frame.pack()

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        for button in buttons:
            if button == '=':
                btn = tk.Button(buttons_frame, text=button, command=calculate)
            else:
                btn = tk.Button(buttons_frame, text=button, command=lambda b=button: entry.insert(tk.END, b))
            btn.grid(row=buttons.index(button) // 4, column=buttons.index(button) % 4, padx=5, pady=5)

    def open_clock(self):
        clock_window = tk.Toplevel(self.root)
        clock_window.title("Zegar")
        clock_window.geometry("300x200")
        clock_label = tk.Label(clock_window, text="", font=("Arial", 24))
        clock_label.pack(expand=True)

        def update_clock_window():
            current_time = time.strftime("%H:%M:%S")
            clock_label.config(text=current_time)
            clock_window.after(1000, update_clock_window)

        update_clock_window()

    def open_paint(self):
        paint_window = tk.Toplevel(self.root)
        paint_window.title("Paint")
        paint_window.geometry("600x400")
        canvas = tk.Canvas(paint_window, bg="white")
        canvas.pack(fill=tk.BOTH, expand=True)

        def draw(event):
            x1, y1 = (event.x - self.pen_size), (event.y - self.pen_size)
            x2, y2 = (event.x + self.pen_size), (event.y + self.pen_size)
            canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")

        def erase(event):
            x1, y1 = (event.x - self.eraser_size), (event.y - self.eraser_size)
            x2, y2 = (event.x + self.eraser_size), (event.y + self.eraser_size)
            canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")

        canvas.bind("<B1-Motion>", draw)
        canvas.bind("<B3-Motion>", erase)

        menu_bar = tk.Menu(paint_window)
        paint_window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Plik", menu=file_menu)
        file_menu.add_command(label="Zapisz", command=lambda: self.save_canvas(canvas))
        file_menu.add_command(label="Zamknij", command=paint_window.destroy)

    def save_canvas(self, canvas):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            canvas.postscript(file=file_path + ".ps")
            try:
                from PIL import Image
                img = Image.open(file_path + ".ps")
                img.save(file_path)
                os.remove(file_path + ".ps")
            except ImportError:
                messagebox.showwarning("Warning", "Pillow library is required to save as PNG.")

    def open_file_manager(self):
        file_manager_window = tk.Toplevel(self.root)
        file_manager_window.title("Zarządca plików")
        file_manager_window.geometry("600x400")

        file_listbox = tk.Listbox(file_manager_window)
        file_listbox.pack(fill=tk.BOTH, expand=True)

        current_dir = os.getcwd()
        files = os.listdir(current_dir)
        for file in files:
            file_listbox.insert(tk.END, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniWindows(root)
    root.mainloop()
