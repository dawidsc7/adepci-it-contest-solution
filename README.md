# Rozwiązanie Konkursowe - Łamacz Szyfru Cezara

Aplikacja stworzona na potrzeby konkursu "Adepci IT". Program automatycznie deszyfruje wiadomości zakodowane szyfrem Cezara, identyfikując poprawne przesunięcie na podstawie analizy języka polskiego.

## Funkcjonalności

- **Automatyczne łamanie szyfru**: Sprawdza wszystkie 26 możliwych przesunięć.
- **Inteligentna detekcja języka**: Wykorzystuje bibliotekę `lingua-py` do automatycznego rozpoznawania języka polskiego z wysoką dokładnością, nawet przy krótkich tekstach.
- **Obsługa plików i tekstu**: Możliwość podania ścieżki do pliku lub tekstu bezpośrednio w argumencie.
- **Raportowanie**: Zapisuje zdekodowaną wiadomość oraz pełną analizę do plików wynikowych.

## Wymagania

- Python 3.8+
- Biblioteki zewnętrzne (zainstaluj przez `pip`)

## Instalacja

1. Sklonuj repozytorium lub pobierz pliki.
2. Zainstaluj wymagane zależności:
   ```bash
   pip install -r requirements.txt
   ```

## Użycie

Uruchom program podając ścieżkę do pliku z zaszyfrowanym tekstem:

```bash
python main.py ciphertext.txt
```

Możesz też podać tekst bezpośrednio:

```bash
python main.py "Treść do odszyfrowania..."
```

Po uruchomieniu program:
1. Wyświetli najlepsze dopasowanie w konsoli.
2. Zapisze wyniki w pliku `solution.txt`.

## Testy

Projekt posiada zestaw testów jednostkowych. Aby je uruchomić, wpisz:

```bash
python -m pytest tests/
```

## Jak to działa

Program wykorzystuje podejście brute-force z inteligentną detekcją języka:

1. **Generowanie kandydatów**: Dla każdego z 26 możliwych przesunięć (0-25) generowany jest odszyfrowany tekst.
2. **Detekcja języka**: Każdy kandydat jest analizowany przez bibliotekę `lingua-py`, która oblicza pewność (confidence score 0.0-1.0) że tekst jest w języku polskim.
3. **Wybór najlepszego**: Kandydat z najwyższym confidence score jest wybierany jako rozwiązanie.
4. **Fallback**: Dla bardzo krótkich tekstów, gdy detekcja języka nie jest możliwa, zwracany jest tekst oryginalny.

## Dlaczego lingua-py?

Wybrano bibliotekę `lingua-py` ze względu na:
- **Wysoką dokładność** - szczególnie dla krótkich tekstów
- **Deterministyczne wyniki** - ten sam tekst zawsze daje ten sam wynik
- **Confidence score** - pozwala porównać pewność detekcji między kandydatami
- **Brak zewnętrznych plików** - modele wbudowane w bibliotekę

## Przykładowy output

```
Odszyfrowana wiadomość: Wyslij email na adres rekrutacja@adepci.pl aby dostac staz...
Ilość przesunięć: 7
Email: rekrutacja@adepci.pl
```

Wynik zapisywany jest również do pliku `solution.txt`.
