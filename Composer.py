import tkinter as tk
import subprocess
from lywriter import *


KEYS = ["C", "G", "D", "A", "E", "B"]

TIME_SIGNATURES = {
	'4/4': (4, 4),
	'3/4': (3, 4),
	'2/4': (2, 4),
	'2/2': (2, 2),
	'6/8': (6, 8),
	'7/8': (7, 8),
	'5/16': (5,16)
}

OUTPUT_FILEPATH = "Output\\"

class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.title("Masterpiece Symphony Composer")

		self.create_widgets()

	def create_widgets(self):

		self.title_label = tk.Label(self, text="Piece Title: ")
		self.title_entry = tk.Entry(self)

		self.key_label = tk.Label(self, text="Key")
		self.key_choice = tk.StringVar()
		self.key_choice.set("Select Key")
		self.key_menu = tk.OptionMenu(self, self.key_choice, *KEYS)

		self.time_signature_label = tk.Label(self, text="Key Signature: ")
		self.time_signature_choice = tk.StringVar()
		self.time_signature_choice.set("Select Key Signature")
		self.time_signature_menu = tk.OptionMenu(self, self.time_signature_choice, *TIME_SIGNATURES)

		self.compose_button = tk.Button(self, text="Compose", command=self.execute)

		current_row = 1
		self.title_label.grid(column=0, row=current_row, sticky='e')
		self.title_entry.grid(column=1, row=current_row, sticky='w')
		current_row += 1

		self.key_label.grid(column=0, row=current_row, sticky='e')
		self.key_menu.grid(column=1, row=current_row, sticky='w')
		current_row += 1

		self.time_signature_label.grid(column=0, row=current_row, sticky='e')
		self.time_signature_menu.grid(column=1, row=current_row, sticky='w')
		current_row += 1

		self.compose_button.grid(column=0, row=current_row, columnspan=2)

	def execute(self):
		self.get_input()
		self.clear_fields()
		self.compose()

	def get_input(self):
		pass

	def compose(self):
		pass

	def clear_fields(self):
		self.title_entry.delete(0, 'end')
		self.key_menu.selection_clear()
		# Needs to reset OptionMenu's. Haven't found the solution


# create_ly(content, 'testttt')

# subprocess.call(["lilypond", "long.ly"])

app = App()
app.mainloop()