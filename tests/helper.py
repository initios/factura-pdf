from os.path import dirname, abspath, join


def get_tests_folder():
    return dirname(abspath(__file__))


def get_output_folder():
    return join(get_tests_folder(), "output")


def get_image_folder():
    return join(get_tests_folder(), "assets", "img")


def get_asset_image(file):
    return join(get_image_folder(), file)


def get_initios_logo_path():
    return get_asset_image("initios_logo.png")