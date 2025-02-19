from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import sqlite3
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivy.core.text import  LabelBase
from kivymd.uix.snackbar import  MDSnackbar
from kivymd.uix.label import MDLabel
import random
import threading
import time
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.textfield import MDTextField
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.spinner import MDSpinner

#import required modules for firebase functionality
import firebase_admin
from firebase_admin import db, credentials

#authenticate to firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://momonkeywords-default-rtdb.europe-west1.firebasedatabase.app/"})

#creating reference to root node - cursor
ref = db.reference("/")

#test code, remove later
print(ref.get())

#AddWordContent sets the text fields of adding a new word to the database and firebase
#it is strictly UI
class AddWordContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.word_input  = MDTextField(
            hint_text="Enter a word",
            mode="round")
        self.size_hint_y = None
        self.add_widget(self.word_input)

#Class SplashScreen sets the members of the loading screen
class SplashScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=dp(10), padding=dp(20), **kwargs)
        # self.spinner = MDSpinner(
        #     size_hint=(None, None),
        #     size=(dp(48), dp(48)),
        #     active=True,
        #     pos_hint={"center_x": 0.5, "center_y": 0.5}
        # )

        self.label = MDLabel(text="Loading...",
                             halign="center",
                             theme_text_color="Custom",
                             text_color=(1,1,1,1),
                             font_name = "TeachersPet"
                             )

        self.add_widget(self.label)
        # self.add_widget(self.spinner)

#Main entry point of the program: The class has the build method which builds the UI.
#Class Monkey is also housing the members which assist in the function of the program.
class Monkey(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.info = None
        self.left_section = None
        self.layout = None
        self.generate_word = None
        self.splash = None
        self.generate_label = None
        self.conn = None
        self.dialog = None

    def build(self):
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
        #registering the different fonts used in the app.
        LabelBase.register(name="TeachersPet", fn_regular="assets/teachersPet.ttf")

        #creating a splash object that'll be used to display the loading widgets upon opening the app
        self.splash = SplashScreen()

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

        #left section buttons binding to the functions
        self.about_program.bind(on_press=self.show_about_dialog)
        self.add_word_btn.bind(on_press=self.add_word_dialog)

        #adding the buttons we need for the left panel to the left section of the box layout.
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


        #middle section
        self.middle = BoxLayout(
            orientation="vertical",
            size_hint = (None, None),
            size=(300,120),
            size_hint_y=0.3,
            pos_hint={"center_x":0.5}
        )

        #label which will change dynamically with random words from the database
        self.generate_label = Label(text="Click Button to generate a Word",
                                    font_size=80, size_hint_y=0.3,
                                    text_size=(400, None),
                                    halign="center",
                                    valign="middle",
                                    font_name="TeachersPet")
        #Main button on the screen
        self.generate_word = MDRaisedButton(text="Generate",
                                    font_name="TeachersPet",
                                    font_size=20,
                                    size_hint=(1,None),
                                    md_bg_color = get_color_from_hex("#C3FDB8"),
                                    text_color= get_color_from_hex("#000000"),
                                    height=30)

        self.generate_word.bind(on_press=self.generate_random_word) #Binds the Button to the button function



        #bottom section
        self.bottom = BoxLayout(
            orientation="vertical",
            size_hint=(None, None),
            size=(300, 120),
            size_hint_y=0.1,
            pos_hint={"center_x": 0.5}
        )

        #company information at the bottom of the window.
        self.info = Label(text="techmerce productions",size_hint_y=0.3, font_size=12,halign="center", valign="middle")

        #adding the splash screen to the main layout object
        self.root.add_widget(self.splash)

        #returns the main layout object
        return self.root



    #Begins the loading thread and points to initialize_app()
    def on_start(self):
        threading.Thread(target=self.initialize_app, daemon=True).start()
    #Second step after on_start() and can help loading components and functions
    def initialize_app(self):
        time.sleep(5)
        Clock.schedule_once(self.on_initialize_complete)
    #Third step - once second step of the thread is complete, begin loading UI elements here
    def on_initialize_complete(self, dt):
        self.conn = sqlite3.connect("monkeywords.db")
        self.init_db()


        self.root.remove_widget(self.splash)  #remove the splash widget

        #Add relevant widgets to the 3 sections
        self.header.add_widget(self.header_label)
        self.layout.add_widget(self.header)
        self.middle.add_widget(self.generate_label)
        self.middle.add_widget(self.generate_word)
        self.layout.add_widget(self.middle)
        self.bottom.add_widget(self.info)
        self.layout.add_widget(self.bottom)
        self.root.add_widget(self.left_section)
        self.root.add_widget(self.layout)



    #initializes the database if it does not exist, it creates a new one
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

    #generates a random word and sends it to generate_label Label in the UI
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

    #TODO(kat, 2025/02/19): Need to change the add_word_dialogue to a
    # separate screen where database has full CRUD functions
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


    #TODO(kat,2025/02/19): Change this snackbar's context to
    # match the new CRUD window for a successful CRUD operation
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

    # TODO(kat,2025/02/19): Change this snackbar's context to
    # match the new CRUD window for a unsuccessful CRUD operation
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
