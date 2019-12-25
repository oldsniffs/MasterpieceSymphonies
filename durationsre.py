import random

ALL_DURATION_NOTATIONS = ['1.', '1', '2.', '2', '4.', '4', '8.', '8', '16.', '16', '32', '32.', '64']
DURATION_WEIGHTS = [('1.', 3), ('1', 12), ('2.', 6), ('2', 18), ('4.', 8), ('4', 25), ('8.', 8), ('8', 20), ('16.', 6), ('16', 12), ('32.', 6), ('32', 2), ('64', 2)]

FILLER_ONLY_DURATIONS = ['1..', '2..', '4..', '8..', '16..', '32..', '64..'] # God forbid 64.. is ever used

GROUPING_DURATIONS = ["4", "8", "16", "32"]
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
		self.all_durations = self.get_all_durations()
		print(f"DISPLAYING self.all_durations: {self.all_durations}\n")
		self.appropriate_durations = self.get_appropriate_durations()
		print(f"DISPLAYING self.appropriate_durations: {self.appropriate_durations}\n")
		self.whole_beat_durations = self.get_whole_beat_durations()
		print(f"DISPLAYING self.whole_beat_durations: {self.whole_beat_durations}\n")
		self.weights_list = self.get_weights()
		print(f"DISPLAYING self.weights_list: {self.weights_list}\n")

#(self, number, time_signature, all_durations, appropriate_durations, duration_weights, right_carryover_beats=0, left_carryover_beats=0, grouping=[]):

		self.pattern = []
		self.test_measure = Measure(1, self.time_signature, self.all_durations, self.appropriate_durations, self.whole_beat_durations, self.weights_list)
		self.test_measure.display_right_hand()


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

	def get_all_durations(self):
		beat_values = self.generate_beat_value_list()
		all_durations = [bv for bv in beat_values if self.time_signature[0]]
		all_durations = sorted(all_durations, key=lambda d: d[1])
		all_durations.reverse()
		return all_durations

	def get_appropriate_durations(self):
		beat_values = self.generate_beat_value_list()
		return [bv for bv in beat_values if self.time_signature[0] >= bv[1] and ".." not in bv[0]]

	def get_whole_beat_durations(self):
		return [d for d in self.all_durations if float(int(d[1])) == d[1]]

	def generate_beat_value_list(self):
		beat_values = []
		for d in ALL_DURATION_NOTATIONS+FILLER_ONLY_DURATIONS:

			if '..' in d:
				base_value = 1/int(d[:-2])
				beat_value = base_value * self.time_signature[1] * 1.75
			elif '.' in d:
				base_value = 1/int(d[:-1])
				beat_value = base_value * self.time_signature[1] * 1.5
			else:
				base_value = 1/int(d)
				beat_value = base_value * self.time_signature[1]

			beat_values.append((d, beat_value))
		
		return beat_values

	# Proportion generation could well change with user feedback.
	# Does time signature matter? Are 1/8 notes more common in 6/8 than 3/4?
	# Should large notes be left appropriate, and allowed to form long tied carryovers? -> Yes, but weight should drop
	def get_weights(self):
		return [weight[1] for weight in [dw for dw in DURATION_WEIGHTS if dw[0] in [d[0] for d in self.appropriate_durations]]]


class Measure:
	def __init__(self, number, time_signature, all_durations, appropriate_durations, whole_beat_durations, duration_weights, right_carryover_beats=0, left_carryover_beats=0, grouping=[]):
		# measure number not necessary, but used to help debugging
		self.number = number
		self.time_signature = time_signature
		self.beats_per_measure = time_signature[0]

		self.all_durations = all_durations
		self.appropriate_durations = appropriate_durations
		self.whole_beat_durations = whole_beat_durations
		self.duration_weights = duration_weights

		self.right_carryover_beats = right_carryover_beats
		self.grouping = grouping

		# Patterns are lists of beats, 1 per bpm, and beats are lists of durations
		# Beat lists can be empty if previous duration is fully covering that beat
		self.right_hand_pattern = []
		self.right_overflow_beats = self.fill_right_hand()
		self.left_hand_pattern = []

	def display_right_hand(self):
		for b in self.right_hand_pattern:
			count = 0
			for d in b:
				print(f"{d[0]}", end=" ")
				count += d[1]
			print(f" /  --> {count}")
		print(f"Overflow beats: {self.right_overflow_beats}")

	def fill_right_hand(self):
		print(f"LOG: Starting fill of measure {self.number}, right hand pattern")
		grouping = self.grouping
		carryover_beats = self.right_carryover_beats
		filled_beats = 0

		next_beat_empty = False # Prob deprecated, using filled_beats var

		for beat in range(self.beats_per_measure):
			new_beat = []
			count = 0 # Floatable beat count within beat
			if beat > 0:
				print(f"LOG: Starting beat {beat+1} with {carryover_beats} carryover_beats and {filled_beats} filled beats. Count reset to {count}")

			if filled_beats:
				print(f"LOG (filled_beats): {filled_beats} filled_beats left. Appending empty beat list")
				self.right_hand_pattern.append(new_beat)
				print(f"LOG (filled_beats): {new_beat} appended to measure --> {self.right_hand_pattern}")
				filled_beats -= 1
				continue
		
			if carryover_beats:

				if carryover_beats < 1:
					new_duration, carryover_count = self.fill_small_carryover(carryover_beats, new_beat)
					count += carryover_count
					carryover_beats -= new_duration[1]	

				# Overflows measure
				# elif len(self.right_hand_pattern) + carryover_beats > self.beats_per_measure:
				# 	new_duration = self.find_duration_by_beat_value(self.beats_per_measure-len(self.right_hand_pattern))
				# 	carryover_beats = carryover_beats-new_duration[1]
				# 	filled_beats = new_duration[1]-1

				else:
					print(f"LOG: Carryover {carryover_beats} >= 1")
					biggest_whole = float(int(carryover_beats))
					new_duration, whole_carryover = self.get_filled_beats_spawn(biggest_whole)
					carryover_beats -= new_duration[1]
					filled_beats = new_duration[1]-1
					if carryover_beats:
						new_duration = (new_duration[0]+"~", new_duration[1])
					print(f"LOG: Carryover {carryover_beats} filled {filled_beats}")

					# # Ends on line
					# if carryover_beats % 1 == 0:
					# 	new_duration = self.find_duration_by_beat_value(carryover_beats)
					# 	filled_beats = new_duration[1]-1
					# 	carryover_beats = 0

					# # Does not land on line, more than 1 beat
					# else:
					# 	new_duration = self.find_duration_by_beat_value(float(int(carryover_beats)))
					# 	filled_beats = new_duration[1]-1
					# 	carryover_beats -= new_duration[1]

				print(f"LOG: Appending new_duration {new_duration} to new_beat at count {count}")
				new_beat.append(new_duration)
				count+=new_duration[1]

			while count < 1:

				virgin_duration = self.get_random_duration()
				print(f"LOG: Virgin selected --> {virgin_duration} at count {count}")

				if count + virgin_duration[1] <= 1:
					new_duration = virgin_duration

				elif count == 0 and virgin_duration[1] % 1 == 0:
					for duration in [d for d in self.whole_beat_durations if d[1] + len(self.right_hand_pattern) <= self.beats_per_measure]:
						if duration[1] == virgin_duration[1]:
							new_duration = duration
							filled_beats = new_duration[1]-1
							print(f"LOG(==): {duration} selected as biggest available whole beat duration.")
							break
						elif duration[1] < virgin_duration[1]:
							new_duration = duration
							carryover_beats = virgin_duration[1] - new_duration[1]
							filled_beats = new_duration[1]-1
							print(f"LOG(<): {duration} selected as biggest available whole beat duration. Carryover: {carryover_beats}")

				else:
					# count + virgin_duration[1] + len(self.right_hand_pattern) >= self.beats_per_measure:
					print(f"LOG: Virgin OVERFLOWS by {virgin_duration[1]-(1-count)}")
					new_duration = self.complete_beat(1-count, new_beat) 
					carryover_beats = virgin_duration[1]-(1-count)
					count += (1-count)-new_duration[1]

				print(f"LOG: Appending new_duration {new_duration} to new_beat at count {count}")
				new_beat.append(new_duration)
				count+=new_duration[1]

			print(f"LOG: Count {count} reached for beat {len(self.right_hand_pattern)+1}. Appending to right_hand_pattern with {filled_beats} filled_beats and {carryover_beats} carryover_beats")
			self.right_hand_pattern.append(new_beat)


		print(f"LOG: End of Measure reached. Returning {carryover_beats} carryover_beats OR converting {filled_beats} filled_beats for right_overflow_beats variable")
		
		# Depped because filling beat spawns will check remaining measure lenght at selection

		# if filled_beats:
		# 	print(f"LOG: Fill beats remaining. Altering spawning duration and converting remaining fills to carryover")
		# 	# Get last duration (which made filled_beats), replace it with duration, length by filled 
		# 	for i in range(len(self.right_hand_pattern), 0 , -1):
		# 		print(f"DEBUG: self.right_hand_pattern[{i-1}]: {self.right_hand_pattern[i-1]}")
		# 		if self.right_hand_pattern[i-1] != []:
		# 			self.right_hand_pattern[i-1][0] = self.find_duration_by_beat_value(self.right_hand_pattern[i-1][0][1]-filled_beats)
		# 			break
		carryover_beats += filled_beats
		return carryover_beats

	def get_filled_beats_spawn(self, spawn_beats):
		# Appends with tie if no exact match, returns finisher for new_duration
		print(f"LOG(get_filled_beats_spawn): Seeking whole beat for spawn_beats {spawn_beats} + past beats {len(self.right_hand_pattern)} <= beats_per_measure {self.beats_per_measure}")
		for duration in [d for d in self.whole_beat_durations if d[1] + len(self.right_hand_pattern) <= self.beats_per_measure]:
			if duration[1] <= spawn_beats:
				print(f"LOG(get_filled_beats_spawn): {duration} selected. Returning with whole_carryover {spawn_beats-duration[1]}")
				return duration, spawn_beats-duration[1]

	def find_best_fit_by_beat_value(self, beat_value): # Use if match might not exist. Returns biggest fit, remainder
		print(f"LOG(find_best_fit_by_beat_value): seeking duration for beat value {beat_value}")
		for duration in self.all_durations:
			if duration[1] == beat_value:
				return duration, 0
			elif duration[1] < beat_value:
				return duration, beat_value-duration[1]

	def find_duration_by_beat_value(self, beat_value): # Use if you know match exists
		print(f"LOG(find_duration_by_beat_value): seeking duration for beat value {beat_value}")
		for duration in self.all_durations:
			if duration[1] == beat_value:
				return duration

	# Should == duration always be tied?
	# This could be merged with carryover. Only difference is if the position of the larger/smaller durations from a split matters
	def complete_beat(self, remaining_beats, pattern):
		print(f"LOG(complete_beat): Completing beat, {remaining_beats} beats remaining")
		for duration in self.all_durations:
			if duration[1] == remaining_beats:
				print(f"LOG(complete_beat) {duration} matches {remaining_beats} remaining_beats. Returning")
				return (duration[0]+"~", duration[1])
			elif duration[1] < remaining_beats:
				print(f"LOG(complete_beat): appending {duration} towards {remaining_beats} remaining_beats")
				pattern.append((duration[0]+"~", duration[1]))
				remaining_beats -= duration[1]


	def fill_small_carryover(self, carryover_beats, pattern):

		print(f"LOG(fill_small_carryover): Filling carryover at beat {len(self.right_hand_pattern)+1} starting with {carryover_beats} carryover beats. Attempting to fill")
		remaining_beats = carryover_beats
		count = 0

		for duration in self.all_durations:
			print(f"LOG(fill_small_carryover: Checking {duration} with {remaining_beats} beats remaining to fill")
			if duration[1] == remaining_beats:
				print(f"LOG(fill_small_carryover) {duration} matches {remaining_beats} remaining_beats. Returning")
				return (duration[0], duration[1]), count
			elif duration[1] < remaining_beats:
				# if self.time_signature[1] % duration[1]
				print(f"LOG(fill_small_carryover): {duration} found to fit in {remaining_beats}. Appending. {remaining_beats-duration[1]} beats remaining")
				pattern.append((duration[0]+"~", duration[1]))
				remaining_beats -= duration[1]
				count += duration[1]

	def get_random_duration(self, beat_limit=None):
		if not beat_limit:
			return random.choices(self.appropriate_durations, self.duration_weights)[0]
		else:
			limited_durations = self.appropriate_durations.copy()
			limited_weights = self.duration_weights.copy()
			for i in range(len(self.appropriate_durations)):
				if self.appropriate_durations[i][1] > beat_limit:
					del(limited_durations[0])
					del(limited_weights[0])
			return random.choices(limited_durations, limited_weights)


if __name__ == "__main__":
	rhythm = Rhythm(16, (7,8))
	print(rhythm.display_right_hand_pattern())

	# measure = Measure(1, (4,4), carryover_beats=.5)
