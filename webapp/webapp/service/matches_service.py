from webapp.repository.matches_repo import *
from webapp.repository.item_repo import *
from webapp.repository.image_repo import *
from webapp.service.account_service import get_user_account_details
from webapp.models2.models import ArchivedItems
from webapp.models2.enums import MatchStatusEnum
from webapp.util.pickup_report import generate_pickup_report

def get_unconfirmed_matches(worker_email: str) -> list[dict[str, str]]:
    matches_list = []
    items = select_items_by_email(worker_email)

    found_items_with_a_conf = []
    for i in items:
        matches = select_matches_by_item(i)

        for m in matches:
            if m.status == MatchStatusEnum.CONFIRMED or m.status == MatchStatusEnum.PICKED_UP or m.status == MatchStatusEnum.FALSE_PICKUP:
                found_items_with_a_conf.append(i.id)

    for i in items:
        if i.id in found_items_with_a_conf:
            continue

        matches = select_matches_by_item(i)
        for m in matches:
            if m.status == MatchStatusEnum.UNCONFIRMED:

                synopsis = ""
                for k, v in i.to_dict().items():
                    synopsis += f"{v} "
                synopsis += i.type
                matches_list.append({
                    "match_id": str(m.id),
                    "synopsis": synopsis
                })

    return matches_list

def get_unconfirmed_match(match_id: str):
    match = select_match_by_id(int(match_id))
    if match is None:
        return False
    else:
        lost_item = select_item_by_id(match.lost_item_id)
        found_item = select_item_by_id(match.found_item_id)
        lost_dict = lost_item.to_dict()
        lost_dict["image"] = get_image(str(lost_item.id))
        found_dict = lost_item.to_dict()
        found_dict["image"] = get_image(str(found_item.id))
        return {
            "match_id": match_id,
            "lost": lost_dict,
            "found": found_dict,
            "percentage": str(match.percentage)
        }

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
                found_item = select_item_by_id(m.found_item.id)
                owner['firstname'] = owner.pop('name')
                matches_list.append(
                    {"match_id": str(m.id)} | found_item.to_dict() | owner
                )

    return matches_list

def confirm_match(match_id: str) -> bool:
    match = select_match_by_id(int(match_id))
    if match == None:
        return False
    elif match.status == MatchStatusEnum.UNCONFIRMED:
        match.status = MatchStatusEnum.CONFIRMED
        insert_update_match(match)
        return True
    
def hand_over_and_archive_match(match_id: str, pesel: str, print_receipt: bool) -> bytes:
    match = select_match_by_id(int(match_id))

    if match == None:
        return False
    elif match.status == MatchStatusEnum.CONFIRMED:
        # owner_details should never be false due to the foreign key constraint on the lost_item email
        # if it is, this function will throw an exception, blocking the handover
        owner_details = get_user_account_details(match.lost_item.email)
        found_item = select_item_by_id(match.found_item.id)
        item_summary = found_item.__str__()

        archive = ArchivedItems(item_summary=item_summary, owner_email=owner_details["email"], owner_name=owner_details["name"],
                                owner_surname=owner_details["surname"], owner_pesel=pesel, match_id=match.id)
        try:
            insert_update_item(archive)
        except:
            return False

        match.status = MatchStatusEnum.PICKED_UP
        insert_update_match(match)

        if print_receipt:
            item_details = found_item.to_dict()
            owner_details["pesel"] = pesel

            del item_details['status']
            del item_details['created_at']
            del item_details['email']
            item_details['Archive ID'] = item_details.pop('id', None)
            item_details['Category'] = item_details.pop('category', None)
            item_details['Item type'] = item_details.pop('it', None)
            item_details['Descripton'] = item_details.pop('desc', None)
            item_details['Color'] = item_details.pop('color', None)
            item_details['Size'] = item_details.pop('size', None)
            item_details['Material'] = item_details.pop('material', None)
            item_details['Brand'] = item_details.pop('brand', None)
            item_details['Name'] = item_details.pop('name', None)

            return generate_pickup_report(owner_details, item_details)
        else:
            return True
