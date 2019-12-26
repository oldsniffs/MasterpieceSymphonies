import random
import durationsre

SHARP_LIST = ['a,,,,', 'ais,,,,', 'b,,,,', 'c,,,,', 'cis,,,,', 'd,,,,', 'dis,,,,', 'e,,,,', 'f,,,,', 'fis,,,,', 'g,,,,', 'gis,,,,', 'a,,,', 'ais,,,', 'b,,,', 'c,,,', 'cis,,,', 'd,,,', 'dis,,,', 'e,,,', 'f,,,', 'fis,,,', 'g,,,', 'gis,,,', 'a,,', 'ais,,', 'b,,', 'c,,', 'cis,,', 'd,,', 'dis,,', 'e,,', 'f,,', 'fis,,', 'g,,', 'gis,,', 'a,', 'ais,', 'b,', 'c,', 'cis,', 'd,', 'dis,', 'e,', 'f,', 'fis,', 'g,', 'gis,', 'a', 'ais', 'b', 'c', 'cis', 'd', 'dis', 'e', 'f', 'fis', 'g', 'gis', "a'", "ais'", "b'", "c'", "cis'", "d'", "dis'", "e'", "f'", "fis'", "g'", "gis'", "a''", "ais''", "b''", "c''", "cis''", "d''", "dis''", "e''", "f''", "fis''", "g''", "gis''", "a'''", "ais'''", "b'''", "c'''", "cis'''", "d'''", "dis'''", "e'''", "f'''", "fis'''", "g'''", "gis'''", "a'''", "ais'''", "b'''", "c''''"]
FLAT_LIST = ['a,,,,', 'bes,,,,', 'b,,,,', 'c,,,,', 'des,,,,', 'd,,,,', 'ees,,,,', 'e,,,,', 'f,,,,', 'ges,,,,', 'g,,,,', 'aes,,,', 'a,,,', 'bes,,,', 'b,,,', 'c,,,', 'des,,,', 'd,,,', 'ees,,,', 'e,,,', 'f,,,', 'ges,,,', 'g,,,', 'aes,,', 'a,,', 'bes,,', 'b,,', 'c,,', 'des,,', 'd,,', 'ees,,', 'e,,', 'f,,', 'ges,,', 'g,,', 'aes,', 'a,', 'bes,', 'b,', 'c,', 'des,', 'd,', 'ees,', 'e,', 'f,', 'ges,', 'g,', 'aes', 'a', 'bes', 'b', 'c', 'des', 'd', 'ees', 'e', 'f', 'ges', 'g', "aes'", "a'", "bes'", "b'", "c'", "des'", "d'", "ees'", "e'", "f'", "ges'", "g'", "aes''", "a''", "bes''", "b''", "c''", "des''", "d''", "ees''", "e''", "f''", "ges''", "g''", "aes'''", "a'''", "bes'''", "b'''", "c'''", "des'''", "d'''", "ees'''", "e'''", "f'''", "ges'''", "g'''", "aes'''", "a'''", "bes'''", "b'''", "c''''"]

MAJOR_MAP = [2, 2, 1, 2, 2, 2, 1]*5
MINOR_MAP = [2, 1, 2, 2, 1, 2, 2]*5

INTERVALS = [1, 2, 3, 4, 5, 6, 7]

test_rhythm = durationsre.Rhythm(10, (4,4))

class Notation:

	def __init__(self, key, key_type, right_rhythm, accidental_rate, anchor_strength):
		self.key = key
		self.key_type = key_type
		self.scale_map = self.get_scale_map() # Only used in function map_scale
		self.scale = self.map_scale()

		self.right_rhythm = right_rhythm

		self.accidental_rate = accidental_rate
		self.anchor_strength = anchor_strength # Will control how much intervals run away from anchor point. Can influence interval weights

		self.interval_weights = [6, 12, 12, 6, 4, 2, 1]

		self.right_notation = self.compose_right_hand()


	def map_scale(self):
		scale = []
		if self.key in ["g", "d", "a", "e", "b", "fis", "cis"]:
			base_list = SHARP_LIST
		else:
			base_list = FLAT_LIST

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
				if "'" not in base_list[start_index-run]:
					scale.insert(0, base_list[start_index-run])

			except IndexError:
				break

		return scale

	def get_scale_map(self):
		if self.key_type == "major":
			return MAJOR_MAP
		if self.key_type == "minor":
			return MINOR_MAP


	def compose_right_hand(self):

		right_hand_notation = []

		measure = 1
		anchor_count = 1
		anchor = self.scale.index(self.key+"'")
		previous_note = anchor
		previous_direction = None
		tied_note = False

		for d in self.right_rhythm:

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

			current_direction = self.set_direction(previous_direction)
			print(f"LOG: rolling new pitch in measure {measure} with interval {interval} in direction {current_direction}")
			p = self.scale[previous_note+interval*current_direction]
			print(f"LOG: rolled pitch: {p}")


			right_hand_notation.append(f"{p}{d} ")
			previous_note = self.scale.index(p)
			previous_direction = current_direction
			if "~" in d:
				tied_note = True

		return right_hand_notation

	def set_direction(self, current_direction):
		if not current_direction:
			return random.choice([1, -1])

		flip = False
		if random.randint(0,2) == 0:
			flip = True
		if not flip:
			return current_direction
		else:
			if current_direction == 1:
				return -1
			else:
				return 1


if __name__ == "__main__":
	notation = Notation("cis", "major", test_rhythm.right_hand_pattern, 4, 1)
	print(notation.right_hand_notation)
