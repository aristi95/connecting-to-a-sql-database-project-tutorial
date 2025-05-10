import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1) Connect to the database with SQLAlchemy
connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(connection_string).execution_options(autocommit=True)
engine.connect()

# 2) Create the tables
with engine.connect() as connection:
        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS authors (
            author_id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            middle_name VARCHAR(50) NULL,
            last_name VARCHAR(100) NULL
        );

        CREATE TABLE IF NOT EXISTS books (
            book_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            total_pages INT NULL,
            rating DECIMAL(4, 2) NULL,
            isbn VARCHAR(13) NULL,
            published_date DATE,
            publisher_id INT NULL,
            CONSTRAINT fk_publisher FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS book_authors (
            book_id INT NOT NULL,
            author_id INT NOT NULL,
            PRIMARY KEY (book_id, author_id),
            CONSTRAINT fk_book FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE,
            CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE
        );
        """))
               
# 3) Insert data
with engine.connect() as connection:
        connection.execute(text("""
        INSERT INTO publishers (publisher_id, name) VALUES
        (1, 'O Reilly Media'),
        (2, 'A Book Apart'),
        (3, 'A K PETERS'),
        (4, 'Academic Press'),
        (5, 'Addison Wesley'),
        (6, 'Albert&Sweigart'),
        (7, 'Alfred A. Knopf')
    ON CONFLICT (publisher_id) DO NOTHING;

    INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES
        (1, 'Merritt', NULL, 'Eric'),
        (2, 'Linda', NULL, 'Mui'),
        (3, 'Alecos', NULL, 'Papadatos'),
        (4, 'Anthony', NULL, 'Molinaro'),
        (5, 'David', NULL, 'Cronin'),
        (6, 'Richard', NULL, 'Blum'),
        (7, 'Yuval', 'Noah', 'Harari'),
        (8, 'Paul', NULL, 'Albitz')
    ON CONFLICT (author_id) DO NOTHING;

    INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES 
            (1, 'Lean Software Development: An Agile Toolkit', 240, 4.17, '9780320000000', '2003-05-18', 5),
            (2, 'Facing the Intelligence Explosion', 91, 3.87, null, '2013-02-01', 7),
            (4, 'Patterns of Software: Tales from the Software Community', 256, 3.84, '9780200000000', '1996-08-15', 1),
            (5, 'Anatomy Of LISP', 446, 4.43, '9780070000000', '1978-01-01', 3),
            (6, 'Computing machinery and intelligence', 24, 4.17, null, '2009-03-22', 4),
            (7, 'XML: Visual QuickStart Guide', 269, 3.66, '9780320000000', '2009-01-01', 5),
            (8, 'SQL Cookbook', 595, 3.95, '9780600000000', '2005-12-01', 7),
            (9, 'The Apollo Guidance Computer: Architecture And Operation (Springer Praxis Books / Space Exploration)', 439, 4.29, '9781440000000', '2010-07-01', 6),
            (10, 'Minds and Computers: An Introduction to the Philosophy of Artificial Intelligence', 222, 3.54, '9780750000000', '2007-02-13', 7);                                                     

        """))

# 4) Use Pandas to read and display a table
import pandas as pd
df = pd.read_sql("SELECT * FROM publishers", engine)
print(df)

