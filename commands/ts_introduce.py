from firebase_admin import firestore

def intro(indi, db, guild_id, author, author_id, sheet):
    total = sheet.get_all_values()
    final_add = []
    for i in indi:
        final_add.append(i.split(":")[1].strip()[1:-1])  # to remove quotes
    final_add.append(f'{author}')
    col_doc = db.collection(u'registered users').document(u'{}'.format(guild_id))
    doc_val = col_doc.get()
    if doc_val.exists:
        doc = doc_val.to_dict()
        check = False
        for dv in doc.values():
            if author_id not in dv:
                check = False
            else:
                check = True
                break
        if not check:
            sheet.insert_row(final_add, len(total) + 1)
            col_doc.update({u'ids': firestore.ArrayUnion([author_id])})
            return 'add'
        else:
            all_values = sheet.get_all_values()
            for i in all_values:
                if i[-1] == str(author):
                    ind = all_values.index(i)
                    break
            for i in range(1, len(final_add) + 1):
                sheet.update_cell(ind+1, i, final_add[i-1])
            return 'update'
    else:
        add = [author_id]
        sheet.insert_row(final_add, len(total) + 1)
        db.collection(u'registered users').document(u'{}'.format(guild_id)).set({
            u'ids': add
        })
        return 'add'