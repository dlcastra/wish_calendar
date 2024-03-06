from app.helpers import generate_wish, save_or_get_other, get_short_path


def test_generate_wish():
    wish = generate_wish()

    assert wish is not None
    assert type(wish) == str


def test_save_or_get_other():
    db_list = ["wish1", "wish2", "wish3", "wish4", "wish5"]
    new_wish = "wish1"
    get_other = save_or_get_other(new_wish, db_list)

    assert get_other not in db_list
    assert get_other is not None


def test_get_short_path():
    path = "path/to/my/app/project/images/winter/winter.png"
    short_path = get_short_path(path)

    assert short_path != "path/to/my/app/project/images/winter/winter.png"
    assert short_path != "images/winter/"
    assert short_path != "images/"
    assert short_path is not None
    assert short_path == "images/winter/winter.png"