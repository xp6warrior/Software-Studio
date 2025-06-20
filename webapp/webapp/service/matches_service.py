from webapp.repository.matches_repo import *
from webapp.repository.item_repo import select_items_by_email, insert_update_item
from webapp.service.account_service import get_user_account_details
from webapp.models2.models import ArchivedItems
from webapp.models2.enums import MatchStatusEnum
from webapp.util.pickup_report import generate_pickup_report

def get_unconfirmed_matches(worker_email: str) -> list[dict[str, str]]:
    matches_list = []
    items = select_items_by_email(worker_email)
    if items == []:
        return False

    for i in items:
        matches = select_matches_by_item(i)

        for m in matches:
            if m.status == MatchStatusEnum.UNCONFIRMED:
                matches_list.append({
                    "match_id": str(m.id),
                    "lost": m.lost_item.to_dict(),
                    "found": m.found_item.to_dict(),
                    "percentage": str(m.percentage)
                })

    return matches_list

def get_confirmed_matches_with_owner_info(worker_email: str) -> list[dict[str, str]]:
    matches_list = []
    items = select_items_by_email(worker_email)
    if items == []:
        return False
    
    for i in items:
        matches = select_matches_by_item(i)

        for m in matches:
            if m.status == MatchStatusEnum.CONFIRMED:
                # owner should never be false due to the foreign key constraint on the lost_item email
                # if it is, it will show up as false
                owner = get_user_account_details(m.lost_item.email)
                matches_list.append({
                    "match_id": str(m.id),
                    "found": m.found_item.to_dict(),
                    "owner": owner
                })

    return matches_list

def confirm_match(match_id: str) -> bool:
    match = select_match_by_id(int(match_id))
    if match == None:
        return False
    elif match.status == MatchStatusEnum.UNCONFIRMED:
        match.status = MatchStatusEnum.CONFIRMED
        insert_update_match(match)
        return True
    
def hand_over_and_archive_match(match_id: str, owner_pesel: str) -> bool:
    if archive_match(match_id, owner_pesel) is not None:
        return True
    else:
        return False

def hand_over_and_generate_receipt_and_archive_match(match_id: str, owner_pesel: str) -> str:
    results = archive_match(match_id, owner_pesel)
    
    if results is not None:
        item_details = results[0]
        owner_details = results[1]
        filename = f"{owner_details['name']}_{owner_details['surname']}_Pickup_Report.pdf"
        return generate_pickup_report(filename, owner_details, item_details)
    else:
        return False
        

def archive_match(match_id: str, owner_pesel: str) -> ArchivedItems:
    match = select_match_by_id(int(match_id))

    if match == None:
        return None
    elif match.status == MatchStatusEnum.CONFIRMED:
        # owner_details should never be false due to the foreign key constraint on the lost_item email
        # if it is, this function will throw an exception, blocking the handover
        owner_details = get_user_account_details(match.lost_item.email)
        item_summary = match.found_item.__str__()

        archive = ArchivedItems(item_summary=item_summary, owner_email=owner_details["email"], owner_name=owner_details["name"],
                                owner_surname=owner_details["surname"], owner_pesel=owner_pesel)
        insert_update_item(archive)

        match.status = MatchStatusEnum.PICKED_UP
        insert_update_match(match)

        item_details = match.found_item.to_dict()
        item_details["id"] = archive.id
        return [item_details, owner_details]
