import tkinter as tk


def record():
    count_down_label.config(text="starting job")


# After 'pushing the button' display countdown to give time to set up full screen etc
def start():
    count_down_label.config(text="counting down")
    msg = 'Counting down'
    print(f"countdown {time.get()=}")
    time.set(time.get() - 1)
    status.config(text=f'{msg} ({time.get()}sec)')
    if time.get() != 0:
        root.after(1000, start)
    else:
        counter.withdraw()
        record()  # if job is blocking then create start_button thread


root = tk.Tk()
counter = tk.Tk()
counter.attributes('-topmost', True)
time = tk.IntVar(root, 5)

start_button = tk.Button(root, text="Click This", command=start)
start_button.pack()
count_down_label = tk.Label(root, text="Gross steps show here")
count_down_label.pack()

status = tk.Label(counter)
status.pack()

root.mainloop()
counter.mainloop()
