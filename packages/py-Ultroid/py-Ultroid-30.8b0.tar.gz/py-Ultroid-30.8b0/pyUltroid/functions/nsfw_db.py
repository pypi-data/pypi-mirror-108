from .. import udB

try:
    eval(udB.get("NSFW"))
except BaseException:
    udB.set("NSFW", "{}")


def nsfw_chat(chat, action):
    x = eval(udB.get("NSFW"))
    x.update({chat: action})
    return udB.set("NSFW", str(x))


def rem_nsfw(chat):
    x = eval(udB.get("NSFW"))
    x.pop(chat)
    return udB.set("NSFW", str(x))


def is_nsfw(chat):
    x = eval(udB.get("NSFW"))
    if x.get(chat):
        return x[chat]
    return
