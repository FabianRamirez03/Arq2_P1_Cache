import tkinter as tk
from tkinter import scrolledtext

# Main widget settings
main = tk.Tk(className="Arquitectura de Computadores 2. Proyecto I")
main.geometry("900x500")
main.resizable(False, False)

# Framing

main_frame = tk.Frame(main, bg="white", height=500, width=900)
main_frame.place(x=0, y=0)

cpus_frame = tk.Frame(main_frame, bg="grey", height=300, width=900)
cpus_frame.place(x=0, y=0)

cpu0_frame = tk.Frame(cpus_frame, bg="red", height=300, width=225)
cpu0_frame.place(x=0, y=0)

cpu1_frame = tk.Frame(cpus_frame, bg="yellow", height=300, width=225)
cpu1_frame.place(x=225, y=0)

cpu2_frame = tk.Frame(cpus_frame, bg="blue", height=300, width=225)
cpu2_frame.place(x=450, y=0)

cpu3_frame = tk.Frame(cpus_frame, bg="green", height=300, width=225)
cpu3_frame.place(x=675, y=0)

bus_frame = tk.Frame(main_frame, bg="LightSeaGreen", height=100, width=900)
bus_frame.place(x=0, y=300)

botton_frame = tk.Frame(main_frame, bg="OrangeRed", height=100, width=900)
botton_frame.place(x=0, y=400)

memory_frame = tk.Frame(botton_frame, bg="blue", height=100, width=400)
memory_frame.place(x=0, y=0)

buttons_frame = tk.Frame(botton_frame, bg="red", height=100, width=200)
buttons_frame.place(x=400, y=0)

console_frame = tk.Frame(botton_frame, bg="green", height=100, width=300)
console_frame.place(x=600, y=0)

# --------------- Componenents ----------------------------------------

# Consola

console_text = scrolledtext.ScrolledText(
    console_frame, wrap=tk.WORD, width=40, height=6, font=("Arial", 10)
)
console_text.grid(column=0, pady=0, padx=0)
console_text["state"] = "disabled"


def printToConsole(text: str):
    console_text["state"] = "normal"
    console_text.insert("end", str(text) + "\n")
    console_text.see("end")
    console_text["state"] = "disabled"


def cleanConsole():
    console_text["state"] = "normal"
    console_text.delete("1.0", "end")
    console_text["state"] = "disabled"


# Botones

new_instruction_button = tk.Button(
    buttons_frame,
    text="Nueva Instrucción",
    command=lambda: printToConsole("Hola Mundo"),
)
new_instruction_button.place(x=0, y=0)


main.mainloop()
