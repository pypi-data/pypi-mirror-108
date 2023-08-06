from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE domains (
            id SERIAL PRIMARY KEY, 
            domain TEXT NOT NULL,
            status_code INTEGER,
            UNIQUE(domain)
        )""",
         "DROP TABLE domains"
        )
]