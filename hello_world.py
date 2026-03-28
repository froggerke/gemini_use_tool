import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Hello World")
    root.geometry("800x600")

    label = tk.Label(root, text="hello world", font=("Arial", 32))
    label.pack(expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
