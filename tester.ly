upper = {
  \clef treble
  \key c \major
  \time 4/4

  a4 b c d 
}

lower = {
  \clef bass
  \key c \major
  \time 4/4

  a2 c a,, c,, a, c,
  a,,1 c, e, f,
}

\score {
  \new PianoStaff <<
    \set PianoStaff.instrumentName = #"Piano  "
    \new Staff = "upper" \upper
    \new Staff = "lower" \lower
  >>
  \layout { }
  \midi { }
} 