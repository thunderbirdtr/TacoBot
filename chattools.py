from dbmodels import Usernames


async def get_uid(message):
    """ this makes your life easier """
    return message.from_user.id


async def get_cid(message):
    """ this makes your life easier """
    return message.chat.id
""

async def get_mid(message):
    """ this makes your life easier """
    return message.message_id


async def store_name(message):
    """ this function is here only for /tacotop """

    uid = get_uid(message)

    username = Usernames.select().where(Usernames.uid == uid)
    if username.exists():
        return username.get().name

    user = message.from_user
    if user.username is None:
        username = None
        first_name = user.first_name
        last_name = user.last_name
        if last_name is None:
            name = first_name
        else:
            name = first_name + ' ' + last_name
    else:
        name = '@' + user.username
        username = user.username.lower()

    Usernames.create(
        uid=uid,
        name=name,
        username=username)
    return name


async def resolve_name(uid):                                                               # returns username if present in DB
    user = Usernames.select().where(Usernames.uid == uid)
    if user.exists():
        return user.get().name
    else:
        return uid


async def ensure_username(name: str):
    """
    Forces an @ sign to be inserted at the beginning of the passed `name`
    :param name: A telegram username
    """
    return '@' + ensure_no_at_sign(name)


async def ensure_no_at_sign(name: str):
    return name.lstrip('@')
