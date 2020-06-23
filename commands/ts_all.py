def all_vars(db, guild_id):
    col = db.collection(u'sheet_variables').document(u'{}'.format(guild_id))
    var_col = col.get()
    if var_col.exists:
        var = var_col.to_dict()
        to_print = ''
        for i in var.keys():
            to_print = to_print + i + '\n'
        return to_print
    