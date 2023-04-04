import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import random

main = tk.Tk(className="Arquitectura de Computadores 2. Proyecto I")
# ----------------- Logic --------------------------------------------

# -------------CPUS-------------------
class CPU:
    def __init__(self, id: int):
        self.id = id
        self.instruction = ""
        self.instructionList = []
        self.instruction_Step = 0
        self.cache = {
            "B0": CacheBlock(self.id),
            "B1": CacheBlock(self.id),
            "B2": CacheBlock(self.id),
            "B3": CacheBlock(self.id),
        }
        self.parity = {
            "0": [self.cache["B0"], self.cache["B1"]],
            "1": [self.cache["B2"], self.cache["B3"]],
        }

    def executeCycle(self):
        if self.instruction == "":
            self.generateNewInstruction()
        else:
            self.executeInstruction()

    def generateNewInstruction(self):
        self.instruction = self.newInstruction()
        self.instructionList = self.createListFromInstruction(self.instruction)
        self.instruction_Step = self.setInstructionLenght(self.instructionList)

    def executeInstruction(self):
        # 1 = calc
        # 2 = read
        # 3 = write
        inst_type = len(self.instructionList)

        # Calc
        if inst_type == 1:
            self.instruction_Step = 0

        if self.instruction_Step == 0:
            self.instruction = ""
        # Read
        elif inst_type == 2:
            mem_dir = self.instructionList[1]
            self.executeRead(mem_dir)

        else:
            self.instruction_Step -= 1

    def setInstructionLenght(self, instructionList):
        inst_type = len(instructionList)
        # Calc Instruction
        if inst_type == 1:
            return 0
        # Read Instruction
        if inst_type == 2:
            return 5
        else:
            return 1

    def newInstruction(self):
        def binary(num, length=4):
            return format(num, f"0{length}b")

        def hexa(num, length=4):
            return format(num, f"0{length}X")

        # Distribución de probabilidad
        p_calc = 1 / 5
        p_write = 2 / 3

        r = random.random()

        if r < p_calc:
            return f"P{self.id}: CALC"
        elif r < p_calc + p_write:
            addr = binary(random.randint(0, 7), 3)
            data = hexa(random.randint(0, 65535))
            return f"P{self.id}: WRITE {addr} {data}"
        else:
            addr = binary(random.randint(0, 7), 3)
            return f"P{self.id}: READ {addr}"

    def reset(self):
        self.instruction = ""
        self.resetCacheBlocks()

    def resetCacheBlocks(self):
        for block, cacheObject in self.cache.items():
            cacheObject.reset()

    def createListFromInstruction(self, instruction):
        # Dividimos la cadena en palabras utilizando split()
        values = instruction.split()
        # Eliminamos el primer elemento de la lista (Pn:)
        del values[0]
        # Retornamos la lista modificada
        return values

    # Read logic -------------------------------------------------------------------------

    def executeRead(self, mem_dir):
        # Checkea si es un readMiss o si tengo el dato
        if self.instruction_Step == 5:
            printToConsole(f"Paso 5. Mem {mem_dir}")
            self.read_CheckMiss(mem_dir)
            return
        elif self.instruction_Step == 4:
            printToConsole(f"Paso 4. Mem {mem_dir}")
            self.read_missDetected(mem_dir)
            return
        elif self.instruction_Step == 3:
            printToConsole(f"Paso 3. Mem {mem_dir}")
            self.read_searchDataInOtherCPU(mem_dir)
            return
        elif self.instruction_Step == 2:
            printToConsole(f"Paso 2. Mem {mem_dir}")
            self.read_loadDataFromMemory(mem_dir)
            return
        # Tiene el dato y no es invalido, solamente lo lee
        elif self.instruction_Step == 1:
            printToConsole(f"Paso 1. Mem {mem_dir}")
            self.instruction_Step = 0
            return
        # Doy por finalizada la ejecución
        elif self.instruction_Step == 0:
            printToConsole(f"Paso 0. Mem {mem_dir}")
            self.instruction == ""
            return

    def removeCacheBlockFromBus(self, mem_dir, cacheBlock):

        global bus_dict
        try:
            bus_dict[mem_dir].remove(cacheBlock)
        except ValueError:
            printToConsole(
                f"No existe un bloque {cacheBlock.memory} en el CPU{cacheBlock.cpuID}."
            )

    def addBlockToBus(self, mem_dir: str, cacheBlock):
        global bus_dict
        if cacheBlock not in bus_dict[mem_dir]:
            bus_dict[mem_dir].append(cacheBlock)
        else:
            print(f"El dato ya se encuentra en cache del CPU{cacheBlock.cpuID}")

    def read_searchDataInOtherCPU(self, mem_dir):
        global bus_dict
        bus_dir_reg = bus_dict[mem_dir]
        try:
            for block in bus_dir_reg:
                if block.memory == mem_dir and block.state != "Invalid":
                    # Exclusive -> Shared
                    if block.state == "Exclusive":
                        insertedBlock = self.read_loadData(
                            "Shared", mem_dir, block.data
                        )
                        block.state = "Shared"
                        self.addBlockToBus(mem_dir, insertedBlock)
                    # Modified -> Owned
                    elif block.state == "Modified":
                        insertedBlock = self.read_loadData(
                            "Shared", mem_dir, block.data
                        )
                        block.state = "Owned"
                        self.addBlockToBus(mem_dir, insertedBlock)
                    # Shared -> Shared
                    else:
                        pass
        except:
            printToConsole(bus_dir_reg)
        # Finalizo la lectura
        self.instruction_Step = 0

    def read_loadData(self, state, mem_dir, data):
        global bus_dict
        last_caracter = mem_dir[-1]
        parityBlocks = self.parity[last_caracter]
        # Intenta ingresa el dato a un bloque con información inválida primeramente.
        for block in parityBlocks:
            if block.state == "Invalid":
                self.removeCacheBlockFromBus(mem_dir, block)
                block.state = state
                block.memory = mem_dir
                block.data = data
                return block

    def read_missDetected(self, mem_dir):
        global bus_dict
        bus_dir_reg = bus_dict[mem_dir]
        # Si nadie tiene el dato, lo traigo de memoria
        if len(bus_dir_reg) == 0:
            self.instruction_Step = 2
        # Si no, busco quien lo tiene:
        else:
            self.instruction_Step = 3

    def read_CheckMiss(self, mem_dir):
        last_caracter = mem_dir[-1]
        parityBlocks = self.parity[last_caracter]
        Changeflag = False
        for cacheBlock in parityBlocks:
            if cacheBlock.memory == mem_dir and cacheBlock.state != "Invalid":
                self.instruction_Step = 1
                Changeflag = True

        # Detecta el cache miss ya que no tiene el valor en memoria o lo tiene y es inválido
        if not Changeflag:
            self.instruction_Step = 4

    def read_loadDataFromMemory(self, mem_dir):
        global memory_dict
        data = memory_dict[mem_dir]
        insertedBlock = self.read_loadData("Exclusive", mem_dir, data)
        self.addBlockToBus(mem_dir, insertedBlock)
        # Finaliza el ciclo de ejecución
        self.instruction_Step = 0


class CacheBlock:
    def __init__(self, cpuID):
        self.state = "Invalid"
        self.memory = "000"
        self.data = 0x0000
        self.cpuID = cpuID

    def read(self, instructionsList):
        if self.state == "Invalid":
            print("Read miss")
            self.state = "Shared"
        elif self.state == "Exclusive":
            print("Read hit")
        else:
            print("Read hit")

    def write(self):
        if self.state == "Invalid":
            print("Write miss")
            self.state = "Modified"
        elif self.state == "Exclusive":
            print("Write hit")
            self.state = "Modified"
        elif self.state == "Shared":
            print("Write miss")
            self.state = "Modified"
        elif self.state == "Owned":
            print("Write miss")
            self.state = "Modified"
        else:
            print("Write hit")

    def bus_read(self):
        if self.state == "Invalid":
            pass
        elif self.state == "Exclusive":
            self.state = "Shared"
        elif self.state == "Owned":
            pass
        elif self.state == "Modified":
            print("Bus read miss")
            self.state = "Owned"

    def bus_write(self):
        if self.state == "Invalid":
            pass
        elif self.state == "Exclusive":
            self.state = "Invalid"
        elif self.state == "Shared":
            self.state = "Invalid"
        elif self.state == "Owned":
            self.state = "Invalid"
        elif self.state == "Modified":
            print("Bus write miss")
            self.state = "Invalid"

    def print_state(self):
        print("Current state:", self.state)

    def reset(self):
        self.state = "Invalid"
        self.memory = "000"
        self.data = 0x0000


def newCycle_cpus():
    global main, cpus_list
    printToConsole("------------------------------------------------")
    for cpu in cpus_list:
        cpu.executeCycle()
    render_CPU_info()


def resetAllCpus():
    global main, cpus_list
    for cpu in cpus_list:
        cpu.reset()


# ------------- Instruction Generation ---------------------------


# -------- New Cycle Logic------------------------------


def manualGlobalCycle():
    if not loopCyclesFlag:
        newCycle_cpus()
    else:
        printToConsole("Activada la ejecucion en bucle")


def changeLoopFlag():
    global loopCyclesFlag
    loopCyclesFlag = not loopCyclesFlag

    if loopCyclesFlag:  # El programa está enciclado para leer nuevas instrucciones
        loop_button.config(image=loop_photoimage_detener)
        LoopExecution()
    else:
        loop_button.config(image=loop_photoimage_iniciar)


# Loop para crear las instrucciones
def LoopExecution():
    global main, loopCyclesFlag
    if loopCyclesFlag:
        newCycle_cpus()
        main.after(cycle_duration, LoopExecution)
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
    global loopCyclesFlag
    # Set the loop logic to false
    loopCyclesFlag = False
    loop_button.config(image=loop_photoimage_iniciar)
    cleanConsole()
    # Clean and reset memory
    resetMemory()
    create_memory_table(memory_frame, ("Arial", 12), "white")
    # Clean and reset cpus
    resetAllCpus()
    render_CPU_info()


def resetMemory():
    global memory_dict
    for i in range(8):
        bin_key = format(i, "03b")
        memory_dict[bin_key] = 0x0


def close_app():
    main.destroy()


def on_ctrl_s(event):
    with open("logs.txt", "w") as file:
        file.write(console_text.get("1.0", tk.END))
    messagebox.showinfo(
        "Archivo guardado", "El archivo logs.txt se ha guardado correctamente."
    )


main.bind("<Control-s>", on_ctrl_s)

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
            cell = tk.Entry(parent, font=font, bg=bg_color, justify="center", width=11)
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
        clean_frame(parent)
        render_cpu_headers(cpu, parent)
        render_cpu_cache(cpu, parent)


def render_cpu_headers(cpu, parent):
    global cpus_dict
    Titlelabel = tk.Label(
        parent, text="CPU " + str(cpus_dict[cpu].id), font=("Arial", 24), bg="white"
    )
    Titlelabel.place(x=60, y=10)

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
    for block, cacheObject in cache.items():
        blockName = tk.Label(
            parent,
            text=block,
            font=("Arial", 10),
            bg="white",
            justify="center",
        )
        blockName.place(x=10, y=y_pos)

        Statelabel = tk.Label(
            parent,
            text=cacheObject.state,
            font=("Arial", 10),
            bg="white",
            justify="center",
        )
        Statelabel.place(x=60, y=y_pos)

        Memlabel = tk.Label(
            parent,
            text=cacheObject.memory,
            font=("Arial", 10),
            bg="white",
            justify="center",
        )
        Memlabel.place(x=135, y=y_pos)

        Datalabel = tk.Label(
            parent,
            text=format(cacheObject.data, "04X"),
            font=("Arial", 10),
            bg="white",
            justify="center",
        )
        Datalabel.place(x=185, y=y_pos)

        instructionText = cpus_dict[cpu].instruction
        if instructionText != "":
            instructionText = instructionText[4:]
        Instructionlabel = tk.Label(
            parent,
            text="Instruction: " + instructionText,
            font=("Arial", 10),
            bg="white",
            justify="center",
        )
        Instructionlabel.place(x=20, y=275)

        y_pos += 50


def clean_frame(frame):
    # Eliminar todos los widgets del frame
    for widget in frame.winfo_children():
        widget.destroy()


# -------------------------------Variables globales--------------------------------------------------

# Bus

bus_dict = {
    "000": [],
    "001": [],
    "010": [],
    "011": [],
    "100": [],
    "101": [],
    "110": [],
    "111": [],
}

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

cpus_list = [cpu0, cpu1, cpu2, cpu3]

loopCyclesFlag = False
SingleCycleFlag = False

cycle_duration = 2000  # 2000 milisegundos = 2 segundos por ciclo

# Main widget settings

main.geometry("900x400")
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


botton_frame = tk.Frame(
    main_frame,
    bg="white",
    height=100,
    width=900,
    borderwidth=1,
    relief="ridge",
)
botton_frame.place(x=0, y=300)

memory_frame = tk.Frame(botton_frame, bg="white", height=100, width=420)
memory_frame.place(x=0, y=0)

buttons_frame = tk.Frame(botton_frame, bg="white", height=100, width=130)
buttons_frame.place(x=325, y=0)

console_frame = tk.Frame(botton_frame, bg="white", height=100, width=445)
console_frame.place(x=455, y=0)

# --------------- Componenents ----------------------------------------

# Consola

console_text = scrolledtext.ScrolledText(
    console_frame, wrap=tk.WORD, width=60, height=6, font=("Arial", 10)
)
console_text.grid(column=0, pady=0, padx=0)
console_text["state"] = "disabled"


# ----------------------------Botones----------------------------------

new_instruction_photoimage = tk.PhotoImage(file=r"images\button_nueva-instruccion.png")
new_instruction_button = tk.Button(
    buttons_frame,
    image=new_instruction_photoimage,
    command=manualGlobalCycle,
    bg="white",
    borderwidth=0,
)


loop_photoimage_detener = tk.PhotoImage(file=r"images\button_detener-ciclo.png")
loop_photoimage_iniciar = tk.PhotoImage(file=r"images\button_iniciar-ciclo.png")

loop_photoimage = loop_photoimage_detener if loopCyclesFlag else loop_photoimage_iniciar


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

create_memory_table(memory_frame, ("Arial", 12), "white")


# ----------------------------CPU labels----------------------------------

render_CPU_info()


main.protocol("WM_DELETE_WINDOW", close_app)


main.mainloop()
