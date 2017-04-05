drop table if exists posts;

create table posts ( 
	id integer primary key AUTOINCREMENT,
	title CHAR(80), 
	post TEXT, 
	post_date TEXT,
	draft integer,
        categories TEXT
);
