def link(a, db, guild_id):
    sheetVar = a[2].strip()
    link = a[1][1:-1]
    var_doc = db.collection(u'sheet_variables').document(u'{}'.format(guild_id))
    doc = var_doc.get()
    if doc.exists:
        var_doc.update({db.field_path(str(sheetVar)): u'{}'.format(link)})
    else:
        var_doc.set({db.field_path(str(sheetVar)): u'{}'.format(link)})
    return sheetVar