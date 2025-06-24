def get_email_template(template_id, full_name, item_id=None, item_type=None):
    return {
        1: (
            "Welcome to Back2U",
            f"Hi {full_name}!\n\nYour Back2U account has been created successfully🎉! We're so excited to have you on board.\n\nLet's bring the lost things back where they belong 💜"
        ),
        2: (
            "Item ready for Pickup", 
            f"Hi!\n\nYour item (ID: {item_id}) is matched and ready for pickup!\nPlease contact us for detail on when and where."
        ),
        3: (
            "Item added", 
            f"Hi {full_name},\n\nYour item (ID: {item_id}, Type: {item_type}) has been successfully added to your Back2U account.\n\nWe will reach out as soon as we find a match!\nFingers crossed it finds its way back soon! 🤞"
        ),
        4: (
            "Item updated", 
            f"Hi {full_name},\n\nYour item (ID: {item_id}) has been updated successfully. Thanks for keeping things current!"
        ),
        5: (
            "Item removed", 
            f"Hi {full_name},\n\nYour item (ID: {item_id}) has been removed from your account.\n\nHope everything's all good!"
        ),
        6: (
            "Item expiring soon", 
            f"Hi {full_name},\n\nJust a heads up — your item (ID: {item_id}) is about to expire and will be deleted soon (in 5 days time).\n\nYou can extend its duration in your account if you'd like to keep it active! 😊"
        ),
        7: (
            "Item automatically deleted", 
            f"Hi {full_name},\n\nYour item (ID: {item_id}) has been automatically deleted due to it having no activity in the past 30 days.\n\nYou can re-create the lost item report anytime from your Back2U dashboard!"
        ),
        8: (
            "It’s a match!", 
            f"Hi {full_name},\n\nGood news — a match was confirmed for your item (ID: {item_id})!\n\nWe’re one step closer to bringing it back to its owner ✨"
        ),
        9: (
            "Item picked up!", 
            f"Hi {full_name},\n\nPickup for your item (ID: {item_id}) has been confirmed.\n\nThanks for helping close the loop — you're awesome! ✨\n\nIf you believe that someone stole your item, you have 30 days to submit a false pickup."
        ),
        10: (
            "New match found!", 
            f"Hi {full_name},\n\nA new potential match was found for the item (ID: {item_id}, Type: {item_type}).\n\nCheck it out in your Back2U Worker account to confirm it's the one!"
        ),
        11: (
            "Inactivity Detected!",
            f"Hi {full_name},\n\nYou have been inactive for 10 days! This is just a reminder that there may be potential matches waiting to be confirmed!"
        )
    }.get(template_id, (
        "Hello from Back2U", 
        f"Hi {full_name},\n\nWe couldn’t find a message for this notification. But we’re glad you’re here!"
    ))
