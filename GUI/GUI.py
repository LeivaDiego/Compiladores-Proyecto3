import tkinter as tk  
from tkinter import scrolledtext, Menu, PanedWindow, Frame, filedialog, ttk, messagebox  
import os
import subprocess  
from PIL import Image, ImageTk  

# Crear la ventana principal
root = tk.Tk()  
root.title("Compilador (Construcción de Compiladores CC3032) - Editor de Código")  
root.geometry("1000x600") 

# Variable global para almacenar la ruta del archivo abierto
current_file_path = None

# Definir colores para los temas
dark_gray = "#2E2E2E"  # Color gris oscuro para el tema oscuro
light_gray = "#F0F0F0"  # Color gris claro para el tema claro
light_text_color = "black"
dark_text_color = "white"

# Configuración de estilos para Treeview
style = ttk.Style()
style.theme_use("default")

# Función para cambiar el tema
def set_theme(theme):
    if theme == "claro":
        root.config(bg="white")
        code_editor.config(bg="white", fg=light_text_color, insertbackground=light_text_color)
        terminal_frame.config(bg="white")
        run_button.config(bg="lightgray", fg=light_text_color)
        save_button.config(bg="lightgray", fg=light_text_color)
        
        # Cambiar estilo del Treeview
        style.configure("Treeview", background="white", foreground=light_text_color, fieldbackground="white")
        style.map('Treeview', background=[('selected', 'lightblue')])
    elif theme == "oscuro":
        root.config(bg=dark_gray)
        code_editor.config(bg=dark_gray, fg=dark_text_color, insertbackground=dark_text_color)
        terminal_frame.config(bg=dark_gray)
        run_button.config(bg=dark_gray, fg=dark_text_color)
        save_button.config(bg=dark_gray, fg=dark_text_color)
        
        # Cambiar estilo del Treeview
        style.configure("Treeview", background=dark_gray, foreground=dark_text_color, fieldbackground=dark_gray)
        style.map('Treeview', background=[('selected', 'darkblue')])

# Función para ejecutar el código cuando se presiona el botón "Compilar"
def run_code():
    code = code_editor.get("1.0", tk.END)  # Obtenemos todo el contenido del editor de código.
    
    # Guardar el código en un archivo temporal
    with open("temp_code.py", "w") as f:
        f.write(code)  # Escribimos el código en un archivo temporal llamado 'temp_code.py'.
    
    # Ejecutar el archivo y capturar la salida
    process = subprocess.Popen(
        ["python", "temp_code.py"],  # Ejecutamos el archivo temporal usando Python.
        stdout=subprocess.PIPE,  
        stderr=subprocess.PIPE,  
        text=True  
    )
    output, error = process.communicate()  # Obtenemos la salida y el error de la ejecución.
    
    # Mostrar la salida en la "terminal" de la GUI
    terminal_output.config(state=tk.NORMAL)  
    terminal_output.delete("1.0", tk.END)  
    terminal_output.insert(tk.END, output + error)  
    terminal_output.config(state=tk.DISABLED)  

# Función para guardar el contenido del editor de código en el archivo actual
def save_file():
    global current_file_path
    if current_file_path:
        try:
            with open(current_file_path, 'w', encoding='utf-8') as file:
                code = code_editor.get("1.0", tk.END)
                file.write(code)
                messagebox.showinfo("Guardar", f"Archivo guardado exitosamente: {os.path.basename(current_file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
    else:
        messagebox.showerror("Error", "No hay ningún archivo abierto para guardar.")

# Función para abrir un archivo y mostrar su contenido en el editor de código
def open_file(file_path=None):
    global current_file_path
    if not file_path:
        file_path = filedialog.askopenfilename(
            filetypes=[("Todos los archivos", "*.*")]
        )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
                code_editor.delete("1.0", tk.END)  # Borra el contenido actual del editor
                code_editor.insert(tk.END, code)  # Inserta el contenido del archivo
                current_file_path = file_path  # Guarda la ruta del archivo abierto
                root.title(f"Compilador - {os.path.basename(file_path)}")  # Actualiza el título con el nombre del archivo
        except Exception as e:
            terminal_output.config(state=tk.NORMAL)  
            terminal_output.insert(tk.END, f"Error al abrir el archivo: {e}\n")  
            terminal_output.config(state=tk.DISABLED)  

# Función para abrir una carpeta y poblar el explorador de archivos
def open_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        populate_file_explorer(folder_path, file_tree)
        root.title(f"Compilador - {os.path.basename(folder_path)}")  # Actualiza el título con el nombre de la carpeta

# Función para poblar el explorador con archivos y carpetas
def populate_file_explorer(path, tree):
    tree.delete(*tree.get_children())
    parent_node = tree.insert("", "end", text=path, open=True)
    load_tree_nodes(parent_node, path)

# Función para cargar archivos y carpetas en un nodo
def load_tree_nodes(parent_node, path):
    # Primero eliminamos el nodo "dummy" si existe
    if file_tree.get_children(parent_node):
        file_tree.delete(*file_tree.get_children(parent_node))

    for item in os.listdir(path):
        abs_path = os.path.join(path, item)
        node = file_tree.insert(parent_node, "end", text=item, open=False)
        if os.path.isdir(abs_path):
            # Añadir un nodo "dummy" para que la carpeta sea expansible
            file_tree.insert(node, "end")

# Función para manejar la expansión de un nodo (carpeta) y cargar su contenido
def on_tree_expand(event):
    node = file_tree.focus()
    abs_path = get_node_path(node)
    load_tree_nodes(node, abs_path)

# Función para obtener la ruta absoluta de un nodo en el Treeview
def get_node_path(node):
    path = []
    while node:
        path.insert(0, file_tree.item(node, 'text'))
        node = file_tree.parent(node)
    return os.path.join(*path)

# Función para manejar la selección de un archivo en el explorador
def on_file_select(event):
    selected_item = file_tree.focus()
    file_path = get_node_path(selected_item)
    
    if os.path.isfile(file_path):
        open_file(file_path)

# Crear un PanedWindow para permitir el cambio de tamaño entre el explorador, el editor de código y la consola
pane = PanedWindow(root, orient=tk.HORIZONTAL)
pane.pack(fill=tk.BOTH, expand=True)

# Crear el explorador de archivos
explorer_frame = Frame(pane)
pane.add(explorer_frame, width=200)

# Añadir un Treeview (árbol) para mostrar archivos y carpetas
file_tree = ttk.Treeview(explorer_frame)
file_tree.pack(fill=tk.BOTH, expand=True)

# Vincular la expansión del nodo con la función para cargar su contenido
file_tree.bind("<<TreeviewOpen>>", on_tree_expand)

# Vincular la selección del archivo en el explorador con la apertura del archivo
file_tree.bind("<Double-1>", on_file_select)

# Crear otro PanedWindow para el editor de código y la consola
editor_console_pane = PanedWindow(pane, orient=tk.VERTICAL)
pane.add(editor_console_pane)

# Crear el frame para los botones (arriba del editor de texto, fijo)
button_frame = Frame(editor_console_pane, height=50)
button_frame.pack_propagate(False)
editor_console_pane.add(button_frame)

# Crear contenedor para centrar los botones
button_container = Frame(button_frame)
button_container.place(relx=0.5, rely=0.5, anchor="center")

# Cargar la imagen para el botón "Compilar"
image_path = "image.png"
img = Image.open(image_path).resize((20, 20), Image.LANCZOS)
run_icon = ImageTk.PhotoImage(img)

# Crear los botones
run_button = tk.Button(button_container, text="Compilar", image=run_icon, compound="right", command=run_code)
run_button.pack(side=tk.LEFT, padx=10)

save_button = tk.Button(button_container, text="Guardar", command=save_file)
save_button.pack(side=tk.LEFT, padx=10)

# Crear el editor de texto
code_editor = scrolledtext.ScrolledText(editor_console_pane, undo=True, wrap=tk.WORD)
editor_console_pane.add(code_editor, stretch="always")

# Crear el frame para la terminal
terminal_frame = Frame(editor_console_pane)
editor_console_pane.add(terminal_frame, stretch="always")

# Crear la terminal
terminal_output = scrolledtext.ScrolledText(terminal_frame, height=10, state=tk.DISABLED, wrap=tk.WORD, bg="black", fg="white")
terminal_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Crear el menú
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Submenú Archivo
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Archivo", menu=file_menu)
file_menu.add_command(label="Abrir Archivo", command=open_file)
file_menu.add_command(label="Abrir Carpeta", command=open_folder)

# Submenú Configuraciones
config_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Configuraciones", menu=config_menu)

# Submenú de Tema
theme_menu = Menu(config_menu, tearoff=0)
config_menu.add_cascade(label="Tema", menu=theme_menu)
theme_menu.add_command(label="Claro", command=lambda: set_theme("claro"))
theme_menu.add_command(label="Oscuro", command=lambda: set_theme("oscuro"))

root.mainloop()
