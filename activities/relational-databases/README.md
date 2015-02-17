# Relational Databases #

There are a number of relational databases with a great variety of features.  In this activity, we'll use the 
popular [SQLite database](http://www.sqlite.org/) as a local embedded database.  This will avoid the need to configure
remote connections.  Given the core interoperability of SQL, most of the activity can easily be ported to 
other databases once the connection has been established.

## Setup ##

SQLite3 comes packaged with python.  You may also want the sqlite3 command-line tools.  If you do not have the
command-line shell for sqlite, you may have only the supporting libraries for the python interface.  Additional
tools can be installed via the [SQLite website](http://www.sqlite.org/).

You can test whether you have a SQLite command-line shell by:

    $ sqlite3
    SQLite version 3.8.7.4 2014-12-09 01:34:36
    Enter ".help" for usage hints.
    Connected to a transient in-memory database.
    Use ".open FILENAME" to reopen on a persistent database.
    sqlite>
    
## ER Models to SQLite Tables ##

Once you have a Entity-Relationship Model (ER model), you'll need to translate the model into
a set of table definitions.  For SQLite, simple primary/foreign key relationships can be created
by use of integer row identitifiers.

A primary key is simply labeled with `INTEGER PRIMARY KEY` and this enables SQLite to manage autocreation
integer values for primary keys.

A foreign key is a specially labeled column that references the table column:

    FOREIGN KEY(user) REFERENCES users(id)
    
You can create a set of tables either by executing SQL statements via python or the command-line shell:

    CREATE TABLE users (
       id INTEGER PRIMARY KEY,
       alias TEXT UNIQUE NOT NULL,
       name TEXT
    );
    CREATE TABLE tweets (
       user INTEGER NOT NULL,
       tweet TEXT NOT NULL,
       FOREIGN KEY(user) REFERENCES users(id)
    );
    
Note: See the syntax of [CREATE TABLE](https://www.sqlite.org/lang_createtable.html) for more information on the possibilities and the [datatypes supported by SQLite](http://www.sqlite.org/datatype3.html).

Try this now my running the sqlite3 command-line tool and just cut-n-past the above definitions:

    $ sqlite3 test.db
    SQLite version 3.8.7.4 2014-12-09 01:34:36
    Enter ".help" for usage hints.
    sqlite> CREATE TABLE users (
       ...>        id INTEGER PRIMARY KEY,
       ...>        alias TEXT UNIQUE NOT NULL,
       ...>        name TEXT
       ...>     );
    sqlite> CREATE TABLE tweets (
       ...>        user INTEGER NOT NULL,
       ...>        tweet TEXT NOT NULL,
       ...>        FOREIGN KEY(user) REFERENCES users(id)
       ...>     );
    sqlite> 
    
## Inserting Data ##

You can insert data into tables via simple SQL commands.  SQLite will handle row identifiers for primary keys if you've defined them to be integers:

    sqlite> insert into users(alias,name) values ('alexmilowski','Alex Milowski');
    sqlite> insert into users(alias,name) values ('ghopper','Grace Hopper');
    sqlite> select * from users;
    1|alexmilowski|Alex Milowski
    2|ghopper|Grace Hopper

If know the user's primary key, we can insert tweet text:

    sqlite> insert into tweets values (1,"Hello World!");
    sqlite> select * from tweets where user=(select id from users where alias='alexmilowski');
    1|Hello World!
   
## SQLite in Python ##

Connecting to a database is simple.  Given the previous example database, we can do:

    >>> import sqlite3
    >>> conn = sqlite3.connect('test.db')

and execute a query:

    >>> c = conn.cursor()
    >>> c.execute('SELECT * FROM users')
    >>> c.fetchone()
    (1, u'alexmilowski', u'Alex Milowski')
    >>> c.fetchone()
    (2, u'ghopper', u'Grace Hopper')
    >>> c.fetchone()

We can also bind values in queries:

    >>> c.execute('SELECT * FROM users WHERE alias=?', ['alexmilowski'])
    >>> c.fetchone()
    (1, u'alexmilowski', u'Alex Milowski')

Or iterate results:

    >>> for row in c.execute('SELECT * FROM users'):
    ...    print row
    ... 
    (1, u'alexmilowski', u'Alex Milowski')
    (2, u'ghopper', u'Grace Hopper')

Inserting data requires both a query (insert statement) and a commit:

    >>> users=[('mariecurie',"Marie Curie"),
    ...        ('albert',"Albert Einstein")]
    >>> c.executemany("INSERT INTO users(alias,name) VALUES(?,?)",users)
    <sqlite3.Cursor object at 0x10bdfdf80>
    >>> conn.commit()

Finally, don't forget to close the connection:

    >>> conn.close()




