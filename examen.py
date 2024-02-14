import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import ply.lex as lex

class AnalizadorLexico:
    palabras_reservadas = {
        'for': 'FOR', 'do': 'DO', 'while': 'WHILE',
        'if': 'IF', 'else': 'ELSE', 'switch': 'SWITCH',
        'case': 'CASE', 'break': 'BREAK', 'return': 'RETURN',
        'static': 'STATIC', 'print': 'PRINT', 'int': 'INT',
        'float': 'FLOAT', 'void': 'VOID', 'public': 'PUBLIC',
        'private': 'PRIVATE',
        'area': 'Palabra_R', 'base': 'Palabra_R', 'altura': 'Palabra_R',
    }

    tokens = [
        'IDENTIFICADOR', 'NUMERO', 'CADENA',
        'OPERADOR', 'SIMBOLO', 'FIN',  
    ] + list(palabras_reservadas.values())

    t_OPERADOR = r'[\+\*-/=]'
    t_SIMBOLO = r'[\(\)\[\]\{\};,]'
    t_ignore = ' \t'

    def t_NUMERO(self, t):
        r'\d*\.\d+|\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print("Float value too large %d", t.value)
            t.value = 0
        if t.value.is_integer():
            t.value = int(t.value)
        return t

    def t_IDENTIFICADOR(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.palabras_reservadas.get(t.value.lower(), 'IDENTIFICADOR') 
        return t

    def t_CADENA(self, t):
        r'\".*?\"'
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.build()
        self.lexer.input(data)
        return list(self.lexer)

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Léxico")
        self.geometry("800x600")

        self.inicializar_interfaz()

    def inicializar_interfaz(self):
        estilo = ttk.Style()
        estilo.configure('TFrame', background='#8E44AD')  # Color morado de fondo

        self.configure(bg='#8E44AD')  # Cambiar el color de fondo del Tkinter

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame_izquierda = ttk.Frame(self, style='TFrame')  # Aplicar estilo
        self.frame_izquierda.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.entrada_codigo = ScrolledText(self.frame_izquierda, width=40, height=10, wrap=tk.WORD, font=("Arial", 12), background='#ECF0F1')  # Fondo gris claro
        self.entrada_codigo.pack(fill="both", expand=True)

        self.boton_analizar = tk.Button(self.frame_izquierda, text="Analizar Código", command=self.analizar_codigo, font=("Arial", 14))
        self.boton_analizar.pack(pady=10)

        self.frame_derecha = ttk.Frame(self, style='TFrame')  # Aplicar estilo
        self.frame_derecha.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.result_tree = ttk.Treeview(self.frame_derecha, columns=("Token", "Palabra Reservada", "Identificador", "Operador", "Número", "Símbolo"), show="headings", style='Treeview')
        self.result_tree.heading("Token", text="Token")
        self.result_tree.heading("Palabra Reservada", text="Palabra Reservada")
        self.result_tree.heading("Identificador", text="Identificador")
        self.result_tree.heading("Operador", text="Operador")
        self.result_tree.heading("Número", text="Número")
        self.result_tree.heading("Símbolo", text="Símbolo")

        for col in ("Token", "Palabra Reservada", "Identificador", "Operador", "Número", "Símbolo"):
            self.result_tree.column(col, width=120, anchor="center")

        self.result_tree.pack(fill="both", expand=True)

    def analizar_codigo(self):
        codigo = self.entrada_codigo.get("1.0", "end-1c")
        analizador_lexico = AnalizadorLexico()
        tokens = analizador_lexico.test(codigo)

        self.result_tree.delete(*self.result_tree.get_children())

        for tok in tokens:
            palabra_reservada = 'x' if tok.type in AnalizadorLexico.palabras_reservadas.values() else ''
            identificador = 'x' if tok.type == 'IDENTIFICADOR' else ''
            operador = 'x' if tok.type == 'OPERADOR' else ''
            numero = 'x' if tok.type == 'NUMERO' else ''
            simbolo = 'x' if tok.type == 'SIMBOLO' else ''

            self.result_tree.insert("", 'end', values=(tok.value, palabra_reservada, identificador, operador, numero, simbolo))

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
