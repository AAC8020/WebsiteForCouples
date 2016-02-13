CREATE TABLE passage(
	id integer primary key autoincrement,
	time text not NULL,
	passage text not NULL,
	sex text not NULL,
	type text default 'text'
);