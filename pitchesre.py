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

	def __init__(self, key, key_type, right_limits, left_limits, rhythm, accidental_freq, rest_freq, anchor_strength):
		self.key = key
		self.key_type = key_type
		self.base_list = self.get_base_list
		self.scale_map = self.get_scale_map() # Only used in function map_scale
		self.scale = self.map_scale()
		self.right_limits = right_limits
		self.left_limits = left_limits
		self.rh_notes = self.map_hand(self.right_limits)
		self.lh_notes = self.map_hand(self.left_limits)
		print(f"DEBUG: {self.scale_map}")
		print(f"DEBUG: rh_notes: {self.rh_notes}")
		print(f"DEBUG: lh_notes: {self.lh_notes}")

		self.right_rhythm = rhythm.right_notation
		self.left_rhythm = rhythm.left_notation

		self.accidental_freq = accidental_freq
		self.rest_freq = rest_freq
		self.anchor_strength = anchor_strength # Will control how much intervals run away from anchor point. Can influence interval weights

		self.interval_weights = [12, 14, 10, 4, 3, 2, 1]

		self.right_notation = self.compose_right_hand()
		self.left_notation = self.compose_left_hand()

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

	def map_hand(self, limits):
		pitches = []
		base_list = self.base_list()

		start_index = base_list.index(self.key+"'")

		run = 0
		for i in self.scale_map:
			try:
				if base_list[start_index+run] != limits[1]:
					pitches.append(base_list[start_index+run])
					run += i
				else:
					break
			except IndexError:
				break

		run = 0
		for i in reversed(self.scale_map):
			try:
				run += i
				if base_list[start_index-run] != limits[0] and start_index-run >= 0:
					pitches.insert(0, base_list[start_index-run])
				else:
					break
			except IndexError:
				break

		return pitches

	def map_left(self):
		pitches = []
		base_list = self.base_list()

		# run = 0
		# for i in self.scale_map:
		# 	try:
		# 		run += 1
		# 		if base_list:
		# 			pass


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
		anchor = self.rh_notes.index(self.key+"'")
		previous_note = anchor
		previous_direction = None
		span = 0
		tied_note = False
		p = 'r'

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

			current_direction, span = self.set_direction(previous_direction, previous_note-anchor, span)
			print(f"LOG: rolling new pitch in measure {measure} with interval {interval} from previous note index {previous_note} in direction {current_direction}")
			print(f"LOG: index for p should be: {previous_note+(interval*current_direction)}")
			if previous_note+(interval*current_direction) < 0:
				current_direction *= -1			
			try:
				p = self.rh_notes[previous_note+(interval*current_direction)]
			except IndexError:
				p = self.rh_notes[previous_note-(interval*current_direction)]
			print(f"LOG: rolled pitch: {p}")

			# if random.randint(0, 5) == 5:
			# 	print(f"LOG: Rest inserted ============================")
			# 	p = "r"

			right_hand_notation.append(f"{p}{d} ")
			print(f"LOG: {p}{d}  appended")
			previous_note = self.rh_notes.index(p)
			previous_direction = current_direction
			if "~" in d:
				tied_note = True

		return right_hand_notation

	def compose_left_hand(self):

		print(f"LOG(compose_left_hand): Composing right hand. Checking lh_notes: {self.lh_notes}")

		left_hand_notation = []

		measure = 1
		anchor_count = 1
		anchor = self.lh_notes.index(self.key+",")-2
		previous_note = anchor
		previous_direction = None
		span = 0
		tied_note = False

		for d in self.left_rhythm:

			if "M" in d:
				continue

			if d == "|":
				left_hand_notation.append(d)
				measure += 1
				continue

			if tied_note:
				print(f"LOG(compose_left_hand): Tie detected, setting interval 0")
				interval = 0
				tied_note = False
			else:
				interval = random.choices(INTERVALS, self.interval_weights)[0]

			# if for rests. Different duration rules for rests?

			current_direction, span = self.set_direction(previous_direction, previous_note-anchor, span)
			print(f"LOG(compose_left_hand): rolling new pitch in measure {measure} with interval {interval} from previous note index {previous_note} in direction {current_direction}")
			print(f"LOG(compose_left_hand): index for p should be: {previous_note+(interval*current_direction)}")
			if previous_note+(interval*current_direction) < 0:
				current_direction *= -1
			try:
				p = self.lh_notes[previous_note+(interval*current_direction)]
			except IndexError:
				p = self.lh_notes[previous_note-(interval*current_direction)]
			print(f"LOG(compose_left_hand): rolled pitch: {p}")


			left_hand_notation.append(f"{p}{d} ")
			previous_note = self.lh_notes.index(p)
			previous_direction = current_direction
			if "~" in d:
				tied_note = True

		return left_hand_notation

	def set_direction(self, current_direction, distance_from_anchor, span):
		if not current_direction:
			return random.choice([1, -1]), 1

		anchor_weight = self.weigh_anchor(distance_from_anchor, current_direction)

		base = anchor_weight + span
		flip = False

		if base > 9:
			flip = True
		
		else: 
			print(f"LOG(set_direction): Rolling for flip with base = anchor_weight + span: {anchor_weight} + {span} = {base}")
			if random.randint(base, 14) > 9:
				flip = True
				span = 0
		
		if flip:
			if current_direction == 1:
				new_direction = -1
			else:
				new_direction = 1
		else:
			new_direction = current_direction
			span += 1
		return new_direction, span

	def weigh_anchor(self, distance_from_anchor, current_direction):
		anchor_weight = 0
		if abs(distance_from_anchor) > 7: # Point at which distance weights flip roll
			if (distance_from_anchor < 0 and current_direction == -1) or (distance_from_anchor > 0 and current_direction == 1):
				anchor_weight = int(abs(distance_from_anchor)/3)
				print(f"LOG(weight_anchor): Anchor weighing in at abs(distance_from_anchor): abs({distance_from_anchor}) /3 rounded down: {anchor_weight}")
		return anchor_weight

if __name__ == "__main__":
	notation = Notation("d", 'major', RH_LIMITS, LH_LIMITS, durationsre.Rhythm(10, (4,4)), 0, 1, 0)
	print(f"LOG: rh_notes: {notation.rh_notes}")
	print(notation.scale)
	print(f"right_notation: {notation.right_notation}")
	print(f"left_notation: {notation.left_notation}")