# Local application imports
from data.menus import models as menu_models


def delete_menu_item(*, item: menu_models.MenuItem) -> None:
    item.delete()
