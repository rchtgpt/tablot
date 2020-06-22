from terminaltables import AsciiTable

def return_doc(db, guild_id):
    var_doc = db.collection(u'sheet_variables').document(u'{}'.format(guild_id))
    doc_val = var_doc.get()
    if doc_val.exists:
        doc = doc_val.to_dict()
        return doc

def show_var(gClient, doc, var):
    sheet = gClient.open_by_url(doc[var]).sheet1
    data = sheet.get_all_values()
    tableData = [data[0]]
    for i in range(1, len(data)):
        val = [k for k in data[i]]
        tableData.append(val)
    table = AsciiTable(tableData)
    return table

def show_var_row(a, gClient, doc, var):
    if len(a) > 3:
        sheet = gClient.open_by_url(doc[var]).sheet1
        data = sheet.findall(a[-1])
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
                #return final
                yield final
            
def show_var_col(a, gClient, doc, var):
    if len(a) > 3:
        sheet = gClient.open_by_url(doc[var]).sheet1
        tableData = sheet.row_values(1)
        if a[-1] in tableData:
            table = tableData.index(a[-1])
            colVals = sheet.col_values(table + 1)
            lst = []
            for i in colVals:
                lst.append([i])
            return lst
        else:
            return 'error'
    