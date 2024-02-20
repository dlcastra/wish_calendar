from app.helpers import generate_wish, save_or_get_other


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
