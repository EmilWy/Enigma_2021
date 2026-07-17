Celem mojego projektu było zaprojektowanie i zaimplementowanie symulatora Enigmy.

Założenia:
	-po wybraniu ustawień enigmy(w tym przypadku najbardziej rozpowszechnionej z trzema rotorami i dwoma reflektorami)czyli, trzech rotorów, ustawień rotorów jak i ich położeń początkowych oraz reflektora z połączeniami wtyczek na „Plugboard”,
	-w czasie wybierania liter do kodowania, byłoby łatwo zobaczyć kodowanie krok po kroku i była możliwość przyrównania z innym symulatorem,
	-nie było możliwości wpisania nieodpowiednich liter czy cyfr i zostały one wybrane odgórnie(w przypadku używania GUI).

Wykorzystanie:
		Cały program pokazuje się w Gui, więc potrzebny jest serwer X, następnie wchodzimy na Gui_show.py i aktywujemy program. Wybieramy ustawienia(ewentualnie pozostawić domyślne), naciskamy przycisk “Apply” i wybieramy literkę do kodowania z listy w lewym dolnym rogu. Po wybraniu litery pojawi się kodowanie krok po kroku w okienku “step_by_step_encryption” (Letter_After_first/second/third_rotor_1 jest to powrotne kodowanie “decrypt”) oraz zakodowana literka w “encrypted_letter”. „Clear” tylko wyczyści okienka ale nie zmienia dotychczasowych ustawień.
(polecam https://www.101computing.net/enigma-machine-emulator/ tam będzie można najlepiej przyrównać wyniki, jedynie nazwy rotorów są zamienione, ale proszę wybrać ustawienia po kolei tak jak na stronie).

Wykonanie:
Pierwszym problemem jaki napotkałam było same kodowanie litery przechodzącej przez “rotory”, więc znalazłam dwa wzory, które były zachowane dla każdego rotora tylko zależne od której strony jest kodowana litera.
Pierwszym kodem było “encrypt”(znalezione na końcu kodu w Encrypt.py), który kodował literkę przez wybrany motor, druga natomiast ”decrypt” kodowała tą literkę w drugą stronę “wracając”, przez wybrany rotor.
Przykład działania funkcji dla :
-encrypt("D", "III", "B", "D")
-decrypt("S", "III", "B", "D")
 
W “Plugboard” jest możliwość wpisania więcej niż 20 literek ale funkcja “make_it_two” skraca zbiór znaków do 20 a potem łączy w pary litery obok siebie. Jeżeli literka się powtórzy w którymkolwiek nawiasie to poprzez “connect” który najpierw zwraca literki do poprzedniej formy potem je znowu łączy, więc połączenie z daną literką działa w ostatnim nawiasie gdzie się znajduje. Set_plugboard zapisuje zmiany w pliku (plugboard.json).
“Rotors.json”, to w praktyce biblioteka danych, gdzie czytamy indeksy i literki, oraz gdzie sczytujemy możliwe do wykorzystania “rotory” i “reflektory”. Wszystkie metody w klasie “Rotor” mają na celu przesuwania się między indeksami liter czy wyszukiwania liter z indeksów z wybranego rotora.
