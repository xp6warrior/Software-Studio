from webapp.models2.enums import StatusEnum, MatchStatusEnum
from webapp.repository.item_repo import select_item_stats, select_num_of_archived_items
from webapp.repository.matches_repo import select_match_stats

def get_stats():
    results = {
        "Lost items": "0",
        "Found items": "0",
        "Unconfirmed matches": "0",
        "Confirmed matches": "0",
        "Items waiting for pickup": "0",
        "False pickup claims": "0",
        "Picked-up items": "0"
    }
    item_stats = select_item_stats()
    for i in item_stats:
        if i[0] == StatusEnum.LOST:
            results["Lost items"] = str(i[1])
        elif i[0] == StatusEnum.FOUND:
            results["Found items"] = str(i[1])

    match_stats = select_match_stats()
    for m in match_stats:
        if i[0] == MatchStatusEnum.UNCONFIRMED:
            results["Unconfirmed matches"] = str(i[1])
        elif i[0] == MatchStatusEnum.CONFIRMED:
            results["Confirmed matches"] = str(i[1])
        elif i[0] == MatchStatusEnum.PICKED_UP:
            results["Items waiting for pickup"] = str(i[1])
        elif i[0] == MatchStatusEnum.FALSE_PICKUP:
            results["False pickup claims"] = str(i[1])

    archive_stats = select_num_of_archived_items()
    results["Picked-up items"] = archive_stats

    return results

