import os
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog

# create a function to read the bone indexes and names from a file
def read_bone_indexes(filename):
    # create an empty dictionary to store the bone indexes and names
    bone_indexes = {}
    # get the absolute path of the filename
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    # open the file in read mode
    with open(filename) as file:
        # loop through each line in the file
        for line in file:
            # split the line by whitespace
            parts = line.split()
            # check if the line has three parts
            if len(parts) == 3:
                # get the index, name, and parent from the line
                index = int(parts[0])
                name = parts[1].strip('"')
                parent = int(parts[2])
                # add the index and name to the dictionary
                bone_indexes[index] = name
    # return the dictionary
    return bone_indexes

# create a function to read the default bone names and flags from a file
def read_default_bones(filename):
    # create an empty dictionary to store the default bone names and flags
    default_bones = {}
    # get the absolute path of the filename
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    # open the file in read mode
    with open(filename) as file:
        # loop through each line in the file
        for line in file:
            # strip the newline character from the line
            line = line.strip()
            # check if the line is not empty and has a colon
            if line and ':' in line:
                # split the line by colon
                name, flag = line.split(':')
                # convert the flag to an integer (0 or 1)
                flag = int(flag)
                # add the name and flag to the dictionary
                default_bones[name] = flag
    # return the dictionary
    return default_bones

# read the bone indexes and names from a file named bone_indexes.txt
boneIndexes = read_bone_indexes("bone_indexes.txt")

# read the default bone names and flags from a file named default_bones.txt
defaultBones = read_default_bones("default_bones.txt")

def run_script():
    if multiplier_entry.get() == "":
        tkinter.messagebox.showerror("Error", "Please enter a value for the multiplier.")
        return

    if add_entry.get() == "":
        tkinter.messagebox.showerror("Error", "Please enter a value for the Vertical Offset.")
        return

    multiplier = float(multiplier_entry.get())
    add = float(add_entry.get())
    
    smd_dir = tkinter.filedialog.askdirectory(title="Select smd directory")
    if smd_dir:
        smd_files = [f for f in os.listdir(smd_dir) if f.endswith(".smd")]
    else:
        tkinter.messagebox.showerror("Error", "No directory selected.")
        return
    
    # create a list of selected indexes from the checkbuttons
    selected_indexes = []
    for i in boneIndexes:
        if bone_vars[i].get() == 1:
            selected_indexes.append(i)
    
    for smd_file in smd_files:
        f = open(os.path.join(smd_dir,smd_file), "r")
        new_lines = []
        for line in f:
            try:
                l = [float(x) for x in line.replace("\n","").split()]
            except:
                new_lines.append(line.replace("\n",""))
                continue
            
            # check if the index is in the selected list
            if  round(l[0]) not in selected_indexes:
                new_lines.append(line.replace("\n",""))
                continue
            
            if len(l) == 7:
                l[1] *= multiplier
                l[2] *= multiplier
                # check if the bone name is in the default bones dictionary and has a flag of 1
                if boneIndexes[round(l[0])] in defaultBones and defaultBones[boneIndexes[round(l[0])]] == 1:
                    # apply the add to l[3]
                    l[3] = l[3] * multiplier + add
            
            new_lines.append(format(l[0],'.0f')+" "+" ".join([format(x,'.6f') for x in l[1:7]]))
                
        f.close()
        f = open(os.path.join(smd_dir,smd_file), "w")
        f.write("\n".join(new_lines))
        f.close()
    
    tk.messagebox.showinfo("Done", f"The script has modified {len(smd_files)} files.")

window = tk.Tk()
window.resizable(False, False)
window.title("Scale and Translate animation bones")

multiplier_label = tk.Label(window, text="Multiplier:")
multiplier_entry = tk.Entry(window)
add_label = tk.Label(window, text="Vertical Offset:")
add_entry = tk.Entry(window)
run_button = tk.Button(window, text="Modify .smd files", command=run_script)

multiplier_label.grid(row=0, column=0, padx=10, pady=10)
multiplier_entry.grid(row=0, column=1, padx=10, pady=10)
add_label.grid(row=1, column=0, padx=10, pady=10)
add_entry.grid(row=1, column=1, padx=10, pady=10)
run_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# create a frame to hold the checkbuttons
check_frame = tk.Frame(window)
check_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# create a dictionary of checkbutton variables
bone_vars = {}
for i in boneIndexes:
    bone_vars[i] = tk.IntVar()

# create checkbuttons for each bone index and name
# use a grid layout with 4 columns and 15 rows
for i in boneIndexes:
    check = tk.Checkbutton(check_frame, text=boneIndexes[i], variable=bone_vars[i])
    check.grid(row=i//4, column=i%4, sticky=tk.W)

# create a function to toggle the visibility of the checkbuttons
def toggle_checkbuttons():
    global hidden
    if hidden:
        # show the checkbuttons
        check_frame.grid()
    else:
        # hide the checkbuttons
        check_frame.grid_remove()
    hidden = not hidden

# create a variable to store the hidden state
hidden = False
toggle_checkbuttons()
# create a toggle button to control the checkbuttons
toggle_button = tk.Button(window, text="Advanced Parameters", command=toggle_checkbuttons)
toggle_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# set the default bone indexes to be checked by default
# by finding the index of the bone name in the boneIndexes dictionary
for bone in defaultBones:
    for i in boneIndexes:
        if boneIndexes[i] == bone:
            bone_vars[i].set(1)
            break

window.mainloop()
