import tkinter as tk
from tkinter import ttk, messagebox

from logic import HigherLower, Player
from gamestate import GameState

root = tk.Tk()
higher_lower = HigherLower()
player = Player()
gs = GameState(player)

multiplier = {}


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


def show_hide_multipliers(show, buttons, multipliers={}):
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


def reset(buttons, player_label, dealer_label, balance_label, streak_label):
    global multiplier

    enable_disable_btn(False, buttons)
    show_hide_multipliers(False, buttons)

    change_card_img(player_label, higher_lower.get_card_img_path("", True))
    change_card_img(dealer_label, higher_lower.get_card_img_path("", True))

    higher_lower.reset_game()
    player.reset_bet()

    higher_lower.draw_card()
    higher_lower.draw_hidden_card()
    multiplier = higher_lower.calc_multiplier()

    balance_label.config(text=f"Balance: ${player.balance}")
    streak_label.config(text=f"Streak: {player.streak}")


def restart(buttons, player_label, dealer_label, balance_label, streak_label):
    higher_lower.reset_game()
    player.reset_game()

    gs.reset_all()
    reset(buttons, player_label, dealer_label, balance_label, streak_label)


def submit_guess(
    guess, multipliers, buttons, balance_label, player_label, dealer_label, streak_label
):
    if not player.currently_betting:
        return

    change_card_img(
        dealer_label,
        higher_lower.get_card_img_path(higher_lower.current_hidden_card_suit),
    )

    correct = higher_lower.make_guess(guess)
    gs.resolve_round(
        correct,
        player.bet,
        multipliers[guess],
        guess,
        higher_lower.current_card,
        higher_lower.current_hidden_card,
    )

    for attribute, value in vars(gs).items():
        print(f"* {attribute}: {value}")
    print()

    if correct:
        amount = player.update_balance(multipliers[guess])
        player.increase_streak()

        balance_label.config(text=f"Balance: ${player.balance}")
        streak_label.config(text=f"Streak: {player.streak}")

        messagebox.showinfo(
            "Betting Result", f"You guessed correctly and made ${amount}!"
        )

        player.done_bet()
    else:
        player.reset_streak()
        streak_label.config(text=f"Streak: {player.streak}")

        messagebox.showinfo("Betting Result", "You guessed incorrectly.")

    if player.is_bankrupt():
        confirm_restart = messagebox.askyesno(
            "Game Over",
            "You are bankrupt and can't make any more bets! Would you like to restart?",
            default="yes",
        )

        if not confirm_restart:
            root.destroy()
            exit(0)

        restart(buttons, player_label, dealer_label, balance_label, streak_label)

    reset(buttons, player_label, dealer_label, balance_label, streak_label)


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

player_card = tk.PhotoImage(file="")
player_card_label = ttk.Label(frame, image=player_card)
player_card_label.grid(row=2, column=0, sticky="SE", pady=(10, 20), padx=5)

dealer_card = tk.PhotoImage(file="")
dealer_card_label = ttk.Label(frame, image=dealer_card)
dealer_card_label.grid(row=2, column=2, sticky="SW", pady=(10, 20), padx=5)

buttons = {
    "higher": ttk.Button(
        frame,
        text=f"Higher",
        command=lambda: submit_guess(
            "higher",
            multiplier,
            buttons,
            balance_label,
            player_card_label,
            dealer_card_label,
            streak_label,
        ),
        style="TButton",
    ),
    "lower": ttk.Button(
        frame,
        text=f"Lower",
        command=lambda: submit_guess(
            "lower",
            multiplier,
            buttons,
            balance_label,
            player_card_label,
            dealer_card_label,
            streak_label,
        ),
        style="TButton",
    ),
    "same": ttk.Button(
        frame,
        text=f"Same",
        command=lambda: submit_guess(
            "same",
            multiplier,
            buttons,
            balance_label,
            player_card_label,
            dealer_card_label,
            streak_label,
        ),
        style="TButton",
    ),
}

btn_format_counter = 0
for button in buttons:
    buttons[button].grid(row=3, column=btn_format_counter, sticky="EW", pady=10, padx=2)
    buttons[button].grid_configure(ipady=15)

    btn_format_counter += 1

bet_amount = ttk.Entry(frame, textvariable=bet_var, font=("Helvetica", 14))
bet_amount.grid(row=5, column=0, columnspan=2, sticky="EW", pady=10)

line = tk.Frame(frame, height=1, width=400, bg="lightgrey")
line.grid(row=4, column=0, columnspan=3, sticky="EW", pady=20)


def copy_balance(_):
    bet_amount.delete(0, tk.END)
    bet_amount.insert(0, str(player.balance))


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
    text="Place Bet",
    command=submit_bet,
    style="TButton",
)
bet_btn.grid(row=5, column=2, sticky="EW", pady=10, padx=(10, 2))

balance_label.bind("<Button-1>", copy_balance)
bet_amount.bind("<Return>", submit_bet)

reset(buttons, player_card_label, dealer_card_label, balance_label, streak_label)
root.mainloop()
