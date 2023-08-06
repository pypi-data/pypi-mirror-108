from .. import udB, ultroid_bot

CMD_HELP = {}


def sudoers():
    return udB["SUDOS"].split()


def owner_and_sudos():
    return [str(ultroid_bot.uid), *sudoers()]
