# Rozwiązanie Konkursowe - Łamacz Szyfru Cezara

Aplikacja stworzona na potrzeby konkursu "Adepci IT". Program automatycznie deszyfruje wiadomości zakodowane szyfrem Cezara, identyfikując poprawne przesunięcie na podstawie analizy języka polskiego.

## Funkcjonalności

- **Automatyczne łamanie szyfru**: Sprawdza wszystkie 26 możliwych przesunięć.
- **Dwuetapowa detekcja języka**: Łączy bibliotekę `langdetect` z autorskim systemem punktacji opartym o polskie słowa kluczowe, co zapewnia wysoką skuteczność nawet przy krótkich tekstach.
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
2. **Detekcja języka**: Każdy kandydat jest analizowany przez bibliotekę `langdetect` w celu identyfikacji języka polskiego.
3. **Scoring**: Kandydaci zidentyfikowani jako polski są dodatkowo punktowani na podstawie występowania typowych polskich słów (spójniki, przyimki, zaimki).
4. **Fallback**: Jeśli `langdetect` nie wykryje polskiego tekstu, program wybiera kandydata z najwyższym wynikiem scoringu - zapewnia to działanie nawet dla bardzo krótkich tekstów.

## Dlaczego langdetect?

Wybrano bibliotekę `langdetect` ze względu na:
- **Prostotę** - nie wymaga zewnętrznych API ani kluczy
- **Sprawdzone działanie** - port Google's language-detection
- **Wystarczającą dokładność** - w połączeniu z autorskim systemem scoringu radzi sobie nawet z trudnymi przypadkami

## Przykładowy output

```
Odszyfrowana wiadomość: Wyslij email na adres rekrutacja@adepci.pl aby dostac staz...
Ilość przesunięć: 7
Email: rekrutacja@adepci.pl
```

Wynik zapisywany jest również do pliku `solution.txt`.
