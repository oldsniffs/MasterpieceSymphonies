#TODO: Add ties
# Can check for measure break, and use a tie to maintain randomized rhythm
# TODO: "beats" value has to be adjustable to match time signature

import random


ALL_DURATION_NOTATIONS = ['1', '1.', '2', '2.', '4', '4.', '8', '8.', '16', '16.', '32']


# Indexing note durations
# list of tuples: ('string value of duration for lilypond', beat value determined by time signature)
# Whole notes are 1, half are 2, etc
def generate_beat_value_list(time_signature):
    # Some durations will be invalid in a particular time signature
    # dotted wholes will be invalid in most
    # strike any durations that are longer than a single measure

    beat_values = []
    for d in ALL_DURATION_NOTATIONS:

        if '.' in d:
            base_value = 1/int(d[:-1])
            beat_value = base_value * time_signature[1] * 1.5
        else:
            base_value = 1/int(d)
            beat_value = base_value * time_signature[1]

        beat_values.append((d, beat_value))

    # Cull list for beat values bigger than possible measure
    # OR - have allot_rhythm convert it into multiple tied notes across measure marker

    return beat_values


def allot_rhythm(total_beats, time_signature=(4, 4)):
    cycle_count = 0
    rhythm = []
    beat_count = 0
    proportions = get_proportion_list(index=1)
    while beat_count != total_beats:
        new_duration = add_duration(proportions)
        old_beat_count = beat_count
        beat_count = beat_count + new_duration[1]

        # if note carries into new measure, and song isn't over
        if check_bar_cross(old_beat_count, beat_count, time_signature) and beat_count < total_beats:
            # either reroll, or enter new measure with 2 tied notes
            print('bar crossed, ')
            if random.randint(0, 1) == 0:
                print('killing overflow duration')
                rhythm.pop()
                beat_count -= new_duration[1]
                continue
            else:
                print('splitting over measure')
                overflow = beat_count % time_signature[0]
                stem = time_signature[0] - overflow
                beat_values = generate_beat_value_list(time_signature)
                for bv in beat_values:
                    if stem == bv[1]:
                        stem_duration = bv
                        rhythm.append(f'{stem_duration[0]}~')
                    elif overflow == bv[1]:
                        new_duration = bv

        rhythm.append(new_duration[0])

        if '.' in new_duration[0] and beat_count < total_beats:
            if '2' in new_duration[0]:
                complementary_duration = ('4', 1)
            elif '4' in new_duration[0]:
                complementary_duration = ('8', .5)
            elif '8' in new_duration[0]:
                complementary_duration = ('16', .25)
            elif '16' in new_duration[0]:
                complementary_duration = ('32', .125)
            rhythm.append(complementary_duration[0])
            beat_count = beat_count + complementary_duration[1]

        # 1/4, 1/8, 1/16, and 1/32 notes get a chance to extend to a set of like durations
        if new_duration[0] == '4':
            # roll a multiple
            # check if it will fit piece, fall on measure line
            sequence = random.choices([1, 2, 3], [3, 2, 1])





        if beat_count > total_beats:
            print('crossed limit, getting new duration')
            rhythm.pop()
            beat_count -= new_duration[1]
            continue

        print(f'beat count:{beat_count}  newest beat:{new_duration[1]}')

    return rhythm


def beats_left_in_measure(current_beat, time_signature):
    pass

# Check to see if a bar has been crossed by a beat
def check_bar_cross(start_beat, end_beat, time_signature):
    if start_beat < end_beat - (end_beat % time_signature[0]):
        return True
    else:
        return False


def add_duration(proportion_list):
    index = random.randint(0, len(proportion_list)-1)
    return proportion_list[index]


# durations list gives tuples, 1st value is lily duration notation, second is number of beats to count in allot_rhythm
# Depending on how durations get randomized, this list might be deprecated
durations = [('1', 4), ('2', 2), ('2.', 3), ('4', 1), ('4.', 1.5), ('8', .5), (16, .25)]
def get_proportion_list(index=1):
    if index == 1:
        proportion_list = []
        for i in range(3):
            proportion_list.append(('1', 4))
        for i in range(5):
            proportion_list.append(('2', 2))
        for i in range(2):
            proportion_list.append(('2.', 3))
        for i in range(12):
            proportion_list.append(('4', 1))
        for i in range(1):
            proportion_list.append(('4.', 1.5))
        for i in range(8):
            proportion_list.append(('8', .5))
        for i in range(2):
            proportion_list.append(('8.', .75))
        for i in range(3):
            proportion_list.append(('16', .25))
        for i in range(2):
            proportion_list.append(('16.', .375))
        for i in range(1):
            proportion_list.append(('32', .125))
        return proportion_list

    if index == 2:
        # A sample 3/4 list
        pass

if __name__ == '__main__':

    for i in allot_rhythm(64):
        print(i)

    # for v in generate_beat_value_list((4, 4)):
    #     print(v)
