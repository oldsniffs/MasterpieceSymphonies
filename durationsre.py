import random

ALL_DURATION_NOTATIONS = ['1.', '1', '2.', '2', '4.', '4', '8.', '8', '16.', '16', '32']
DURATION_WEIGHTS = [('1.', 3), ('1', 12), ('2.', 6), ('2', 18), ('4.', 8), ('4', 25), ('8.', 8), ('8', 20), ('16.', 6), ('16', 12), ('32', 6)]
# should odd-timed tied beats be added to duration list? Almost certainly, they should group with any other note and follow same behavior
# Grouping them here would probably allow more precise weighting decisions. Would probably be more difficult to streamline into pattern
# Adding a condition in pattern generation would probably be programmatically easier

# Placeholders for user defined variables:
MEASURES = 16
TIME_SIGNATURE = (4, 4)


class Rhythm:
	def __init__(self, measures, time_signature):
		self.measures = measures
		self.time_signature = time_signature
		print(f"DISPLAYING self.measures, self.time_signature: {self.measures}, {self.time_signature}")
		self.duration_list = self.get_appropriate_durations()
		print(f"DISPLAYING self.duration_list: {self.duration_list}\n")
		self.weights_list = self.get_weights()
		print(f"DISPLAYING self.weights_list: {self.weights_list}\n")

		self.pattern = []
		self.make_pattern()
		print(f"DISPLAYING pattern: {self.pattern}")

	def make_pattern(self):

		pattern = []

		tied_carryover_beats = 0
		for measure in range(self.measures):

			new_measure = Measure(measure+1, self.time_signature[0])
			print(f"LOG: =========== starting measure number {new_measure.number}============")
			self.pattern.append(f"M{new_measure.number}")

			if tied_carryover_beats:
				print(f"LOG: {tied_carryover_beats} tied carryover beats detected, seeking appropriate tied duration to start measure")
				self.fill_carry_over(new_measure, tied_carryover_beats)

				# See if this can be done in function
				new_measure.beats += tied_carryover_beats

			while new_measure.beats < new_measure.beats_per_measure:

				print(f"LOG Starting @ beat {new_measure.beats}")
				new_duration = self.get_random_duration()
				print(f"Virgin duration selected: ({new_duration[0]}, {new_duration[1]})")
				new_measure.beats += new_duration[1]

				if new_measure.beats == new_measure.beats_per_measure:

					new_measure.pattern.append(new_duration[0])

				elif new_measure.beats > new_measure.beats_per_measure:

					if new_measure.number == self.measures:
						print(f"LOG: Measure overflow but it's the last one. finishing out")
						new_measure.beats -= new_duration[1]
						self.complete_measure(new_measure, carryover=False)

					else:
						roll = random.randint(0,2)
						print(f"LOG: Measure overflow, rolled option {roll}")

						# Backtrack beat, reroll new duration
						if roll == 0:
							new_measure.beats -= new_duration[1]
							print("LOG: Measure overflow -- option 0: get different duration")
							new_duration = self.get_random_duration(beat_limit=new_measure.beats_per_measure-new_measure.beats)

						# Fill measure
						elif roll == 1:
							new_measure.beats -= new_duration[1]
							self.complete_measure(new_measure, carryover=False)

						# Carryover to a tied note in next measure
						# Needs to do same as previous roll, but also provide tied_carryover_beats
						elif roll == 2:
							tied_carryover_beats = new_measure.beats - new_measure.beats_per_measure
							new_measure.beats -= new_duration[1]
							print(f"LOG: Carrying over {tied_carryover_beats} beats to tie, and filling in rest of measure.")
							self.complete_measure(new_measure, carryover=True)

				else:
					new_measure.pattern.append(new_duration[0])

			self.pattern += new_measure.pattern
			self.pattern.append(" | ")
			print(f"LOG: {new_measure.beats} in measure {new_measure.number}. Adding it's pattern: {new_measure.pattern}: ")
			
		print(f"DISPLAYING finished self.pattern: {self.pattern}")

	def fill_carry_over(self, measure, carryover_beats, tied=True):
		print(f"LOG: (fill_carry_over) filling carryover of {carryover_beats} beats")
		for duration in self.duration_list:
			print(f"LOG: Checking if {duration[1]} beats fits inside {carryover_beats} remaining beats")
			if duration[1] <= carryover_beats:
				print(f"LOG: {duration} found to fit ")
				if tied == True:
					measure.pattern.insert(0, duration[0]+"~")
				else:
					measure.pattern.insert(0, duration[0])
				carryover_beats -= duration[1]
		# Remove tie from last duration
		if tied == True:
			measure.pattern[-1] = measure.pattern[-1][:-1]

	def complete_measure(self, measure, carryover=False):
		# takes measure as argument. If carryover is True, adds a tie to last duration
		# Addition of "~" in the last list element for carryover=True could probably be done better. But not certain on that as measure.pattern is a list reference passed by value
		remaining_beats = measure.beats_per_measure - measure.beats
		print(f"LOG: {remaining_beats} left in measure. Attempting to fill.")

		insertions = 0
		for duration in self.duration_list:
			if duration[1] == remaining_beats:
				print(f"LOG: {duration} has been found to match {remaining_beats} remaining beats. Adding to measure")
				if carryover == False:
					measure.pattern.append(duration[0])
				else:
					measure.pattern.append(duration[0]+"~")
				measure.beats += duration[1]
				# should only need 1 of the following 2 lines
				remaining_beats -= duration[1]
				break
			elif duration[1] < remaining_beats:
				print(f"LOG: {duration} has been found to fit in {remaining_beats} remaining_beats")
				if insertions == 0 and carryover == False:
					measure.pattern.insert(len(measure.pattern)-insertions, duration[0])
				else:
					measure.pattern.insert(len(measure.pattern)-insertions, duration[0]+"~")
				insertions += 1
				measure.beats += duration[1]
				remaining_beats -= duration[1]

	def get_random_duration(self, beat_limit=None):
		if not beat_limit:
			return random.choices(self.duration_list, self.weights_list)[0]
		else:
			limited_durations = self.duration_list.copy()
			limited_weights = self.weights_list.copy()
			for i in range(len(self.duration_list)):
				if self.duration_list[i][1] > beat_limit:
					del(limited_durations[0])
					del(limited_weights[0])
			return random.choices(limited_durations, limited_weights)

	# Proportion generation could well change with user feedback.
	# Does time signature matter? Are 1/8 notes more common in 6/8 than 3/4?
	# Should large notes be left appropriate, and allowed to form long tied carryovers? -> could be a user setting?
	def get_weights(self):
		return [weight[1] for weight in [dw for dw in DURATION_WEIGHTS if dw[0] in [d[0] for d in self.duration_list]]]

	def get_appropriate_durations(self):
		beat_values = self.generate_beat_value_list()
		return [bv for bv in beat_values if self.time_signature[0] >= bv[1]]


	def generate_beat_value_list(self):
		print("LOG: Beginning generate_beat_value_list")
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


class Measure:
	def __init__(self, number, beats_per_measure):
		# measure number not necessary, but used to help debugging
		self.number = number
		self.beats = 0
		self.beats_per_measure = beats_per_measure
		self.pattern = []

rhythm = Rhythm(10, (3,4))