import tkinter as tk
from tkinter import font
import math


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tooltip,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class Calculadora:
    def __init__(self, master):
        self.master = master
        master.title("Calculadora Científica")

        self.modo_oscuro = True
        self.memoria = 0
        self.historial = []
        self.operaciones_deshechas = []
        self.operaciones_rehechas = []

        self.fuente_pantalla = font.Font(family="Arial", size=36, weight="bold")
        self.fuente_operacion = font.Font(family="Arial", size=24)
        self.fuente_botones = font.Font(family="Arial", size=16)

        master.configure(bg="#1E1E1E")
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=0)
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=3)
        master.grid_rowconfigure(3, weight=1)
        master.grid_rowconfigure(4, weight=1)

        master.minsize(600, 800)

        self.frame_modo = tk.Frame(master, bg="#1E1E1E")
        self.frame_modo.grid(row=0, column=0, sticky="ne", padx=10, pady=10)

        self.boton_modo = tk.Button(
            self.frame_modo,
            text="☀",
            command=self.cambiar_modo,
            bg="#1E1E1E",
            fg="#FFFFFF",
            activebackground="#1E1E1E",
            activeforeground="#FFFFFF",
            bd=0,
            font=("Arial", 20),
        )
        self.boton_modo.pack()

        self.frame_pantalla = tk.Frame(master, bg="#1E1E1E")
        self.frame_pantalla.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.frame_pantalla.grid_columnconfigure(0, weight=1)
        self.frame_pantalla.grid_rowconfigure(0, weight=1)
        self.frame_pantalla.grid_rowconfigure(1, weight=1)

        self.pantalla_operacion = tk.Entry(
            self.frame_pantalla,
            justify="right",
            font=self.fuente_operacion,
            bg="#2B2B2B",
            fg="#FFFFFF",
            bd=0,
            insertbackground="#FFFFFF",
        )
        self.pantalla_operacion.grid(row=0, column=0, sticky="nsew")

        self.pantalla_resultado = tk.Label(
            self.frame_pantalla,
            justify="right",
            font=self.fuente_pantalla,
            bg="#1E1E1E",
            fg="#FFFFFF",
            anchor="e",
            wraplength=540,
        )
        self.pantalla_resultado.grid(row=1, column=0, sticky="nsew")

        self.frame_botones = tk.Frame(master, bg="#1E1E1E")
        self.frame_botones.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

        botones = [
            ("C", 0, 0),
            ("⌫", 0, 1),
            ("(", 0, 2),
            (")", 0, 3),
            ("÷", 0, 4),
            ("sin", 1, 0),
            ("7", 1, 1),
            ("8", 1, 2),
            ("9", 1, 3),
            ("×", 1, 4),
            ("cos", 2, 0),
            ("4", 2, 1),
            ("5", 2, 2),
            ("6", 2, 3),
            ("−", 2, 4),
            ("tan", 3, 0),
            ("1", 3, 1),
            ("2", 3, 2),
            ("3", 3, 3),
            ("+", 3, 4),
            ("√", 4, 0),
            ("±", 4, 1),
            ("0", 4, 2),
            (".", 4, 3),
            ("=", 4, 4),
        ]

        for texto, fila, columna in botones:
            comando = lambda x=texto: self.click(x)
            boton = tk.Button(
                self.frame_botones,
                text=texto,
                command=comando,
                bg="#4A4A4A",
                fg="#FFFFFF",
                font=self.fuente_botones,
                bd=0,
                relief="flat",
                activebackground="#6C6C6C",
                activeforeground="#FFFFFF",
            )
            boton.grid(row=fila, column=columna, sticky="nsew", padx=2, pady=2)
            boton.bind("<Enter>", lambda e, b=boton: self.on_enter(b))
            boton.bind("<Leave>", lambda e, b=boton: self.on_leave(b))

            if texto in ["sin", "cos", "tan", "√"]:
                Tooltip(boton, text=f"Calcular {texto}")
            elif texto == "±":
                Tooltip(boton, text="Cambiar signo")

        for i in range(5):
            self.frame_botones.grid_rowconfigure(i, weight=1)
            self.frame_botones.grid_columnconfigure(i, weight=1)

        self.frame_funciones = tk.Frame(master, bg="#1E1E1E")
        self.frame_funciones.grid(row=3, column=0, sticky="nsew", padx=20, pady=20)

        funciones = [
            ("^", "Potencia"),
            ("π", "Pi"),
            ("e", "e"),
            ("log", "Logaritmo"),
            ("M+", "Sumar a memoria"),
            ("M-", "Restar de memoria"),
            ("MR", "Recuperar memoria"),
            ("MC", "Borrar memoria"),
            ("↩", "Deshacer"),
            ("↪", "Rehacer"),
        ]

        for i, (texto, tooltip) in enumerate(funciones):
            comando = lambda x=texto: self.click(x)
            boton = tk.Button(
                self.frame_funciones,
                text=texto,
                command=comando,
                bg="#4A4A4A",
                fg="#FFFFFF",
                font=self.fuente_botones,
                bd=0,
                relief="flat",
                activebackground="#6C6C6C",
                activeforeground="#FFFFFF",
            )
            boton.grid(row=i // 5, column=i % 5, sticky="nsew", padx=2, pady=2)
            boton.bind("<Enter>", lambda e, b=boton: self.on_enter(b))
            boton.bind("<Leave>", lambda e, b=boton: self.on_leave(b))
            Tooltip(boton, text=tooltip)

        for i in range(2):
            self.frame_funciones.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.frame_funciones.grid_columnconfigure(i, weight=1)

        self.frame_historial = tk.Frame(master, bg="#1E1E1E")
        self.frame_historial.grid(row=4, column=0, sticky="nsew", padx=20, pady=20)

        self.historial_texto = tk.Text(
            self.frame_historial,
            bg="#2B2B2B",
            fg="#FFFFFF",
            font=("Arial", 12),
            height=5,
            wrap=tk.WORD,
        )
        self.historial_texto.pack(fill=tk.BOTH, expand=True)

        self.operacion = ""
        self.resultado = ""

        master.bind("<Return>", lambda event: self.click("="))
        master.bind("<BackSpace>", lambda event: self.click("⌫"))
        master.bind("<Escape>", lambda event: self.click("C"))
        master.bind("<Key>", self.tecla_presionada)

        self.cambiar_modo()

    def on_enter(self, button):
        button["background"] = "#6C6C6C"

    def on_leave(self, button):
        button["background"] = "#4A4A4A" if self.modo_oscuro else "#E0E0E0"

    def click(self, key):
        if key == "=":
            self.calcular()
        elif key == "C":
            self.borrar()
        elif key == "⌫":
            self.borrar_caracter()
        elif key == "±":
            self.cambiar_signo()
        elif key in ["sin", "cos", "tan", "√", "log"]:
            self.agregar_funcion(key)
        elif key == "^":
            self.agregar_caracter("**")
        elif key == "π":
            self.agregar_caracter("π")
        elif key == "e":
            self.agregar_caracter("e")
        elif key == "M+":
            self.memoria_sumar()
        elif key == "M-":
            self.memoria_restar()
        elif key == "MR":
            self.memoria_recuperar()
        elif key == "MC":
            self.memoria_borrar()
        elif key == "↩":
            self.deshacer()
        elif key == "↪":
            self.rehacer()
        elif key == "×":
            self.agregar_caracter("*")
        elif key == "÷":
            self.agregar_caracter("/")
        elif key == "−":
            self.agregar_caracter("-")
        else:
            self.agregar_caracter(key)
        self.pantalla_operacion.delete(0, tk.END)
        self.pantalla_operacion.insert(tk.END, self.operacion)

    def calcular(self):
        try:
            operacion_evaluar = self.operacion
            operacion_evaluar = operacion_evaluar.replace("√", "math.sqrt")
            operacion_evaluar = operacion_evaluar.replace("log", "math.log10")
            operacion_evaluar = operacion_evaluar.replace("π", "math.pi")
            operacion_evaluar = operacion_evaluar.replace("e", "math.e")

            for func in ["sin", "cos", "tan"]:
                math_func = f"math.{func[0:3]}"
                operacion_evaluar = operacion_evaluar.replace(func, math_func)

            self.resultado = str(
                eval(operacion_evaluar, {"math": math, "__builtins__": None})
            )
            self.resultado = self.formatear_numero(float(self.resultado))
            self.pantalla_resultado.config(text=self.resultado)
            self.historial.append(f"{self.operacion} = {self.resultado}")
            self.actualizar_historial()
            self.operaciones_deshechas.clear()
            self.operaciones_rehechas.clear()
        except Exception as e:
            self.pantalla_resultado.config(text="Error")
            self.resultado = ""

    def borrar(self):
        self.operaciones_deshechas.append(self.operacion)
        self.operacion = ""
        self.pantalla_operacion.delete(0, tk.END)
        self.pantalla_resultado.config(text="")
        self.operaciones_rehechas.clear()

    def borrar_caracter(self):
        if self.operacion:
            self.operaciones_deshechas.append(self.operacion)
            self.operacion = self.operacion[:-1]
            self.pantalla_operacion.delete(0, tk.END)
            self.pantalla_operacion.insert(tk.END, self.operacion)
            self.actualizar_resultado()
            self.operaciones_rehechas.clear()

    def cambiar_signo(self):
        self.operaciones_deshechas.append(self.operacion)
        if self.operacion and self.operacion[0] == "-":
            self.operacion = self.operacion[1:]
        elif self.operacion:
            self.operacion = "-" + self.operacion
        self.pantalla_operacion.delete(0, tk.END)
        self.pantalla_operacion.insert(tk.END, self.operacion)
        self.actualizar_resultado()
        self.operaciones_rehechas.clear()

    def agregar_caracter(self, caracter):
        self.operaciones_deshechas.append(self.operacion)
        self.operacion += str(caracter)
        self.pantalla_operacion.delete(0, tk.END)
        self.pantalla_operacion.insert(tk.END, self.operacion)
        self.actualizar_resultado()
        self.operaciones_rehechas.clear()

    def agregar_funcion(self, funcion):
        self.operaciones_deshechas.append(self.operacion)

        if funcion == "√":
            self.operacion += "√("
            cursor_pos = len(self.operacion)
        elif funcion == "log":
            self.operacion += "log("
            cursor_pos = len(self.operacion)
        elif funcion in ["sin", "cos", "tan"]:
            self.operacion += f"{funcion}("
            cursor_pos = len(self.operacion)

        self.operacion += ")"
        self.pantalla_operacion.delete(0, tk.END)
        self.pantalla_operacion.insert(tk.END, self.operacion)
        self.pantalla_operacion.icursor(cursor_pos)
        self.operaciones_rehechas.clear()

    def memoria_sumar(self):
        if self.resultado:
            self.memoria += float(self.resultado)

    def memoria_restar(self):
        if self.resultado:
            self.memoria -= float(self.resultado)

    def memoria_recuperar(self):
        self.operaciones_deshechas.append(self.operacion)
        self.operacion = str(self.memoria)
        self.pantalla_operacion.delete(0, tk.END)
        self.pantalla_operacion.insert(tk.END, self.operacion)
        self.actualizar_resultado()
        self.operaciones_rehechas.clear()

    def memoria_borrar(self):
        self.memoria = 0

    def actualizar_resultado(self):
        try:
            if self.operacion:
                operacion_evaluar = self.operacion
                operacion_evaluar = operacion_evaluar.replace("√", "math.sqrt")
                operacion_evaluar = operacion_evaluar.replace("log", "math.log10")
                operacion_evaluar = operacion_evaluar.replace("π", "math.pi")
                operacion_evaluar = operacion_evaluar.replace("e", "math.e")

                for func in ["sin", "cos", "tan"]:
                    math_func = f"math.{func[0:3]}"
                    operacion_evaluar = operacion_evaluar.replace(func, math_func)

                self.resultado = str(
                    eval(operacion_evaluar, {"math": math, "__builtins__": None})
                )
                self.resultado = self.formatear_numero(float(self.resultado))
                self.pantalla_resultado.config(text=self.resultado)
            else:
                self.pantalla_resultado.config(text="")
        except:
            self.pantalla_resultado.config(text="")

    def find_matching_paren(self, string, start):
        count = 0
        for i in range(start, len(string)):
            if string[i] == "(":
                count += 1
            elif string[i] == ")":
                count -= 1
                if count == 0:
                    return i
        return -1

    def tecla_presionada(self, event):
        if event.char.isdigit() or event.char in [
            "+",
            "-",
            "*",
            "/",
            ".",
            "%",
            "(",
            ")",
        ]:
            self.click(event.char)
        elif event.char == "^":
            self.click("^")
        elif event.char.lower() == "p":
            self.click("π")
        elif event.char.lower() == "e":
            self.click("e")

    def cambiar_modo(self):
        self.modo_oscuro = not self.modo_oscuro
        if self.modo_oscuro:
            bg_color = "#1E1E1E"
            fg_color = "#FFFFFF"
            btn_bg = "#4A4A4A"
            pantalla_bg = "#2B2B2B"
            self.boton_modo.config(text="☀")
        else:
            bg_color = "#F0F0F0"
            fg_color = "#000000"
            btn_bg = "#E0E0E0"
            pantalla_bg = "#FFFFFF"
            self.boton_modo.config(text="☾")

        self.master.configure(bg=bg_color)
        self.frame_pantalla.configure(bg=bg_color)
        self.frame_botones.configure(bg=bg_color)
        self.frame_funciones.configure(bg=bg_color)
        self.frame_historial.configure(bg=bg_color)
        self.pantalla_operacion.configure(bg=pantalla_bg, fg=fg_color)
        self.pantalla_resultado.configure(bg=bg_color, fg=fg_color)
        self.historial_texto.configure(bg=pantalla_bg, fg=fg_color)
        self.boton_modo.configure(
            bg=bg_color,
            fg=fg_color,
            activebackground=bg_color,
            activeforeground=fg_color,
        )

        for frame in [self.frame_botones, self.frame_funciones]:
            for widget in frame.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg=btn_bg, fg=fg_color)

    def formatear_numero(self, numero):
        if numero.is_integer():
            return f"{numero:,.0f}".replace(",", " ")
        else:
            return f"{numero:,.6f}".replace(",", " ").rstrip("0").rstrip(".")

    def deshacer(self):
        if self.operaciones_deshechas:
            operacion_actual = self.operacion
            self.operacion = self.operaciones_deshechas.pop()
            self.operaciones_rehechas.append(operacion_actual)
            self.pantalla_operacion.delete(0, tk.END)
            self.pantalla_operacion.insert(tk.END, self.operacion)
            self.actualizar_resultado()

    def rehacer(self):
        if self.operaciones_rehechas:
            operacion_actual = self.operacion
            self.operacion = self.operaciones_rehechas.pop()
            self.operaciones_deshechas.append(operacion_actual)
            self.pantalla_operacion.delete(0, tk.END)
            self.pantalla_operacion.insert(tk.END, self.operacion)
            self.actualizar_resultado()

    def actualizar_historial(self):
        self.historial_texto.delete(1.0, tk.END)
        for calculo in self.historial[-5:]:
            self.historial_texto.insert(tk.END, calculo + "\n")
        self.historial_texto.see(tk.END)


root = tk.Tk()
calculadora = Calculadora(root)
root.mainloop()
