from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import requests
import sqlite3
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.text import  LabelBase
import random

class Monkey(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.primary_hue = "500"
        # Window.fullscreen = 'auto'
        LabelBase.register(name="Cakeroll", fn_regular="assets/Cakeroll.ttf")
        LabelBase.register(name="SquareKids", fn_regular="assets/SquareKids.ttf")
        self.info = None
        self.bottom = None
        self.generate_word = None
        self.generate_label = None
        self.middle = None
        self.header_label = None
        self.header = None
        self.layout = None
        self.conn= sqlite3.connect("monkeywords.db")
        self.init_db()

    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=5, spacing=10)

        #Top section
        self.header = BoxLayout(
            orientation="vertical",
            size_hint = (None,None),
            size=(300, 120),
            size_hint_y=0.1,
            pos_hint={"center_x": 0.5}
        )

        self.header_label = Label(
            text="Monkey Trees",
            halign="center",
            valign="middle",
            font_size=50,
            font_name="SquareKids"
        )
        self.header.add_widget(self.header_label)
        self.layout.add_widget(self.header)


        #middle section
        self.middle = BoxLayout(
            orientation="vertical",
            size_hint = (None, None),
            size=(300,120),
            size_hint_y=0.3,
            pos_hint={"center_x":0.5}
        )
        self.generate_label = Label(text="Click Button to generate a Word",
                                    font_size=50, size_hint_y=0.3,
                                    text_size=(400, None),
                                    halign="center",
                                    valign="middle",
                                    font_name="Cakeroll")
        self.generate_word = Button(text="Generate", size_hint=(1,None), height=30)
        self.generate_word.bind(on_press=self.generate_random_word)

        self.middle.add_widget(self.generate_label)
        self.middle.add_widget(self.generate_word)
        self.layout.add_widget(self.middle)


        #bottom section
        self.bottom = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            size=(300, 120),
            size_hint_y=0.1,
            pos_hint={"center_x": 0.5}
        )
        self.info = Label(text="techmerce productions",size_hint_y=0.3, font_size=12,halign="center", valign="middle")
        self.bottom.add_widget(self.info)
        self.layout.add_widget(self.bottom)

        return self.layout

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS monkeywords (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             word TEXT NOT NULL)''')
        self.conn.commit()
        self.conn.close()

    def generate_random_word(self,instance):
        conn = sqlite3.connect("monkeywords.db")  # Connect to your database
        cursor = conn.cursor()

        cursor.execute("SELECT word FROM monkeywords")  # Fetch all words
        words = cursor.fetchall()  # Get the result as a list of tuples

        conn.close()  # Close the connection

        if words:  # If there are words in the database
            random_word = random.choice(words)[0]  # Choose a random word
            self.generate_label.text = f"{random_word}"  # Update the label
        else:
            self.generate_label.text="No words found"  # Handle empty database

