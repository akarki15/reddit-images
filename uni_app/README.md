Screenshots: 
![alt tag](https://raw.githubusercontent.com/akarki15/uni_app/master/screenshot/Screen%20Shot%202015-07-01%20at%2010.24.00%20AM.png)
![alt tag](https://raw.githubusercontent.com/akarki15/uni_app/master/screenshot/Screen%20Shot%202015-07-01%20at%2010.24.14%20AM.png)
![alt tag](https://raw.githubusercontent.com/akarki15/uni_app/master/screenshot/Screen%20Shot%202015-07-01%20at%2010.25.34%20AM.png)
![alt tag](https://raw.githubusercontent.com/akarki15/uni_app/master/screenshot/Screen%20Shot%202015-07-01%20at%2010.24.30%20AM.png)

Setup Instructions: 

Clone this repo

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
	
Start a local mysql server
	
	mysql.server start
	
Create a local MySQL database called uni_database and execute the following sql commands to create the following tables: 

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

Note that the connection settings to mysql are in __init__.py
	
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/uni_database'
	
Run the MySQL server

Python runserver.py
