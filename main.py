#
#

#
# # def add_word_window():
# #     add = tk.Toplevel(root)
# #     add.title("Add words")
# #     add.geometry("300x150")
# #     Label(add, text="Add Words to the database").pack(pady=10)
# #     word_entry = tk.Entry(add)
# #     word_entry.pack(pady=10)
# #
# #     def add_word():
# #         word = word_entry.get().strip().title()
# #
# #         if not word:
# #             messagebox.showerror("Error", "A valid word is required")
# #             return
# #         else:
# #             conn = sqlite3.connect("monkeywords.db")
# #             cursor =conn.cursor()
# #             cursor.execute("INSERT INTO monkeywords (word) VALUES (?)", (word,))
# #
# #             conn.commit()
# #             conn.close()
# #
# #             messagebox.showinfo("Success", "Word Added Successfully")
# #             word_entry.delete(0, tk.END)
# #     tk.Button(add, text="Add", command=add_word).pack(pady=10)
# #
# # def close_window():
# #     root.destroy()
#
# # def about_window():
# #     about = tk.Toplevel(root)
# #     about.title("Mo The Monkey")
# #     about.geometry("400x250")
# #     tk.Label(about, text="This is an educational app for grade 1 students").pack(pady=100)
#
# def generate_random_word():
#     conn = sqlite3.connect("monkeywords.db")  # Connect to your database
#     cursor = conn.cursor()
#
#     cursor.execute("SELECT word FROM monkeywords")  # Fetch all words
#     words = cursor.fetchall()  # Get the result as a list of tuples
#
#     conn.close()  # Close the connection
#
#     if words:  # If there are words in the database
#         random_word = random.choice(words)[0]  # Choose a random word
#         word_label.config(text=random_word)  # Update the label
#     else:
#         word_label.config(text="No words found")  # Handle empty database
#
# # root = Tk()
# # root.title('Mo the Monkey')
# # root.geometry(f"900x600")
# #
# # #Create toolbar frame
# # menu_bar = Menu(root)
# #
# # file_menu = Menu(menu_bar,tearoff=0)
# # file_menu.add_command(label="Add Words", command=add_word_window)
# # file_menu.add_command(label="Close", command=close_window)
# #
# # help_menu = Menu(menu_bar,tearoff=0)
# # help_menu.add_command(label="About", command=about_window)
# #
# # menu_bar.add_cascade(label="File", menu=file_menu)
# # menu_bar.add_cascade(label="Help", menu=help_menu)
# # root.config(menu=menu_bar)
# #
# # word_label = Label(root, text="Press 'Generate' to get a word", font=("Arial", 14))
# # word_label.pack(pady=20)
# # tk.Button(root, text="Next Word", command=generate_random_word).pack(pady=100)
# # #
# # init_db()
# #
# #
# # # root.mainloop()
from monkey import Monkey

if __name__ =="__main__":
    Monkey().run()