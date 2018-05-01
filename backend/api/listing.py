from sqlalchemy import Table, Column, Integer, ForeignKey, desc, asc
from sqlalchemy.orm import relationship
from flask_restful import Resource, reqparse
from math import ceil  # for ceil used for paging
from book import BookModel  # for error handling, cannot add listing if book not in db
from user import UserModel  # for error handling, cannot add listing if user not in db
import datetime

from db import db

page_size = 2


class ListingModel(db.Model):
    """The ListingModel object stores information about the listing, as well as
    the book and user objects associated with it.

    Attributes:
        listing_id (int): An id to represent the listing, generated by the table.
        price (float): The price of the listing.
        condition (string): The condition of the listing.
        isbn (int): The isbn of the listing.
        book (BookModel): The book being represented by the listing.
        google_tok (string): The google token of the user who made the posting.
        user (UserModel): The user who made the posting.
        status (string): The status of the listing.
        timestamp (int): The time the listing was posted.
    """
    __tablename__ = 'listings'  # our listings database

    # listing id's are assigned by integer key, not used by constructor
    listing_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float(precision=2))
    condition = db.Column(db.String(15))
    isbn = db.Column(db.Integer, db.ForeignKey('books.isbn'))
    book = db.relationship('BookModel')
    google_tok = db.Column(db.String, db.ForeignKey('users.google_tok'))
    user = db.relationship('UserModel')
    status = db.Column(db.String(15))
    timestamp = db.Column(db.Integer)

    def __init__(self, price, condition, isbn, google_tok, status):
        self.price = price
        self.condition = condition
        self.isbn = isbn
        self.google_tok = google_tok
        self.status = status
        self.timestamp = datetime.datetime.now()

    # Both json functions below used to also include 'isbn': self.isbn

    def listing_json_w_user(self):
        """Returns the listing jsonified, with a reference to the user who posted.

        Args:
            none.

        Returns:
            json: A jsonified listing.
        """
        try:
            return {"listing_id": self.listing_id, 'price': self.price, 'condition': self.condition, 'status': self.status, 'user': self.user.user_json_wo_listings(), 'timestamp': self.timestamp}
        except:
            return {"Message": "User does not exist in DB"}

    def listing_json_w_book(self):
        """Returns the listing jsonified, with a reference to the book being
        represented.

        Args:
            none.

        Returns:
            json: A jsonified listing.
        """
        try:
            return {"listing_id": self.listing_id, 'price': self.price, 'condition': self.condition, 'status': self.status, 'book': self.book.book_json_wo_listings(), 'timestamp': self.timestamp}
        except:
            return {"Message": "Book does not exist in DB"}

    def listing_json_w_book_and_user(self):
        """Returns the listing jsonified, with a reference to the book being
        represented and the user who posted it.

        Args:
            none.

        Returns:
            json: A jsonified listing.
        """
        try:
            return {"listing_id": self.listing_id, 'price': self.price, 'condition': self.condition, 'status': self.status, 'book': self.book.book_json_wo_listings(), 'user': self.user.user_json_wo_listings(), 'timestamp': self.timestamp}
        except:
            return {"Message": "Object does not exist in DB"}

    def bare_json(self):
        """Returns a json object representing the listing.

        Args:
            none.

        Returns:
            json: A jsonified listing.
        """
        return {'price': self.price, 'condition': self.condition, 'status': self.status, "listing_id": self.listing_id, 'timestamp': self.timestamp, 'bookTitle': self.book.title}

    def bu_bare_json(self):  # Book to user bare jason
        """Returns a json object representing the listing. Used when
        going from books to users.

        Args:
            none.

        Returns:
            json: A jsonified listing.
        """
        return {'price': self.price, 'condition': self.condition, 'status': self.status, "listing_id": self.listing_id, "google_tok": self.google_tok, 'timestamp': self.timestamp, 'bookTitle': self.book.title}
<<<<<<< HEAD
    # def get_user(self):
    #    user = []
    #    user.append(user.find_by_google_tok(self.google_tok))
    #    return user
=======
>>>>>>> 9a1b5cddab303fa85c0c281b5542019eeb9d16ac

    @classmethod
    def find_by_isbn(cls, isbn):  # abstracted and redifined from get
        """Finds all listings matching an isbn.

        Args:
            isbn (int): The isbn to search with.

        Returns:
            ListingModel[]: A list of listings.
        """
        listings = ListingModel.query.filter_by(
            name=isbn).all()  # returns all listings of isbn as a list
        if len(listings) > 0:
            return listings
        return None

    @classmethod
    def find_by_listing_id(cls, listing_id):
        """Finds all listings matching a listing id.

        Args:
            listing_id (int): The listing id to search for.

        Returns:
            ListingModel[]: A list of listings.
        """
        listing = ListingModel.query.filter_by(listing_id=listing_id).first()
        if listing:
            return listing
        return None

    def save_to_db(self):
        """Saves the listing to the database.

        Args:
            none.

        Returns:
            none.
        """
        # write to database
        # abstracted just like find_by_name so that it can be used by both post and put
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """deletes the listing to the database.

        Args:
            none.

        Returns:
            none.
        """
        db.session.delete(self)
        db.session.commit()


class Listing(Resource):
    """The Listing object handles API requests such as Get/Post/Delete/Put.

    Attributes:
        none.
    """
    parser = reqparse.RequestParser()  # Item class parser
    parser.add_argument("listing_id",  # requests must be in format { "price": float}
                        type=int,
                        required=False,
                        help="FORMAT ERROR: This request must have be string : integer "
                        )
    parser.add_argument("price",  # requests must be in format { "price": float}
                        type=float,
                        required=True,
                        help="FORMAT ERROR: This request must have be string : float where string == price "
                        )
    parser.add_argument("condition",
                        type=str,
                        required=True,
                        help="FORMAT ERROR: This request must have be string : string "
                        )
    parser.add_argument("isbn",
                        type=int,
                        required=False,
                        help="FORMAT ERROR: This request must have be string : integer where string == price "
                        )
    parser.add_argument("google_tok",
                        type=str,
                        required=True,
                        help="FORMAT ERROR: This request must have be string : integer where string == price "
                        )
    parser.add_argument("status",
                        type=str,
                        required=True,
                        help="FORMAT ERROR: This request must have be string : string where string == price "
                        )

    def get(self, ids):  # get request, looking for all listing objects from listing ID's, user -> books
        """Get request, looking for all listings matching an id in ids.

        Args:
            ids (str[]): A list of ids to query with.

        Returns:
            json[]: A list of jsonified listings.
        """

        ids = ids.split(",")
        for id_ in range(0, len(ids)):
            ids[id_] = int(ids[id_])
        all_listings = ListingModel.query.filter(
            ListingModel.listing_id.in_(ids)).all()
        isbns = []
        for l in all_listings:
            if l.isbn not in isbns:  # avoid duplicates
                isbns.append(l.isbn)
<<<<<<< HEAD
        # PAGING
        #of = ceil(len(all_listings)/page_size)
        print(listing.bare_json() for listing in all_listings)
=======
>>>>>>> 9a1b5cddab303fa85c0c281b5542019eeb9d16ac
        return {"listings": [listing.bare_json() for listing in all_listings], "isbns": isbns}

    def post(self, ids):
        """Posts a listing to the database.

        Args:
            ids (str): The listing id of the listing being posted.

        Returns:
            message: What happened with the post call.
        """

        # what the user will send to the post request (in good format)
        data = Listing.parser.parse_args()
        # In our case, the user sends the price as JSON, but the item name gets passed into the function
        # if user doesn't exist
        if not UserModel.find_by_google_tok(data['google_tok']):
            return {"message": "invalid google token, user does not exist in database"}
        if not BookModel.find_by_isbn(ids):  # if book doesn't exist
            return {"message": "invalid isbn, book model does not exist in database"}

        isbn = int(ids)

        item = ListingModel(data["price"], data["condition"],
                            isbn, data["google_tok"], data["status"])

        try:
            item.save_to_db()
        except:
            # internal server error
            return{"message": "An error occurred while inserting"}, 500

        return {"message": "post was successful"}, 201  # post was successful

    def delete(self, ids):
        """Deletes a listing from the database.

        Args:
            ids (str): The id of the listing being deleted.

        Returns:
            message: What happened with the delete call.
        """

        id_ = int(ids)
        item = ListingModel.find_by_listing_id(ids)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}
        return {"message": "Listing with ID " + str(id_) + " does not exist"}

    # aka "mostly just use to change status"
    def put(self, listing_id, price, condition, isbn, google_tok, status):
        """Either posts listing to database, or updates it.

        Args:
            listing_id (int): An id to represent the listing, generated by the table.
            price (float): The price of the listing.
            condition (str): The condition of the listing.
            isbn (int): The isbn of the listing.
            google_tok (str): The google token of the user who made the posting.
            status (str): The status of the listing.

        Returns:
            json: A jsonified listing object representing what was put.
        """

        data = Listing.parser.parse_args()  # only add valid JSON requests into data

        if(listing_id):
            item = ListingModel.find_by_listing_id(listing_id)  # find item
            if item:
                item.condition = condition  # returns one element or None,
            else:
                return {"message": "listing not found"}

        else:  # no listing found, add listing (probably unnecessary)
            item = ListingModel(data['price'], data["condition"],
                                data["isbn"], data["google_tok"], data["status"])

        item.save_to_db()

        return item.listing_json_w_book()


class allListings(Resource):
    """The allListings object handles the entire list of listings in the database.

    Attributes:
        none.
    """

    def get(self, search):
        """Gets a list of all listings in database that match a search.

        Args:
            search (str[]): A list of search terms defining what to search with.

        Returns:
            json[]: A list of jsonified listings that match the search result.
        """

        # used to go from books to users, also called on the home page to display most recent listings
        if search == "home":  # right now, it just returns the most recent listings, not most recent 20 books
            listings = ListingModel.query.order_by(
                ListingModel.timestamp.desc())
        else:
            strings = search.split("+")
            listing_ids = strings[0].split(",")
            for i in range(0, len(listing_ids)):
                listing_ids[i] = int(listing_ids[i])
            if len(strings) > 1:
                if strings[1] == "condition":  # sort by price
                    listings = ListingModel.query.filter(ListingModel.listing_id.in_(
                        listing_ids)).order_by(ListingModel.condition.desc())
                elif strings[1] == "price":  # sort by condition
                    listings = ListingModel.query.filter(
                        ListingModel.listing_id.in_(listing_ids)).order_by(ListingModel.price)
                else:  # no filters provided
                    listings = ListingModel.query.filter(
                        ListingModel.listing_id.in_(listing_ids))
            else:
                return{"message": "format error, '/listings/listing_id1,listing_id2+price xor condition', or '/listing/listing_id1,listing_id2+'"}
        tokens = []
        for listing in listings:
            if listing.google_tok not in tokens:
                tokens.append(listing.google_tok)
        if search == "home":
            isbns = []
            for listing in listings:
                if listing.isbn not in isbns:
                    isbns.append(listing.isbn)
            (print(listing.bare_json()) for listing in listings)
            return{"listings": [listing.bare_json() for listing in listings], "google_tokens": tokens, "isbns": isbns}
        (print(listing.bare_json()) for listing in listings)
        return {"listings": [listing.bu_bare_json() for listing in listings], "google_tokens": tokens}
