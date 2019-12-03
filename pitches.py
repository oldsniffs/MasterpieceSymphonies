"""
TODO: Direction needs to be tweaked so the farther from anchor point, the more likely direction is to return
TODO: If meets client needs, interval magnitude selection must be normalized to a key, so accidentals are key based. Would need a list for natural steps, and a way to know where
appropriate half note accidentals should be avoided (so no C flat, etc)
"""

import random

MAJOR_KEY_SCALE = [2, 2, 1, 2, 2, 2, 1, 2]
MINOR_KEY_SCALE = [2, 1, 2, 2, 1, 2, 2, 1]
# If not needed elsewhere, can move some of following into generate_master_list
A_TO_G = ["a", "b", "c", "d", "e", "f", "g"]
OCTAVE_SUFFIXES = [",,,,", ",,,", ",,", ",", "", "'", "''", "'''"]
ACCIDENTAL = ["es", "", "is"]


# Generates master list of all available pitches of all accidental formats for MASTER_LIST
def generate_master_list():
    master_list = []

    for suffix in OCTAVE_SUFFIXES:
        for p in A_TO_G:
            for a in ACCIDENTAL:
                master_list.append(f"{p}{suffix}{a}")

    # Finishing touch to match up with real piano
    del master_list[0]
    for n in ["a'''es", "a'''", "a'''is", "b'''es", "b'''", "b'''is", "c''''es", "c''''"]:
        master_list.append(n)

    return master_list


MASTER_LIST = generate_master_list()


def generate_sharp_list(master):
    sharp_list = master
    for p in sharp_list:
        if "es" in p:
            sharp_list.remove(p)
    return sharp_list


def generate_flat_list(master):
    flat_list = master
    for p in flat_list:
        if "is" in p:
            flat_list.remove(p)


def generate_key(root, key_type):
    if key_type == "major":
        # key is a list of indexes for either flat or sharp pitch list, highlighting in key notes
        key = []
        if root in ["g", ""]



def allot_pitches(rhythm_list, pitch_range='Normal', accidental_frequency=6):
    # Placeholder if statement to allow user decided pitch ranges
    if pitch_range != 'Normal':
        pass

    direction = "up"
    l_index = 10
    starting_l_pitch = left_pitches[l_index]
    print(starting_l_pitch)

    l_pitches = [starting_l_pitch]
    print(f'rhythm list length: {len(rhythm_list)}')
    while len(l_pitches) < len(rhythm_list):
        # Rests
        # Can base on user defined rest frequency, or default
        if random.randint(0, 22) == 1:
            l_pitches.append('r')

        else:
            try:
                interval = get_interval_magnitude()
                direction = get_interval_direction(direction)
                if direction == "up":
                    l_index += interval
                else:
                    l_index -= interval
                print(l_index)
                print(left_pitches[l_index])
                l_pitches.append(left_pitches[l_index])
            except IndexError:
                if direction == "up":
                    direction = "down"
                else:
                    direciton = "up"

    return l_pitches


def get_interval_magnitude():
    roll = random.randint(1, 100)
    interval = 0
    if roll <= 10:
        interval = 1
    elif 10 < roll <= 35:
        interval = 2
    elif 35 < roll <= 40:
        interval = 3
    elif 40 < roll <= 60:
        interval = 4
    elif 60 < roll <= 68:
        interval = 5
    elif 68 < roll <= 72:
        interval = 0
    elif 72 < roll <= 80:
        interval = 6
    elif 80 < roll <= 85:
        interval = 7
    elif 85 < roll <= 90:
        interval = 8
    elif 90 < roll <= 94:
        interval = 9
    elif 94 < roll <= 96:
        interval = 10
    elif 96 < roll <= 98:
        interval = 11
    elif 98 < roll <= 100:
        interval = 12

    return interval


def get_interval_direction(last_direction):
    flip = False
    if random.randint(0,2) == 0:
        flip = True

    if not flip:
        return last_direction
    else:
        if last_direction == "up":
            return "down"
        else:
            return "up"


def make_accidental(note):
    if 'c' or 'f' in note:
        return sharpen(note)
    elif 'b' or 'e' in note:
        return flatten(note)
    elif random.randint(0,1) == 1:
        return sharpen(note)
    else:
        return flatten(note)


def flatten(note):
    return f'{note[0]}es{note[1:]}'


def sharpen(note):
    return f'{note[0]}is{note[1:]}'


if __name__ == "__main__":
    import durations

    durations_list = durations.allot_rhythm(64)

    for i in allot_pitches(durations_list):
        print(i)