import random
import durationsre

SHARP_LIST = ['a,,,', 'ais,,,', 'b,,,', 'c,,', 'cis,,', 'd,,', 'dis,,', 'e,,', 'f,,', 'fis,,', 'g,,', 'gis,,', 'a,,', 'ais,,', 'b,,', 'c,', 'cis,', 'd,', 'dis,', 'e,', 'f,', 'fis,', 'g,', 'gis,', 'a,', 'ais,', 'b,', 'c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', 'a', 'ais', 'b', "c'", "cis'", "d'", "dis'", "e'", "f'", "fis'", "g'", "gis'", "a'", "ais'", "b'", "c''", "cis''", "d''", "dis''", "e''", "f''", "fis''", "g''", "gis''", "a''", "ais'''", "b''", "c'''", "cis'''", "d'''", "dis'''", "e'''", "f'''", "fis'''", "g'''", "gis'''", "a'''", "ais'''", "b'''", "c''''", "cis''''", "d''''", "dis''''", "e''''", "f''''", "fis''''", "g''''", "gis''''", "a''''", "ais''''", "b''''", "c'''''"]
FLAT_LIST = ['a,,,', 'bes,,,', 'b,,,', 'c,,', 'des,,', 'd,,', 'ees,,', 'e,,', 'f,,', 'ges,,', 'g,,', 'aes,,', 'a,,', 'bes,,', 'b,,', 'c,', 'des,', 'd,', 'ees,', 'e,', 'f,', 'ges,', 'g,', 'aes,', 'a,', 'bes,', 'b,', 'c', 'des', 'd', 'ees', 'e', 'f', 'ges', 'g', 'aes', 'a', 'bes', 'b', "c'", "des'", "d'", "ees'", "e'", "f'", "ges'", "g'", "aes'", "a'", "bes'", "b'", "c''", "des''", "d''", "ees''", "e''", "f''", "ges''", "g''", "aes''", "a''", "bes''", "b''", "c'''", "des'''", "d'''", "ees'''", "e'''", "f'''", "ges'''", "g'''", "aes'''", "a'''", "bes'''", "b'''", "c''''", "des''''", "d''''", "ees''''", "e''''", "f''''", "ges''''", "g''''", "aes''''", "a''''", "bes''''", "b''''", "c'''''"]

RH_LIMITS = ['g', "c'''''"]
LH_LIMITS = ["a,,,", 'f']

MAJOR_MAP = [2, 2, 1, 2, 2, 2, 1]*5
MINOR_MAP = [2, 1, 2, 2, 1, 2, 2]*5
MINOR_HARM_MAP = [2, 1, 2, 2, 1, 3, 1]*5
MINOR_MEL_MAP = [2, 1, 2, 2, 2, 2, 1]*5

INTERVALS = [1, 2, 3, 4, 5, 6, 7]

class Notation:

	def __init__(self, key, key_type, right_limits, left_limits, rhythm, accidental_rate, anchor_strength):
		self.key = key
		self.key_type = key_type
		self.base_list = self.get_base_list
		self.scale_map = self.get_scale_map() # Only used in function map_scale
		self.scale = self.map_scale()
		self.right_limits = right_limits
		self.left_limits = left_limits
		self.rh_notes = self.map_right()
		print(f"DEBUG: rh_notes: {self.rh_notes}")

		self.right_rhythm = rhythm.right_notation
		print(f"DEBUG: rhythm.right_notation {rhythm.right_notation}")

		self.accidental_rate = accidental_rate
		self.anchor_strength = anchor_strength # Will control how much intervals run away from anchor point. Can influence interval weights

		self.interval_weights = [12, 14, 10, 4, 3, 2, 1]

		self.right_notation = self.compose_right_hand()

	def get_base_list(self):
		if self.key_type == "major":
			if self.key in ["g", "d", "a", "e", "b"] or "is" in self.key:
				return SHARP_LIST
			else:
				return FLAT_LIST
		else:
			if self.key in ["b", "e"] or "is" in self.key:
				return SHARP_LIST
			else:
				return FLAT_LIST

	def map_right(self):
		right_pitches = []
		base_list = self.base_list()

		start_index = base_list.index(self.key+"'")

		run = 0
		for i in self.scale_map:
			try:
				if base_list[start_index+run] != self.right_limits[1]:
					right_pitches.append(base_list[start_index+run])
					run += i
				else:
					break
			except IndexError:
				break

		run = 0
		for i in reversed(self.scale_map):
			try:
				run += i
				if base_list[start_index-run] != self.right_limits[0] and start_index-run >= 0:
					right_pitches.insert(0, base_list[start_index-run])
				else:
					break
			except IndexError:
				break

		return right_pitches


	def map_scale(self): # Currently deprecated, keeping for time
		scale = []
		base_list = self.get_base_list()

		# Append at root
		start_index = base_list.index(self.key)

		# Get first, fill up
		run = 0
		for i in self.scale_map:
			try:
				scale.append(base_list[start_index+run])
				run += i
			except IndexError:
				break

		# Now fill backwards behind first
		run = 0
		for i in reversed(self.scale_map):
			try:
				run += i
				if start_index-run >= 0:
					scale.insert(0, base_list[start_index-run])

			except IndexError:
				break

		return scale

	def get_scale_map(self):
		if self.key_type == "major":
			return MAJOR_MAP
		elif self.key_type == "minor":
			return MINOR_MAP
		elif self.key_type == "harmonic":
			return MINOR_HARM_MAP
		else:
			return MINOR_MEL_MAP

	def compose_right_hand(self):

		print(f"LOG: Composing right hand. Checking rh_notes: {self.rh_notes}")

		right_hand_notation = []

		measure = 1
		anchor_count = 1
		anchor = self.rh_notes.index(self.key+"'")+2
		previous_note = anchor
		previous_direction = None
		tied_note = False

		for d in self.right_rhythm:

			if "M" in d:
				continue

			if d == "|":
				right_hand_notation.append(d)
				measure += 1
				continue

			if tied_note:
				print(f"LOG: Tie detected, setting interval 0")
				interval = 0
				tied_note = False
			else:
				interval = random.choices(INTERVALS, self.interval_weights)[0]

			# if for rests. Different duration rules for rests?

			current_direction = self.set_direction(previous_direction, (anchor-previous_note)^2)
			print(f"LOG: rolling new pitch in measure {measure} with interval {interval} from previous note index {previous_note} in direction {current_direction}")
			print(f"LOG: index for p should be: {previous_note+(interval*current_direction)}")
			try:
				p = self.rh_notes[previous_note+(interval*current_direction)]
			except IndexError:
				p = self.rh_notes[previous_note-(interval*current_direction)]
			print(f"LOG: rolled pitch: {p}")


			right_hand_notation.append(f"{p}{d} ")
			previous_note = self.rh_notes.index(p)
			previous_direction = current_direction
			if "~" in d:
				tied_note = True

		return right_hand_notation

	# Base this on -- previous direction(+), distance from anchor(farther away, likelier to return)
	# and sequence. Give a chance to boost odds to continue in current direction for a number of pitches.
	def set_direction(self, current_direction, distance_from_anchor):
		if not current_direction:
			return random.choice([1, -1])

		base = 0 + int(distance_from_anchor/2)
		flip = False
		if random.randint(base, 14) > 9:
			flip = True
		if not flip:
			return current_direction
		else:
			if current_direction == 1:
				return -1
			else:
				return 1


if __name__ == "__main__":
	notation = Notation("d", 'major', RH_LIMITS, LH_LIMITS, durationsre.Rhythm(10, (4,4)), 0, 0)
	print(f"LOG: rh_notes: {notation.rh_notes}")
	print(notation.scale)
	print(notation.right_notation)