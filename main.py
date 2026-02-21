import tkinter as tk
from tkinter import ttk, messagebox

from logic import HigherLower, Player

ENABLE_CHEATS = False

keypress_code = [
    "Up",
    "Up",
    "Down",
    "Down",
    "Left",
    "Right",
    "Left",
    "Right",
    "b",
    "a",
    "Return",
]
pressed_keys = []


def submit_guess(guess, higher_lower, player):
    pass


def change_card_img(label, path):
    new_img = tk.PhotoImage(file=path)
    label.config(image=new_img)
    label.image = new_img


def enable_disable_btn(enable, buttons):
    if enable:
        buttons["higher"].config(state="normal")
        buttons["lower"].config(state="normal")
        buttons["same"].config(state="normal")
    else:
        buttons["higher"].config(state="disabled")
        buttons["lower"].config(state="disabled")
        buttons["same"].config(state="disabled")


def show_hide_multipliers(show, buttons, multipliers):
    if show:
        buttons["higher"].config(text=f"Higher (x{multipliers["higher"]})")
        buttons["lower"].config(text=f"Lower (x{multipliers["lower"]})")
        buttons["same"].config(text=f"Same (x{multipliers["same"]})")

        for multiplier in multipliers:
            if multipliers[multiplier] <= 0:
                buttons[multiplier].config(state="disabled")
    else:
        buttons["higher"].config(text="Higher")
        buttons["lower"].config(text="Lower")
        buttons["same"].config(text="Same")


def check_cheat_code(event, label, player):
    pressed_keys.append(event.keysym)

    if len(pressed_keys) > len(keypress_code):
        pressed_keys.pop(0)

    if pressed_keys == keypress_code and ENABLE_CHEATS:
        player.increase_balance(500)
        pressed_keys.clear()

        print("Increased balance by $500!")
        label.config(text=f"Balance: ${player.balance}")


def main():
    higher_lower = HigherLower()
    player = Player()

    card = higher_lower.draw_card()
    multiplier = higher_lower.calc_multiplier()

    root = tk.Tk()
    root.title("Higher or Lower")
    root.geometry("800x600")
    root.resizable(False, False)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    btn_style = ttk.Style()
    btn_style.configure("TButton", font=("Helvetica", 12))

    bet_var = tk.StringVar(value="100")

    frame = ttk.Frame(root, padding=12)
    frame.grid(row=0, column=0, sticky="NSEW")

    for i in range(3):
        frame.grid_columnconfigure(i, weight=1, uniform="equal")

    balance_label = ttk.Label(
        frame, text=f"Balance: ${player.balance}", font=("Helvetica", 16, "bold")
    )
    balance_label.grid(row=0, column=0, sticky="W", pady=5, padx=5)

    streak_label = ttk.Label(frame, text="Streak: 0", font=("Helvetica", 16, "bold"))
    streak_label.grid(row=0, column=2, sticky="E", pady=5, padx=5)

    ttk.Label(frame, text="Your Card", font=("Helvetica", 12)).grid(
        row=1, column=0, sticky="S", pady=(10, 2), padx=5
    )
    ttk.Label(frame, text="Dealer's Card", font=("Helvetica", 12)).grid(
        row=1, column=2, sticky="W", pady=(10, 2), padx=5
    )

    player_card = tk.PhotoImage(file=higher_lower.get_card_img_path("", True))
    player_card_label = ttk.Label(frame, image=player_card)
    player_card_label.grid(row=2, column=0, sticky="SE", pady=(10, 20), padx=5)

    dealer_card = tk.PhotoImage(file=higher_lower.get_card_img_path("", True))
    dealer_card_label = ttk.Label(frame, image=dealer_card)
    dealer_card_label.grid(row=2, column=2, sticky="SW", pady=(10, 20), padx=5)

    buttons = {
        "higher": ttk.Button(
            frame,
            text=f"Higher",
            command=lambda: submit_guess("higher", higher_lower, player),
            style="TButton",
            state="disabled",
        ),
        "lower": ttk.Button(
            frame,
            text=f"Lower",
            command=lambda: submit_guess("lower", higher_lower, player),
            style="TButton",
            state="disabled",
        ),
        "same": ttk.Button(
            frame,
            text=f"Same",
            command=lambda: submit_guess("same", higher_lower, player),
            style="TButton",
            state="disabled",
        ),
    }

    btn_format_counter = 0
    for button in buttons:
        buttons[button].grid(
            row=3, column=btn_format_counter, sticky="EW", pady=10, padx=2
        )
        buttons[button].grid_configure(ipady=15)

        btn_format_counter += 1

    bet_amount = ttk.Entry(frame, textvariable=bet_var, font=("Helvetica", 14))
    bet_amount.grid(row=5, column=0, columnspan=2, sticky="EW", pady=10)

    line = tk.Frame(frame, height=1, width=400, bg="lightgrey")
    line.grid(row=4, column=0, columnspan=3, sticky="EW", pady=20)

    def submit_bet(_=None):
        bet = bet_var.get().strip()

        if bet.startswith("$"):
            bet = bet[1:]

        if not bet:
            messagebox.showerror("Invalid Bet", "Please enter a bet amount.")
            return
        elif player.currently_betting:
            messagebox.showwarning(
                "Bet in Progress",
                "You are currently betting. Please complete the bet before making a new one.",
            )
            return
        elif not bet.isdigit():
            messagebox.showerror(
                "Invalid Bet",
                "Bet must be a non-negative whole number (no decimals or symbols).",
            )
            return
        elif int(bet) < player.min_bet:
            messagebox.showerror(
                "Invalid Bet",
                f"Bet amount must be at least ${player.min_bet}, but you entered ${bet}. Please increase the amount.",
            )
            return
        elif not player.validate_bet(int(bet)):
            messagebox.showerror(
                "Invalid Bet",
                f"The bet amount exceeds the available balance of ${player.balance}.",
            )
            return

        player.place_bet(int(bet))
        balance_label.config(text=f"Balance: ${player.balance}")

        enable_disable_btn(True, buttons)
        show_hide_multipliers(True, buttons, multiplier)
        change_card_img(
            player_card_label,
            higher_lower.get_card_img_path(higher_lower.current_card_suit),
        )

    bet_btn = ttk.Button(
        frame,
        text="Submit Bet",
        command=submit_bet,
        style="TButton",
    )
    bet_btn.grid(row=5, column=2, sticky="EW", pady=10, padx=(10, 2))

    bet_amount.bind("<Return>", submit_bet)
    root.bind("<KeyPress>", lambda e: check_cheat_code(e, balance_label, player))

    root.mainloop()


if __name__ == "__main__":
    main()
