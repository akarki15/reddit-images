Install following dependencies: 

	Flask==0.10.1
	Flask-SQLAlchemy==2.0
	Flask-WTF==0.11
	gunicorn==19.3.0
	itsdangerous==0.24
	Jinja2==2.7.3
	MarkupSafe==0.23
	MySQL-python==1.2.5
	SQLAlchemy==1.0.3
	Werkzeug==0.10.4
	WTForms==2.0.2

Create a local MySQL database and create the following tables: 

	CREATE TABLE users (
	userID INT NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(userID),
	firstname VARCHAR(100) NOT NULL,
	lastname VARCHAR(100) NOT NULL,
	username VARCHAR(120) NOT NULL UNIQUE,
	hashpass VARCHAR(100) NOT NULL
	) ENGINE=INNODB ;


	CREATE TABLE posts (

	postID INT AUTO_INCREMENT,
	text VARCHAR(1000),
	imageURI VARCHAR(100),
	userID INT NOT NULL, 
	 
	PRIMARY KEY(postID),

	FOREIGN KEY (userID)
	REFERENCES users (userID)
	ON DELETE CASCADE,

	categoryID INT NOT NULL,
	FOREIGN KEY (categoryID)
	REFERENCES categories (categoryID)
	ON DELETE CASCADE

	) ENGINE=INNODB;


	CREATE TABLE categories (

	categoryID INT AUTO_INCREMENT,
	name VARCHAR(1000),
	 
	PRIMARY KEY(categoryID)

	) ENGINE=INNODB;
