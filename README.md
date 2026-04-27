# 🎬 Cinema-Booking-App

> A console-based cinema seat booking system with **SQLite-backed seat inventory**, **simulated card payments**, and **automatic PDF ticket generation**.

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)]()
[![SQLite](https://img.shields.io/badge/database-SQLite-lightgrey)]()
[![FPDF](https://img.shields.io/badge/pdf-fpdf-red)]()

---

## 📌 Overview

A small but complete OOP exercise that simulates the full booking lifecycle:

1. The user picks a seat
2. The system checks seat availability against the **`cinema.db`** SQLite database
3. The user provides card details
4. Card balance is verified against the **`banking.db`** SQLite database
5. On success, the seat is marked as taken, the card is charged, and a **PDF ticket** is generated

Only **after a successful payment** is the ticket issued — making it a small but realistic two-database transactional flow.

## 🧱 Architecture

```
┌─────────┐       ┌──────────┐       ┌──────────────┐
│  User   │──────▶│   Seat   │──────▶│  cinema.db   │
└─────────┘       │ (price,  │       │ (seat_id,    │
     │            │  taken)  │       │  price,      │
     │            └──────────┘       │  taken)      │
     │                               └──────────────┘
     ▼
┌─────────┐       ┌──────────┐       ┌──────────────┐
│  Card   │──────▶│ validate │──────▶│  banking.db  │
└─────────┘       │ (price)  │       │ (number,     │
     │            └──────────┘       │  cvc,        │
     ▼                               │  balance)    │
┌─────────┐                          └──────────────┘
│ Ticket  │  ───────► sample.pdf  (FPDF generated)
└─────────┘
```

## 🗂️ Project Structure

```
Cinema-Booking-App/
├── main.py             # OOP classes + CLI entry point
├── cinema.db           # SQLite DB — seats inventory
├── banking.db          # SQLite DB — payment cards
├── sample.pdf          # Example output ticket
├── design.txt          # Initial design notes
└── requirements.txt    # fpdf==1.7.2
```

## 🧩 Core Classes

| Class | Responsibility |
|---|---|
| `User` | Holds user details and orchestrates the `buy(seat, card)` flow |
| `Seat` | Reads price from `cinema.db`, checks `is_free()`, calls `occupy()` |
| `Card` | Validates against `banking.db`; debits balance only if sufficient funds |
| `Ticket` | Generates a styled A4 PDF ticket with random 8-char ticket ID |

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python main.py
```

### 3. Interactive prompts
```
Your full name: Denis Vreshtazi
Your seat: A1
Your Card Type: Visa
Your card number: 1234567890123456
Your card cvc: 123
The name of the card holder: Denis Vreshtazi
```

### 4. Outcome
- ✅ **Success** → `sample.pdf` is generated and the seat is marked occupied.
- ❌ **Seat taken** → "Seat is taken!"
- ❌ **Insufficient funds / invalid card** → "There was a problem with your card!"

## 🗃️ Database Schemas

**`cinema.db` → table `Seat`**

| Column | Type | Description |
|---|---|---|
| `seat_id` | TEXT | e.g. `"A1"`, `"B5"` |
| `price` | REAL | Seat ticket price |
| `taken` | INTEGER | `0` = free, `1` = occupied |

**`banking.db` → table `Card`**

| Column | Type | Description |
|---|---|---|
| `number` | TEXT | Card number |
| `cvc` | TEXT | Security code |
| `balance` | REAL | Remaining funds |

## 📄 PDF Ticket Output

Each successful booking writes a single-page A4 PDF with:
- **Title:** "Your Digital Ticket"
- **Name** (cardholder name)
- **Ticket ID** — randomly generated 8-letter string
- **Price** charged
- **Seat Number**

## 💡 Possible Extensions

- Multi-row seat layout with rendered floor map
- Real payment gateway (Stripe sandbox)
- Web frontend (Flask) using the same OOP core
- Email the PDF instead of saving it locally

## 👤 Author

**Denis Vreshtazi** — [GitHub](https://github.com/denisvreshtazi)
