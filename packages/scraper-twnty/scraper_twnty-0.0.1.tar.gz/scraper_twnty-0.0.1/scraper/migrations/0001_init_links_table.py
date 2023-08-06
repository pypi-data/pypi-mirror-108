from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE links (
            id SERIAL PRIMARY KEY, 
            domain TEXT NOT NULL,
            UNIQUE(domain)
        )""",
         "DROP TABLE links"
        )
]