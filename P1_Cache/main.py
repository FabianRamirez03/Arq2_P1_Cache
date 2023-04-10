import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import random

main = tk.Tk(
    className="Modelo de protocolo para coherencia de caché en sistemas multiprocesador"
)
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
        printToConsole(f"CPU{self.id}: Generando instrucciones.")
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
            printToConsole(f"CPU{self.id}: Calculando.")
            self.instruction_Step = 0
        if self.instruction_Step == 0:
            self.instruction = ""
        # Read
        elif inst_type == 2:
            mem_dir = self.instructionList[1]
            self.executeRead(mem_dir)
        # Write
        else:
            mem_dir = self.instructionList[1]
            data = self.instructionList[2]
            data = int(data, 16)
            self.executeWrite(mem_dir, data)

    def setInstructionLenght(self, instructionList):
        inst_type = len(instructionList)
        # Calc Instruction
        if inst_type == 1:
            return 0
        # Read Instruction
        if inst_type == 2:
            return 5
        # Write Instruction
        else:
            return 6

    def newInstruction(self):
        def binary(num, length=4):
            return format(num, f"0{length}b")

        def hexa(num, length=4):
            return format(num, f"0{length}X")

        # Distribución de probabilidad
        p_calc = 1 / 3
        p_write = 1 / 3

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

    def setNewInstruction(self, instruction):
        printToConsole(f"CPU{self.id}: Ingresando instrucción {instruction[4:]}.")
        self.instruction = instruction
        self.instructionList = self.createListFromInstruction(self.instruction)
        self.instruction_Step = self.setInstructionLenght(self.instructionList)

        render_CPU_info()

    # Read logic -------------------------------------------------------------------------

    def executeRead(self, mem_dir):
        # Checkea si es un readMiss o si tengo el dato
        if self.instruction_Step == 5:
            printToConsole(
                f"CPU{self.id}: Ejecutando instruccion: {self.instruction[4:]}"
            )
            self.read_CheckMiss(mem_dir)
            return
        # Es un read Miss
        elif self.instruction_Step == 4:
            printToConsole(f"CPU{self.id}: Read miss")
            self.read_missDetected(mem_dir)
            return
        # El dato está en otro CPU. Lo busca ahí
        elif self.instruction_Step == 3:
            self.read_searchDataInOtherCPU(mem_dir)
            return
        # El dato no está en otro CPU. Lo busca en memoria
        elif self.instruction_Step == 2:
            self.read_loadDataFromMemory(mem_dir)
            return
        # Tiene el dato y no es invalido, solamente lo lee
        elif self.instruction_Step == 1:
            self.instruction_Step = 0
            return
        # Da por finalizada la ejecución
        elif self.instruction_Step == 0:
            printToConsole(
                f"CPU{self.id}: Finalizada Instrucción instruccion: {self.instruction}"
            )
            self.instruction == ""
            return

    def removeCacheBlockFromBus(self, mem_dir, cacheBlock):

        global bus_dict, bus_dict_quantity
        # Resto uno a la cantidad de procesadores que poseen el dato

        try:
            bus_dict[mem_dir].remove(cacheBlock)
            bus_dict_quantity[mem_dir] -= 1
        except ValueError:
            return

    def addBlockToBus(self, mem_dir: str, cacheBlock):
        global bus_dict
        if cacheBlock not in bus_dict[mem_dir]:
            bus_dict[mem_dir].append(cacheBlock)
        else:
            print(f"El dato ya se encuentra en cache del CPU{cacheBlock.cpuID}")

    # 3
    #  El dato está en otro CPU. Lo busca ahí
    def read_searchDataInOtherCPU(self, mem_dir):
        printToConsole(f"CPU{self.id}: Read buscando el dato en otro CPU")
        global bus_dict
        bus_dir_reg = bus_dict[mem_dir]
        try:
            for block in bus_dir_reg:
                if block.memory == mem_dir and block.state != "Invalid":
                    printToConsole(
                        f"cpu{self.id}: block state: {block.state} CPUID: {block.cpuID}"
                    )
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
            self.instruction_Step = 5
            return
        # Finalizo la lectura
        self.instruction_Step = 0

    def read_loadData(self, state, mem_dir, data):
        global bus_dict
        last_caracter = mem_dir[-1]
        parityBlocks = self.parity[last_caracter]
        # Intenta ingresa el dato a un bloque con información inválida primeramente.
        for block in parityBlocks:
            if block.state in ("Invalid", "Shared", "Exclusive"):
                self.removeCacheBlockFromBus(mem_dir, block)
                block.state = state
                block.memory = mem_dir
                block.data = data
                return block
        for block in parityBlocks:
            printToConsole
            if block.state in ("Modified"):
                block.writeInMemory()
                self.removeCacheBlockFromBus(mem_dir, block)
                block.state = state
                block.memory = mem_dir
                block.data = data
                return block

    # 4
    # Es un read Miss
    def read_missDetected(self, mem_dir):
        global bus_dict_quantity
        # Sé que tendré el dato, sumo uno a la cantidad de procesadores que poseen el dato
        bus_dict_quantity[mem_dir] += 1
        # Si solo lo tendré yo, lo traigo de memoria
        printToConsole(f"{self.instruction} {bus_dict_quantity[mem_dir]}")
        print(bus_dict_quantity)
        if bus_dict_quantity[mem_dir] == 1:
            self.instruction_Step = 2
        # Si no, busco quien lo tiene:
        else:
            self.instruction_Step = 3

    # 5
    # Checkea si es un readMiss o si tengo el dato
    def read_CheckMiss(self, mem_dir):
        last_caracter = mem_dir[-1]
        parityBlocks = self.parity[last_caracter]
        miss_flag = False
        for cacheBlock in parityBlocks:
            if cacheBlock.memory == mem_dir and cacheBlock.state != "Invalid":
                self.instruction_Step = 1
                miss_flag = True

        # Detecta el cache miss ya que no tiene el valor en memoria o lo tiene y es inválido
        if not miss_flag:
            self.instruction_Step = 4

    # 2
    # El dato no está en otro CPU. Lo busca en memoria
    def read_loadDataFromMemory(self, mem_dir):
        global memory_dict
        data = memory_dict[mem_dir]
        insertedBlock = self.read_loadData("Exclusive", mem_dir, data)
        self.addBlockToBus(mem_dir, insertedBlock)
        # Finaliza el ciclo de ejecución
        self.instruction_Step = 0

    # write logic -------------------------------------------------------------------------

    def executeWrite(self, mem_dir, data):
        # Checkea si es un writeMiss o si tengo el dato
        if self.instruction_Step == 6:
            printToConsole(
                f"CPU{self.id}: Ejecutando instruccion: {self.instruction[4:]}"
            )
            self.write_CheckMiss(mem_dir)
            return
        # No tengo el dato, checkeo si alguien más lo tiene
        elif self.instruction_Step == 5:
            printToConsole(f"CPU{self.id}: Write miss")
            self.write_missedCheckOthers(mem_dir)
            return
        # Tengo el dato pero no está invalidado. Si lo tengo pero es S, E, M o O, puedo modificarlo de nuevo, solamente invalidando el resto de ser necesario
        elif self.instruction_Step == 4:
            self.write_notMissedNotInvalid(mem_dir, data)
            return
        # Nadie tiene el dato, lo cargo de memoria
        elif self.instruction_Step == 3:
            self.write_NobodyHasIt_LoadFromMemory(mem_dir, data)
            return
        # Alguien tiene el dato, lo cargo de otro CPU
        elif self.instruction_Step == 2:
            self.write_SomebodyHasIt_LoadFromThere(mem_dir, data)
            return
        # Tengo el dato pero está invalidado. Doy por hecho que alguien más lo tiene porque me invalidó mi dato
        elif self.instruction_Step == 1:
            self.write_notMissedButInvalid(mem_dir, data)
            return
        # Doy por finalizada la ejecución
        elif self.instruction_Step == 0:
            self.instruction == ""
            return

    # 6
    # Checkea si es un writeMiss o si tengo el dato
    def write_CheckMiss(self, mem_dir):
        last_caracter = mem_dir[-1]
        parityBlocks = self.parity[last_caracter]
        blocks_list = []
        for cacheBlock in parityBlocks:
            if cacheBlock.memory == mem_dir:
                blocks_list.append(cacheBlock)

        # Si no lo tengo cargado, voy al paso 5
        if len(blocks_list) == 0:
            self.instruction_Step = 5
            return
        else:
            for block in blocks_list:
                # Si tengo el bloque pero está invalidado, voy al paso 1
                if block.state == "Invalid":
                    self.instruction_Step = 1
                    return

            # Si tengo el bloque pero no está Invalido (M, O, E, S) voy al paso 4
            self.instruction_Step = 4
            return

    # 5
    # No tengo el dato, checkeo si alguien más lo tiene
    def write_missedCheckOthers(self, mem_dir):
        global bus_dict_quantity
        # Sé que tendré el dato, sumo uno a la cantidad de procesadores que poseen el dato
        bus_dict_quantity[mem_dir] += 1
        printToConsole(f"{self.instruction} {bus_dict_quantity[mem_dir]}")
        # Si nadie tiene el dato
        if bus_dict_quantity == 1:
            self.instruction_Step = 3
            return
        # alguien tiene el dato
        else:
            self.instruction_Step = 2
            return

    # 4
    # Tengo el dato pero no está invalidado. Si lo tengo pero es S, E, M o O, puedo modificarlo de nuevo, solamente invalidando el resto de ser necesario
    def write_notMissedNotInvalid(self, mem_dir, data):
        last_caracter = mem_dir[-1]
        parityBlocks = self.parity[last_caracter]
        #
        for cacheBlock in parityBlocks:
            if cacheBlock.memory == mem_dir and cacheBlock.state in (
                "Shared",
                "Exclusive",
                "Modified",
                "Owned",
            ):
                # Escribo el dato en Memoria
                cacheBlock.writeInMemory()
                # Invalido el resto de CPUs
                self.write_invalidOthers(mem_dir)
                # Actualizo el estado de mi cache
                cacheBlock.update("Modified", mem_dir, data)
        # Finalizo la ejecución
        self.instruction_Step = 0
        return

    # 3
    # Nadie tiene el dato, lo cargo de memoria
    def write_NobodyHasIt_LoadFromMemory(self, mem_dir, data):
        global memory_dict
        # Selecciono el bloque en el que insertaré el dato
        insertedBlock = self.write_loadData("Modified", mem_dir, data)
        self.addBlockToBus(mem_dir, insertedBlock)
        # Finaliza el ciclo de ejecución
        self.instruction_Step = 0
        return

    # 2
    # Alguien lo tiene, Modifico e invalido
    def write_SomebodyHasIt_LoadFromThere(self, mem_dir, data):
        global bus_dict
        register_list = bus_dict[mem_dir]
        # Si el dato dejó de estar durante la ejecución de la instrucción, vuelva al paso 3
        if len(register_list) == 0:
            self.instruction_Step = 3
            return
        try:
            for block in register_list:
                if block.state in ("Modified", "Owned", "Exclusive"):
                    # Escribo el valor en el otro CPU en memoria
                    block.writeInMemory()
                    # Invalido el resto de CPUs
                    self.write_invalidOthers(mem_dir)
        except:
            self.instruction_Step = 6
            return

        # Selecciono el bloque en el que insertaré el dato
        insertedBlock = self.write_loadData("Modified", mem_dir, data)
        # Actualizo el estado del bus
        self.addBlockToBus(mem_dir, insertedBlock)

        self.instruction_Step = 0
        return

    # 1
    # Tengo el dato pero está invalidado. Doy por hecho que alguien más lo tiene porque me invalidó mi dato
    def write_notMissedButInvalid(self, mem_dir, data):
        global bus_dict
        register_list = bus_dict[mem_dir]
        # Escribo el dato en memoria del dato que lo haya modificado
        try:
            for block in register_list:
                if block.state in ("Modified", "Owned", "Exclusive"):
                    block.writeInMemory()
        except:
            self.instruction_Step = 6
            return

        # Invalido el resto de CPUs
        self.write_invalidOthers(mem_dir)

        # Actualizo el estado de mi cache
        last_caracter = mem_dir[-1]
        parityBlocks = self.parity[last_caracter]
        changed_flag = True
        for block in parityBlocks:
            if block.memory == mem_dir and changed_flag:
                block.update("Modified", mem_dir, data)
                changed_flag = False

        # Finalizo la ejecución
        self.instruction_Step = 0
        return

    def write_loadData(self, state, mem_dir, data):
        global bus_dict
        last_caracter = mem_dir[-1]
        parityBlocks = self.parity[last_caracter]
        # Intenta ingresa el dato a un bloque con información inválida primeramente.
        for block in parityBlocks:
            if block.state in ("Invalid", "Shared"):
                self.removeCacheBlockFromBus(mem_dir, block)
                block.state = state
                block.memory = mem_dir
                block.data = data
                return block

    def write_invalidOthers(self, mem_dir):
        global bus_dict
        register_list = bus_dict[mem_dir]
        try:
            for block in register_list:
                block.state = "Invalid"
        except:
            return


class CacheBlock:
    def __init__(self, cpuID):
        self.state = "Invalid"
        self.memory = "000"
        self.data = 0x0000
        self.cpuID = cpuID

    def writeInMemory(self):
        global memory_dict
        memory_dict[self.memory] = self.data

    def print_state(self):
        print("Current state:", self.state)

    def update(self, state, memory, data):
        self.state = state
        self.memory = memory
        self.data = data

    def reset(self):
        self.state = "Invalid"
        self.memory = "000"
        self.data = 0x0000


def newCycle_cpus():
    global main, cpus_list
    printToConsole("------------------------------------------------")
    for cpu in cpus_list:
        cpu.executeCycle()
    # checkModifiedCornerCase()
    render_CPU_info()
    create_memory_table(memory_frame, ("Arial", 12), "white")


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


# Por ejemplo, si coinciden justo una escritura y una lectura del mismo espacio de memoria. Se subiría como Exclusivo y modified a la vez
def checkModifiedCornerCase():
    global bus_dict
    for mem_dir, lista in bus_dict.items():
        if len(lista) != 0:
            for block in lista:
                if block.state == "Modified":
                    for possible_invalid_block in lista:
                        if possible_invalid_block.state == "Exclusive":
                            possible_invalid_block.state = "Invalid"


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
    resetBusRegister()
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


def resetBusRegister():
    global bus_dict
    for register, lista in bus_dict.items():
        lista = []


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
        blockName.place(x=5, y=y_pos)

        Statelabel = tk.Label(
            parent,
            text=cacheObject.state,
            font=("Arial", 10),
            bg="white",
            justify="center",
        )
        Statelabel.place(x=55, y=y_pos)

        Memlabel = tk.Label(
            parent,
            text=cacheObject.memory,
            font=("Arial", 10),
            bg="white",
            justify="center",
        )
        Memlabel.place(x=130, y=y_pos)
        Datalabel = tk.Label(
            parent,
            text=format(cacheObject.data, "04X"),
            font=("Arial", 10),
            bg="white",
            justify="center",
        )
        Datalabel.place(x=180, y=y_pos)

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


pop_up_flag = True


def open_popup():
    global pop_up_flag, loopCyclesFlag
    if pop_up_flag and not loopCyclesFlag:
        pop_up_flag = False
        generate_instruction_popup()
    else:
        if loopCyclesFlag:
            printToConsole("Error: El programa se encuentra en modo ciclo")
        return


def generate_instruction_popup():

    popup_win = tk.Toplevel()
    popup_win.wm_title("Generar instrucción")
    popup_win.resizable(False, False)

    popup_frame = tk.Frame(popup_win, bg="white")
    popup_frame.pack(expand=True, fill=tk.BOTH)

    address_entry = tk.Entry(popup_frame)
    data_entry = tk.Entry(popup_frame)
    processor_var = tk.IntVar()
    instruction_var = tk.StringVar()

    def validate_binary(value, num_bits):
        if not value or len(value) != num_bits:
            return False
        for bit in value:
            if bit not in ("0", "1"):
                return False
        return True

    def validate_hex(value, num_digits):
        if not value or len(value) != num_digits:
            return False
        for digit in value:
            if digit not in "0123456789ABCDEFabcdef":
                return False
        return True

    def close_popup():
        global pop_up_flag
        pop_up_flag = True
        popup_win.destroy()

    popup_win.protocol("WM_DELETE_WINDOW", close_popup)

    def submit():
        global cpus_list
        processor = processor_var.get()
        instruction_type = instruction_var.get()

        if instruction_type == "CALC":
            instruction = "P0: CALC"
        elif instruction_type == "READ":
            address = address_entry.get()
            if not validate_binary(address, 3):
                messagebox.showerror(
                    "Error",
                    "Por favor, ingrese una dirección de memoria válida (000-111).",
                )
                return
            instruction = f"P0: READ {address}"
        elif instruction_type == "WRITE":
            address = address_entry.get()
            data = data_entry.get()
            if not validate_binary(address, 3):
                messagebox.showerror(
                    "Error",
                    "Por favor, ingrese una dirección de memoria válida (000-111).",
                )
                return
            if not validate_hex(data, 4):
                messagebox.showerror(
                    "Error",
                    "Por favor, ingrese un dato hexadecimal válido (0000-ffff).",
                )
                return
            instruction = f"P0: WRITE {address} {data.upper()}"
        cpus_list[processor].setNewInstruction(instruction)
        close_popup()

    tk.Label(
        popup_frame, text="Número de procesador (0-3):", font=("Arial", 12), bg="white"
    ).grid(row=0, column=0, sticky="w")
    for i in range(4):
        tk.Radiobutton(
            popup_frame,
            text=str(i),
            variable=processor_var,
            value=i,
            font=("Arial", 12),
            bg="white",
        ).grid(row=0, column=i + 1)

    tk.Label(
        popup_frame, text="Tipo de instrucción:", font=("Arial", 12), bg="white"
    ).grid(row=1, column=0, sticky="w")
    instructions = ["CALC", "READ", "WRITE"]
    for i, instruction in enumerate(instructions):
        tk.Radiobutton(
            popup_frame,
            text=instruction,
            variable=instruction_var,
            value=instruction,
            font=("Arial", 12),
            bg="white",
        ).grid(row=1, column=i + 1)

    tk.Label(
        popup_frame,
        text="Dirección de memoria (000-111):",
        font=("Arial", 12),
        bg="white",
    ).grid(row=2, column=0, sticky="w")

    address_entry.grid(row=2, column=1)

    tk.Label(
        popup_frame,
        text="Dato hexadecimal (0000-ffff):",
        font=("Arial", 12),
        bg="white",
    ).grid(row=3, column=0, sticky="w")

    data_entry.grid(row=3, column=1)

    submit_button = tk.Button(
        popup_frame,
        image=generate_instruction_photoimage,
        bg="white",
        command=submit,
        borderwidth=0,
    )
    submit_button.grid(row=3, column=3)

    main.wait_window(popup_win)


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

bus_dict_quantity = {
    "000": 0,
    "001": 0,
    "010": 0,
    "011": 0,
    "100": 0,
    "101": 0,
    "110": 0,
    "111": 0,
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

memory_frame = tk.Frame(botton_frame, bg="white", height=100, width=330)
memory_frame.place(x=0, y=0)

buttons_frame = tk.Frame(botton_frame, bg="white", height=100, width=160)
buttons_frame.place(x=330, y=0)

console_frame = tk.Frame(botton_frame, bg="white", height=100, width=410)
console_frame.place(x=490, y=0)

# --------------- Componenents ----------------------------------------

# Consola

console_text = scrolledtext.ScrolledText(
    console_frame, wrap=tk.WORD, width=55, height=6, font=("Arial", 10)
)
console_text.grid(column=0, pady=0, padx=0)
console_text["state"] = "disabled"


# ----------------------------Botones----------------------------------
generate_instruction_photoimage = tk.PhotoImage(
    file=r"P1_Cache\\images\button_generar-instruccion.png"
)
generate_instruction_button = tk.Button(
    buttons_frame,
    image=generate_instruction_photoimage,
    command=open_popup,
    bg="white",
    borderwidth=0,
)


single_cycle_photoimage = tk.PhotoImage(file=r"P1_Cache\\images\button_ciclo-unico.png")
single_cycle_button = tk.Button(
    buttons_frame,
    image=single_cycle_photoimage,
    command=manualGlobalCycle,
    bg="white",
    borderwidth=0,
)


loop_photoimage_detener = tk.PhotoImage(
    file=r"P1_Cache\\images\button_detener-ciclo.png"
)
loop_photoimage_iniciar = tk.PhotoImage(
    file=r"P1_Cache\\images\button_iniciar-ciclo.png"
)

loop_photoimage = loop_photoimage_detener if loopCyclesFlag else loop_photoimage_iniciar


loop_button = tk.Button(
    buttons_frame,
    image=loop_photoimage,
    command=changeLoopFlag,
    bg="white",
    borderwidth=0,
)


reset_photoimage = tk.PhotoImage(file=r"P1_Cache\\images\button_reiniciar.png")
reset_button = tk.Button(
    buttons_frame,
    image=reset_photoimage,
    command=resetProgram,
    bg="white",
    borderwidth=0,
)

generate_instruction_button.place(x=2, y=2)
loop_button.place(x=2, y=35)
reset_button.place(x=2, y=68)
single_cycle_button.place(x=75, y=68)

# ----------------------------Memoria----------------------------------

create_memory_table(memory_frame, ("Arial", 12), "white")


# ----------------------------CPU labels----------------------------------

render_CPU_info()


main.protocol("WM_DELETE_WINDOW", close_app)


main.mainloop()
