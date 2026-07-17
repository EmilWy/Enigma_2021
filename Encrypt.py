import json
url = {
    "Plugboard": "../Plugboard.json",
    "Rotors": "../Rotors.json"
}


class NotFound(Exception):
    pass


class InputError(Exception):
    pass


def get_(what_in_file):
    with open(url["Rotors"], "r") as file:
        info = json.load(file)
    list_of_wanted = []
    for thing in info:
        if thing["Name"] == what_in_file:
            list_of_wanted.append(thing)
    if list_of_wanted == []:
        raise NotFound()
    return list_of_wanted


class Rotor:
    def __init__(self, choosen_rotor):
        self._choosen_rotor = choosen_rotor
        with open(url["Rotors"], "r") as file_of_rotors:
            self._rotors = json.load(file_of_rotors)

    def rotor_list(self):
        for rotor in self._rotors:
            if rotor["Number"] == self._choosen_rotor:
                return rotor["List_of_leters"]

    def index_of_letter(self, letter):
        return self.rotor_list().index(letter)

    def letter_by_index(self, index):
        for letter in self.rotor_list():
            if self.index_of_letter(letter) == index:
                return letter

    def next_letter_in_list_by(self, letter, how_much):
        actual_index = Rotor(self._choosen_rotor).index_of_letter(letter)
        wanted_index = to_not_be_bigger_than_25(actual_index + how_much)
        wanted_letter = Rotor(self._choosen_rotor).letter_by_index(wanted_index)
        return wanted_letter, wanted_index

    def letter_earlier_by(self, letter, how_much):
        actual_index = Rotor(self._choosen_rotor).index_of_letter(letter)
        wanted_index = to_not_be_negative(actual_index - how_much)
        wanted_letter = Rotor(self._choosen_rotor).letter_by_index(wanted_index)
        return wanted_letter, wanted_index

    def move_by(self, letter, how_much):
        if how_much < 0:
            how_much = how_much*(-1)
            new_letter = self.letter_earlier_by(letter, how_much)
        else:
            new_letter = self.next_letter_in_list_by(letter, how_much)
        return new_letter


class Plugboard:
    def __init__(self):
        self._plugboard_settings = ""
        with open(url["Plugboard"], "r") as file_of_plug:
            self._board = json.load(file_of_plug)

    def connect(self, first_letter, second_letter):
        a = self._board[first_letter]
        self._board[a] = a
        b = self._board[second_letter]
        self._board[b] = b
        # if we choose letter in second connection it isnt used in first connection^
        self._board[first_letter] = second_letter
        self._board[second_letter] = first_letter
        with open(url["Plugboard"], "w") as new_plug:
            json.dump(self._board, new_plug)
        new_plug.close()

    def make_it_two(self, plugboard_settings):
        plugboard_settings = plugboard_settings[0:20]
        self.clear()
        final_list = []
        every_sec_let = plugboard_settings[0::2]
        every_third_let = plugboard_settings[1::2]
        if plugboard_settings != "":
            for number in range(0, len(every_third_let)):
                two_let = every_sec_let[number].upper(), every_third_let[number].upper()
                final_list.append(two_let)
                if two_let[0].isdigit() or two_let[1].isdigit():
                    raise ValueError
        return final_list

    def set_plugboard(self, plugboard_settings):
        list_of_settings = self.make_it_two(plugboard_settings)
        for a, b in list_of_settings:
            self.connect(a, b)

    def clear(self):
        for letter in self._board:
            self._board[letter] = letter
        with open(url["Plugboard"], "w") as new_plug:
            json.dump(self._board, new_plug)
        new_plug.close()

    def replace_with_plugboard(self, letter):
        return self._board[letter]


class Reflector:
    def __init__(self, choosen_ref):
        self._choosen_ref = choosen_ref
        with open(url["Rotors"], "r") as file_of_rotors:
            self._reflectors = json.load(file_of_rotors)

    def replace_with_reflector(self, letter):
        for reflector in self._reflectors:
            if reflector["Number"] == self._choosen_ref:
                return reflector[letter]


def to_not_be_bigger_than_25(probably_bigger_number):
    rest = int(probably_bigger_number) % 26
    return rest


def to_not_be_negative(probably_negative_number):
    if probably_negative_number < 0:
        number = 26 + probably_negative_number
        return number
    return probably_negative_number


class Settings:
    def __init__(self, plugboard, reflector, rotor3, rotor2, rotor1, rotor_setting, rotor_position):
        self._rotor1 = rotor1
        self._rotor2 = rotor2
        self._rotor3 = rotor3
        self._reflector = find_error(reflector, 1)
        self._rotor_setting = find_error(rotor_setting, 3)
        self._rotor_position = find_error(rotor_position, 3)
        self.plugboard = plugboard
        self._oryginal_rotors_p = rotor_position

    def multi_encryption(self, letter_to_encrypt):
        Plugboard().set_plugboard(self.plugboard)
        # ^ setting plugboard
        beginign_pos_of_third_p = self._oryginal_rotors_p[2]
        beginign_pos_of_second_p = self._oryginal_rotors_p[2]
        self.change_rotor_p_by_one(2)
        if self._rotor_position[2] == beginign_pos_of_third_p:
            self.change_rotor_p_by_one(1)
            if self._rotor_position[1] == beginign_pos_of_second_p:
                self.change_rotor_p_by_one(0)
        # ^ rotors moving with each encryption
        r_p = self._rotor_position
        r_s = self._rotor_setting
        letter_to_encrypt_1 = letter_to_encrypt
        letter_to_encrypt_1 = Plugboard().replace_with_plugboard(letter_to_encrypt)
        # replacing letter with letter in plugboard
        encrypted_first_letter = encrypt(letter_to_encrypt_1, self._rotor1, r_s[2], r_p[2])
        encrypted_second_letter = encrypt(encrypted_first_letter, self._rotor2, r_s[1], r_p[1])
        encrypted_third_letter = encrypt(encrypted_second_letter, self._rotor3, r_s[0], r_p[0])
        # encryption after third rotor
        encrypted_third_letter_2 = Reflector(self._reflector).replace_with_reflector(encrypted_third_letter)
        # relacing letter with letter in choosen reflector
        encrypted_fourth_letter = decrypt(encrypted_third_letter_2, self._rotor3, r_s[0], r_p[0])
        encrypted_fifth_letter = decrypt(encrypted_fourth_letter, self._rotor2, r_s[1], r_p[1])
        encrypted_sixth_letter = decrypt(encrypted_fifth_letter, self._rotor1, r_s[2], r_p[2])
        encrypted_sixth_letter_2 = Plugboard().replace_with_plugboard(encrypted_sixth_letter)
        # replacement with plugboard
        Step_by_step = step_by_step(
            Plugboard().make_it_two(self.plugboard),
            r_p, letter_to_encrypt, letter_to_encrypt_1,
            encrypted_first_letter, encrypted_second_letter,
            encrypted_third_letter, encrypted_third_letter_2,
            encrypted_fourth_letter, encrypted_fifth_letter,
            encrypted_sixth_letter, encrypted_sixth_letter_2
        )
        return encrypted_sixth_letter_2, Step_by_step

    def change_rotor_p_by_one(self, which_rotor):
        a = list(self._rotor_position)
        rot_position = a[which_rotor]
        next_letter = Rotor("abc").move_by(rot_position, 1)
        a[which_rotor] = next_letter[0]
        self._rotor_position = "".join(a)


def step_by_step(a, b, c, d, e, f, g, h, i, j, k, m):
    step_encryprion = f"""
        Plugboard: {a},
        Rotor_position: {b},
        Letter_input: {c},
        Letter_after_plugboard: {d},
        Letter_after_first_rotor: {e},
        Letter_after_second_rotor: {f},
        Letter_after_third_rotor: {g},
        Letter_after_reflector: {h},
        Letter_after_third_rotor_1: {i},
        Letter_after_second_rotor_1: {j},
        Letter_after_first_rotor_1: {k},
        Letter_after_plugboard_1: {m},
        Letter_output: {m}
    """
    return step_encryprion


def encrypt(letter_to_encrypt, rotor, rotor_s, rotor_p):
    index_of_r_s = Rotor("abc").index_of_letter(rotor_s)
    index_of_r_p = Rotor("abc").index_of_letter(rotor_p)
    #  index of rotor setting
    letter_to_encrypt1 = Rotor("abc").next_letter_in_list_by(letter_to_encrypt, index_of_r_p)
    letter_to_encrypt2, index2 = letter_to_encrypt1
    letter_to_encrypt3 = Rotor(rotor).letter_by_index(index2)
    letter_to_encrypt4 = Rotor(rotor).letter_earlier_by(letter_to_encrypt3, index_of_r_s)
    letter_to_encrypt5, index5 = letter_to_encrypt4
    letter_to_encrypt6 = Rotor("abc").next_letter_in_list_by(letter_to_encrypt5, index_of_r_s)
    letter_to_encrypt7, index7 = letter_to_encrypt6
    letter_to_encrypt8 = Rotor("abc").letter_earlier_by(letter_to_encrypt7, index_of_r_p)
    letter_to_encrypt9, index9 = letter_to_encrypt8
    #  Letter after first encryption(Całe kodowanie)
    return letter_to_encrypt9


def decrypt(letter_to_decrypt, rotor, rotor_s, rotor_p):
    index_of_r_s = Rotor("abc").index_of_letter(rotor_s)
    index_of_r_p = Rotor("abc").index_of_letter(rotor_p)
    # index of rotor settings
    how_far = index_of_r_p - index_of_r_s
    letter_to_decrypt = Rotor("abc").move_by(letter_to_decrypt, how_far)
    letter, index = letter_to_decrypt
    letter_to_decrypt = Rotor(rotor).next_letter_in_list_by(letter, index_of_r_s)
    letter, index = letter_to_decrypt
    letter = Rotor("abc").letter_by_index(index)
    letter_to_decrypt = Rotor("abc").letter_earlier_by(letter, index_of_r_p)
    return letter_to_decrypt[0]
    # ^ almost same thinking as in def encrypt() but minimalized


def find_error(look_into, letters_num):
    if look_into.isdigit() or len(look_into) != letters_num:
        raise InputError()
    else:
        return look_into.upper()
