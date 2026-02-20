import tkinter as tk
from tkinter import ttk, messagebox


def main():
    root = tk.Tk()
    root.title("Higher or Lower")
    root.geometry("800x600")
    root.resizable(False, False)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    frame = ttk.Frame(root, padding=12)
    frame.grid(row=0, column=0, sticky="NSEW")

    for i in range(3):
        frame.grid_columnconfigure(i, weight=1, uniform="equal")

    ttk.Label(frame, text="Money: $500", font=("Helvetica", 16, "bold")).grid(
        row=0, column=0, sticky="W", pady=5, padx=5
    )
    ttk.Label(frame, text="Streak: 0", font=("Helvetica", 16, "bold")).grid(
        row=0, column=2, sticky="E", pady=5, padx=5
    )

    card = tk.PhotoImage(file="assets/a/AH.png")
    ttk.Label(frame, image=card).grid(
        row=1, column=1, sticky="S", pady=(10, 20), padx=5
    )

    buttons = {
        "higher": ttk.Button(frame, text="Higher (x??)", command=lambda: print("stub")),
        "lower": ttk.Button(frame, text="Lower (x??)", command=lambda: print("stub")),
        "same": ttk.Button(frame, text="Same (x13)", command=lambda: print("stub")),
    }

    btn_format_counter = 0
    for button in buttons:
        buttons[button].grid(
            row=2, column=btn_format_counter, sticky="EW", pady=10, padx=2
        )
        buttons[button].grid_configure(ipady=15)

        btn_format_counter += 1

    root.mainloop()


if __name__ == "__main__":
    main()
