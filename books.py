'''
The problems are solved by implementing a customized dataframe class.
The program should be executed by Python 3.4
'''
import csv
import argparse

class MyDataFrame(object):
    
    def __init__(self, columns = [], data = []):
        self.columns = set(columns)
        if data:
            self.data = [dict(zip(columns, [e.strip(' ') for e in row])) for row in data]
        else:
            self.data = None
            
    def __getitem__(self, item):
        if isinstance(item[0], bool):
            if len(item) != len(self.data):
                raise Exception("Slice length does not match data")
            else:
                temp_df = MyDataFrame()
                temp_df.columns = self.columns
                temp_df.data = [self.data[i] for i in range(len(self.data)) if item[i]]
                return temp_df

    #Read data from file     
    @classmethod
    def from_file(cls, file_path, columns, delimiter=',', quotechar='\n'):
        with open(file_path, 'r') as infile:
            reader = csv.reader(infile, delimiter=delimiter, quotechar=quotechar)
            data = []
            for row in reader:
                data.append(row)
        return cls(data = data, columns = columns)
    
    #Integrate different dataframe
    def append(self, df):
        if self.columns == df.columns:
            self.data += df.data

        else:
            raise Exceprion("Columns of the datasets not match")
    
    #Sort data by optional key default by Last Name
    def sort_by(self, key = 'Last_Name', reverse = False ,inplace = False):
        if key in self.columns:
            if inplace:
                self.data = sorted(self.data, key = lambda x:x[key], reverse = reverse)
                return self
            else:
                temp_df = MyDataFrame()
                temp_df.columns = self.columns
                temp_df.data = sorted(self.data, key = lambda x:x[key], reverse = reverse)
                return temp_df
        else:
            raise Exception("Key Not in Columns")
    
    #Fileter by optional characters
    def filter_by_char(self, char = ''):
        def isInRow(row, char = char):
            for e in row.values():
                if char in e:
                    return True
            return False
        mask = [isInRow(row, char) for row in self.data]
        return self[mask]

if __name__ == '__main__':

    #Read data from multiple files
    books = MyDataFrame.from_file('csv',['Book_Title', 'Last_Name', 'First_Name', 'year'])
    books.append(MyDataFrame.from_file('pipe',['First_Name','Last_Name','Book_Title', 'year'], 
                                     delimiter='|', quotechar='\n'))
    books.append(MyDataFrame.from_file('slash',['year','First_Name','Last_Name','Book_Title'], 
                                     delimiter='/', quotechar='\n'))
    books.sort_by(inplace=True)

    #Command Lines Argument Parser
    parser = argparse.ArgumentParser(description="Show a list of books, \
                                            alphabetical ascending by author's last name")
    parser.add_argument("--filter", help = "show a subset of books, looks for the argument as\
                                            a substring of any of the fields")
    parser.add_argument("--year", help = "sort the books by year, ascending instead of \
                                        default sort",  action='store_true')
    parser.add_argument("--reverse", help = "reverse sort",  action='store_true')
    args = parser.parse_args()

    output_order = ['Last_Name', 'First_Name','Book_Title','year']

    if args.filter:
        books = books.filter_by_char(args.filter)

    if args.year:
        books.sort_by(key='year', inplace=True)

    if args.reverse:
        for r in books.data[::-1]:
            print([r[c] for c in output_order])
    else:
        for r in books.data:
            print([r[c] for c in output_order])



