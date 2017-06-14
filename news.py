#!/usr/bin/env python3

import psycopg2

DBNAME = "news"


def get_articles():
    """Return 3 most popular articles"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT articles.title, log.views "
    	      "FROM (SELECT path, count(*) as count FROM log "
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
              "GROUP BY authors.name ORDER BY views DESC LIMIT 3;")
    authors = c.fetchall()
    db.close()

    for i in authors:
        print (i[0] + ' | ' + str(i[1]))


def get_errors():
    """On which days did more than 1% of requests lead to errors"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT errors_view.date, count, total_requests from errors_view"
              " INNER JOIN totals_view ON errors_view.date = totals_view.date "
              "WHERE ((errors_view.count*100)/totals_view.total_requests)>1;")
    errors = c.fetchall()
    db.close()

    for i in errors:
        print (i[0])
        print (str(round((i[1]*100)/i[2], 2)) + '% errors')
        print ("---------------")


print ("------------------------------------------------")
print ("The three most popular articles are:")
get_articles()
print ("------------------------------------------------")
print ("The three most popular authors are:")
get_authors()
print ("------------------------------------------------")
print ("These days had more than 1% of page requests as errors:")
get_errors()
