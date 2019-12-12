import durationsre


def create_ly(content, file_name):
    file = open(f'{file_name}.ly', 'w')
    file.write(content)
    file.close


def compose(total_beats):
    rhythm = durationsre.Rhythm(10, (4,4))
    composition = ""
    for n in rhythm:
        composition = composition + f'c{n} '

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
create_ly(content, 'tester')
#
# file = open('testly.ly', 'w')
#
# file.write(content)
# file.close

