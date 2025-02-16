from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import sqlite3
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton
from kivy.core.text import  LabelBase
from kivymd.uix.snackbar import  MDSnackbar
from kivymd.uix.label import MDLabel
import random
from kivymd.uix.textfield import MDTextField
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDRaisedButton

#import required modules
import firebase_admin
from firebase_admin import db, credentials

#authenticate to firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://momonkeywords-default-rtdb.europe-west1.firebasedatabase.app/"})

#creating reference to root node - cursor
ref = db.reference("/")
print(ref.get())
#retrieving data from root node - Select All
# ref.get()

#getting a specific value in the JSON  - Select
# print(db.reference("/words").get())

#Set operation - Update
# print(f"the new value is:{ref.get()}")




class AddWordContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.word_input  = MDTextField(
            hint_text="Enter a word",
            mode="round")
        self.size_hint_y = None
        self.add_widget(self.word_input)


class Monkey(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.snackbar = None
        self.content = None
        self.word_input = None
        self.dialog = None
        self.screen = None
        self.about_program = None
        self.add_word_btn = None
        self.left_section = None
        self.info = None
        self.bottom = None
        self.generate_word = None
        self.generate_label = None
        self.middle = None
        self.header_label = None
        self.header = None
        self.layout = None



        # Window.fullscreen = 'auto'
        LabelBase.register(name="TeachersPet", fn_regular="assets/teachersPet.ttf")
        LabelBase.register(name="SquareKids", fn_regular="assets/SquareKids.ttf")
        self.conn= sqlite3.connect("monkeywords.db")
        self.init_db()

    def build(self):
        """
           Main point in kivy to build the UI.

           Args:
               self

           Returns:
               object - self.root of type BoxLayout

           Raises:
               AttributeError: If any of the properties within the widgets are wrong.
           """

        #Main Layout is root which will contain two boxes side by side
        self.root = MDBoxLayout(orientation="horizontal" , md_bg_color=get_color_from_hex("#008000"))

        #first box situated on the right, and it is the main layout carrying most elements
        self.layout = BoxLayout(orientation="vertical")

        #second box situated on the left, and contains the add action and about window
        self.left_section = BoxLayout(
            orientation="vertical",
            size_hint_x=0.1,
            )
        #ImageButtons on the left comprising the menu of the program.
        # It will disappear once we go full screen.
        self.add_word_btn = MDIconButton(icon= "assets/images/add.png",icon_size="50sp", on_release=lambda x:print("Add Button Clicked"))
        self.about_program = MDIconButton(icon= "assets/images/about.png",icon_size="50sp", on_release=lambda x:print("About Button clicked"))
        self.about_program.bind(on_press=self.show_about_dialog)
        self.add_word_btn.bind(on_press=self.add_word_dialog)

        self.left_section.add_widget(self.add_word_btn)
        self.left_section.add_widget(self.about_program)


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
            font_name="TeachersPet"
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
                                    font_name="TeachersPet")

        self.generate_word = MDRaisedButton(text="Generate",
                                    font_name="TeachersPet",
                                    font_size=20,
                                    size_hint=(1,None),
                                    md_bg_color = get_color_from_hex("#C3FDB8"),
                                    text_color= get_color_from_hex("#000000"),
                                    height=30)

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

        self.root.add_widget(self.left_section)
        self.root.add_widget(self.layout)
        return self.root

    def init_db(self):
        """
           Loads the database

           Args:
               self

           Returns:
               None

           Raises:
               Database Exceptions: SQL errors
       """
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS monkeywords (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             word TEXT NOT NULL)''')
        self.conn.commit()

    def generate_random_word(self, instance):
        """
           Generates the random word after the Generate button is clicked

           Args:
               self

           Returns:
              None

           Raises:

       """

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

    def add_word_dialog(self,instance):
        """
           Add Word Dialog window

           Args:
               self

           Returns:
               None

           Raises:
               AttributeError: If any of the properties within the widgets are wrong.
       """

        if not self.dialog:
            self.content = AddWordContent()
            self.dialog = MDDialog(
                title = "Add a word",
                type="custom",
                height = "100dp",
                pos_hint={"center_y":0.5},
                content_cls= self.content,
                buttons = [
                    MDFlatButton(text = "Cancel", on_release=lambda x: self.dialog.dismiss()),
                    MDFlatButton(text = "Add", on_release=lambda x: self.add_words(),),
            ]

            )

        self.dialog.open()

    def show_successful(self):
        """
          SnackBar message for successful insertion into database.

           Args:
               self

           Returns:
               None

           Raises:
               AttributeError: If any of the properties within the widgets are wrong.
       """

        self.snackbar = MDSnackbar(

            MDLabel(text= "Word Added Successfully", halign="center"),
            pos_hint = {"center_x": 0.5, "y":0.1},
            duration= 3,
            md_bg_color = (0,0,0,1),
        )
        self.snackbar.open()

    @staticmethod
    def show_unsuccessful():
        """
         SnackBar message for unsuccessful insertion into database.

          Args:


          Returns:
              None

          Raises:
              AttributeError: If any of the properties within the widgets are wrong.
      """
        dialog = MDDialog(
            title="Oops!",
            text="Error, Please add a word to the text field and click 'Add' to continue ",
            buttons=[MDFlatButton(text="Close", on_release=lambda x: dialog.dismiss())
                     ],
        )
        dialog.open()

    def add_words(self):
        """
         Code logic to add words to the database

          Args:
              self

          Returns:
              None

          Raises:
              SQL Error: If database is closed, operation cannot be executed.
        """
        word = self.content.word_input.text.title()
        if word:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO monkeywords (word) VALUES (?)", (word,))
            self.conn.commit()
            self.content.word_input.text = ""

            #push the word to the database
            db.reference("/words").push().set(word)

            self.show_successful()


        else:
            self.show_unsuccessful()
        self.dialog.dismiss()

    @staticmethod
    def show_about_dialog(self):
        """
         About window pops up to give more information on the method

          Args:


          Returns:
              None

          Raises:
              AttributeError: If any of the properties within the widgets are wrong.
        """
        dialog = MDDialog(
            title = "About this App",
            text= "Sample application using KivyMD.\nBuilt with Python and Kivy",
            buttons=[MDFlatButton(text="Close", on_release=lambda x:dialog.dismiss())
                ],
        )
        dialog.open()
