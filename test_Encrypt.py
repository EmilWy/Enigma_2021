from Encrypt import get_, Rotor, Settings, to_not_be_bigger_than_25, to_not_be_negative, encrypt, decrypt, Reflector, Plugboard, NotFound, InputError
import pytest


def test_get_rotor_by_number():
    third_rotor = Rotor("III")
    assert third_rotor.rotor_list() == [
            "B", "D", "F", "H", "J", "L",
            "C", "P", "R", "T", "X", "V",
            "Z", "N", "Y", "E", "I", "W",
            "G", "A", "K", "M", "U", "S",
            "Q", "O"
        ]


def test_get_letter_by_index():
    letter_in_third_rotor = Rotor("III")
    assert letter_in_third_rotor.letter_by_index(19) == "A"
    assert letter_in_third_rotor.letter_by_index(0) == "B"


def test_get_index_by_letter():
    index_in_third_rotor = Rotor("III")
    assert index_in_third_rotor.index_of_letter("C") == 6
    assert index_in_third_rotor.index_of_letter("B") == 0
    assert index_in_third_rotor.next_letter_in_list_by("A", 1) == ("K", 20)
    assert index_in_third_rotor.letter_earlier_by("D", 4) == ("S", 23)
    assert index_in_third_rotor.letter_earlier_by("D", 1) == ("B", 0)


def test_encrypt_using_third_rotator():
    assert encrypt("A", "III", "A", "A") == "B"
    assert encrypt("J", "III", "A", "B") == "W"


def test_rest():
    assert to_not_be_bigger_than_25(27) == 1
    assert to_not_be_bigger_than_25(16) == 16


def test_negative_rest():
    assert to_not_be_negative(-3) == 23
    assert to_not_be_negative(-1) == 25


def test_letter_to_encrypt():
    set_settings = Settings([], 'B', 'I', 'II', 'III', 'AAA', 'AAZ')
    assert set_settings.multi_encryption("A")[0] == "U"
    assert set_settings._rotor_position == "AAA"
    assert set_settings.multi_encryption("U")[0] == "Z"


def test_decrypt():
    assert decrypt("O", "III", "A", "A") == "Z"


def test_move_by():
    index_in_third_rotor = Rotor("III")
    assert index_in_third_rotor.move_by("A", 3) == ("U", 22)
    assert index_in_third_rotor.move_by("B", -3) == ("S", 23)


def test_reflector():
    reflector = Reflector("B")
    assert reflector.replace_with_reflector("A") == "Y"


def test_plugboard_connect_and_clear():
    Plugboard()._board == {
            'A': 'B', 'B': 'A', 'C': 'C',
            'D': 'D', 'E': 'E', 'F': 'F',
            'G': 'G', 'H': 'H', 'I': 'I',
            'J': 'J', 'K': 'K', 'L': 'L',
            'M': 'M', 'N': 'N', 'O': 'O',
            'P': 'P', 'R': 'R', 'S': 'S',
            'T': 'T', 'U': 'U', 'V': 'V',
            'W': 'W', 'X': 'X', 'Y': 'Y',
            'Z': 'Z'
            }
    set_settings = Settings([], 'B', 'I', 'II', 'III', 'AAA', 'AAA')
    assert set_settings.multi_encryption("A")[0] == "B"
    assert set_settings.multi_encryption("E")[0] == "L"
    Plugboard().clear()
    assert Plugboard()._board["A"] == "A"
    assert Plugboard()._board["B"] == "B"


def test_plugboard_2():
    plugboard = Plugboard()
    assert plugboard.make_it_two("ABCDEF") == [("A", "B"), ("C", "D"), ("E","F")]


def test_plugboard_3():
    plugboard = Plugboard()
    assert plugboard.make_it_two("ABCDE") == [("A", "B"), ("C", "D")]


def test_plugboard_uppercase():
    plugboard = Plugboard()
    assert plugboard.make_it_two("AbCDE") == [("A", "B"), ("C", "D")]


def test_plugboard_connect_same_letters():
    Plugboard().connect("A", "B")
    Plugboard().connect("B", "C")
    assert Plugboard()._board["B"] == "C"
    assert Plugboard()._board["A"] == "A"
    assert Plugboard()._board["C"] == "B"


def test_plugboard_conecct_text():
    Plugboard().set_plugboard("ABCDEFFG")
    assert Plugboard()._board['A'] == "B"
    assert Plugboard()._board["G"] == "F"


def test_raise_error():
    with pytest.raises(NotFound):
        assert get_("Filmy")


def test_plugboard_number():
    plugboard = Plugboard()
    with pytest.raises(ValueError):
        assert plugboard.make_it_two("A3CDE")


def test_problem_with_settings():
    with pytest.raises(InputError):
        Settings([], '1', 'I', 'II', 'III', 'AAA', 'AAA')
    with pytest.raises(InputError):
        Settings([], 'B', 'I', 'II', 'III', 'AA', 'AAA')
