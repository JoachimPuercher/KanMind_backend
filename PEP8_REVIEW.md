# PEP 8 Review — Checkliste

> Stand: manueller Review (kein Linter). **Zeilennummern sind eine Momentaufnahme** —
> sobald du editierst, verschieben sie sich. Zur Live-Kontrolle: `pip install flake8`
> und `flake8 . --exclude venv,migrations`.
>
> Tipp: pro Datei **von unten nach oben** fixen, dann bleiben die oberen Nummern gültig.

---

## boards_app/api/views.py
- [ ] `:5` — E501 Import-Zeile > 79 Zeichen → umbrechen (Klammern erlauben Mehrzeiligkeit)
- [ ] `:13` — W291 Trailing Whitespace
- [ ] `:29` — E211 `Response (` → `Response(`
- [ ] `:34,35,38,40,50,59` — E111 Einrückung kein Vielfaches von 4 (patch/delete-Bodies)
- [ ] `:39` — W291 Trailing Whitespace
- [ ] `:47` — E211 `Response (` → `Response(`
- [ ] `:56` — Namenskonvention: `updatedBoard` → `updated_board` (snake_case)
- [ ] `:57` — E211 `Response (` → `Response(`
- [ ] `:64` — W292 fehlender Newline am Dateiende

## boards_app/api/serializers.py
- [ ] `:16` — E501 `fields = [...]`-Liste > 79 Zeichen → mehrzeilig
- [ ] `:23,29` — W293 Leerzeile enthält Whitespace
- [ ] `:54` — E111 Einrückung kein Vielfaches von 4 (7 Spaces vor `class Meta`)

## boards_app/api/permissions.py
- [ ] `:5,9` — E501 `has_object_permission(...obj: Board)` > 79 Zeichen
- [ ] `:7` — E302 2 Leerzeilen vor Klassendefinition fehlen
- [ ] `:10` — W291 Trailing Whitespace

## boards_app/models.py
- [ ] `:3` — E271 `from django. utils` → Leerzeichen nach `django.` entfernen

---

## tasks_app/api/views.py
- [ ] `:3` — E401 Mehrere Imports in einer Zeile (`status, generics, mixins`)
- [ ] `:8` — E501 Permission-Import-Zeile > 79 Zeichen → umbrechen
- [ ] `:11,13` — W291 Trailing Whitespace (auskommentierte Zeilen)
- [ ] `:15-17` — E303 zu viele Leerzeilen (max. 2)
- [ ] `:50,56` — W291 Trailing Whitespace
- [ ] `:79` — W292 fehlender Newline am Dateiende

## tasks_app/api/serializers.py
- [ ] `:8` — W291 Trailing Whitespace
- [ ] `:21,24,40,43,56` — E501 Feld-/Signatur-Zeilen > 79 Zeichen
- [ ] `:30` — E501 `fields = [...]`-Liste > 79 Zeichen (130!)
- [ ] `:58` — E302 2 Leerzeilen vor Klassendefinition fehlen
- [ ] `:63` — W291 Trailing Whitespace

## tasks_app/api/permission.py
- [ ] `:36,42,48,60,76` — W291 Trailing Whitespace
- [ ] `:80` — W292 fehlender Newline am Dateiende

## tasks_app/models.py
- [ ] `:16,28` — E302 2 Leerzeilen vor Klassendefinition fehlen
- [ ] `:31` — E501 ForeignKey-Zeile > 79 Zeichen

---

## user_auth_app/api/views.py
- [ ] `:8` — F401 doppelter Import `from ..models import User` (schon aus `django.contrib.auth.models`)
- [ ] `:19-22,41-44,58,63,66-68` — E203 Leerzeichen vor `:` im Dict (`'token' :` → `'token':`)
- [ ] `:28,50` — E225 fehlende Spaces um `=` (sofern nicht Keyword-Argument)
- [ ] `:31,53` — W391 überzählige Leerzeilen am Dateiende
- [ ] `:70` — E211 `Response (` → `Response(`

## user_auth_app/api/serializers.py
- [ ] `:13,14` — E203 Leerzeichen vor `:` im Dict
- [ ] `:20` — E111 Einrückung kein Vielfaches von 4
- [ ] `:38,62` — E712 `== True` → `if value:`
- [ ] `:56` — Debug-`print()` entfernen oder durch `logging` ersetzen
- [ ] `:73` — W292 fehlender Newline am Dateiende

## user_auth_app/models.py
- [ ] `:3` — E271 `from django. utils` → Leerzeichen entfernen

---

## core/settings.py
- [ ] `:125,128` — E203 Leerzeichen vor `:` (`'DEFAULT_..._CLASSES' :` → `...':`)

---

## Reihenfolge-Empfehlung
1. **Mechanisch & risikolos zuerst:** Trailing Whitespace (W291/W293), EOF-Newline (W292/W391), `Response (` (E211), Dict-`:` (E203).
2. **Dann Struktur:** Einrückung (E111), Zeilenlänge (E501), Leerzeilen (E302/E303).
3. **Zuletzt bewusst — die Logik-Smells:** `== True` (E712), `updatedBoard` (Naming), doppelter/kaputter Import (F401/E271), `print()`.

## Künftig automatisch vermeiden (VS Code settings.json)
```json
"files.trimTrailingWhitespace": true,
"files.insertFinalNewline": true,
"editor.renderWhitespace": "all"
```
Damit entstehen W291/W293/W292 gar nicht erst.
