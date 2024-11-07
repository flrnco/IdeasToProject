import time    							# To measure time performance
import sys
import numpy as np
import tkinter as tk
from utils import *


# Build the main window and launch the chat
window = tk.Tk()
window.title("Turn your ideas into projects")

# Set window size to be twice as large as its default size
default_width = 400  # initial assumed width
default_height = 300  # initial assumed height
new_width = default_width * 2
new_height = default_height * 2
window.geometry(f"{new_width}x{new_height}")

# Configure grid to expand with window resizing
window.grid_rowconfigure(1, weight=1)  # Make row with chat canvas expand
window.grid_columnconfigure(0, weight=1)  # Make chat canvas expand horizontally

# Add a title label
title_label = tk.Label(window, text="Turn your ideas into projects", bg="#25D366", fg="white", font=("Helvetica", 16, "bold"), pady=10)
title_label.grid(row=0, column=0, columnspan=2, sticky="ew")

# Create a chat frame with a scroll bar
chat_canvas = tk.Canvas(window, bg="#ECE5DD")
chat_scrollbar = tk.Scrollbar(window, orient="vertical", command=chat_canvas.yview)
chat_frame = tk.Frame(chat_canvas, bg="#ECE5DD")

# Configure the canvas to use the chat_frame as a scrollable window
chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")
chat_canvas.configure(yscrollcommand=chat_scrollbar.set)

# Place the chat canvas and scrollbar in a grid layout
chat_canvas.grid(row=1, column=0, columnspan=2, sticky="nsew")
chat_scrollbar.grid(row=1, column=2, sticky="ns")

# Bind configuration to dynamically adjust the chat frame size
chat_frame.bind("<Configure>", lambda event: on_frame_configure(event, chat_canvas))

# Create the input field for user messages
entry = tk.Entry(window, width=80, font=("Helvetica", 12))  # Adjust width for larger window
entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Bind the "Enter" key to the send_message function
entry.bind("<Return>", lambda event: send_message(entry, chat_frame, chat_canvas))

# Send button
send_button = tk.Button(window, text="Send", command=lambda: send_message(entry, chat_frame, chat_canvas),
                        font=("Helvetica", 12), bg="#25D366", fg="white")
send_button.grid(row=2, column=1, padx=10, pady=10)

# Display initial bot message
display_initial_message(chat_frame, chat_canvas)

# Main loop
window.mainloop()


#"voici un exemple de description de projet :
#XXXX
#Peux-tu évaluer la qualité/complétude de ce descriptif projet et me poser des questions me permettant de l'améliorer ?"

