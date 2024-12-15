from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, author_id, title, content, magazine_id, id=None):
        """Initialize the Article with an author, title, content, and magazine ID."""
        
        # Validate title
        if not isinstance(title, str) or len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be a string between 5 and 50 characters.")
        
        # Validate content
        if not isinstance(content, str) or len(content) == 0:
            raise ValueError("Content must be a non-empty string.")
        
        # Fetch the Author instance using author_id
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM authors WHERE id = ?', (author_id,))
        author_data = cursor.fetchone()
        if author_data is None:
            raise ValueError(f"Author with ID {author_id} not found.")
        
        # Create an Author object
        self._author = Author(author_data[0], author_data[1])

        # Fetch the Magazine instance using magazine_id
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (magazine_id,))
        magazine_data = cursor.fetchone()
        if magazine_data is None:
            raise ValueError(f"Magazine with ID {magazine_id} not found.")
        
        # Create a Magazine object
        self._magazine = Magazine(magazine_data[0], magazine_data[1], magazine_data[2]) 

        # insert the article into the articles table
        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id) 
            VALUES (?, ?, ?, ?)
        ''', (title, content, self._author.id, self._magazine.id))
        
        conn.commit()

        # Retrieve the ID of the newly created article
        self._id = cursor.lastrowid
        self._title = title
        self._content = content

        conn.close()

    @property
    def title(self):
        """Return the article's title."""
        return self._title

    @property
    def content(self):
        """Return the article's content."""
        return self._content

    @property
    def id(self):
        """Return the article's ID."""
        return self._id

    @property
    def author(self):
        """Return the author of the article."""
        return self._author

    @property
    def magazine(self):
        """Return the magazine of the article."""
        return self._magazine

    def __repr__(self):
        return f'<Article {self.title}>'
