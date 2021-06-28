import configparser


def bot_validation(instance, number) -> bool:
    parser = configparser.ConfigParser()
    parser.read("bot_config.txt")
    if instance == 'User':
        if number >= int(parser.get("bot-config", "number_of_users")):
            return False
    elif instance == 'Post':
        if number >= int(parser.get("bot-config", "max_posts_per_user")):
            return False
    elif instance == 'PostRating':
        if number >= int(parser.get("bot-config", "max_likes_per_user")):
            return False
    return True
