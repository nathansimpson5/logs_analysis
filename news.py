#!/usr/bin/env python3

import psycopg2

DBNAME = "news"


def get_articles():
    """Return 3 most popular articles"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT articles.title, log.views "
              "FROM (SELECT path, count(*) as views FROM log "
              "WHERE status = '200 OK' GROUP BY path) AS log "
              "INNER JOIN articles "
              "ON log.path ILIKE '%' || articles.slug "
              "ORDER BY views DESC LIMIT 3;")
    articles = c.fetchall()
    for i in articles:
        print (i[0] + ' | ' + str(i[1]))
    db.close()

    return articles


def get_authors():
    """Return 3 most popular authors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT authors.name, count(*) AS views "
              "FROM articles INNER JOIN authors "
              "ON authors.id = articles.author INNER JOIN "
              "log ON log.path ILIKE '%' || articles.slug "
              "GROUP BY authors.name ORDER BY views DESC;")
    authors = c.fetchall()
    db.close()

    for i in authors:
        print (i[0] + ' | ' + str(i[1]))


def get_errors():
    """On which days did more than 1% of requests lead to errors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT to_char(date, 'FMMonth FMDD, YYYY'), err/total as ratio"
              " from (select time::date as date, "
              "count(*) as total, "
              "sum((status != '200 OK')::int)::float as err "
              "from log "
              "group by date) as errors "
              "where err/total > .01;")
    errors = c.fetchall()
    db.close()

    for i in errors:
        print (i[0])
        print (str(round((i[1]*100), 2)) + '% errors')
        print ("---------------")


print ("------------------------------------------------")
print ("The three most popular articles are:")
get_articles()
print ("------------------------------------------------")
print ("The most popular authors are:")
get_authors()
print ("------------------------------------------------")
print ("These days had more than 1% of page requests as errors:")
get_errors()
