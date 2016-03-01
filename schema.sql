DROP TABLE if EXISTS entries;
CREATE TABLE entries (
  id integer PRIMARY KEY AUTOINCREMENT,
  datetime datetime NOT NULL,
  ping float NOT NULL,
  download float NOT NULL,
  upload float NOT NULL
);