import tkinter as tk
import json
with open("Lube/config.json", "r") as file:
    configfile = json.load(file)
maincolor = configfile["main_color"]
def cycle_color_button1():
    global color_index1
    color_index1 = (color_index1 + 1) % len(colors)
    cycle_button1.config(bg=colors[color_index1])
def cycle_color_button2():
    global color_index2
    color_index2 = (color_index2 + 1) % len(colors)
    cycle_button2.config(bg=colors[color_index2])
def print_and_close():
    print(f"Main color: {colors[color_index1]}")
    print(f"Selected color: {colors[color_index2]}")
    print("Attempting to save...")
    save()
    print("Attempting to close...")
    root.quit()
def save():
    with open("Lube/config.json", "r") as file:
        config = json.load(file)
    config["main_color"] = colors[color_index1]
    config["selected_color"] = colors[color_index2]
    with open("Lube/config.json", "w") as file:
        json.dump(config, file, indent=4)
    print("Configuration updated!")
root = tk.Tk()
rwidth = root.winfo_width()
rheight = root.winfo_height()
root.geometry("400x300")
root.iconbitmap("Lube/source/icon.ico")
root.title("Change main color and the selected color")
mainframe = tk.Frame(root, background=maincolor)
mainframe.place(width=400, height=300)
colors = ["red", "orange", "yellow", "lightgreen", "green", "lightblue", "blue", "pink", "purple", "chocolate", "black", "white"]
print(colors)
color_index1 = 0
color_index2 = 0
cycle_button1 = tk.Button(mainframe, text="Main Color", bg=colors[color_index1], font=("Fredoka"), command=cycle_color_button1)
cycle_button1.pack(pady=20, ipadx=20, ipady=10)
cycle_button2 = tk.Button(mainframe, text="Selected Color", bg=colors[color_index2], font=("Fredoka"), command=cycle_color_button2)
cycle_button2.pack(pady=20, ipadx=20, ipady=10)
print_button = tk.Button(mainframe, text="Done", font=("Fredoka"), background=maincolor, command=print_and_close)
print_button.pack(pady=20, ipadx=20, ipady=10)
root.mainloop()
