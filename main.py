import tkinter as tk
from tkinter import scrolledtext
import time


def newInstruction():
    global memory_dict
    if not loopInstructionsFlag:
        memory_dict["000"] += 1
        create_memory_table(memory_frame, ("Arial", 14), "white")
    else:
        printToConsole("Se encuentra activa la ejecución en ciclo.")


# Variables globales

memory_dict = {
    "000": 0x0,
    "001": 0x0,
    "010": 0x0,
    "011": 0x0,
    "100": 0x0,
    "101": 0x0,
    "110": 0x0,
    "111": 0x0,
}

loopInstructionsFlag = False

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

memory_frame = tk.Frame(botton_frame, bg="white", height=100, width=420)
memory_frame.place(x=0, y=0)

buttons_frame = tk.Frame(botton_frame, bg="white", height=100, width=150)
buttons_frame.place(x=420, y=0)

console_frame = tk.Frame(botton_frame, bg="white", height=100, width=330)
console_frame.place(x=570, y=0)

# --------------- Componenents ----------------------------------------

# Consola

console_text = scrolledtext.ScrolledText(
    console_frame, wrap=tk.WORD, width=44, height=6, font=("Arial", 10)
)
console_text.grid(column=0, pady=0, padx=0)
console_text["state"] = "disabled"


def printToConsole(text: str):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    console_text["state"] = "normal"
    console_text.insert("end", current_time + ": " + str(text) + "\n")
    console_text.see("end")
    console_text["state"] = "disabled"


def cleanConsole():
    console_text["state"] = "normal"
    console_text.delete("1.0", "end")
    console_text["state"] = "disabled"


# Botones

new_instruction_photoimage = tk.PhotoImage(file=r"images\button_nueva-instruccion.png")
new_instruction_button = tk.Button(
    buttons_frame,
    image=new_instruction_photoimage,
    command=newInstruction,
    bg="white",
    borderwidth=0,
)


def changeLoopFlag():
    global loopInstructionsFlag
    loopInstructionsFlag = not loopInstructionsFlag

    if (
        loopInstructionsFlag
    ):  # El programa está enciclado para leer nuevas instrucciones
        loop_button.config(image=loop_photoimage_detener)
        instructionsLoop()

    else:
        loop_button.config(image=loop_photoimage_iniciar)


loop_photoimage_detener = tk.PhotoImage(file=r"images\button_detener-ciclo.png")
loop_photoimage_iniciar = tk.PhotoImage(file=r"images\button_iniciar-ciclo.png")

loop_photoimage = (
    loop_photoimage_detener if loopInstructionsFlag else loop_photoimage_iniciar
)


loop_button = tk.Button(
    buttons_frame,
    image=loop_photoimage,
    command=changeLoopFlag,
    bg="white",
    borderwidth=0,
)


reset_photoimage = tk.PhotoImage(file=r"images\button_reiniciar.png")
reset_button = tk.Button(
    buttons_frame,
    image=reset_photoimage,
    command=cleanConsole,
    bg="white",
    borderwidth=0,
)

new_instruction_button.place(x=15, y=2)
loop_button.place(x=33, y=35)
reset_button.place(x=42, y=68)


# Memory labels


def create_memory_table(parent, font, bg_color):
    global memory_dict
    index = 0
    for i in range(3):
        for j in range(3):
            if i == 2 and j == 2:
                break
            bin_key = format(
                index, "03b"
            )  # Convertir el índice a una llave en formato binario
            cell_value = memory_dict[bin_key]
            cell = tk.Entry(parent, font=font, bg=bg_color, justify="center", width=12)
            cell_value = format(cell_value, "04X")
            cell.insert(0, bin_key + ": " + cell_value)
            cell.config(state="readonly")
            cell.grid(row=i, column=j, padx=3, pady=4, sticky="nsew")
            index += 1

        parent.grid_rowconfigure(i, weight=1)
        parent.grid_columnconfigure(i, weight=1)


create_memory_table(memory_frame, ("Arial", 14), "white")


# Loop para crear las instrucciones
def instructionsLoop():
    if loopInstructionsFlag:
        printToConsole("Hilo")
        main.after(2000, instructionsLoop)
    else:
        return


main.mainloop()
