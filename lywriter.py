import durationsre
import pitchesre

test_rhythm = durationsre.Rhythm(10, (4,4))


def create_ly(content, file_name):
    file = open(f'{file_name}.ly', 'w')
    file.write(content)
    file.close


def compose(total_beats):
	rhythm = pitchesre.Notation("ees", "major", test_rhythm.right_hand_pattern, 4, 1)
	composition = ""
	for n in rhythm.right_hand_notation:
		if "M" in n:
			print(f"Not adding {n}")
		elif "|" in n:
			print(f"Adding {n}")
			composition = composition + n
		else:
			print(f"Adding {n}")
			composition = composition + f'{n} '

	print(composition)
	return composition


right_hand = compose(64)
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

print(right_hand)
create_ly(content, 'test2')
#
# file = open('testly.ly', 'w')
#
# file.write(content)
# file.close

