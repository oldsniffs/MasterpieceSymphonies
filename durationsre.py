import random

ALL_DURATION_NOTATIONS = ['1.', '1', '2.', '2', '4.', '4', '8.', '8', '16.', '16', '32', '32.', '64']
DURATION_WEIGHTS = [('1.', 3), ('1', 12), ('2.', 6), ('2', 18), ('4.', 8), ('4', 25), ('8.', 8), ('8', 20), ('16.', 6), ('16', 12), ('32.', 6), ('32', 2), ('64', 2)]
# should odd-timed tied beats be added to duration list? Almost certainly, they should group with any other note and follow same behavior
# Grouping them here would probably allow more precise weighting decisions. Would probably be more difficult to streamline into pattern
# Adding a condition in pattern generation would probably be programmatically easier

FILLER_ONLY_DURATIONS = ['1..,' '2..', '4..', '8..', '16..', '32..', '64..'] # God forbid 64.. is ever used

GROUPING_INTERVALS = ["4", "8", "16", "32"]
GROUPING_LENGTHS = [1, 2, 3, 4, 5]
GROUPING_WEIGHTS = [[16, 3, 1, 0, 0], [0, 4, 2, 1, 0], [0, 4, 4, 2, 1], [0, 6, 4, 4, 2]]


# Placeholders for user defined variables:
MEASURES = 16
TIME_SIGNATURE = (4, 4)


class Rhythm:
	def __init__(self, measures, time_signature):
		self.measures = measures
		self.time_signature = time_signature
		print(f"DISPLAYING self.measures, self.time_signature: {self.measures}, {self.time_signature}")
		self.appropriate_durations = self.get_appropriate_durations()
		print(f"DISPLAYING self.appropriate_durations: {self.appropriate_durations}\n")
		self.weights_list = self.get_weights()
		print(f"DISPLAYING self.weights_list: {self.weights_list}\n")

		self.pattern = []
		self.make_right_hand_pattern()

	def make_right_hand_pattern(self):

		# Function scope variables
		tied_carryover = 0
		grouping = [0, None] # Remaining, duration tuple

		for measure in range(self.measures):

			new_measure = Measure(measure+1, self.time_signature[0], self.appropriate_durations, self.weights_list, grouping, tied_carryover)
			print(f"LOG: =========== starting measure number {new_measure.number}============")

			tied_carryover = new_measure.fill_right_hand()

			



	def display_right_hand_pattern(self):
		rh_display = ""
		for measure in self.pattern:
			for d in measure.right_hand_pattern:
				rh_display += f"{d} "
			rh_display += "| "
		return rh_display

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
		
		print(beat_values)
		return beat_values

	# Proportion generation could well change with user feedback.
	# Does time signature matter? Are 1/8 notes more common in 6/8 than 3/4?
	# Should large notes be left appropriate, and allowed to form long tied carryovers? -> Yes, but weight should drop
	def get_weights(self):
		return [weight[1] for weight in [dw for dw in DURATION_WEIGHTS if dw[0] in [d[0] for d in self.appropriate_durations]]]


class Measure:
	def __init__(self, number, time_signature, durations_list, duration_weights, right_carryover_beats=0, left_carryover_beats=0, grouping=[]):
		# measure number not necessary, but used to help debugging
		self.number = number
		self.time_signature = time_signature
		self.beats_per_measure = time_signature[0]

		self.durations_list = durations_list
		self.durations_weights = duration_weights

		self.right_carryover_beats = right_carryover_beats
		self.grouping = grouping

		# Patterns are lists of beats, 1 per bpm, and beats are lists of durations
		# Beat lists can be empty if previous duration is fully covering that beat
		self.right_hand_pattern = []
		self.right_overflow_beats = self.fill_right_hand()
		self.left_hand_pattern = []

	def fill_right_hand(self):
		print(f"LOG: Starting fill of measure {self.number}, right hand pattern")
		grouping = self.grouping
		carryover_beats = self.right_carryover_beats
		filled_beats = 0

		next_beat_empty = False # Prob deprecated, using filled_beats var

		for beat in self.beats_per_measure:
			new_beat = []
			count = 0 # Floatable beat count within beat
			duration_count = 0 # used to access previous duration in beat by index

			if filled_beats:
				self.right_hand_pattern.append(new_beat)
				filled_beats -= 1
				next
		
			if carryover_beats:

				if carryover_beats < 1:
					self.fill_small_carryover(carryover_beats, new_beat)
					count += carryover_beats

				# Overflows measure
				if len(self.right_hand_pattern) + carryover_beats > self.beats_per_measure:
					new_duration = self.find_duration_by_beat_value(self.beats_per_measure-len(self.right_hand_pattern))
					carryover_beats = carryover_beats-new_duration[1]
					filled_beats = new_duration[1]-1

				else:

					# Ends on line
					if carryover_beats % 1 == 0:
						new_duration = self.find_duration_by_beat_value(carryover_beats)
						filled_beats = new_duration[1]-1
						carryover_beats = 0

					# Does not land on line, more than 1 beat
					else:
						new_duration = self.find_duration_by_beat_value(int(carryover_beats))
						filled_beats = new_duration[1]-1
						carryover_beats -= new_duration[1]

				new_beat.append(new_duration)
				count+=new_duration[1]

			while count < 1:

				virgin_duration = self.get_random_duration()
				print(f"LOG (fill_right_hand): Selected virgin durations: {new_duration}")

				if count + virgin_duration[1] <= 1:
					new_duration = virgin_duration

				else:
					count + virgin_duration[1] + len(self.right_hand_pattern) >= self.beats_per_measure:
					new_duration = self.find_duration_by_beat_value(1-count, new_beat) 
					carryover_beats = virgin_duration-(1-count)

				new_beat.append(new_duration)
				count+=new_duration[1]

			self.right_hand_pattern.append(new_beat)

		return carryover_beats



	def find_duration_by_beat_value(self, beat_value):
		for duration in self.durations_list + FILLER_ONLY_DURATIONS:
			if duration[1] == beat_value:
				return duration

	def complete_beat(self, remaining_beats, pattern):

		for d in self.appropriate_durations:
			if d <= remaining_beats:


	def fill_small_carryover(self, carryover_beats, pattern):

		print(f"LOG: Measure {self.number} starting with {self.carryover_beats} carryover beats. Attempting to fill")
		remaining_carryover = carryover
		carryover_duration_count = 0

		# Fill carryover_beats
		# Filling up to self.beats, tieing durations until carryover_beats satisfied

		for b in range(self.beats):
			new_beat = []

			for duration in self.appropriate_durations:
				print(f"LOG: Checking if {duration} fits inside {remaining_carryover}")
				if duration[1] <= remaining_carryover :
					if self.time_signature[1] % duration[1]
					print(f"LOG: {duration} found to fit. Appending")
					pattern.append(duration[0]+"~")
					carryover_duration_count += 1
					remaining_carryover -= duration[1]

		# Strip last tie
		pattern[-1] = pattern[-1][:-1]

		return carryover_duration_count

	def get_random_duration(self, beat_limit=None):
		if not beat_limit:
			return random.choices(self.appropriate_durations, self.weights_list)[0]
		else:
			limited_durations = self.appropriate_durations.copy()
			limited_weights = self.weights_list.copy()
			for i in range(len(self.appropriate_durations)):
				if self.appropriate_durations[i][1] > beat_limit:
					del(limited_durations[0])
					del(limited_weights[0])
			return random.choices(limited_durations, limited_weights)


if __name__ == "__main__":
	# rhythm = Rhythm(16, (3,4))
	# print(rhythm.display_right_hand_pattern())

	measure = Measure(1, (4,4), carryover_beats=.5)
