import random
import durations


AGG_NOTES = 64
TIME_SIG = (4,4)


def get_beat_count(total_notes, time_signature):
    total_beats = total_notes / time_signature[1]
    while total_beats % time_signature[0] != 0:
        total_beats -= 1
    return total_beats



# Generate Music

content = """"upper = {
  \\clef treble
  \\key c \\major
  \\time 4/4
  
"""


content = content + """
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
} """
