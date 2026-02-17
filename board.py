import tkinter as tk

root = tk.Tk()

content = tk.Frame(root)
content.grid(column=0, row=0)

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
for i in range(8):
    tk.Label(content, text=str(i)).grid(row=i+1, column=0)
    tk.Label(content, text=letters[i]).grid(row=0, column=i+1)

for ligne in range(8):
    for colonne in range(8):
        frame = tk.Frame(content, width=50, height=50, bg="green", borderwidth=1, relief="solid").grid(row=ligne+1, column=colonne+1)


root.mainloop()