import random
import sqlite3
import string

from fpdf import FPDF


class User:

    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        """Buys the ticket if the card is valid"""
        if seat.is_free():
            if card.validate(price=seat.get_price()):
                seat.occupy()
                ticket = Ticket(user=self, price=seat.get_price(), seat_number=seat.seat_id)
                ticket.to_pdf()
                return "Purchase successful!"
            else:
                return "There was a problem with your card!"
        else:
            return "Seat is taken!"


class Seat:
    database = "cinema.db"

    def __init__(self, seat_id):
        self.seat_id = seat_id

    def get_price(self):
        """Gets the price of theSeat from db"""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "price" FROM "Seat" WHERE "seat_id"==? """,
                       [self.seat_id])
        return cursor.fetchall()[0][0]

    def is_free(self):
        """Check from db if a seat is free or taken"""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT "taken" FROM "Seat" WHERE "seat_id"=? """,
                       [self.seat_id])
        result = cursor.fetchall()[0][0]

        if result == 0:
            return True
        else:
            return False

    def occupy(self):
        """Change the taken seat to 1 and occupy it"""
        if self.is_free():
            connection = sqlite3.connect(self.database)
            connection.execute("""
                    UPDATE "Seat" SET "taken"=? WHERE "seat_id"=? """,
                               [1, self.seat_id])
            connection.commit()
            connection.close()


class Card:
    database = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.type = type
        self.number = number
        self.cvc = cvc
        self.holder = holder

    def validate(self, price):
        """Check if the card has sufficient credit"""
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(""" SELECT "balance" FROM "Card" WHERE "number"=? and cvc=? """,
                       [self.number, self.cvc])
        result = cursor.fetchall()

        if result:
            balance = result[0][0]
            if balance >= price:
                connection.execute("""
                UPDATE "Card" SET "balance"=? where "number"=? and "cvc"=? """,
                                   [balance-price, self.number, self.cvc])
                connection.commit()
                connection.close()
                return True
            else:
                return False
        else:
            return False



class Ticket:

    def __init__(self, user, price, seat_number):
        self.user = user
        self.price = price
        self.seat_number = seat_number
        self.id = "".join([random.choice(string.ascii_letters) for i in range(8)])

    def to_pdf(self):
        """Creates a pdf ticket"""
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        pdf.set_font(family='Times', style='B', size=24)
        pdf.cell(w=0, h=80, txt='Your Digital Ticket', border=1, ln=1, align='C')

        pdf.set_font(family='Times', style='B', size=14)
        pdf.cell(w=100, h=25, txt='Name: ', border=1)
        pdf.set_font(family='Times', style="", size=12)
        pdf.cell(w=0, h=25, txt=self.user.name, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family='Times', style='B', size=14)
        pdf.cell(w=100, h=25, txt='Ticket ID: ', border=1)
        pdf.set_font(family='Times', style="", size=12)
        pdf.cell(w=0, h=25, txt=self.id, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family='Times', style='B', size=14)
        pdf.cell(w=100, h=25, txt='Price: ', border=1)
        pdf.set_font(family='Times', style="", size=12)
        pdf.cell(w=0, h=25, txt=str(self.price), border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family='Times', style='B', size=14)
        pdf.cell(w=100, h=25, txt='Seat Number: ', border=1)
        pdf.set_font(family='Times', style="", size=12)
        pdf.cell(w=0, h=25, txt=self.seat_number, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.output('sample.pdf', 'F')


if __name__ == "__main__":
    name = input("Your full name: ")
    seat_id = input("Your seat: ")
    card_type = input("Your Card Type: ")
    card_number = input("Your card number: ")
    card_cvc = input("Your card cvc: ")
    card_holder = input("The name of the card holder: ")

    user = User(name=name)
    seat = Seat(seat_id=seat_id)
    card = Card(type=card_type, number=card_number, cvc=card_cvc, holder=card_holder)

    print(user.buy(seat=seat, card=card))
