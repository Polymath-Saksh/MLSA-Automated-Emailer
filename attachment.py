import csv

class Attachment:
    def __init__(self):
        self.csv_file = 'participants.csv'
        self.email_list = []

    def parse_csv(self):
        with open(self.csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                name = row[0]
                email = row[1]
                path = f"Certificates/{name}.pdf"
                self.email_list.append((name, email, path))

    def get_email_list(self):
        self.parse_csv()
        return self.email_list