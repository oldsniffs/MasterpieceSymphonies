A_TO_G = ["a", "b", "c", "d", "e", "f", "g"]
OCTAVE_SUFFIXES = [",,,,", ",,,", ",,", ",", "", "'", "''", "'''"]
ACCIDENTAL = ["es", "", "is"]

def generate_master_list():
	master_list = []
	octaves = 7

	# change while to for SUFFIXES
	for suffix in OCTAVE_SUFFIXES:
		for p in A_TO_G:
			for a in ACCIDENTAL:
				master_list.append(f"{p}{suffix}{a}")

	return master_list

for n in generate_master_list():
	print(n)


def check_bar_cross(start_beat, end_beat, time_signature):
    if start_beat < end_beat - (end_beat % time_signature[0]):
        return True, end_beat % time_signature[0]
    else:
        return False, 0

print(check_bar_cross(15, 18, (4,4)))

	# remove first note (a flat), add last 2 half steps to match a real piano

