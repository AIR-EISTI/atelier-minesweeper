import configparser


def config_reader(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        return config["minesweeper"]
    except KeyError:
        return None


def rescue_basic_config(config_file):
    config = config_reader(config_file)
    if config:
        return map(int, (config.get("height"), config.get("width"), config.get("bombs")))
    else:
        return 10, 10, 20

