import tkinter as tk

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

memory_frame = tk.Frame(main_frame, bg="OrangeRed", height=100, width=900)
memory_frame.place(x=0, y=400)

main.mainloop()
