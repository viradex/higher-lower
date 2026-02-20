import tkinter as tk
from tkinter import ttk, messagebox

from logic import HigherLower, Player


def submit_guess(guess, higher_lower):
    pass


def main():
    higher_lower = HigherLower()
    card = higher_lower.draw_card()
    multiplier = higher_lower.calc_multiplier()

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

    card = tk.PhotoImage(file=higher_lower.get_card_resource_location(card))
    ttk.Label(frame, image=card).grid(
        row=1, column=0, sticky="SE", pady=(10, 20), padx=5
    )

    house_card = tk.PhotoImage(file=higher_lower.get_card_resource_location("", True))
    ttk.Label(frame, image=house_card).grid(
        row=1, column=2, sticky="SW", pady=(10, 20), padx=5
    )

    buttons = {
        "higher": ttk.Button(
            frame,
            text=f"Higher (x{multiplier["higher"]})",
            command=lambda: submit_guess("higher", higher_lower),
        ),
        "lower": ttk.Button(
            frame,
            text=f"Lower (x{multiplier["lower"]})",
            command=lambda: submit_guess("lower", higher_lower),
        ),
        "same": ttk.Button(
            frame,
            text=f"Same (x{multiplier["same"]})",
            command=lambda: submit_guess("same", higher_lower),
        ),
    }

    btn_format_counter = 0
    for button in buttons:
        buttons[button].grid(
            row=2, column=btn_format_counter, sticky="EW", pady=10, padx=2
        )
        buttons[button].grid_configure(ipady=15)

        btn_format_counter += 1

    if multiplier["higher"] <= 0:
        buttons["higher"].config(state="disabled")
    if multiplier["lower"] <= 0:
        buttons["lower"].config(state="disabled")

    root.mainloop()


if __name__ == "__main__":
    main()
