CREATE TABLE users (
	id SERIAL NOT NULL, 
	realname TEXT NOT NULL, 
	username TEXT NOT NULL, 
	password_hash TEXT NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
)

CREATE TABLE calendars (
	id SERIAL NOT NULL, 
	owner_id INTEGER, 
	name TEXT, 
	description TEXT, 
	private BOOLEAN DEFAULT true NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id) ON DELETE CASCADE
)

CREATE TABLE categories (
	id SERIAL NOT NULL, 
	calendar_id INTEGER, 
	name TEXT NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(calendar_id) REFERENCES calendars (id) ON DELETE CASCADE
)

CREATE TABLE jobs (
	id SERIAL NOT NULL, 
	category_id INTEGER, 
	name TEXT NOT NULL, 
	description TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id) ON DELETE CASCADE
)

CREATE TABLE tasks (
	id SERIAL NOT NULL, 
	job_id INTEGER, 
	name TEXT NOT NULL, 
	description TEXT, 
	done BOOLEAN DEFAULT false NOT NULL, 
	planned_time INTEGER DEFAULT 0, 
	actual_time INTEGER DEFAULT 0, 
	PRIMARY KEY (id), 
	FOREIGN KEY(job_id) REFERENCES jobs (id) ON DELETE CASCADE
)
