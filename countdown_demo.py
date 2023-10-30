import tkinter as tk


def record():
    b.config(text="starting job")


def start():
    b.config(text="counting down")
    msg = 'Counting down'
    print(f"countdown {time.get()=}")
    time.set(time.get() - 1)
    # counter.withdraw()
    # counter.deiconify()
    status.config(text=f'{msg} ({time.get()}sec)')
    if time.get() != 0:
        root.after(1000, start)
    else:
        counter.withdraw()
        record()  # if job is blocking then create a thread


root = tk.Tk()
counter = tk.Tk()
counter.attributes('-topmost', True)
time = tk.IntVar(root, 5)

a = tk.Button(root, text="Click This", command=start)
a.pack()
b = tk.Label(root, text="Gross steps show here")
b.pack()

status = tk.Label(counter)
status.pack()

root.mainloop()
counter.mainloop()
