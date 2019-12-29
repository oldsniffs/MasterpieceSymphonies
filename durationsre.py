import random

ALL_DURATION_NOTATIONS = ['1.', '1', '2.', '2', '4.', '4', '8.', '8', '16.', '16', '32.', '32', '64']
DURATION_WEIGHTS = [(6, 2), (4, 6), (3, 5), (2, 16), (1.5, 8), (1, 25), (.75, 8), (.5, 20), (.375, 6), (.25, 12), (.1875, 2), (.125, 5), (.0625, 1)]

FILLER_ONLY_DURATIONS = ['1..', '2..', '4..', '8..', '16..', '32..', '64..'] # God forbid 64.. is ever used

PAIRING_DURATIONS = [.5, .25, .125, .0625]
PAIRING_LENGTHS = [1, 2, 3, 4, 5]
# Weights: [(chance/10 of pairing[length weights])]
PAIRING_WEIGHTS = [(2, [6, 2, 1, 0, 0]), (4, [1, 4, 2, 1, 0]), (9, [2, 6, 4, 2, 1]), (9, [2, 6, 4, 2, 2])]


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

#(self, number, time_signature, all_durations, appropriate_durations, duration_weights, right_carryover_beats=0, left_carryover_beats=0, pairing=[]):
		self.pattern = []

		self.fill_pattern()

		self.right_notation = self.prepare_right_notation()
		self.left_notation = self.prepare_left_notation()

	def prepare_left_notation(self):
		notation = []
		for measure in self.pattern:
			for beat in measure.left_hand_pattern:
				for duration in beat:
					notation.append(duration[0])
			notation.append("|")
		return notation

	def prepare_right_notation(self):
		notation = []
		m_count = 1
		for measure in self.pattern:
			notation.append(f"M{m_count}")
			for beat in measure.right_hand_pattern:
				for duration in beat:
					notation.append(duration[0][0])
			notation.append("|")
			m_count += 1
		return notation

	def fill_pattern(self):
		right_carryover = 0
		left_carryover = 0
		pairing = []
		final_measure = False

		for measure in range(self.measures):
			if measure+1 == self.measures:
				final_measure = True

			self.pattern.append(Measure(measure+1, self.time_signature, self.all_durations, self.appropriate_durations, self.whole_beat_durations, self.weights_list, right_carryover_beats=right_carryover, left_carryover_beats=left_carryover, pairing=pairing, final_measure=final_measure))

			right_carryover = self.pattern[-1].right_carryover_beats
			pairing = self.pattern[-1].leftover_pairing

	def display_right_hand_pattern(self):
		rh_display = ""
		for measure in self.pattern:
			measure.display_right_hand()

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
		return [weight[1] for weight in [dw for dw in DURATION_WEIGHTS if dw[0] in [d[1] for d in self.appropriate_durations]]]


class Measure:
	def __init__(self, number, time_signature, all_durations, appropriate_durations, whole_beat_durations, duration_weights, right_carryover_beats=0, left_carryover_beats=0, pairing=[], final_measure=False):
		# measure number not necessary, but used to help debugging
		self.number = number
		self.time_signature = time_signature
		self.beats_per_measure = time_signature[0]
		self.final_measure = final_measure

		self.all_durations = all_durations
		self.appropriate_durations = appropriate_durations
		self.whole_beat_durations = whole_beat_durations
		self.right_duration_weights = duration_weights
		self.left_duration_weights = self.modify_weights_for_lh()

		self.right_carryover_beats = right_carryover_beats
		self.pairing = pairing
		self.leftover_pairing = []

		# Patterns are lists of beats, 1 per bpm, and beats are lists of durations
		# Beat lists can be empty if previous duration is fully covering that beat
		self.right_hand_pattern = []
		self.right_carryover_beats = self.fill_hand(self.right_hand_pattern, "right")
		self.left_hand_pattern = []
		self.left_carryover_beats = self.fill_hand(self.left_hand_pattern, "left")

	def modify_weights_for_lh(self):
		lh_weights = []
		midpoint = int(len(self.right_duration_weights)/2)
		modifier = 1
		for i in range(len(self.right_duration_weights)):
			if i < midpoint:
				modifier = 1.5
			lh_weights.append(self.right_duration_weights[i]*modifier)
		return lh_weights

	def display_right_hand(self):
		for b in self.right_hand_pattern:
			count = 0
			for d in [d for d in b if d[0] != "|"]:
				print(f"{d[0]}", end=" ")
				count += d[1]
			print(f" /  --> {count}")
		print(f"Overflow beats: {self.right_carryover_beats}")

	def get_carryovers(self):
		return right_carryover_beats, left_carryover_beats


	# For left hand, check each beat (or duration, by count) to see if right hand has a duration inserted. Roll a chance to copy that duration
	# For left hand, run the weights through a modifier to weight towards longer durations
	def fill_hand(self, pattern, hand):

		if self.final_measure == True:
			print(f"LOG: === FINAL MEASURE ===")
		print(f"LOG: Starting fill of measure {self.number}, right hand pattern")
		pairing = self.pairing
		carryover_beats = self.right_carryover_beats
		filled_beats = 0

		for beat in range(self.beats_per_measure):
			new_beat = []
			count = 0 # Floatable beat count within beat

			# Not sure why there's a why condition for this LOG
			if beat > 0:
				print(f"LOG: Starting beat {beat+1} with {carryover_beats} carryover_beats and {filled_beats} filled beats. Count reset to {count}")

			if filled_beats:
				print(f"LOG (filled_beats): {filled_beats} filled_beats left. Appending empty beat list")
				pattern.append(new_beat)
				print(f"LOG (filled_beats): {new_beat} appended to measure --> {pattern}")
				filled_beats -= 1
				continue
		
			# Change to elif?
			if carryover_beats:

				if carryover_beats < 1:
					new_duration, carryover_count = self.fill_small_carryover(carryover_beats, new_beat)
					count += carryover_count
					carryover_beats -= new_duration[1]	

				else:
					print(f"LOG: Carryover {carryover_beats} >= 1")
					biggest_whole = float(int(carryover_beats))
					new_duration, whole_carryover = self.get_filled_beats_spawn(biggest_whole, pattern)
					carryover_beats -= new_duration[1]
					filled_beats = new_duration[1]-1
					if carryover_beats:
						new_duration = (new_duration[0]+"~", new_duration[1])
					print(f"LOG: Carryover {carryover_beats} filled {filled_beats}")

				print(f"LOG: Appending new_duration {new_duration} to new_beat at count {count}")
				new_beat.append(((new_duration), count))
				count+=new_duration[1]

			while count < 1:

				if pairing:
					print(f"LOG: Pairing detected: {pairing}")
					new_duration = pairing[0]
					pairing[1] -= 1
					# Count is over, clear list
					if not pairing[1]:
						print("LOG: End of pairing")
						pairing = []
					print(f"LOG: Appending PAIRED new_duration {new_duration} to new_beat at beat count {count}")
					new_beat.append(((new_duration), count))
					count += new_duration[1]
					continue

				virgin_duration = self.get_random_duration(hand)
				print(f"LOG: Virgin selected --> {virgin_duration} at count {count}")

				if count + virgin_duration[1] <= 1:
					new_duration = virgin_duration
					pairing = self.check_pairing(new_duration, count)

				elif count == 0 and virgin_duration[1] % 1 == 0:
					for duration in [d for d in self.whole_beat_durations if d[1] + len(pattern) <= self.beats_per_measure]:
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
					print(f"LOG: Virgin OVERFLOWS by {virgin_duration[1]-(1-count)}")
					new_duration = self.complete_beat(1-count, new_beat, count)
					carryover_beats = virgin_duration[1]-(1-count)
					count += (1-count)-new_duration[1]

				print(f"LOG: Appending new_duration {new_duration} to new_beat at count {count}")
				new_beat.append(((new_duration), count))

				count+=new_duration[1]

			# If final measure, and we have overflow, remove tie

			print(f"LOG: Count {count} reached for beat {len(pattern)+1}. Appending to right_hand_pattern with {filled_beats} filled_beats and {carryover_beats} carryover_beats")
			pattern.append(new_beat)

		print(f"LOG: End of Measure reached. Returning {carryover_beats} carryover_beats OR converting {filled_beats} filled_beats for right_carryover_beats variable")

		carryover_beats += filled_beats

		if self.final_measure == True and carryover_beats:
			self.remove_tie_if_final(pattern)
			pattern[-1].append(("|", 0))
			self.leftover_pairing = pairing

		return carryover_beats

	# Returns pairing list. empty if none
	def check_pairing(self, duration, count):
		if duration[1] not in PAIRING_DURATIONS:
			return []
		
		# check if its on strong beat or beat subdivision
		if self.check_beat_strength(duration, count) == True:
			pairing = self.get_pairing(duration)
			print(f"LOG(check_pairing): Pairing {pairing} created. Returning")
			return pairing


	def check_beat_strength(self, duration, count):
		print(f"LOG(check_beat_strength): Checking if a duration {duration} on count {count} is strong")
		if (count/duration[1]) % 2 == 0:
			print(f"LOG(check_beat_strength): STRONG")
			return True
		# Might not need this else
		else:
			print(f"LOG(check_beat_strength): WEAK")
			return False

	def get_pairing(self, duration):
		print(f"LOG(get_pairing): Getting pairing for {duration}")
		weights = PAIRING_WEIGHTS[PAIRING_DURATIONS.index(duration[1])]
		if random.randint(1, 10) < weights[0]:
			return [duration, random.choices(PAIRING_LENGTHS, weights[1])[0]]

	def remove_tie_if_final(self, pattern):
		for i in range(len(pattern)-1, 0, -1):
			if pattern[i]:
				pattern[i][-1] = (pattern[i][-1][0][:-1], pattern[i][-1][1])

	def get_filled_beats_spawn(self, spawn_beats, pattern):
		# Appends with tie if no exact match, returns finisher for new_duration
		print(f"LOG(get_filled_beats_spawn): Seeking whole beat for spawn_beats {spawn_beats} + past beats {len(pattern)} <= beats_per_measure {self.beats_per_measure}")
		for duration in [d for d in self.whole_beat_durations if d[1] + len(pattern) <= self.beats_per_measure]:
			if duration[1] <= spawn_beats:
				print(f"LOG(get_filled_beats_spawn): {duration} selected. Returning with whole_carryover {spawn_beats-duration[1]}")
				return duration, spawn_beats-duration[1]

	def find_duration_by_beat_value(self, beat_value): # Use if you know match exists
		print(f"LOG(find_duration_by_beat_value): seeking duration for beat value {beat_value}")
		for duration in self.all_durations:
			if duration[1] == beat_value:
				return duration

	def complete_beat(self, remaining_beats, pattern, count):
		print(f"LOG(complete_beat): Completing beat, {remaining_beats} beats remaining")
		for duration in self.all_durations:
			if duration[1] == remaining_beats:
				print(f"LOG(complete_beat) {duration} matches {remaining_beats} remaining_beats. Returning")
				return (duration[0]+"~", duration[1])
			elif duration[1] < remaining_beats:
				print(f"LOG(complete_beat): appending {duration} towards {remaining_beats} remaining_beats")
				pattern.append(((duration[0]+"~", duration[1]), count))
				remaining_beats -= duration[1]
				count += duration[1]

	def fill_small_carryover(self, carryover_beats, pattern):

		print(f"LOG(fill_small_carryover): Filling carryover at beat {len(pattern)+1} starting with {carryover_beats} carryover beats. Attempting to fill")
		remaining_beats = carryover_beats
		count = 0

		for duration in self.all_durations:
			if duration[1] == remaining_beats:
				print(f"LOG(fill_small_carryover) {duration} matches {remaining_beats} remaining_beats. Returning")
				return (duration[0], duration[1]), count
			elif duration[1] < remaining_beats:
				# if self.time_signature[1] % duration[1]
				print(f"LOG(fill_small_carryover): {duration} found to fit in {remaining_beats}. Appending. {remaining_beats-duration[1]} beats remaining")
				pattern.append(((duration[0]+"~", duration[1]), count))
				remaining_beats -= duration[1]
				count += duration[1]

	def get_random_duration(self, hand, beat_limit=None):
		if hand == 'right':
			weights = self.right_duration_weights
		else:
			weights = self.left_duration_weights
		if not beat_limit:
			return random.choices(self.appropriate_durations, weights)[0]
		else:
			limited_durations = self.appropriate_durations.copy()
			limited_weights = weights.copy()
			for i in range(len(self.appropriate_durations)):
				if self.appropriate_durations[i][1] > beat_limit:
					del(limited_durations[0])
					del(limited_weights[0])
			return random.choices(limited_durations, limited_weights)


if __name__ == "__main__":
	rhythm = Rhythm(16, (7,8))
	print(rhythm.right_notation)
