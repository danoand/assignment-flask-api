# Import ORM and database migrations packages/modules
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 

# Create a SQLAlchemy object
db = SQLAlchemy()
# Create a migration object
migrate = Migrate()

# Define a Tweet class which "extends" the Model class
class Tweet(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    tweet   = db.Column(db.String(280))
    handle  = db.Column(db.String(128))
    name    = db.Column(db.String(256))

# parse_rows parses db rows into json documents
def parse_rows(db_rows):
    """
    parse_rows parses db rows into json documents
    """

    # Define a return set (list)
    parsed_rows = []

    # Iterate through the passed db rows
    for row in db_rows:
        parsed_row = row.__dict__
        del parsed_row["_sa_instance_state"]

        # Add a parsed dict (map) to are return set
        parsed_rows.append(parsed_row)

    # Return the compiled set (list) of row dicts
    return parsed_rows

