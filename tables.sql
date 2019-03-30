create table if not exists user_table(
    NAME STRING,
    NETID STRING PRIMARY KEY,
    MAJOR STRING
);

create table if not exists location_table(
    NAME STRING PRIMARY KEY,
    CAPACITY INTEGER,
    XCOORDINATE DOUBLE,
    YCOORDINATE DOUBLE
);

create table if not exists class_table(
    CRN INTEGER PRIMARY KEY,
    NAME STRING
);

create table if not exists group_table(
    GID INTEGER PRIMARY KEY AUTOINCREMENT,
    CREATOR INTEGER REFERENCES user_table(NETID),
    CRN INTEGER REFERENCES class_table(CRN),
    LOCATION STRING REFERENCES location_table(NAME),
    GSIZE INTEGER,
    ABOUT STRING
);
