#!/usr/bin/env python3

import psycopg2


# Variables that hold queries
article_query = """
select articles.title, cast(count(articles.slug)as int) as num
    from articles, log
    where log.path like concat('%', articles.slug)
    group by articles.title
    order by num desc
    limit 3;
"""

author_query = """
select authors.name, cast(sum(article_views.num) as int) as num
    from authors, (select articles.title, articles.author,
                                cast(count(articles.slug) as int) as num
                    from articles, log
                    where log.path like concat('%', articles.slug)
                    group by articles.title, articles.author
                    order by num desc) as article_views
    where authors.id = article_views.author
    group by authors.name
    order by num desc;
"""

error_query = """
select a.date, concat(cast((b.num * 100.0/(a.num + b.num))as float), '%')
    from (select date(time) as date, log.status, count(log.status) as num
                from log
                group by date(time), log.status
                order by date(time) desc) as a,
         (select date(time) as date, log.status, count(log.status) as num
                from log
                group by date(time), log.status
                order by date(time) desc) as b
    where a.date = b.date
        and a.status != b.status
        and a.status = '200 OK'
        and cast((b.num * 100.0/(a.num + b.num))as float) > 1.0
    order by a.date desc;
"""




def execute_query(query):
    """ Dedicated function for running queries that are passed in """
    try:
        db = psycopg2.connect("dbname=news")
        c = db.cursor()

        c.execute(query)

        result = c.fetchall()
        db.close()
        return result
    except:
        return "Unable to connect to the database"


def popular_article():
    """ Finds and lists the articles and their number of views from greatest
    to least """
    # use slug to relate IP views to articles:
    # where log.path = '%'articles.slug
    top_articles = execute_query(article_query)
    print("Top 3 Trending Articles")
    print("-" * 15)
    for article in top_articles:
        print("{} -- {} views".format(article[0], article[1]))


def popular_author():
    """ Finds and lists the authors and their number of views from greatest
    to least """
    # use double select statement with inner being the select statement
    # from the popular_article function
    top_authors = execute_query(author_query)
    print("Most Viewed Authors")
    print("-" * 15)
    for author in top_authors:
        print("{} -- {} views".format(author[0], author[1]))


def percent_error_requests():
    """ Analyzes the site logs to determine days where a percentage of traffic
    receiving error messages such as 404 NOT FOUND that exceed 1% """
    # find a way to pull status messages given the same day
    # then do math for avg
    error_percent = execute_query(error_query)
    print("Days with 404 errors greater than 1%")
    print("-" * 15)
    for error in error_percent:
        print("{} -- {}".format(error[0], error[1]))


# Main function that runs all or some functions in the file
if __name__ == "__main__":
    popular_article()
    print('')
    popular_author()
    print('')
    percent_error_requests()
