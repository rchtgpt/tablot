from terminaltables import AsciiTable

def display_row(gClient, link, content):
    sheet = gClient.open_by_url(link).sheet1
    j = content.split(" ", 5)
    data = sheet.findall(j[-1])
    tableData = list()
    tableData.append(sheet.row_values(1))
    for i in data:
        tableData.append(sheet.row_values(i.row))
    final = ''
    for i in tableData:
        if tableData[tableData.index(i)] == tableData[-1]:
            break
        else:
            final = ''
            for j in range(len(i)):
                final += f'{tableData[0][j]}: {tableData[tableData.index(i) + 1][j]}\n'
            yield final
    
def display_col(gClient, j, link):
    sheet = gClient.open_by_url(link).sheet1
    tableData = sheet.row_values(1)
    if j[-1] in tableData:
        table = tableData.index(j[-1])
        colVals = sheet.col_values(table + 1)
        lst = []
        for i in colVals:
            lst.append([i])
        return lst

def display_link(gClient, link):
    sheet = gClient.open_by_url(link).sheet1
    data = sheet.get_all_values()
    tableData = [data[0]]
    for i in range(1, len(data)):
        val = [k for k in data[i]]
        tableData.append(val)
    table = AsciiTable(tableData)
    return table