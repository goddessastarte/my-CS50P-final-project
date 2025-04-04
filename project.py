import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt


def main():
    window = tk.Tk()
    window.title("Relative Strength Index")
    window.config(bg="black")
    window.geometry("700x500")

    frame = tk.Frame(master=window, bg="black")
    frame.pack()

    btn1 = tk.Button(
        master=frame,
        text="Compare",
        font=("OCR A Extended", 12, "bold"),
        bg="black",
        fg="white",
        activebackground="black",
        activeforeground="white",
        command=lambda: clicked(btn1, frame))

    btn1.pack()

    tk.Button(
        frame,
        text="Instructions",
        command=show_instructions,
        bg="black",
        fg="white"
    ).pack(pady=5)

    window.mainloop()


already_clicked = False


def clicked(btn, frame):
    global already_clicked

    if already_clicked:
        tk.messagebox.showinfo(
            "error", "You already clicked this button!\nplease enter the information needed")
        return
    already_clicked = True

    print(btn, "was clicked")
    btn.config(bg="#7FFF00", fg="black")
    title = tk.Label(
        frame,
        text="hi pls enter 2 to 3 CSV files",
        font=("OCR A Extended", 12, "bold"),
        bg="black",
        fg="white")
    title.pack(pady=5)
    button = tk.Button(
        frame,
        text="choose file",
        font=("OCR A Extended", 12, "bold"),
        bg="black",
        fg="white",
        command=lambda: upload_files(frame))
    button.pack()


name_entries = []


def upload_files(frame):
    global name_entries
    filepath = filedialog.askopenfilenames(
        title="Select csv file",
        filetypes=[("CSV files", "*.csv")]
    )

    if not (2 <= len(filepath) <= 3):
        tk.messagebox.showinfo("Error", "Please select 2 or 3 files only.")
        return

    name_entries.clear()

    for path in filepath:
        label = tk.Label(
            frame,
            text=f"Name for {path.split('/')[-1]}:",
            font=("OCR A Extended", 10),
            fg="white",
            bg="black"
        )
        label.pack()

        entry = tk.Entry(frame, font=("Courier New", 10))
        entry.pack(pady=2)

        name_entries.append((path, entry))
    print(name_entries)
    tk.Button(
        frame,
        text="Compare Now",
        font=("OCR A Extended", 12, "bold"),
        bg="#7FFF00",
        fg="black",
        command=lambda: compare_files(name_entries)
    ).pack(pady=10)


def prepare_df_from_df(df, coin_name):
    df["date"] = pd.to_datetime(df["snapped_at"].str.replace(" UTC", ""))
    df = df[["date", "price"]]
    df = df.rename(columns={"price": coin_name})
    return df


def compare_files(name_entries):

    prepared = []

    for path, entry in name_entries:
        coin_name = entry.get().strip()
        if coin_name == "":
            tk.messagebox.showinfo("Error", "Please enter names for all files.")
            return
        try:
            df = pd.read_csv(path)
            cleaned = prepare_df_from_df(df, coin_name)
            prepared.append(cleaned)
        except Exception as e:
            tk.messagebox.showinfo("Error", f"Failed to load {path}: {e}")
            return

    merged = merge_df(prepared)
    normalized = normalized_df(merged)

    plt.figure(figsize=(12, 6))
    for coin in normalized.columns[1:]:
        plt.plot(normalized["date"], normalized[coin], label=coin)
    plt.title("Relative Strength of Coins (Starting at 100)")
    plt.xlabel("Date")
    plt.ylabel("Normalized Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def merge_df(prepared):
    merged = prepared[0]
    for df in prepared[1:]:
        merged = merged.merge(df, on="date", how="inner")
    return merged

def normalized_df(merged):
    normalized = merged.copy()
    for coin in normalized.columns[1:]:
        normalized[coin] = normalized[coin] / normalized[coin].iloc[0] * 100
    return normalized

def show_instructions():
    popup = tk.Toplevel()
    popup.title("Instructions")
    popup.geometry("700x300")
    popup.config(bg="black")

    text = (
        "Instructions\n\n"
        "1. Click the 'Compare' button.\n"
        "2. Upload 2 or 3 CSV files of crypto data.\n"
        "   - Each file must have columns: 'snapped_at' and 'price'.\n"
        "   - Recommended: Download CSVs from CoinGecko (they match the expected format).\n"
        "3. For each file, type the name of the coin.\n"
        "4. Click 'Compare Now' to see the chart.\n\n"
        "This shows how each coin performed over time, normalized to 100.\n"
        "Tip: Use clean CSVs with consistent timestamps.\n"
        "Don't upload incomplete or unrelated files.\n"
    )

    label = tk.Label(popup, text=text, justify="left", font=(
        "Courier New", 10, "bold"), fg="white", bg="black")
    label.pack(padx=20, pady=20)

    tk.Button(popup, text="Close", command=popup.destroy, bg="#7FFF00", fg="black").pack(pady=10)

if __name__ == "__main__":
    main()
