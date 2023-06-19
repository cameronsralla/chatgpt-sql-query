import openai
import pymysql.cursors
import config

openai.api_key = config.gpt_api_key

def ask_gpt(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an agent that is listening to requests from a user, then looking at data from the smb_app database and then writing a MYSQL query to get the information you need to answer the question appropriately. You should bias towards being as accurate and matter-of-fact as possible."},
            {"role": "user", "content": prompt}
        ]
        )
    print(completion)
    return completion.choices[0].message.content

def run_query(query):
    # Connect to the database
    connection = pymysql.connect(host=config.db_host,
                                 port=config.db_port,
                                 user=config.db_user,
                                 password=config.db_password,
                                 db=config.db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

def main():
    while True:

        db_datasets = '''
        table, column
        asset, id
        asset, company_id
        asset, name
        asset, description
        asset, serial_number
        asset, purchase_date
        asset, purchase_price
        company, id
        company, name
        customer, id
        customer, company_id
        customer, name
        customer, email
        customer, phone
        customer, address
        order, id
        order, company_id
        order, customer_id
        order, service_id
        order, asset_id
        order, date
        order, time
        order, notes
        order, status
        service, id
        service, company_id
        service, name
        service, description
        service, price
        user, id
        user, company_id
        user, username
        user, email
        user, password
        '''

        # get question from user
        question = input("Ask a question about data in the smb_app dbs: ")
        if question.lower().strip() != 'exit' or question.lower().strip() != 'e ':
            try:
                question_prompt = f'''
                You are working as an agent who's job is to gather data from users and query a MYSQL database to get information for them. Whatever question is asked, it is very important that your response only the query and nothing else. The datastructure for the database is as follows: 
                {db_datasets}

                User question: {question}
                '''

                # translate question into SQL
                sql_query = ask_gpt(question_prompt)
                print(f"Generated SQL query: {sql_query}")
                
                # validate the SQL query
                #sql_val_prompt = f'''
                #Read the following MYSQL query and determine if there are any errors. If you see no errors, return the same query as your repsonse. If you see errors, make the needed corrections and only return the corrected SQL query with no other text.
                #Query:
                #{sql_query}
                #'''
                #validated_sql_query = ask_gpt(sql_val_prompt)
                #print(f"Generated SQL query: {validated_sql_query}")

                # execute the SQL query
                db_result = run_query(sql_query)
                print(f"Database returned: {db_result}")

                # get a summary of the results
                summarize_prompt = f'''
                Use the following sql results to answer the question below:
                {db_result}

                Given this information, please answer this question and be explicit in using the results from the query to answer the question in a conversational way for someone who is non-technical:
                {question}
                '''
                result_summary = ask_gpt(f"Summarize the result: {db_result}")
                print(f"Result summary: {result_summary}")
            except Exception as e:
                error_response = f'''
                There was an error in the processing of this request.
                {e}
                Please try again.
                '''
                print(error_response)
                continue
        else:
            break

if __name__ == "__main__":
    main()
