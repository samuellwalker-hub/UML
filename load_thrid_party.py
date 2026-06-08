import csv

# Define your data
headers = ['ticket_id', 'trans_date', 'event_id', 'event_name', 'event_date', 'event_type', 'event_city', 'customer_id', 'price', 'num_tickets']
rows = [
    [1,	2020-8-1, 100, 'The North American International Auto Show', 2020-9-1, 'Exhibition', 'Michigan', 123, 35, 3],
    [2,	2020-8-3, 101, 'Carlisle Ford Nationals', 2020-9-30, 'Exhibition', 'Carlisle', 151,	43,	1],
    [3,	2020-8-3, 102, 'Washington Spirits vs Sky Blue FC', 2020-8-30, 'Sports', 'Washington DC', 223, 59.34, 5],
    [4,	2020-8-5, 103, 'Christmas Spectacular', 2020-10-5, 'Theater', 'New York', 223, 89.95, 2],
    [5,	2020-8-5, 100, 'The North American International Auto Show', 2020-9-1, 'Exhibition', 'Michigan', 126, 35, 1],
    [6, 2020-8-5, 103, 'Christmas Spectacular', 2020-10-5, 'Theater', 'New York', 1024, 89.95, 3]
]

# Write to file
with open('load_third_party.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write header
    writer.writerows(rows)    # Write data rows

print("CSV file created successfully!")
