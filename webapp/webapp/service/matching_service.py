from webapp.repository import matching_repo

def match_item(opposite_type: str, model_name: str, item_id: int):
    #returns list of tuples, opposite tybe because we wanna see matching found items for lost ones and VV

    # 1. get selected item from repo
    item = matching_repo.get_item_by_id(model_name, item_id)
    if not item:
        raise ValueError(f"No item with id {item_id} in {model_name}")

    # 2. get all items of the same model than the chosen one to match others to
    all_items = matching_repo.get_all_items_of_model(model_name)

    # status of the opposite one
    if opposite_type.lower() == "lost":
        target_status = "lost"
        my_status = "found"
    elif opposite_type.lower() == "found":
        target_status = "found"
        my_status = "lost"
    else:
        raise ValueError("opposite_type must be 'lost' or 'found'")

    # we only filter through the opposite items
    candidates = [i for i in all_items if i.status.lower() == target_status]

    # 3 calculate how many matching attributes we have
    ATTRIBUTES_TO_COMPARE = ["type", "color", "size", "material", "brand", "name"]
    results = []

    for candidate in candidates:
        score = 0
        for attr in ATTRIBUTES_TO_COMPARE:
            val1 = getattr(item, attr, None)
            val2 = getattr(candidate, attr, None)
            if val1 and val2 and val1 == val2:
                score += 1
        results.append( (candidate, score) )

    # 4. sort by descending so we see the items with the most matches on top (excluding 0 matches)
    results.sort(key=lambda x: x[1], reverse=True)
    return results
