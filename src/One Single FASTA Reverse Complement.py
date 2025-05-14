import os
import textwrap
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def run_pipeline(input_file, program_mode, progress_bar):
    try:
        # Start the progress bar
        progress_bar.start()

        # Create an output file
        if program_mode == "reverse":
            output_file = f"{os.path.splitext(input_file)[0]}.rev.fa"
        elif program_mode == "complement":
            output_file = f"{os.path.splitext(input_file)[0]}.comp.fa"
        else:
            output_file = f"{os.path.splitext(input_file)[0]}.revcomp.fa"

        # Create output file to appear
        output_file_fixed = str(output_file).replace("/","\\")

        # Insert fasta file
        file = open(input_file, 'r')

        # Stripe leading and trailing characters in each line
        lines = list(map(lambda line: str(line).strip(), file))

        # Close the file
        file.close()

        # Retrieve the header
        header = f"{lines[0]} ({program_mode})"

        # Retrieve the sequence
        seq = "".join(lines[1:]).upper()

        # Retrieve input fasta width
        fasta_width = len(lines[1]) if len(lines[1]) <= 80 else 80

        # Option to reverse sequence
        reversed_seq = seq[::-1] if "reverse" in program_mode else seq

        # Create complement map
        if "complement" in program_mode:
            complement_map = {"A": "T", "T": "A", "C": "G", "G": "C", "R": "Y", "Y": "R", "S": "S", "W": "W", "K": "M", "M": "K", "B": "V", "D": "H", "H": "D", "V": "B", "N": "N"}
            converted_seq = "".join(map(lambda base: complement_map.get(base, base), list(reversed_seq)))
        
        # Wrap by fasta width
        if program_mode=="reverse":
            wrapped_seq = textwrap.fill(reversed_seq, width=fasta_width)
        else:
            wrapped_seq = textwrap.fill(converted_seq, width=fasta_width)
            
        # Export to fasta
        with open(output_file,'w') as f:
            f.writelines(f"{header}\n{wrapped_seq}\n")

        progress_bar.stop()
        messagebox.showinfo("Success", f"Program run in {program_mode} mode.\nConverted sequence saved at: {output_file_fixed}")

    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("Error", str(e))
        
def start_thread():
    input_file = input_file_var.get()
    program_mode = mode_var.get()

    if not input_file:
        messagebox.showwarning("Input Error", "Please select an input file.")
        return
    
    # Start command in a new thread
    thread = threading.Thread(target=run_pipeline, args=(input_file, program_mode, progress_bar))
    thread.start()

def select_file():
    file_path = filedialog.askopenfilename()
    input_file_var.set(file_path)

# Set up tkinter app
app = tk.Tk()
app.title("One Single FASTA Reverse and/or Complement")

# Input file selection
input_file_var = tk.StringVar()
tk.Label(app, text="Input file:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(app, textvariable=input_file_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# Fasta width selection
tk.Label(app, text="Program mode:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
mode_var = tk.StringVar(value="reverse complement")
mode_options = ["reverse", "complement", "reverse complement"]
mode_dropdown = tk.OptionMenu(app, mode_var, *mode_options)
mode_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Progress Bar (indeterminate)
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=200)
progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=20)

# Start button
tk.Button(app, text="Run program", command=start_thread).grid(row=3, column=1, padx=10, pady=20)

app.mainloop()
