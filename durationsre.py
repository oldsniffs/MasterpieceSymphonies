import random

ALL_DURATION_NOTATIONS = ['1', '1.', '2', '2.', '4', '4.', '8', '8.', '16', '16.', '32']
DURATION_WEIGHTS = [('1', 12), ('1.', 3), ('2', 18), ('2.', 6), ('4', 25), ('4.', 8), ('8', 20), ('8.', 8), ('16', 12), ('16.', 6), ('32', 6)]


# User defined variables:

measures = 16
time_signature = (4, 4)


def get_rhythm(measures, time_signature):

	measure = 1

	# Durations and propabilities for randomizer
	duration_list = get_appropriate_durations((time_signature))
	weights = get_weights(duration_list)

	rhythm = []

	tied_carryover_beat = 0
	while measure <= measures:

		if tied_carryover_beat:
			for duration in duration_list:
				if duration[1] == tied_carryover_beat:
					rhythm.append(f"{duration[0]}")
					break

			beat = tied_carryover_beat

		else:	
			beat = 0

		while beat < time_signature[1]:
			
			new_duration = get_random_duration(duration_list, weights)
			print(f"printing new duration[0] {new_duration[0]}")
			beat += new_duration[1]

			if beat == time_signature[1]:

				rhythm.append(f"{new_duration[0]} | ")

			elif beat > time_signature[1]:

				beat -= new_duration[1]

				if measure == measures:
					new_duration = fill_measure(beat, time_signature, duration_list)

				roll = random.randint(0,3)

				# Backtrack beat, reroll new duration
				if roll == 0:
					print("LOG: Measure overrun, getting different beat")
					continue

				# Fill measure
				elif roll == 1:
					finishing_durations = fill_measure(beat, time_signature, duration_list)
					for fd in finishing_durations:
						# probably roll for tie or not. maybe just tie
						finishing = fd
						if fd != finishing_durations[-1]:

						rhythm.append(f"{fd[0]}")   # ____________ Left off here


				# Carryover to a tied note in next measure
				elif roll == 2:
					finishing_durations = fill_measure(beat, time_signature, duration_list)
					for fd in finishing_durations:
						rhythm.append(f"{fd[0]}~ ")
					tied_carryover_beat = beat % time_signature[0]

			rhythm.append(f"{new_duration[0]} ")

		rhythm.append("| ")
		measure += 1

	return rhythm


def fill_measure(current_beat, time_signature, duration_list):
	# delete if working: if one split doesn't work, use a while loop to keep splitting
	remaining_beats = current_beat - time_signature[0]

	for duration in duration_list:
		if duration[1] == remaining_beats:
			return [duration]

	# Needs to split
	finishing_durations = []
	for duration in duration_list:
		if duration[1] < remaining_beats:
			finishing_durations.append(duration)
			remaining_beats -= duration[1]

			for smaller_duration in duration_list:
				if duration == remaining_beats:
					finishing_durations.insert(0, smaller_duration)
		return finishing_durations

def get_random_duration(duration_list, weights_list):
	return random.choices(duration_list, weights=weights_list)[0]

# Proportion generation could well change with user feedback. 
# Does time signature matter? Are 1/8 notes more common in 6/8 than 3/4?
# Should large notes be left appropriate, and allowed to form long tied carryovers? -> could be a user setting?
def get_weights(d_list):
	return [weight[1] for weight in [dw for dw in DURATION_WEIGHTS if dw[0] in [d[0] for d in d_list]]]


def get_appropriate_durations(time_signature):
	beat_values = generate_beat_value_list(time_signature)
	return [bv for bv in beat_values if time_signature[0] >= bv[1]]


def generate_beat_value_list(time_signature):

    beat_values = []
    for d in ALL_DURATION_NOTATIONS:

        if '.' in d:
            base_value = 1/int(d[:-1])
            beat_value = base_value * time_signature[1] * 1.5
        else:
            base_value = 1/int(d)
            beat_value = base_value * time_signature[1]

        beat_values.append((d, beat_value))

    return beat_values


# for ad in get_appropriate_durations((4,4)):
# 	print(ad)

# for prop in get_weights(get_appropriate_durations((4,4))):
# 	print(prop)

for r in get_rhythm(10, (4,4)):
	print(r)