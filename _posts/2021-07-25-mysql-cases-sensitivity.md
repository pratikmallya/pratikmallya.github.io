---
layout: post
title: "Be Careful With MySQL Case Insensitivity"
description: "Some surprising bugs when working with MySQL queries"
tags: ["MySQL"]
---

TLDR: MySQL collations are are case-insensitive by default leading to
unexpected behavior in certain situations.

The other day we saw the following issue in our production system: A service
that fetches files from remote sources kept fetching a file repeatedly and
indefinitely. The logic for the system was simple: it periodically scanned a
"source" (e.g. an s3 bucket). If a file name existed in the source that did not
exist in a DB table of fetched files, it would download the file, create a db
entry with the file name. On further scans, the file would no longer be fetched
since an entry for it would exist in our database.

A closer inspection revealed the existence of multiple files in the source,
differing in case. e.g.

```
my_file.txt
My_file.txt
```

The system seemed to _always_ fetch `my_file.txt` and always skip `My_file.txt`.
This seemed suspicious, so we looked at the query to check against the table of
retrieved files, which looked something like such:

```sql
SELECT MAX(files.created_at) AS files_created_at_max, files.name
FROM files
GROUP BY files.name;
```
Explanation of SQL:

1. `SELECT MAX(files.created_at) AS files_created_at_max, files.name FROM files`:
select the columns `created_at` and `name` from the `files` table. Apply the
`MAX` [aggregation operation] to the `created_at` column and call the resulting
column `files_created_at_max`.

2. `GROUP BY files.name`: For 2 rows with the same `name`, get the row with the
_larger value for `created_at`_ (the `MAX` aggregator from the previous step).
The result is a list of rows with unique `name` and `created_at`.

[aggregation operation]: https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html

For demonstration, I've created a table with 2 entries with the names differing
only in case:

```sql
SELECT * FROM files;
+-------------+------------+
| name        | created_at |
+-------------+------------+
| my_file.txt | 2021-07-26 |
| My_file.txt | 2021-07-26 |
+-------------+------------+
```

The query seemed to only fetch results for one case:

```sql
SELECT MAX(files.created_at) AS files_created_at_max, files.name
FROM files
GROUP BY files.name;
+----------------------+-------------+
| files_created_at_max | name        |
+----------------------+-------------+
| 2021-07-26           | my_file.txt |
+----------------------+-------------+
1 row in set (0.00 sec)
```

This seemed suspicious: why would the query return just one of the names when
both existed in the table?

A quick google search for "MySQL case sensitive" gave some pointers to what the
problem might be. MySQL defines _collations_ for every _character set_
(e.g. ascii, utf-8); in general, a collation is a rule for comparing characters
in a character set. A MySQL collation simply defines a _weight_
(a numerical value) for each character, and uses that for comparisons. Two
characters with the same weight are considered the "same" when sorting.

We can get information about the character sets and collations used in our table using `show full columns`:

```sql
SHOW FULL COLUMNS from files;
+------------+-------------+--------------------+------+-----+---------+-------+---------------------------------+---------+
| Field      | Type        | Collation          | Null | Key | Default | Extra | Privileges                      | Comment |
+------------+-------------+--------------------+------+-----+---------+-------+---------------------------------+---------+
| name       | varchar(20) | utf8mb4_0900_ai_ci | YES  |     | NULL    |       | select,insert,update,references |         |
| created_at | date        | NULL               | YES  |     | NULL    |       | select,insert,update,references |         |
+------------+-------------+--------------------+------+-----+---------+-------+---------------------------------+---------+
2 rows in set (0.01 sec)
```

Collations with a `ci` suffix means that the _collation is case insensitive_!
To MySQL, both the strings `my_file.txt` and `My_file.txt` were the "same",
when using aggregations, and thus the query aggregated across both cases and
returned just one.

To fix this, we could change the collation for the table:
```sql
ALTER TABLE files convert to CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_cs;
```
The query now returns both files:
```sql
SELECT MAX(files.created_at) AS files_created_at_max, files.name FROM files GROUP BY files.name;
+----------------------+-------------+
| files_created_at_max | name        |
+----------------------+-------------+
| 2021-07-26           | my_file.txt |
| 2021-07-26           | My_file.txt |
+----------------------+-------------+
2 rows in set (0.01 sec)
```

If we don't want to alter the DB, we can also tell MySQL to use a specific
collation just for this query:
```sql
SELECT MAX(files.created_at) AS files_created_at_max, files.name COLLATE utf8mb4_0900_as_cs
FROM files
GROUP BY files.name COLLATE utf8mb4_0900_as_cs;
+----------------------+---------------------------------------+
| files_created_at_max | files.name COLLATE utf8mb4_0900_as_cs |
+----------------------+---------------------------------------+
| 2021-07-26           | my_file.txt                           |
| 2021-07-26           | My_file.txt                           |
+----------------------+---------------------------------------+
2 rows in set (0.00 sec)

```
Note that we're using the `_cs` (case sensitive) version of the collation. If
a case sensitive collation isn't present, you may also use the `_bin` collation
for the character set (in this case it would be `utf8mb4_bin`). To see all
collations for a character set, use e.g.

```sql
SHOW COLLATIONS WHERE Charset LIKE 'utf8mb4'
```

And that's it! Once we changed our queries to use a case-sensitive collation,
the query returned different cased versions of the files, and our system was
able to recognize the file was already pulled from the source.

As an aside, the [official MySQL documentation] explains these concepts pretty
well and I would highly recommend reading it at least once.

[official MySQL documentation]: https://dev.mysql.com/doc/refman/8.0/en/charset.html

### Reproducing the Experiment

In this section, I'll describe how to set up an MySQL environment to test this
behavior.

Lets use a dockerized MySQL `v8.0`. Start up the server ([instructions]):
```
docker run --name mysql-test -e MYSQL_ROOT_PASSWORD=secret -p 127.0.0.1:33060:3306 -d mysql:8.0
```
connect using `mysql` client:
```
$ mysql -u root --protocol=tcp --port 33060 -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 8.0.26 MySQL Community Server - GPL

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

Now lets create the table and add a few rows:

```sql
CREATE DATABASE demo;
USE DATABASE demo;
CREATE TABLE files (name VARCHAR(20), created_at DATE);
INSERT INTO files
VALUES
("my_file.txt", NOW()),
("My_file.txt", DATE_SUB(NOW(), INTERVAL 2 HOUR));
```

check values in the table:

```sql
SELECT * FROM files;
+-------------+------------+
| name        | created_at |
+-------------+------------+
| my_file.txt | 2021-07-26 |
| My_file.txt | 2021-07-26 |
+-------------+------------+
```

You can now run the queries described in the post!

[instructions]: https://hub.docker.com/_/mysql?tab=description























