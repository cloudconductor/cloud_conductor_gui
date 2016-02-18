
def valiCheck(form):

    errors = form.errors.as_data()
    msg = ""
    for e in errors:
        msg = errors[e][0].messages[0]
        break
    return msg
