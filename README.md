# logs_analysis
udacity logs analysis

This program has 3 outputs every time it is run. The 3 most popular articles in the database, the 3 most popular authors in
the database, and all of the days where more than 1% of page requests were 404 errors. 

The views created in the SQL are:
create view errors_view as select date(time), count(*) from log where status = '404 NOT FOUND' group by date order by date;

and 

CREATE VIEW totals_view AS select date(time), count(*) as total_requests from log group by date order by date;



This program assumes you have the same database that I was provided by Udacity.

To run the program: 
- download the python file news.py
- update the variable DBNAME on line 5 to whatever your database is called
- from the command line, run the file with the command 'python3 news.py' (without the quotations)

Please report any bugs to me on Github
