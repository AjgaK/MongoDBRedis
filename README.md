# API z MongoDB i Redis napisane w Pythonie

## Wymagania
- MongoDB na porcie 27017
- Redis na porcie 6379
- Serwer działa na porcie 5000

## Endpointy API

### 1. Pobieranie wszystkich danych
**URL:**  
`GET http://localhost:5000/getall`

**Opis:**  
Za pierwszym razem pobiera dane z bazy danych i aktualizuje cache ze wszystkimi obiektami. Następne wywołania pobierają dane z cache (jeśli się nie zmieniły).  
Zapisane cache wygasa po 120 sekundach.

**Przykład użycia:**
```bash
curl http://localhost:5000/getall
```

---

### 2. Pobieranie obiektu za pomocą ID
**URL:**  
`GET http://localhost:5000/getbyid?_id=example_id`

**Opis:**  
Za pierwszym razem pobiera dane z bazy danych i aktualizuje cache tego obiektu. Następne wywołania pobierają dane z cache (jeśli się nie zmieniły).  
Zapisane cache wygasa po 120 sekundach.

**Przykład użycia:**
```bash
curl http://localhost:5000/getbyid?_id=example_id
```
```bash
curl http://localhost:5000/getbyid?_id=67797151faeb388d02035723
```

---

### 3. Tworzenie nowego obiektu
**URL:**  
`POST http://localhost:5000/insert`

**Opis:**  
Obiekt zostaje dodany do bazy danych i istniejące cache ze wszystkimi obiektami zostaje usunięte.  
ID zostaje wygenerowane automatycznie.

**Przykład użycia:**
```bash
curl -d "{\"name\":\"example_name\"}" -H "Content-Type: application/json" http://localhost:5000/insert
```

---

### 4. Usuwanie obiektu
**URL:**  
`DELETE http://localhost:5000/delete`

**Opis:**  
Obiekt zostaje usunięty z bazy danych oraz cache obiektu i wszystkich obiektów.

**Przykład użycia:**
```bash
curl -X DELETE -d "{\"_id\":\"example_id\"}" -H "Content-Type: application/json" http://localhost:5000/delete
```
```bash
curl -X DELETE -d "{\"_id\":\"677972273983d00d1b3e10b8\"}" -H "Content-Type: application/json" http://localhost:5000/delete
```

---

### 5. Modyfikowanie obiektu
**URL:**  
`PUT http://localhost:5000/update?_id=example_id`

**Opis:**  
Obiekt z danym ID zostaje zmodyfikowany w bazie danych oraz usunięty z cache obiektu i wszystkich obiektów.

**Przykład użycia:**
```bash
curl -X PUT -d "{\"name\":\"updated_name\"}" -H "Content-Type: application/json" http://localhost:5000/update?_id=example_id
```
```bash
curl -X PUT -d "{\"name\":\"updated_name\"}" -H "Content-Type: application/json" http://localhost:5000/update?_id=67797151faeb388d02035723
```
