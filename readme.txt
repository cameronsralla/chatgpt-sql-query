gpt_query allows for a user to query a given database in natural language

basic setup:
- install python dependencies
- add the ChatGPT api key
- add the credentials to connect to the sql database of your choice
- enter the database structure for ChatGPT to know where to look for content by passing a list of tables and rows in the database

Once this is done you should be able to run the program which will ask for user input via terminal and wait for a response. It will prompt ChatGPT and have it write a sql query to
retieve the necessary data to answer the question, then the program will run the query against the database. It will then pass the return from the database to ChatGPT in a second
prompt and ask it to answer the question based on the sql response and report these results to the user. 
