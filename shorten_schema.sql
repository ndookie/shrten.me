CREATE TABLE "url_table" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`url`	TEXT NOT NULL,
	`shortened_url`	TEXT
);
;
CREATE TABLE sqlite_sequence(name,seq);