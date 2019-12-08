import random

ALL_DURATION_NOTATIONS = ['1', '1.', '2', '2.', '4', '4.', '8', '8.', '16', '16.', '32']
DURATION_WEIGHTS = [('1', 12), ('1.', 3), ('2', 18), ('2.', 6), ('4', 25), ('4.', 8), ('8', 20), ('8.', 8), ('16', 12), ('16.', 6), ('32', 6)]


# User defined variables:

measures = 16
time_signature = (4, 4)


class Rhythm:
	def __init__(self, measures, time_signature):
		self.measures = measures
		self.time_signature = time_signature
		self.duration_list = self.get_appropriate_durations()
		self.weights_list = self.get_weights()

		self.pattern = self.make_pattern()

	def make_pattern(self):

		pattern = []
		measure = 1

		tied_carryover_beat = 0
		while measure <= self.measures:

			if tied_carryover_beat:
				for duration in self.duration_list:
					if duration[1] == tied_carryover_beat:
						pattern.append(f"{duration[0]}")
						break

				beat = tied_carryover_beat

			else:
				beat = 0

			while beat < self.time_signature[1]:

				new_duration = self.get_random_duration()
				print(f"Virgin new_duration[0]: {new_duration[0]}")
				beat += new_duration[1]

				if beat == self.time_signature[1]:

					pattern.append(f"{new_duration[0]} | ")

				elif beat > self.time_signature[1]:

					beat -= new_duration[1]

					if measure == self.measures:
						new_duration = self.fill_measure(beat)

					roll = random.randint(0,3)

					# Backtrack beat, reroll new duration
					if roll == 0:
						print("LOG: Measure overrun, getting different beat")
						continue

					# Fill measure
					elif roll == 1:
						finishing_durations = self.fill_measure(beat)
						# probably roll for if fill notes should be tied or separate
						pattern.append(f"{finishing_durations[0][0]}~ ")
						new_duration = finishing_durations[1]

					# Carryover to a tied note in next measure
					# Needs to do same as previous roll, but also give tied_carryover_beat
					elif roll == 2:
						finishing_durations = self.fill_measure(beat)
						for fd in finishing_durations:
							pattern.append(f"{fd[0]}~ ")
						tied_carryover_beat = beat % self.time_signature[0]

				pattern.append(f"{new_duration[0]} ")

			pattern.append("| ")
			measure += 1

		return pattern


	def fill_measure(self, current_beat):
		# delete if working: if one split doesn't work, use a while loop to keep splitting
		# while fill_beats < remaining_beats  --- get next sized duration
		remaining_beats = current_beat - self.time_signature[0]
		print(f"LOG: {remaining_beats} left in measure. Attempting to fill.")

		for duration in self.duration_list:
			if duration[1] == remaining_beats:
				return [duration]

		# Needs to split
		finishing_durations = []

		for duration in self.duration_list:
			if duration[1] < remaining_beats:
				finishing_durations.append(duration)
				remaining_beats -= duration[1]

				for smaller_duration in self.duration_list:
					if duration == remaining_beats:
						finishing_durations.insert(0, smaller_duration)
			return finishing_durations

	def get_random_duration(self):
		return random.choices(self.duration_list, self.weights_list)[0]

	# Proportion generation could well change with user feedback.
	# Does time signature matter? Are 1/8 notes more common in 6/8 than 3/4?
	# Should large notes be left appropriate, and allowed to form long tied carryovers? -> could be a user setting?
	def get_weights(self):
		return [weight[1] for weight in [dw for dw in DURATION_WEIGHTS if dw[0] in [d[0] for d in self.duration_list]]]

	def get_appropriate_durations(self):
		beat_values = self.generate_beat_value_list()
		return [bv for bv in beat_values if self.time_signature[0] >= bv[1]]


	def generate_beat_value_list(self):

		beat_values = []
		for d in ALL_DURATION_NOTATIONS:

			if '.' in d:
				base_value = 1/int(d[:-1])
				beat_value = base_value * self.time_signature[1] * 1.5
			else:
				base_value = 1/int(d)
				beat_value = base_value * self.time_signature[1]

			beat_values.append((d, beat_value))

		return beat_values



if __name__ == "__main__":

	rhythm = Rhythm(16, (3, 4))
	for ad in rhythm.get_appropriate_durations():
		print(ad)