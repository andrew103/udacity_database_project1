import psycopg2


def popular_article():
    """ Finds and lists the articles and their number of views from greatest
    to least """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    # use slug to relate IP views to articles:
    # where log.path = '%'articles.slug
    c.execute("""select articles.title, articles.author,
                        cast(count(articles.slug) as int) as num
                    from articles, log
                    where log.path like concat('%', articles.slug)
                    group by articles.title, articles.author
                    order by num desc;""")

    return c.fetchall()
    db.close()


def popular_author():
    """ Finds and lists the authors and their number of views from greatest
    to least """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    # use double select statement with inner being the select statement
    # from the popular_article function
    c.execute("""select authors.name,
                        cast(sum(article_views.num) as int) as num
                    from authors, (select articles.title,
                                    articles.author,
                                    cast(count(articles.slug) as int) as num
                                    from articles, log
                                    where log.path
                                        like concat('%', articles.slug)
                                    group by articles.title, articles.author
                                    order by num desc) as article_views
                    where authors.id = article_views.author
                    group by authors.name
                    order by num desc;""")

    return c.fetchall()
    db.close()


def percent_error_requests():
    """ Analyzes the site logs to determine days where a percentage of traffic
    receiving error messages such as 404 NOT FOUND that exceed 1% """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    # find a way to pull status messages given the same day
    # then do math for avg
    c.execute("""select a.date,
                    concat(cast((b.num * 100.0/(a.num + b.num))as float), '%')
                    from (select date(time) as date,
                                log.status, count(log.status) as num
                            from log
                            group by date(time), log.status
                            order by date(time) desc) as a,
                         (select date(time) as date,
                                log.status, count(log.status) as num
                            from log
                            group by date(time), log.status
                            order by date(time) desc) as b
                    where a.date = b.date
                    and a.status != b.status
                    and a.status = '200 OK'
                    and cast((b.num * 100.0/(a.num + b.num))as float) > 1.0
                    order by a.date desc;""")

    return c.fetchall()
    db.close()


# Main function that runs all or some functions in the file
def run():
    print(popular_article())
    print('')
    print(popular_author())
    print('')
    print(percent_error_requests())


run()
