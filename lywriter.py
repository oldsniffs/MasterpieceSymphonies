import durationsre
import pitchesre
import composer



test_rhythm = durationsre.Rhythm(12, (4,4))


class Masterpiece:
	def __init__(self, key, key_type, time_signature, left_limits, right_limits):
		pass

def create_ly(content, file_name):
    file = open(f'{file_name}.ly', 'w')
    file.write(content)
    file.close


def compose():
	notation = pitchesre.Notation("d", "major",['g', "c'''''"], ['a,,,', "f'"], test_rhythm, None, 1, None)
	test_rhythm.display_hand_patterns()
	right_composition = ""
	left_composition = ""
	for n in notation.right_notation:
		if "|" in n:
			print(f"Adding {n}")
			right_composition = right_composition + f'{n} '
		else:
			print(f"Adding {n}")
			right_composition = right_composition + f'{n} '

	for n in notation.left_notation:
		if "|" in n:
			print(f"Adding {n}")
			left_composition = left_composition + f'{n} '
		else:
			print(f"Adding {n}")
			left_composition = left_composition + f'{n} '

	print(f"Right: {right_composition}") 
	print(f"Left: {left_composition}")
	return right_composition, left_composition


right_hand, left_hand = compose()
content = """upper = {
  \\clef treble
  \\key c \\major
  \\time 4/4
  
"""
content = content + right_hand

content = content + """
}

lower = {
  \\clef bass
  \\key c \\major
  \\time 4/4

"""
content = content + left_hand

content = content + """
}

\\score {
  \\new PianoStaff <<
    \\set PianoStaff.instrumentName = #"Piano  "
    \\new Staff = "upper" \\upper
    \\new Staff = "lower" \\lower
  >>
  \\layout { }
  \\midi { }
} """


if __name__ == "__main__":

	print(right_hand)
	create_ly(content, 'test11')
	#
	# file = open('testly.ly', 'w')
	#
	# file.write(content)
	# file.close
