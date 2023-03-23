import tkinter as tk
from tkinter import scrolledtext
import time

# ----------------- Logic --------------------------------------------


class CPU:
    def __init__(self, id: int):
        self.id = id
        self.cache = {
            "B0": ["S", "000", 0x0000],
            "B1": ["S", "000", 0x0000],
            "B2": ["S", "000", 0x0000],
            "B3": ["S", "000", 0x0000],
        }


# -------- New Instruction Logic------------------------------


def newInstruction():
    global memory_dict
    if not loopInstructionsFlag:
        memory_dict["000"] += 1
        create_memory_table(memory_frame, ("Arial", 14), "white")
    else:
        printToConsole("Se encuentra activa la ejecución en ciclo.")


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


# Loop para crear las instrucciones
def instructionsLoop():
    if loopInstructionsFlag:
        printToConsole("Hilo")
        main.after(2000, instructionsLoop)
    else:
        return


# -------- Console Logic ------------------------------


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


# -------- util Logic ------------------------------


def resetProgram():
    global loopInstructionsFlag
    # Set the loop logic to false
    loopInstructionsFlag = False
    loop_button.config(image=loop_photoimage_iniciar)
    cleanConsole()
    # Clean and reset memory
    resetMemory()
    create_memory_table(memory_frame, ("Arial", 14), "white")


def resetMemory():
    global memory_dict
    for i in range(8):
        bin_key = format(i, "03b")
        memory_dict[bin_key] = 0x0


def close_app():
    main.destroy()


# -------- Graphic Logic ------------------------------


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


def render_CPU_info():
    cpus_frames = {
        "cpu0": cpu0_frame,
        "cpu1": cpu1_frame,
        "cpu2": cpu2_frame,
        "cpu3": cpu3_frame,
    }
    for cpu, parent in cpus_frames.items():
        render_cpu_headers(parent)
        render_cpu_cache(cpu, parent)


def render_cpu_headers(parent):
    stateLabel = tk.Label(
        parent,
        text="Estado\nCoherencia",
        font=("Arial", 10),
        bg="white",
        justify="center",
    )
    dirLabel = tk.Label(
        parent,
        text="Dirección\nMemoria",
        font=("Arial", 10),
        bg="white",
        justify="center",
    )
    dataLabel = tk.Label(
        parent,
        text="Dato",
        font=("Arial", 10),
        bg="white",
        justify="center",
    )

    stateLabel.place(x=40, y=55)
    dirLabel.place(x=120, y=55)
    dataLabel.place(x=185, y=65)


def render_cpu_cache(cpu, parent):
    global cpus_dict
    cache = cpus_dict[cpu].cache
    y_pos = 100
    x_pos = [70, 135, 185]
    for block, values in cache.items():
        blockName = tk.Label(
            parent,
            text=block,
            font=("Arial", 10),
            bg="white",
            justify="center",
        )
        blockName.place(x=10, y=y_pos)
        cont = 0
        for data in values:
            if cont == 2:
                data = format(data, "04X")
            label = tk.Label(
                parent,
                text=data,
                font=("Arial", 10),
                bg="white",
                justify="center",
            )
            label.place(x=x_pos[cont], y=y_pos)

            cont += 1
        y_pos += 50


# Variables globales

# Memoria

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


# CPUS
cpu0 = CPU(0)
cpu1 = CPU(1)
cpu2 = CPU(2)
cpu3 = CPU(3)

cpus_dict = {
    "cpu0": cpu0,
    "cpu1": cpu1,
    "cpu2": cpu2,
    "cpu3": cpu3,
}


loopInstructionsFlag = False

# Main widget settings
main = tk.Tk(className="Arquitectura de Computadores 2. Proyecto I")
main.geometry("900x500")
main.resizable(False, False)

# Framing

main_frame = tk.Frame(main, bg="white", height=500, width=900)
main_frame.place(x=0, y=0)

cpus_frame = tk.Frame(main_frame, bg="white", height=300, width=900)
cpus_frame.place(x=0, y=0)

cpu0_frame = tk.Frame(
    cpus_frame,
    bg="white",
    height=300,
    width=225,
    border=2,
    borderwidth=1,
    relief="ridge",
)
cpu0_frame.place(x=0, y=0)

cpu1_frame = tk.Frame(
    cpus_frame,
    bg="white",
    height=300,
    width=225,
    border=2,
    borderwidth=1,
    relief="ridge",
)
cpu1_frame.place(x=225, y=0)

cpu2_frame = tk.Frame(
    cpus_frame,
    bg="white",
    height=300,
    width=225,
    border=2,
    borderwidth=1,
    relief="ridge",
)
cpu2_frame.place(x=450, y=0)

cpu3_frame = tk.Frame(
    cpus_frame,
    bg="white",
    height=300,
    width=225,
    border=2,
    borderwidth=1,
    relief="ridge",
)
cpu3_frame.place(x=675, y=0)

bus_frame = tk.Frame(main_frame, bg="LightSeaGreen", height=100, width=900)
bus_frame.place(x=0, y=300)

botton_frame = tk.Frame(
    main_frame,
    bg="white",
    height=100,
    width=900,
    borderwidth=1,
    relief="ridge",
)
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


# ----------------------------Botones----------------------------------

new_instruction_photoimage = tk.PhotoImage(file=r"images\button_nueva-instruccion.png")
new_instruction_button = tk.Button(
    buttons_frame,
    image=new_instruction_photoimage,
    command=newInstruction,
    bg="white",
    borderwidth=0,
)


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
    command=resetProgram,
    bg="white",
    borderwidth=0,
)

new_instruction_button.place(x=15, y=2)
loop_button.place(x=33, y=35)
reset_button.place(x=42, y=68)


# ----------------------------Memoria----------------------------------

create_memory_table(memory_frame, ("Arial", 14), "white")


# ----------------------------CPU labels----------------------------------

cpu0_title_label = tk.Label(cpu0_frame, text="CPU 0", font=("Arial", 24), bg="white")
cpu0_title_label.place(x=60, y=10)

cpu1_title_label = tk.Label(cpu1_frame, text="CPU 1", font=("Arial", 24), bg="white")
cpu1_title_label.place(x=60, y=10)

cpu2_title_label = tk.Label(cpu2_frame, text="CPU 2", font=("Arial", 24), bg="white")
cpu2_title_label.place(x=60, y=10)

cpu3_title_label = tk.Label(cpu3_frame, text="CPU 3", font=("Arial", 24), bg="white")
cpu3_title_label.place(x=60, y=10)

render_CPU_info()


main.protocol("WM_DELETE_WINDOW", close_app)

main.mainloop()
