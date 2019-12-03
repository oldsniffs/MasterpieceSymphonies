
def create_ly(content, file_name):
    file = open(f'{file_name}.ly', 'w')
    file.write(content)
    file.close


content = """upper = {
  \\clef treble
  \\key c \\major
  \\time 4/4

  a4 b c d 
}

lower = {
  \\clef bass
  \\key c \\major
  \\time 4/4

  a2 c a,, c,, a, c,
  a,,1 c, e, f,
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

create_ly(content, 'tester')

# file = open('testly.ly', 'w')
#
# file.write(content)
# file.close