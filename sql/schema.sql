CREATE TABLE lk_entries (
	id INTEGER PRIMARY KEY,
	manuscripts_id INTEGER,
	lk_entry INTEGER,
	lk_page INTEGER,
	settlement TEXT NOT NULL,
	repository TEXT NOT NULL,
	idno TEXT,
	locus TEXT,
	opus TEXT,
	author INTEGER,
	provenance TEXT,
	dating TEXT,
	refs TEXT,
	raw_text TEXT	
);