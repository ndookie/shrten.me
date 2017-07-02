CREATE TABLE "url_table" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`date`	DATETIME,
	`url`	TEXT NOT NULL,
	`shortened_url`	TEXT,
	`ip` TEXT
);
;
CREATE TABLE sqlite_sequence(name,seq);
