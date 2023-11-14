import csv
def Read_Data(p):
    # 打开CSV文件
    ipad = '/private/var/mobile/Containers/Data/Application/BD13E5CF-FC75-4FE8-910E-9E061253A0E7/Documents/Multi_Charge.git/data/data'+ str(p) + '.csv'
    other = '../data/data' + str(p) + '.csv'
    with open(other, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Initialize dictionaries for each column
        columns = {header: [] for header in reader.fieldnames}
        # Iterate through the rows and append each value to the corresponding column
        for row in reader:
            for header, value in row.items():
                columns[header].append(value)
    N = len(columns['x']) - 2
    return N,columns
