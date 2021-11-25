from __future__ import unicode_literals, print_function
import unicodecsv as csv

# Define data
data = [
    (1, "maçã,", 1.0),
    (42, "manga, uva", 2.0),
    (1337, "jaca", -1),
    (0, "kiwi", 123),
    (-2, "Nada.", 3),
]
def setup():
    size(600, 600)
    background(0, 100, 0)
    # textSize(24)
    textFont(createFont('Source Code Pro', 24))
    # # Write CSV file
    # with open("test.csv", "wb") as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["your", "header", "foo"])  # write header
    #     writer.writerows(data)
    
    
    with open('test.csv') as file:
        reader = csv.DictReader(file)
        data_read = [row for row in reader]
        for row in data_read:
            print(row['your'])
        
    
    
    # # Read CSV file
    # # encoding="utf-8"
    # with open("test.csv") as file:
    #     reader = csv.reader(file)
    #     cabecalho = next(reader, None)  # skip the headers
    #     print(cabecalho)
    #     data_read = [row for row in reader]
    #     x, y = 20, 100
    #     for row in data_read:
    #         for item in row:
    #             print(item.ljust(12), end='')
    #             text(item.ljust(12), x, y)
    #             x += textWidth(item.ljust(12))
    #         y += 32
    #         x = 20
    #         print()
