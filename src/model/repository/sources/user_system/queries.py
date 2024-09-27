CREATE_RECORDS = '''
INSERT INTO parser_records(
    name, 
    phone_number,
    web_link,
    city, 
    org_type,
    task_id
) VALUES (
    :name, 
    :phone_number, 
    :web_link,
    :city, 
    :org_type,
    :task_id
)
'''

SELECT_BY_TASK = """
SELECT DISTINCT 
    phone_number, 
    name
FROM parser_records
WHERE task_id = :task_id
AND web_link IS NOT NULL
"""
