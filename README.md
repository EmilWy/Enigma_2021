# Enigma Simulator

## Opis projektu

Celem projektu było zaprojektowanie i zaimplementowanie symulatora maszyny szyfrującej **Enigma**, umożliwiającego szyfrowanie i deszyfrowanie wiadomości z możliwością obserwowania całego procesu krok po kroku.

Program został wyposażony w interfejs graficzny (GUI), który pozwala na konfigurację poszczególnych elementów maszyny oraz śledzenie zmian zachodzących podczas kodowania wybranych liter.

Symulator odwzorowuje działanie Enigmy wykorzystującej trzy rotory, jeden z dostępnych reflektorów oraz tablicę wtyczkową (*Plugboard*).

## Funkcjonalności

Program umożliwia:

- Wybór trzech rotorów oraz konfigurację ich ustawień.
- Określenie początkowych pozycji rotorów.
- Wybór reflektora.
- Konfigurację połączeń liter na tablicy wtyczkowej (*Plugboard*).
- Szyfrowanie pojedynczych liter.
- Wyświetlanie procesu szyfrowania krok po kroku.
- Podgląd wyników działania poszczególnych rotorów podczas szyfrowania i deszyfrowania.
- Czyszczenie okienek wynikowych bez konieczności ponownego konfigurowania maszyny.

Dodatkowo interfejs ogranicza możliwość wprowadzania nieprawidłowych znaków, udostępniając użytkownikowi wyłącznie dozwolone opcje wyboru.

## Uruchomienie programu

Program wykorzystuje interfejs graficzny GUI, dlatego do jego uruchomienia wymagany jest serwer X.

Aby uruchomić symulator:

1. Otwórz plik `Gui_show.py`.
2. Uruchom program.
3. Wybierz ustawienia Enigmy lub pozostaw wartości domyślne.
4. Zatwierdź konfigurację przyciskiem **Apply**.
5. Wybierz literę przeznaczoną do zaszyfrowania z listy znajdującej się w lewym dolnym rogu okna.
6. Odczytaj wynik szyfrowania oraz kolejne etapy przetwarzania litery.

### Elementy interfejsu

- **Apply** – zatwierdza wybraną konfigurację maszyny.
- **Clear** – czyści pola wyświetlające wyniki, nie zmieniając aktualnych ustawień Enigmy.
- **step_by_step_encryption** – wyświetla kolejne etapy szyfrowania i deszyfrowania.
- **encrypted_letter** – prezentuje końcową, zaszyfrowaną literę.

W polach `Letter_After_first_rotor_1`, `Letter_After_second_rotor_1` oraz `Letter_After_third_rotor_1` prezentowane są również etapy powrotnej drogi sygnału przez rotory, odpowiadające procesowi deszyfrowania.

## Implementacja

### 1. Szyfrowanie i deszyfrowanie przez rotory

Jednym z pierwszych i najważniejszych problemów podczas implementacji było prawidłowe odwzorowanie przepływu sygnału przez rotory Enigmy.

W tym celu zaimplementowane zostały dwie funkcje:

- `encrypt()` – odpowiada za przetwarzanie litery podczas przechodzenia sygnału przez rotor w kierunku szyfrowania.
- `decrypt()` – odpowiada za przetwarzanie litery podczas powrotnej drogi sygnału przez rotor.

Obie funkcje wykorzystują odpowiednie przesunięcia indeksów liter w alfabecie, zależne od aktualnego ustawienia rotora i jego początkowej pozycji.

Przykładowe wywołania:

```python
encrypt("D", "III", "B", "D")
decrypt("S", "III", "B", "D")
```

Parametry określają kolejno:
- literę wejściową,
- wybrany rotor,
- ustawienie pierścienia,
- początkową pozycję rotora.

W przypadku funkcji `encrypt()` operacje wykonywane są w następującej kolejności:

1. Odczytanie indeksu litery wejściowej w alfabecie.
2. Przesunięcie indeksu zgodnie z aktualną pozycją rotora.
3. Odczytanie litery znajdującej się pod wyznaczonym indeksem w konfiguracji wybranego rotora.
4. Uwzględnienie przesunięcia wynikającego z ustawienia pierścienia.
5. Odnalezienie odpowiadającej litery w alfabecie i cofnięcie wcześniejszych przesunięć.

Funkcja `decrypt()` realizuje analogiczny proces, jednak wyszukiwanie liter odbywa się w odwrotnym kierunku – zgodnie z drogą powrotną sygnału przez rotor.

### 2. Proces szyfrowania krok po kroku

Funkcja `multi_encryption()` łączy działanie wszystkich mniejszych funkcji odpowiedzialnych za poszczególne etapy szyfrowania.

Jej zadaniem jest przeprowadzenie litery przez całą maszynę Enigma, uwzględniając:
- tablicę wtyczkową,
- kolejne rotory,
- reflektor,
- powrotną drogę sygnału przez rotory,
- ponowną zamianę na tablicy wtyczkowej.

Funkcja zwraca końcową zaszyfrowaną literę oraz dane wykorzystywane do wyświetlenia procesu szyfrowania w oknie `step_by_step_encryption`.

Dzięki temu użytkownik może prześledzić, jak zmienia się litera na każdym etapie działania maszyny.

### 3. Tablica wtyczkowa (Plugboard)

Tablica wtyczkowa umożliwia zamianę liter w parach przed rozpoczęciem właściwego procesu szyfrowania oraz po jego zakończeniu.

W projekcie zaimplementowano funkcję `make_it_two()`, której zadaniem jest przygotowanie połączeń w postaci par liter.

Nawet jeśli użytkownik wprowadzi większą liczbę znaków, funkcja ogranicza zbiór do maksymalnie 20 liter, a następnie łączy sąsiadujące znaki w pary.

W przypadku powtórzenia tej samej litery w różnych parach wykorzystywana jest funkcja `connect()`. Najpierw przywraca ona wcześniejsze połączenie, a następnie tworzy nowe. Dzięki temu ostatnie wystąpienie danej litery określa jej aktualne połączenie.

Funkcja `set_plugboard()` zapisuje skonfigurowane połączenia w pliku `plugboard.json`, dzięki czemu ustawienia mogą być odczytywane przez program.

### 4. Pliki JSON

W projekcie wykorzystano pliki JSON do przechowywania danych i konfiguracji maszyny:

- **`rotors.json`** – pełni funkcję biblioteki danych zawierającej informacje o dostępnych rotorach, reflektorach, literach oraz odpowiadających im indeksach.
- **`plugboard.json`** – przechowuje aktualną konfigurację połączeń liter na tablicy wtyczkowej.

### 5. Klasa Rotor

Klasa `Rotor` zawiera metody odpowiedzialne za operacje na indeksach i literach wykorzystywanych podczas szyfrowania.

Jej zadaniem jest m.in.:
- przesuwanie się pomiędzy indeksami liter,
- wyszukiwanie liter na podstawie indeksów,
- odczytywanie odpowiednich wartości z wybranego rotora,
- obsługa operacji niezbędnych do prawidłowego przepływu sygnału.

Dzięki wydzieleniu tych operacji do osobnej klasy kod jest bardziej uporządkowany, a logika działania poszczególnych rotorów może być wykorzystywana w różnych etapach szyfrowania.

## Weryfikacja poprawności działania

Poprawność działania symulatora można sprawdzić poprzez porównanie uzyskanych wyników z inną implementacją maszyny Enigma:

[Enigma Machine Emulator – 101 Computing](https://www.101computing.net/enigma-machine-emulator/)

Podczas porównywania wyników należy pamiętać, że nazewnictwo rotorów w obu symulatorach jest zamienione. Aby uzyskać zgodne wyniki, należy odpowiednio dopasować kolejność i ustawienia rotorów, reflektor oraz połączenia na tablicy wtyczkowej.

## Podsumowanie

Projekt pozwolił na praktyczne poznanie mechanizmu działania maszyny szyfrującej Enigma oraz implementację jej najważniejszych elementów. Szczególny nacisk został położony na odwzorowanie przepływu sygnału przez rotory i reflektor, obsługę tablicy wtyczkowej oraz możliwość obserwowania procesu szyfrowania na każdym etapie.

Zastosowanie interfejsu graficznego umożliwia nie tylko korzystanie z symulatora, ale również lepsze zrozumienie zasad działania historycznej maszyny Enigma.
