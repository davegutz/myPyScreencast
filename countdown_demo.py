import tkinter as tk


def job():
    status.config(text="starting job")


def countdown(time, msg='Counting down'):
    time -= 1
    status.config(text=f'{msg} ({time}sec)')

    if time != 0:
        root.after(1000, countdown, time)

    else:
        job()  # if job is blocking then create a thread


root = tk.Tk()

status = tk.Label(root)
status.pack()

countdown(5)

root.mainloop()
