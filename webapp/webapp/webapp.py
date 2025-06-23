# my recently editing webapp

import reflex as rx
from rxconfig import config


import base64
import os

#   V------this "apperance" "config" we can read this from a file
# ========================================CONFIG============================================
logo = "/logo.png"
banner = "/banner.png"
config_path = os.getenv("CONFIGS_PATH") + "/config.txt"
if not os.path.exists(config_path):
    print("CONFIG IS NOT SET")
    exit(-1)
config_file = open(config_path, "r")
cnfg = config_file.readlines()
for i in range(len(cnfg)):
    cnfg[i] = cnfg[i].strip("\n\r")
app_name = cnfg[0]
app_desc = cnfg[1]
email_domain = cnfg[2]
bg_style = {"background": cnfg[3], "padding": cnfg[4]}
button_style_1 = cnfg[5]
button_style_2 = cnfg[6]
hover_style = cnfg[7]


# ========================================BACKEND===================================================
from webapp.service.account_service import *
from webapp.service.item_service import *
from webapp.service.matches_service import *
from webapp.service.stats_service import *
from webapp.repository.configs_repo import *

# def login(email, password):
#     return "WORKER"
#     return "ADMIN"
#     return "USER"


# def create_account(email, password, role, firstname, surname):
#     print(email, password, role, firstname, surname)
#     return "ACCOUNT CREATED SUCCESSFULLY"


# def get_user_account_details(email):
#     return {"email": "a@b.c", "role": "USER", "name": "Arin", "surname": "Upadhyay"}


# def get_policy():
#     return "POLICY TEXT"


# def submit_item(email, item):
#     print(email, item)
#     return "Item submitted successfully"


# def get_submitted_lost_items(user_email):
#     return [
#         {
#             "id": "12",
#             "category": "Personal Items",
#             "it": "Passport",
#             "desc": "ss",
#             "color": "Green",
#             "size": "",
#             "material": "",
#             "brand": "",
#             "name": "",
#             "status": "Matched",
#         },
#         {
#             "id": "13",
#             "category": "Personal Items",
#             "it": "Passport",
#             "desc": "pp",
#             "color": "Red",
#             "size": "",
#             "material": "",
#             "brand": "",
#             "name": "",
#             "status": "Picked Up",
#         },
#     ]


# def update_lost_item(user_email, iid, updated_item):
#     print(user_email, iid, updated_item)
#     return "OK"


# def delete_lost_item(user_email, iid):
#     print(user_email, iid)
#     return True


# def report_false_pickup(user_email, iid):
#     print(user_email, iid)
#     return True


# def get_unconfirmed_matches(worker_email):
#     return [
#         {"match_id": "123", "synopsis": "Black Passport Paper S"},
#         {"match_id": "145", "synopsis": "Green Handbag Fabric M"},
#     ]


# def get_unconfirmed_match(mid):
#     from pathlib import Path

#     image_path1 = Path("C:\\Users\\HP\\Desktop\\bgs\\doo.jpeg")
#     image_bytes1 = image_path1.read_bytes()
#     image_path2 = Path("C:\\Users\\HP\\Desktop\\bgs\\doom.jpg")
#     image_bytes2 = image_path2.read_bytes()
#     return {
#         "match_id": "123",
#         "lost": {
#             "id": "12",
#             "image": image_bytes1,
#             "category": "Personal Items",
#             "it": "Passport",
#             "desc": "ss",
#             "color": "Green",
#             "size": "",
#             "material": "",
#             "brand": "",
#             "name": "",
#         },
#         "found": {
#             "id": "13",
#             "image": image_bytes2,
#             "category": "Personal Items",
#             "it": "Passport",
#             "desc": "ss",
#             "color": "Green",
#             "size": "",
#             "material": "",
#             "brand": "",
#             "name": "",
#         },
#         "score": "87%",
#     }


# def confirm_match(mid):
#     print(mid)
#     return True


# def get_confirmed_matches_with_owner_info(worker_email):
#     return [
#         {
#             "match_id": "123",
#             "id": "13",
#             "category": "Personal Items",
#             "it": "Passport",
#             "desc": "ss",
#             "color": "Green",
#             "size": "",
#             "material": "",
#             "brand": "",
#             "name": "",
#             "email": "a@b.c",
#             "firstname": "ARIN",
#             "surname": "Upadhyay",
#         },
#         {
#             "match_id": "124",
#             "id": "13",
#             "category": "Personal Items",
#             "it": "Passport",
#             "desc": "ss",
#             "color": "Green",
#             "size": "",
#             "material": "",
#             "brand": "",
#             "name": "",
#             "email": "a@b.c",
#             "firstname": "ARIN",
#             "surname": "Upadhyay",
#         },
#     ]


# def hand_over_and_archive_match(mid, pesel, print_receipt):
#     from pathlib import Path

#     r = Path("C:\\Users\\HP\\Downloads\\uykladSWITCH.pdf")
#     rb = r.read_bytes()
#     print(mid, pesel, print_receipt)
#     return rb


# def write_policy(policy):
#     print(policy)
#     return True


# def get_stats():
#     return {"NUMBER OF ITEMS DELIVERED": "100"}


# def get_false_pickup_reports():
#     return [
#         {
#             "id": "13",
#             "owner_fullname": "ARIN Upadhyay",
#             "owner_email": "a@b.c",
#             "pickedupby_fullname": "ARIN2 Upadhyay",
#             "pickedupby_email": "a2@b.c",
#         }
#     ]


# def get_accounts():
#     return [
#         {
#             "email": "a@b.c",
#             "password": "dd",
#             "role": "USER",
#             "firstname": "ARIN",
#             "surname": "Upadhyay",
#         }
#     ]


# def delete_account(email):
#     print(email)
#     return True


# ============================================================================================================

categories = [
    "Personal Items",
    "Jewelry",
    "Accessories",
    "Travel Items",
    "Electronic Devices",
    "Clothing",
    "Office Items",
    "Other Items",
]
personal_item_types = ["ID Card", "Passport", "Keys", "Credit Card", "Other"]
jewelry_types = ["Ring", "Earrings", "Necklace", "Piercing", "Other"]
accessory_types = ["Glasses", "Sun Glasses", "Wrist Watch", "Other"]
travel_item_types = [
    "Suitcase",
    "Handbag",
    "Backpack",
    "Luggage",
    "Umbrella",
    "Wallet",
    "Purse",
    "Water Bottle",
    "Other",
]
electronic_device_types = [
    "Phone",
    "Laptop",
    "Tablet",
    "Cable",
    "Earbuds",
    "Headphones",
    "Camera",
    "Smart Watch",
    "Powerbank",
    "Other",
]
clothing_types = ["Coat", "Jacket", "Gloves", "Scarf", "Hat", "Shoes", "Other"]
office_item_types = ["Pen", "Folder", "Book", "Other"]
sizes = ["XS", "S", "M", "L", "XL"]
materials = [
    "Wood",
    "Metal",
    "Plastic",
    "Glass",
    "Ceramic",
    "Fabric",
    "Leather",
    "Rubber",
    "Paper",
    "Other",
]
colors = [
    "Red",
    "Green",
    "Blue",
    "Yellow",
    "Orange",
    "Purple",
    "Pink",
    "Brown",
    "Black",
    "White",
    "Gray",
    "Cyan",
    "Maroon",
    "Navy",
    "Beige",
    "Other",
]


class State(rx.State):
    # ===============================Login==========================
    email: str = ""
    password: str = ""
    logged_in_as_user: bool = False
    logged_in_as_worker: bool = False
    logged_in_as_admin: bool = False
    not_logged_in: bool = True
    login_response: str = ""

    def call_login(self):
        temp = login(self.email, self.password)
        if temp == False:
            self.login_response = "INCORRECT EMAIL OR PASSWORD"
        elif temp == "USER":
            self.logged_in_as_user = True
            self.not_logged_in = False
            self.load_account_details()
            self.load_submitted_lost_items()
            self.load_policy()
            return rx.redirect("/user-dashboard")
        elif temp == "WORKER":
            self.logged_in_as_worker = True
            self.not_logged_in = False
            self.load_account_details()
            self.load_unconfirmed_matches()
            self.load_confirmed_matches_with_owner_info()
            self.load_policy()
            return rx.redirect("/worker-dashboard")
        elif temp == "ADMIN":
            self.logged_in_as_admin = True
            self.not_logged_in = False
            self.load_policy()
            self.load_stats()
            self.load_false_pickup_reports()
            self.load_accounts()
            return rx.redirect("/admin-dashboard")

    def logout(self):
        self.logged_in_as_user = False
        self.logged_in_as_worker = False
        self.logged_in_as_admin = False
        self.not_logged_in = True

    def redirect_if_bad_auth(self, required_role):
        if (required_role == "USER" and not self.logged_in_as_user) or (required_role == "WORKER" and not self.logged_in_as_worker) or (required_role == "ADMIN" and not self.logged_in_as_admin):
            return rx.redirect("/")

    # ===============================Register User account==========================
    register_user_response: str = ""

    def call_register_user(self):
        if "@" not in self.email or "." not in self.email:
            self.register_user_response = "INVALID EMAIL FORMAT"
            return
        self.register_user_response = create_account(
            self.email, self.password, "USER", self.firstname, self.surname
        )

    # ===============================Account details==========================
    firstname: str = ""
    surname: str = ""

    def load_account_details(self):
        temp = get_user_account_details(self.email)
        self.firstname = temp["name"]
        self.surname = temp["surname"]

    # ===============================Submit Item==========================
    picture_data: bytes = b""
    category: str = ""
    it: str = ""
    desc: str = ""
    color: str = ""
    size: str = ""
    material: str = ""
    brand: str = ""
    name: str = ""
    submit_item_response: str = ""

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        if files is not None:
            upload_data = await files[0].read()
            self.picture_data = upload_data

    def call_submit_item(self):
        temp = {
            "image": self.picture_data,
            "category": self.category,
            "it": self.it,
            "desc": self.desc,
            "color": self.color,
            "size": self.size,
            "material": self.material,
            "brand": self.brand,
            "name": self.name,
        }
        self.submit_item_response = submit_item(self.email, temp)
        self.picture_data = b""
        return rx.clear_selected_files("upload1")
    
    def renew_item(self, id: str):
        self.delete_lost_item_response = renew_lost_item(self.email, id)

    # ===============================Get Submitted Lost Item==========================
    #submitted_lost_items: list[list] = []
    submitted_lost_items: list[dict[str, str]] = []
    get_submitted_lost_items_response: str = ""

    def load_submitted_lost_items(self):
        temp = get_submitted_lost_items(self.email)
        if temp == False:
            self.get_submitted_lost_items_response = "SOMETHING WENT WRONG"
            return
        self.submitted_lost_items = []
        for item in temp:
            pass
            #self.submitted_lost_items.append(list(item.values()))
        self.submitted_lost_items = temp

    # NEW for inline editing
    editing_iid: str = ""
    is_editing: bool = False

    def start_edit(self, iid: str):
        # load that item into update_… fields
        self.editing_iid = iid
        item = get_submitted_lost_items(self.email)
        for it in item:
            if it["id"] == iid:
                self.update_category = it.get("category")
                self.update_it = it.get("it")
                self.update_desc = it.get("desc")
                self.update_color = it.get("color")
                self.update_size = it.get("size")
                self.update_material = it.get("material")
                self.update_brand = it.get("brand")
                self.update_name = it.get("name")
                break
        self.is_editing = True

    def cancel_edit(self):
        self.is_editing = False
        self.editing_iid = ""
        self.update_lost_item_response = ""

    update_picture_data: bytes = b""
    update_category: str = ""
    update_it: str = ""
    update_desc: str = ""
    update_color: str = ""
    update_size: str = ""
    update_material: str = ""
    update_brand: str = ""
    update_name: str = ""
    update_lost_item_response: str = ""
    delete_lost_item_response: str = ""

    async def handle_update_upload(self, files: list[rx.UploadFile]):
        upload_data = await files[0].read()
        self.update_picture_data = upload_data

    def call_update_lost_item(self, iid):
        temp = {
            "image": self.update_picture_data,
            "category": self.update_category,
            "it": self.update_it,
            "desc": self.update_desc,
            "color": self.update_color,
            "size": self.update_size,
            "material": self.update_material,
            "brand": self.update_brand,
            "name": self.update_name,
        }
        self.update_lost_item_response = update_lost_item(self.email, iid, temp)
        self.load_submitted_lost_items()

    def call_delete_lost_item(self, iid):
        temp = delete_lost_item(self.email, iid)
        if temp == False:
            self.delete_lost_item_response = "SOMETHING WENT WRONG"
        else:
            self.delete_lost_item_response = "Item deleted successfully"
        self.load_submitted_lost_items()

    def call_report_false_pickup(self, iid):
        temp = report_false_pickup(self.email, iid)
        if temp == False:
            self.delete_lost_item_response = "SOMETHING WENT WRONG"
        else:
            self.delete_lost_item_response = "Report submitted successfully"
        self.load_submitted_lost_items()

    # =============================User Misc====================================
    policy: str = ""

    def load_policy(self):
        self.policy = get_policy()

    # ==============================Get unconfirmed matches and confirm==========================
    unconfirmed_matches: list[dict] = []

    def load_unconfirmed_matches(self):
        self.unconfirmed_matches = get_unconfirmed_matches(self.email)

    unconfirmed_match_id: str = ""
    unconfirmed_match_lost_id: str = ""
    unconfirmed_match_lost_picture_data: str = ""
    unconfirmed_match_lost_category: str = ""
    unconfirmed_match_lost_it: str = ""
    unconfirmed_match_lost_desc: str = ""
    unconfirmed_match_lost_color: str = ""
    unconfirmed_match_lost_size: str = ""
    unconfirmed_match_lost_material: str = ""
    unconfirmed_match_lost_brand: str = ""
    unconfirmed_match_lost_name: str = ""
    unconfirmed_match_found_id: str = ""
    unconfirmed_match_found_picture_data: str = ""
    unconfirmed_match_found_category: str = ""
    unconfirmed_match_found_it: str = ""
    unconfirmed_match_found_desc: str = ""
    unconfirmed_match_found_color: str = ""
    unconfirmed_match_found_size: str = ""
    unconfirmed_match_found_material: str = ""
    unconfirmed_match_found_brand: str = ""
    unconfirmed_match_found_name: str = ""
    unconfirmed_match_score: str = ""

    def load_unconfirmed_match(self, mid):
        temp = get_unconfirmed_match(mid)
        self.unconfirmed_match_id = temp["match_id"]
        self.unconfirmed_match_lost_id = temp["lost"]["id"]
        self.unconfirmed_match_lost_picture_data = (
            "data:image/jpeg;base64," + base64.b64encode(temp["lost"]["image"]).decode()
        )
        self.unconfirmed_match_lost_category = temp["lost"].get("category")
        self.unconfirmed_match_lost_it = temp["lost"].get("it")
        self.unconfirmed_match_lost_desc = temp["lost"].get("desc")
        self.unconfirmed_match_lost_color = temp["lost"].get("color")
        self.unconfirmed_match_lost_size = temp["lost"].get("size")
        self.unconfirmed_match_lost_material = temp["lost"].get("material")
        self.unconfirmed_match_lost_brand = temp["lost"].get("brand")
        self.unconfirmed_match_lost_name = temp["lost"].get("name")
        self.unconfirmed_match_found_id = temp["found"].get("id")
        self.unconfirmed_match_found_picture_data = (
            "data:image/jpeg;base64,"
            + base64.b64encode(temp["found"]["image"]).decode()
        )
        self.unconfirmed_match_found_category = temp["found"].get("category")
        self.unconfirmed_match_found_it = temp["found"].get("it")
        self.unconfirmed_match_found_desc = temp["found"].get("desc")
        self.unconfirmed_match_found_color = temp["found"].get("color")
        self.unconfirmed_match_found_size = temp["found"].get("size")
        self.unconfirmed_match_found_material = temp["found"].get("material")
        self.unconfirmed_match_found_brand = temp["found"].get("brand")
        self.unconfirmed_match_found_name = temp["found"].get("name")
        self.unconfirmed_match_score = temp["percentage"]

    confirm_match_response: str = ""

    def call_confirm_match(self):
        temp = confirm_match(self.unconfirmed_match_id)
        if temp:
            self.confirm_match_response = "Match confirmed successfully"
        else:
            self.confirm_match_response = "Match confirm failed"
        self.load_unconfirmed_matches()

    # ======================Get confirmed matches=============================
    confirmed_matches_with_owner_info: list[dict] = []

    def load_confirmed_matches_with_owner_info(self):
        self.confirmed_matches_with_owner_info = get_confirmed_matches_with_owner_info(
            self.email
        )

    hand_over_and_archive_match_response: str = ""
    claimer_pesel: str = ""

    def call_hand_over_and_archive_match(self, mid):
        temp = hand_over_and_archive_match(mid, self.claimer_pesel, False)
        if temp:
            self.hand_over_and_archive_match_response = "Handed Over successfully"
        else:
            self.hand_over_and_archive_match_response = (
                "Hand Over failed and/or Invalid PESEL"
            )
        self.load_confirmed_matches_with_owner_info()

    @rx.event
    def call_hand_over_and_archive_match_print_receipt(self, mid):
        temp = hand_over_and_archive_match(mid, self.claimer_pesel, True)
        if temp:
            self.hand_over_and_archive_match_response = (
                "Handed Over successfully. Printing receipt..."
            )
            return rx.download(data=temp, filename="receipt.pdf")
        else:
            self.hand_over_and_archive_match_response = (
                "Hand Over failed and/or Invalid PESEL"
            )
        self.load_confirmed_matches_with_owner_info()

    # ===================================Write policy===========================================
    new_policy: str = ""

    def call_write_policy(self):
        write_policy(self.new_policy)
        self.load_policy()

    # — Admin‐tab tracking for sidebar —
    admin_tab: str = "write_policy"

    def set_admin_tab(self, tab: str):
        self.admin_tab = tab

    preview_size: str = "md"

    def set_preview_size(self, size: str):
        self.preview_size = size

    # ===================================Stats===============================================
    stats: dict = ""

    def load_stats(self):
        self.stats = get_stats()

    # ===================================Settings===============================================
    settings_tab: str = "profile"

    def set_settings_tab(self, tab: str):
        self.settings_tab = tab

    # =====================================False pickup reports=================================
    false_pickup_reports: list[dict] = []

    def load_false_pickup_reports(self):
        self.false_pickup_reports = get_false_pickup_reports()

    # =====================================Manage accounts===================================
    role: str = ""
    manage_account_response: str = ""
    accounts: list[dict] = []

    def call_create_account(self):
        self.manage_account_response = create_account(
            self.email, self.password, self.role, self.firstname, self.surname
        )
        self.email = ""
        self.password = ""
        self.role = ""
        self.firstname = ""
        self.surname = ""

    def load_accounts(self):
        self.accounts = get_accounts()

    def call_delete_account(self, email):
        temp = delete_account(email)
        if temp:
            self.manage_account_response = "ACCOUNT DELETED"
        else:
            self.manage_account_response = "ACCOUNT DELETION FAILED"

    email2 = ""
    password2 = ""
    role2 = ""
    firstname2 = ""
    surname2 = ""
    def call_create_account2(self):
        self.manage_account_response = create_account(
            self.email2, self.password2, self.role2, self.firstname2, self.surname2
        )

    # =================================================================================


NAV_H = "64px"


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="medium", color="white"),
        on_click=rx.redirect(url),
        _hover={"color": hover_style},
    )


# ----------------------------------
# Navigation bar for Worker
# ----------------------------------
def navbar_worker() -> rx.Component:
    return rx.box(
        # Desktop
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(src=logo, width="2.25em", border_radius="25%"),
                    rx.heading(app_name, size="7", weight="bold", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                # Main links: Home, Task (dropdown)
                rx.hstack(
                    navbar_link("Home", "/worker-dashboard"),
                    # Task dropdown
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.text(
                                "Task",
                                size="4",
                                weight="medium",
                                color="white",
                                _hover={"color": "cyan.300"},
                                cursor="pointer",
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item(
                                "Submit Found Item",
                                on_click=rx.redirect("/submit-found"),
                            ),
                            rx.menu.item(
                                "Match Found Items",
                                on_click=rx.redirect("/match-items"),
                            ),
                            rx.menu.item(
                                "Confirm Return",
                                on_click=rx.redirect("/confirm-return"),
                            ),
                        ),
                        placement="bottom-start",
                    ),
                    spacing="8",
                ),
                rx.spacer(),
                # Profile menu
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(
                            rx.icon("user"), size="2", radius="full", color="white"
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            "Settings", on_click=rx.redirect("/setting-worker")
                        ),
                        rx.menu.separator(),
                        rx.menu.item(
                            "Log out", on_click=[State.logout, rx.redirect("/")]
                        ),
                    ),
                    placement="bottom-end",
                ),
                align="center",
                height=NAV_H,
                px="6",
                bg="#1B357A",
            )
        ),
        # Mobile & tablet
        rx.mobile_and_tablet(
            rx.hstack(
                # Logo
                rx.hstack(
                    rx.image(src=logo, width="2em", border_radius="25%"),
                    rx.heading(app_name, size="6", weight="bold", color="white"),
                ),
                rx.spacer(),
                # Hamburger menu
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(rx.icon("menu"), size="2", color="white")
                    ),
                    rx.menu.content(
                        rx.menu.item("Home", on_click=rx.redirect("/worker-dashboard")),
                        rx.menu.item(
                            "Report Found Item", on_click=rx.redirect("/submit-found")
                        ),
                        rx.menu.item(
                            "Unconfirmed Matches", on_click=rx.redirect("/match-items")
                        ),
                        rx.menu.item(
                            "Confirmed Matches", on_click=rx.redirect("/confirm-return")
                        ),
                        rx.menu.separator(),
                        rx.menu.item(
                            "Settings", on_click=rx.redirect("/setting-worker")
                        ),
                        rx.menu.item(
                            "Log out", on_click=[State.logout, rx.redirect("/")]
                        ),
                    ),
                    placement="bottom-end",
                ),
                align="center",
                justify="between",
                height=NAV_H,
                px="4",
                bg="#1B357A",
            )
        ),
        as_="nav",
        position="fixed",
        top="0",
        left="0",
        width="100vw",
        z_index=1000,
    )


# ----------------------------------
# Navigation bar for User
# ----------------------------------
def navbar_user() -> rx.Component:
    return rx.box(
        # Desktop
        rx.desktop_only(
            rx.hstack(
                # Logo + title
                rx.hstack(
                    rx.image(src=logo, width="2.25em", border_radius="25%"),
                    rx.heading(app_name, size="7", weight="bold", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                # User links
                rx.hstack(
                    navbar_link("Home", "/user-dashboard"),
                    navbar_link("Submit Lost", "/submit-lost"),
                    navbar_link("View Reports", "/view-lost"),
                    navbar_link("Policy", "/policy"),
                    spacing="8",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.icon_button(
                                rx.icon("user"), size="2", radius="full", color="white"
                            )
                        ),
                        rx.menu.content(
                            rx.menu.item(
                                "Settings", on_click=rx.redirect("/setting-user")
                            ),
                            rx.menu.separator(),
                            rx.menu.item(
                                "Log out", on_click=[State.logout, rx.redirect("/")]
                            ),
                        ),
                        placement="bottom-end",
                    ),
                    spacing="4",
                ),
                align="center",
                height=NAV_H,
                px="6",
                bg="#1B357A",
            )
        ),
        # Mobile
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(src=logo, width="2em", border_radius="25%"),
                    rx.heading(app_name, size="6", weight="bold", color="white"),
                ),
                rx.spacer(),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(rx.icon("menu"), size="2", color="white")
                    ),
                    rx.menu.content(
                        rx.menu.item("Home", on_click=rx.redirect("/user-dashboard")),
                        rx.menu.item(
                            "Submit Lost", on_click=rx.redirect("/submit-lost")
                        ),
                        rx.menu.item(
                            "View Reports", on_click=rx.redirect("/view-lost")
                        ),
                        rx.menu.item("Policy", on_click=rx.redirect("/policy")),
                        rx.menu.separator(),
                        rx.menu.item("Settings", on_click=rx.redirect("/setting-user")),
                        rx.menu.item(
                            "Log out", on_click=[State.logout, rx.redirect("/")]
                        ),
                    ),
                    placement="bottom-end",
                ),
                align="center",
                justify="between",
                height=NAV_H,
                px="4",
                bg="#1B357A",
            )
        ),
        as_="nav",
        position="fixed",
        top="0",
        left="0",
        width="100vw",
        z_index=1000,
        height=NAV_H,
        mb=NAV_H,
    )


# ----------------------------------
# Admin Sidebar Helpers
# ----------------------------------


def sidebar_item(text: str, icon_name: str, on_click) -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.icon(icon_name, box_size=5),
            rx.text(text, size="5"),
            spacing="3",
            align="center",
            justify="start",
            width="100%",
        ),
        variant="ghost",
        justify="start",
        px="4",
        on_click=on_click,
        width="100%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item(
            "Write Policy",
            "pencil",
            State.set_admin_tab("write_policy"),
        ),
        sidebar_item(
            "Statistics",
            "bar-chart-4",
            State.set_admin_tab("statistics"),
        ),
        sidebar_item(
            "False Pickups",
            "circle-help",
            State.set_admin_tab("false_pickups"),
        ),
        sidebar_item(
            "Manage Accounts",
            "users",
            State.set_admin_tab("manage_accounts"),
        ),
        spacing="2",
        width="100%",
    )


def sidebar_top_profile() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.icon_button(
                        rx.icon("user"), size="3", radius="full", color_scheme="gray"
                    ),
                    rx.vstack(
                        rx.text("Admin", size="3", weight="bold"),
                        rx.text(State.email, size="2", weight="medium"),
                        spacing="0",
                        width="100%",
                    ),
                    rx.spacer(),
                    padding_x="0.5rem",
                    align="center",
                    width="100%",
                ),
                rx.divider(mb="4"),
                sidebar_items(),
                rx.spacer(),
                # ─── logout button ─────────────────────────
                rx.button(
                    rx.hstack(
                        rx.icon("log-out", box_size=5),
                        rx.text("Log out", size="5"),
                        spacing="3",
                        align="start",
                        justify="start",
                    ),
                    variant="ghost",
                    px="4",
                    width="100%",
                    on_click=[State.logout, rx.redirect("/")],
                ),
                spacing="5",
                padding_x="1em",
                padding_y="1.5em",
                bg=bg_style["background"],
                align="start",
                height="100vh",
                width="16em",
            )
        )
    )


# ----------------------------------
# Admin Dashboard
# ----------------------------------
def AdminDashboard() -> rx.Component:
    return rx.flex(
        # Sidebar
        sidebar_top_profile(),
        # Main content area
        rx.box(
            rx.vstack(
                # Page title (changes with tab)
                rx.cond(
                    State.admin_tab == "write_policy",
                    rx.heading("Write Policy", size="8", weight="bold", mb="6"),
                    rx.cond(
                        State.admin_tab == "statistics",
                        rx.heading("Statistics", size="8", weight="bold", mb="6"),
                        rx.cond(
                            State.admin_tab == "false_pickups",
                            rx.heading(
                                "False Pickup Reports", size="8", weight="bold", mb="6"
                            ),
                            rx.heading(
                                "Manage Accounts", size="8", weight="bold", mb="6"
                            ),
                        ),
                    ),
                ),
                # write_policy pane
                rx.cond(
                    State.admin_tab == "write_policy",
                    rx.vstack(
                        # 2) Editor & live‐preview side by side
                        rx.hstack(
                            # a) Markdown editor
                            rx.vstack(
                                rx.text(
                                    "You can use Markdown (`# Heading`, `- bullet`):",
                                    color="gray.300",
                                    font_size="sm",
                                ),
                                rx.text_area(
                                    placeholder="Type policy here…",
                                    value=State.new_policy,
                                    on_change=State.set_new_policy,
                                    width="500px",
                                    height="500px",
                                ),
                                rx.button(
                                    "Apply",
                                    on_click=State.call_write_policy,
                                    color_scheme=button_style_1,
                                    width="100%",
                                    mt="2",
                                ),
                                spacing="3",
                            ),
                            # b) Live preview box
                            rx.vstack(
                                rx.text("Preview", weight="medium", mb="2"),
                                rx.box(
                                    rx.markdown(State.new_policy),
                                    p="4",
                                    border="1px solid",
                                    border_color="gray.400",
                                    border_radius="md",
                                    width="500px",
                                    height="500px",
                                    overflow_y="auto",
                                ),
                            ),
                            spacing="8",
                        ),
                        spacing="4",
                    ),
                    # statistics pane
                    rx.cond(
                        State.admin_tab == "statistics",
                        rx.vstack(
                            rx.button(
                                "Refresh",
                                on_click=State.load_stats,
                                color_scheme=button_style_2,
                                align_self="flex-end",
                            ),
                            rx.foreach(
                                State.stats.items(),
                                lambda stat: rx.hstack(
                                    rx.text(stat[0], weight="medium", width="100%"),
                                    rx.text(stat[1]),
                                ),
                            ),
                        ),
                        # false_pickups pane
                        rx.cond(
                            State.admin_tab == "false_pickups",
                            rx.vstack(
                                rx.button(
                                    "Refresh",
                                    on_click=State.load_false_pickup_reports,
                                    color_scheme=button_style_2,
                                    align_self="flex-end",
                                ),
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("ID"),
                                            rx.table.column_header_cell("Owner"),
                                            rx.table.column_header_cell("Owner Email"),
                                            rx.table.column_header_cell("Picked Up By"),
                                            rx.table.column_header_cell(
                                                "Picked Up Email"
                                            ),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            State.false_pickup_reports,
                                            lambda r: rx.table.row(
                                                rx.table.cell(r["id"]),
                                                rx.table.cell(r["owner_fullname"]),
                                                rx.table.cell(r["owner_email"]),
                                                rx.table.cell(r["pickedupby_fullname"]),
                                                rx.table.cell(r["pickedupby_email"]),
                                            ),
                                        )
                                    ),
                                    variant="surface",
                                    width="100%",
                                ),
                            ),
                            # manage_accounts pane
                            rx.vstack(
                                rx.button(
                                    "Refresh",
                                    on_click=State.load_accounts,
                                    color_scheme=button_style_2,
                                    align_self="flex-end",
                                ),
                                rx.divider(my="4"),
                                # registration form
                                rx.hstack(
                                    rx.input(
                                        placeholder="Email", on_change=State.set_email2
                                    ),
                                    rx.input(
                                        placeholder="Password",
                                        on_change=State.set_password2,
                                    ),
                                    rx.select(
                                        items=["USER", "WORKER", "ADMIN"],
                                        value=State.role2,
                                        on_change=State.set_role2,
                                        placeholder="Role",
                                    ),
                                    rx.input(
                                        placeholder="First Name",
                                        on_change=State.set_firstname2,
                                    ),
                                    rx.input(
                                        placeholder="Surname",
                                        on_change=State.set_surname2,
                                    ),
                                    spacing="3",
                                    wrap="wrap",
                                ),
                                rx.button(
                                    "Register",
                                    on_click=State.call_create_account2,
                                    color_scheme=button_style_1,
                                    mt="2",
                                ),
                                rx.text(
                                    State.manage_account_response,
                                    color="green.300",
                                    mt="2",
                                ),
                                rx.divider(my="4"),
                                # accounts table
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("Email"),
                                            rx.table.column_header_cell("Role"),
                                            rx.table.column_header_cell("First Name"),
                                            rx.table.column_header_cell("Surname"),
                                            rx.table.column_header_cell("Action"),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            State.accounts,
                                            lambda a: rx.table.row(
                                                rx.table.cell(a["email"]),
                                                rx.table.cell(a["role"]),
                                                rx.table.cell(a["name"]),
                                                rx.table.cell(a["surname"]),
                                                rx.table.cell(
                                                    rx.button(
                                                        "Delete",
                                                        on_click=[
                                                            State.call_delete_account(
                                                                a["email"]
                                                            )
                                                        ],
                                                        color_scheme="red",
                                                    )
                                                ),
                                            ),
                                        )
                                    ),
                                    variant="surface",
                                    width="100%",
                                ),
                            ),
                        ),
                    ),
                ),
                spacing="6",
                width="100%",
            ),
            padding="50px",
            flex=1,
            overflow_y="auto",
        ),
        direction="row",
        width="100vw",
        height="100vh",
        bg=bg_style["background"],
        on_mount=State.redirect_if_bad_auth(required_role="ADMIN"),
    )

# ---------------------
#  Page: Login Page
# ---------------------


def index() -> rx.Component:
    return rx.center(
        rx.hstack(
            # Branding column
            rx.vstack(
                rx.image(
                    src="/Logovertical.png",
                    alt=app_name,
                    width="15em",
                ),
                rx.text(app_desc, color="white", max_width="15em"),
                align="center",
            ),
            # Auth card column
            rx.card(
                rx.tabs(
                    # Tab headers
                    rx.tabs.list(
                        rx.tabs.trigger("Sign In", value="signin"),
                        rx.tabs.trigger("Sign Up", value="signup"),
                    ),
                    # Sign In content
                    rx.tabs.content(
                        rx.vstack(
                            rx.input(
                                placeholder="Email",
                                on_change=State.set_email,
                                width="100%",
                                mb="2",
                            ),
                            rx.input(
                                placeholder="Password",
                                type_="password",
                                on_change=State.set_password,
                                width="100%",
                                mb="4",
                            ),
                            rx.button(
                                "Login",
                                color_scheme=button_style_1,
                                width="100%",
                                on_click=State.call_login,
                            ),
                            rx.text(State.login_response, color="red", mt="2"),
                            align="stretch",
                        ),
                        value="signin",
                    ),
                    # Sign Up content
                    rx.tabs.content(
                        rx.vstack(
                            rx.input(
                                placeholder="Email",
                                on_change=State.set_email,
                                width="100%",
                                mb="2",
                            ),
                            rx.input(
                                placeholder="Password",
                                type_="password",
                                on_change=State.set_password,
                                width="100%",
                                mb="2",
                            ),
                            rx.input(
                                placeholder="First Name",
                                on_change=State.set_firstname,
                                width="100%",
                                mb="2",
                            ),
                            rx.input(
                                placeholder="Surname",
                                on_change=State.set_surname,
                                width="100%",
                                mb="4",
                            ),
                            rx.button(
                                "Register",
                                color_scheme=button_style_1,
                                width="100%",
                                on_click=State.call_register_user,
                            ),
                            rx.text(State.register_user_response, color="red", mt="2"),
                            align="stretch",
                        ),
                        value="signup",
                    ),
                    default_value="signin",
                    variant="soft-rounded",
                    color_scheme="blue",
                    mb="4",
                ),
                width="400px",
                padding="2rem",
                border_radius="2xl",
                box_shadow="lg",
            ),
            spacing="6",
            align="center",
            justify="center",
        ),
        height="100vh",
        width="100vw",
        style=bg_style,
    )


# ---------------------
#  User Dashboard
# ---------------------


def UserDashboard() -> rx.Component:
    return rx.flex(
        # 1) Navbar
        navbar_user(),
        # 2) Main area
        rx.flex(
            # ─ Left panel ─
            rx.box(
                rx.vstack(
                    rx.heading(
                        f"Welcome, {State.name}!",
                        color="white",
                        font_size="4xl",
                        mb="2",
                    ),
                    rx.text(
                        "Start by submitting a new lost item or checking your notifications.",
                        color="gray.300",
                        font_size="lg",
                        mb="6",
                    ),
                    rx.button(
                        "Submit Lost Item",
                        on_click=lambda: rx.redirect("/submit-lost"),
                        color_scheme=button_style_1,
                        _hover={"bg": "purple"},
                        width="50%",
                        font_weight="bold",
                    ),
                    rx.button(
                        "View Lost Report",
                        on_click=lambda: rx.redirect("/view-lost"),
                        color_scheme=button_style_1,
                        _hover={"bg": "purple"},
                        width="50%",
                        font_weight="bold",
                    ),
                    spacing="6",
                    align_items="center",
                    text_align="center",
                    width="100%",
                ),
                width="60%",
                padding_x="6",
            ),
            # ─ Right illustration ─
            rx.image(
                src="/navigateuser.png",
                alt="Lost Item Illustration",
                width="40%",
                border_radius="xl",
            ),
            align="center",
            justify="center",
            spacing="2",
            flex="1",
            pt=NAV_H,
            style=bg_style,
            width="100%",
            direction="row",
            wrap="nowrap",
        ),
        # 3) Footer
        footer(),
        direction="column",
        width="100vw",
        height="100vh",

        on_mount=State.redirect_if_bad_auth(required_role="USER"),
    )


# ----------------------------------
#  Page: User Submit Lost Item Page
# ----------------------------------
def SubmitLostItemPage() -> rx.Component:
    return rx.flex(
        # 1) Navbar
        navbar_user(),
        # 2) Scrollable form region
        rx.box(
            rx.center(
                rx.card(
                    rx.vstack(
                        # Header
                        rx.hstack(
                            rx.badge(
                                rx.icon(tag="clipboard-list", size=32),
                                color_scheme=button_style_2,
                                radius="full",
                                padding="0.5rem",
                            ),
                            rx.heading("Lost Item Form", size="4", weight="bold"),
                            spacing="2",
                            align_items="center",
                        ),
                        # The form
                        rx.form.root(
                            rx.vstack(
                                # 1) Image upload
                                rx.form.field(
                                    rx.form.label("Image"),
                                    rx.upload(
                                        rx.button(
                                            "Select Image (JPG/JPEG)",
                                            color_scheme=button_style_2,
                                        ),
                                        rx.text(rx.selected_files("upload1")),
                                        id="upload1",
                                        accept={"image/jpeg": [".jpg", ".jpeg"]},
                                        multiple=False,
                                    ),
                                    name="image",
                                ),
                                # upload / clear
                                rx.hstack(
                                    rx.button(
                                        "Upload",
                                        color_scheme=button_style_2,
                                        on_click=State.handle_upload(
                                            rx.upload_files(upload_id="upload1")
                                        ),
                                    ),
                                    rx.button(
                                        "Clear",
                                        color_scheme=button_style_2,
                                        variant="outline",
                                        on_click=rx.clear_selected_files("upload1"),
                                    ),
                                    spacing="3",
                                ),
                                # 2) Category
                                rx.form.field(
                                    rx.form.label("Category"),
                                    rx.select(
                                        items=categories,
                                        value=State.category,
                                        on_change=State.set_category,
                                        placeholder="Choose…",
                                    ),
                                    name="category",
                                ),
                                # 3) Type per category
                                rx.cond(
                                    State.category == "Personal Items",
                                    rx.form.field(
                                        rx.form.label("Type of Personal Item"),
                                        rx.select(
                                            items=personal_item_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_personal",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Jewelry",
                                    rx.form.field(
                                        rx.form.label("Type of Jewelry"),
                                        rx.select(
                                            items=jewelry_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_jewelry",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Accessories",
                                    rx.form.field(
                                        rx.form.label("Type of Accessory"),
                                        rx.select(
                                            items=accessory_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_accessory",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Travel Items",
                                    rx.form.field(
                                        rx.form.label("Type of Travel Item"),
                                        rx.select(
                                            items=travel_item_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_travel",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Electronic Devices",
                                    rx.form.field(
                                        rx.form.label("Type of Electronic Device"),
                                        rx.select(
                                            items=electronic_device_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_electronic",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Clothing",
                                    rx.form.field(
                                        rx.form.label("Type of Clothing"),
                                        rx.select(
                                            items=clothing_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_clothing",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Office Items",
                                    rx.form.field(
                                        rx.form.label("Type of Office Item"),
                                        rx.select(
                                            items=office_item_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_office",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Other Items",
                                    rx.form.field(
                                        rx.form.label("Type of Other Item"),
                                        rx.input(
                                            placeholder="Type of Other Item",
                                            on_change=State.set_it,
                                        ),
                                        name="type_other",
                                    ),
                                ),
                                # 4) Size
                                rx.cond(
                                    (State.category == "Jewelry")
                                    | (State.category == "Travel Items")
                                    | (State.category == "Clothing")
                                    | (State.category == "Office Items")
                                    | (State.category == "Other Items"),
                                    rx.form.field(
                                        rx.form.label("Size"),
                                        rx.select(
                                            items=sizes,
                                            value=State.size,
                                            on_change=State.set_size,
                                            placeholder="Choose…",
                                        ),
                                        name="size",
                                    ),
                                ),
                                # 5) Material
                                rx.cond(
                                    (State.category == "Accessories")
                                    | (State.category == "Travel Items")
                                    | (State.category == "Electronic Devices")
                                    | (State.category == "Clothing")
                                    | (State.category == "Office Items")
                                    | (State.category == "Other Items"),
                                    rx.form.field(
                                        rx.form.label("Material"),
                                        rx.select(
                                            items=materials,
                                            value=State.material,
                                            on_change=State.set_material,
                                            placeholder="Choose…",
                                        ),
                                        name="material",
                                    ),
                                ),
                                # 6) Brand
                                rx.cond(
                                    (State.category == "Accessories")
                                    | (State.category == "Travel Items")
                                    | (State.category == "Electronic Devices")
                                    | (State.category == "Clothing")
                                    | (State.category == "Office Items")
                                    | (State.category == "Other Items"),
                                    rx.form.field(
                                        rx.form.label("Brand"),
                                        rx.input(
                                            placeholder="Brand",
                                            on_change=State.set_brand,
                                        ),
                                        name="brand",
                                    ),
                                ),
                                # 7) Name (Other Items)
                                rx.cond(
                                    State.category == "Other Items",
                                    rx.form.field(
                                        rx.form.label("Name"),
                                        rx.input(
                                            placeholder="Name",
                                            on_change=State.set_name,
                                        ),
                                        name="name",
                                    ),
                                ),
                                # 8) Color
                                rx.form.field(
                                    rx.form.label("Color"),
                                    rx.select(
                                        items=colors,
                                        value=State.color,
                                        on_change=State.set_color,
                                        placeholder="Choose…",
                                    ),
                                    name="color",
                                ),
                                # 9) Description
                                rx.form.field(
                                    rx.form.label("Description"),
                                    rx.form.control(
                                        rx.input(
                                            placeholder="Optional description…",
                                            on_change=State.set_desc,
                                        ),
                                        as_child=True,
                                    ),
                                    name="desc",
                                ),
                                # 10) Submit
                                rx.form.submit(
                                    rx.button(
                                        "SUBMIT",
                                        color_scheme=button_style_1,
                                        width="100%",
                                        font_weight="bold",
                                        on_click=State.call_submit_item()
                                    ),
                                    as_child=True,
                                ),
                                rx.text(State.submit_item_response),
                                spacing="4",
                            ),
                            # on_submit=lambda data: [
                            #     State.call_submit_item(),
                            #     rx.clear_selected_files("upload1"),
                            # ],
                            reset_on_submit=False,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    size="3",
                ),
            ),
            flex=1,
            min_height=0,
            overflow_y="auto",
            padding="100px",
            px="4",
            style=bg_style,
        ),
        footer(),
        direction="column",
        height="100vh",
        width="100vw",

        on_mount=State.redirect_if_bad_auth(required_role="USER"),
    )


# ----------------------------------
# Page: User View Lost Reported Items
# ----------------------------------


def ViewLostReportPage() -> rx.Component:
    return rx.flex(
        # 1) Navbar
        navbar_user(),
        rx.box(height=NAV_H),
        # 2) Main scrollable area
        rx.box(
            rx.center(
                rx.box(
                    rx.vstack(
                        # Title + Refresh
                        rx.heading("Your reported lost items", size="4", color="white"),
                        rx.button(
                            "REFRESH",
                            on_click=State.load_submitted_lost_items,
                            color_scheme=button_style_1,
                        ),
                        # Table of reports
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("ID"),
                                    rx.table.column_header_cell("Category"),
                                    rx.table.column_header_cell("Status"),
                                    rx.table.column_header_cell("Expires"),
                                )
                            ),
                            rx.table.body(
                                rx.foreach(
                                    State.submitted_lost_items,
                                    lambda item: rx.table.row(
                                        rx.table.cell(item["id"]),
                                        rx.table.cell(item["category"]),
                                        rx.table.cell(item["status"]),
                                        rx.table.cell(item['expires']),
                                        # Actions: DETAIL / EDIT / DELETE / (maybe) REPORT FALSE
                                        rx.table.cell(
                                            rx.hstack(
                                                # DETAIL popover unchanged
                                                rx.popover.root(
                                                    rx.popover.trigger(
                                                        rx.button("DETAIL", size="2")
                                                    ),
                                                    rx.popover.content(
                                                        rx.card(
                                                            rx.vstack(
                                                                rx.text(
                                                                    "Details",
                                                                    weight="bold",
                                                                    size="2",
                                                                    mb="2",
                                                                ),
                                                                rx.text(
                                                                    f"Category: {item['category']}",
                                                                    mb="2",
                                                                ),
                                                                # PERSONAL ITEMS → show type, color, desc
                                                                rx.cond(
                                                                    item['category']
                                                                    == "Personal Items",
                                                                    rx.vstack(
                                                                        rx.text(
                                                                            f"Type: {item['it']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Color: {item['color']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Description: {item['desc']}"
                                                                        )
                                                                    ),
                                                                ),
                                                                # JEWELRY → show type, size, color, desc
                                                                rx.cond(
                                                                    item['category']
                                                                    == "Jewelry",
                                                                    rx.vstack(
                                                                        rx.text(
                                                                            f"Type: {item['it']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Size: {item['size']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Color: {item['color']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Description: {item['desc']}"
                                                                        ),
                                                                    ),
                                                                ),
                                                                # ACCESSORIES → show type, material, brand, color, desc
                                                                rx.cond(
                                                                    item['category']
                                                                    == "Accessories",
                                                                    rx.vstack(
                                                                        rx.text(
                                                                            f"Type: {item['it']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Material: {item['material']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Brand: {item['brand']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Color: {item['color']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Description: {item['desc']}"
                                                                        ),
                                                                    ),
                                                                ),
                                                                # TRAVEL ITEMS → type, size, material, color, desc, brand
                                                                rx.cond(
                                                                    item['category']
                                                                    == "Travel Items",
                                                                    rx.vstack(
                                                                        rx.text(
                                                                            f"Type: {item['it']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Size: {item['size']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Material: {item['material']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Color: {item['color']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Brand: {item['brand']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Description: {item['desc']}"
                                                                        ),
                                                                    ),
                                                                ),
                                                                # ELECTRONIC → type, material, brand, color, desc
                                                                rx.cond(
                                                                    item['category']
                                                                    == "Electronic Devices",
                                                                    rx.vstack(
                                                                        rx.text(
                                                                            f"Type: {item['it']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Material: {item['material']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Brand: {item['brand']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Color: {item['color']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Description: {item['desc']}"
                                                                        ),
                                                                    ),
                                                                ),
                                                                # CLOTHING → type, size, material, color, desc, brand
                                                                rx.cond(
                                                                    item['category']
                                                                    == "Clothing",
                                                                    rx.vstack(
                                                                        rx.text(
                                                                            f"Type: {item['it']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Size: {item['size']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Material: {item['material']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Color: {item['color']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Brand: {item['brand']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Description: {item['desc']}"
                                                                        ),
                                                                    ),
                                                                ),
                                                                # OFFICE ITEMS → type, material, color, desc, size, name
                                                                rx.cond(
                                                                    item['category']
                                                                    == "Office Items",
                                                                    rx.vstack(
                                                                        rx.text(
                                                                            f"Type: {item['it']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Material: {item['material']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Color: {item['color']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Size: {item['size']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Name: {item['name']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Description: {item['desc']}"
                                                                        ),
                                                                    ),
                                                                ),
                                                                # OTHER ITEMS → name, color, desc
                                                                rx.cond(
                                                                    item['category']
                                                                    == "Other Items",
                                                                    rx.vstack(
                                                                        rx.text(
                                                                            f"Type: {item['type']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Color: {item['color']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Size: {item['size']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Material: {item['material']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Brand: {item['brand']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Name: {item['Name']}"
                                                                        ),
                                                                        rx.text(
                                                                            f"Description: {item['desc']}"
                                                                        )
                                                                    ),
                                                                ),
                                                            ),
                                                            p="4",
                                                            border_radius="md",
                                                            shadow="lg",
                                                            # ensure it sits on top:
                                                            style={"zIndex": 2000},
                                                        )
                                                    ),
                                                    use_portal=True,
                                                    placement="right-start",
                                                ),
                                                # EDIT → show inline form
                                                rx.button(
                                                    "EDIT",
                                                    size="2",
                                                    color_scheme="blue",
                                                    on_click=State.start_edit(item["id"]),
                                                ),
                                                # RENEW → show inline form
                                                rx.cond(
                                                    item['status'] != "Under false pickup review",
                                                    rx.button(
                                                        "RENEW",
                                                        size="2",
                                                        color_scheme="blue",
                                                        on_click=State.renew_item(item["id"]),
                                                    ),
                                                ),
                                                # DELETE
                                                rx.button(
                                                    "DELETE",
                                                    size="2",
                                                    color_scheme="red",
                                                    on_click=[
                                                        State.call_delete_lost_item(
                                                            item["id"]
                                                        )
                                                    ],
                                                ),
                                                # REPORT FALSE PICKUP if applicable
                                                rx.cond(
                                                    item['status'] == "Picked up",
                                                    rx.button(
                                                        "REPORT FALSE PICKUP",
                                                        size="2",
                                                        color_scheme="orange",
                                                        on_click=[
                                                            State.call_report_false_pickup(
                                                                item["id"]
                                                            )
                                                        ],
                                                    ),
                                                ),
                                                spacing="2",
                                            )
                                        ),
                                    ),
                                )
                            ),
                            width="100%",
                        ),
                        # DELETE-response
                        rx.text(State.delete_lost_item_response, color="red"),
                        # ——— Inline edit form  ———
                        rx.cond(
                            State.is_editing,
                            rx.box(
                                rx.card(
                                    rx.vstack(
                                        rx.heading("Edit Lost Item", size="4", mb="4"),
                                        rx.form.root(
                                            rx.vstack(
                                                # 1) Image upload
                                                rx.form.field(
                                                    rx.form.label("Image"),
                                                    rx.upload(
                                                        rx.button(
                                                            "Select Image (JPG/JPEG)"
                                                        ),
                                                        rx.text(
                                                            rx.selected_files("upload2")
                                                        ),
                                                        id="upload2",
                                                        accept={
                                                            "image/jpeg": [
                                                                ".jpg",
                                                                ".jpeg",
                                                            ]
                                                        },
                                                        multiple=False,
                                                    ),
                                                    name="image",
                                                ),
                                                rx.hstack(
                                                    rx.button(
                                                        "Upload",
                                                        on_click=State.handle_update_upload(
                                                            rx.upload_files(
                                                                upload_id="upload2"
                                                            )
                                                        ),
                                                    ),
                                                    rx.button(
                                                        "Clear",
                                                        on_click=rx.clear_selected_files(
                                                            "upload2"
                                                        ),
                                                    ),
                                                    spacing="2",
                                                ),
                                                # 2) Category
                                                rx.form.field(
                                                    rx.form.label("Category"),
                                                    rx.select(
                                                        items=categories,
                                                        value=State.update_category,
                                                        on_change=State.set_update_category,
                                                    ),
                                                    # name="category",
                                                ),
                                                # 3) Type / Name (per‐category)
                                                rx.cond(
                                                    State.update_category
                                                    == "Personal Items",
                                                    rx.form.field(
                                                        rx.form.label("Type"),
                                                        rx.select(
                                                            items=personal_item_types,
                                                            value=State.update_it,
                                                            on_change=State.set_update_it,
                                                        ),
                                                        name="it",
                                                    ),
                                                ),
                                                rx.cond(
                                                    State.update_category == "Jewelry",
                                                    rx.form.field(
                                                        rx.form.label("Type"),
                                                        rx.select(
                                                            items=jewelry_types,
                                                            value=State.update_it,
                                                            on_change=State.set_update_it,
                                                        ),
                                                        name="it",
                                                    ),
                                                ),
                                                rx.cond(
                                                    State.update_category
                                                    == "Accessories",
                                                    rx.form.field(
                                                        rx.form.label("Type"),
                                                        rx.select(
                                                            items=accessory_types,
                                                            value=State.update_it,
                                                            on_change=State.set_update_it,
                                                        ),
                                                        name="it",
                                                    ),
                                                ),
                                                rx.cond(
                                                    State.update_category
                                                    == "Travel Items",
                                                    rx.form.field(
                                                        rx.form.label("Type"),
                                                        rx.select(
                                                            items=travel_item_types,
                                                            value=State.update_it,
                                                            on_change=State.set_update_it,
                                                        ),
                                                        name="it",
                                                    ),
                                                ),
                                                rx.cond(
                                                    State.update_category
                                                    == "Electronic Devices",
                                                    rx.form.field(
                                                        rx.form.label("Type"),
                                                        rx.select(
                                                            items=electronic_device_types,
                                                            value=State.update_it,
                                                            on_change=State.set_update_it,
                                                        ),
                                                        name="it",
                                                    ),
                                                ),
                                                rx.cond(
                                                    State.update_category == "Clothing",
                                                    rx.form.field(
                                                        rx.form.label("Type"),
                                                        rx.select(
                                                            items=clothing_types,
                                                            value=State.update_it,
                                                            on_change=State.set_update_it,
                                                        ),
                                                        name="it",
                                                    ),
                                                ),
                                                rx.cond(
                                                    State.update_category
                                                    == "Office Items",
                                                    rx.form.field(
                                                        rx.form.label("Type"),
                                                        rx.select(
                                                            items=office_item_types,
                                                            value=State.update_it,
                                                            on_change=State.set_update_it,
                                                        ),
                                                        name="it",
                                                    ),
                                                ),
                                                rx.cond(
                                                    State.update_category
                                                    == "Other Items",
                                                    rx.form.field(
                                                        rx.form.label("Name"),
                                                        rx.input(
                                                            placeholder="Other item name",
                                                            on_change=State.set_update_name,
                                                        ),
                                                        name="name",
                                                    ),
                                                ),
                                                # 4) Size
                                                rx.cond(
                                                    (State.update_category == "Jewelry")
                                                    | (
                                                        State.update_category
                                                        == "Travel Items"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Clothing"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Office Items"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Other Items"
                                                    ),
                                                    rx.form.field(
                                                        rx.form.label("Size"),
                                                        rx.select(
                                                            items=sizes,
                                                            value=State.update_size,
                                                            on_change=State.set_update_size,
                                                        ),
                                                        name="size",
                                                    ),
                                                ),
                                                # 5) Material
                                                rx.cond(
                                                    (
                                                        State.update_category
                                                        == "Accessories"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Travel Items"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Electronic Devices"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Clothing"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Office Items"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Other Items"
                                                    ),
                                                    rx.form.field(
                                                        rx.form.label("Material"),
                                                        rx.select(
                                                            items=materials,
                                                            value=State.update_material,
                                                            on_change=State.set_update_material,
                                                        ),
                                                        name="material",
                                                    ),
                                                ),
                                                # 6) Brand
                                                rx.cond(
                                                    (
                                                        State.update_category
                                                        == "Accessories"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Travel Items"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Electronic Devices"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Clothing"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Office Items"
                                                    )
                                                    | (
                                                        State.update_category
                                                        == "Other Items"
                                                    ),
                                                    rx.form.field(
                                                        rx.form.label("Brand"),
                                                        rx.input(
                                                            placeholder="Brand",
                                                            on_change=State.set_update_brand,
                                                        ),
                                                        name="brand",
                                                    ),
                                                ),
                                                # 7) Color
                                                rx.form.field(
                                                    rx.form.label("Color"),
                                                    rx.select(
                                                        items=colors,
                                                        value=State.update_color,
                                                        on_change=State.set_update_color,
                                                    ),
                                                    name="color",
                                                ),
                                                # 8) Description
                                                rx.form.field(
                                                    rx.form.label("Description"),
                                                    rx.input(
                                                        value=State.update_desc,
                                                        placeholder=State.update_desc,
                                                        on_change=State.set_update_desc,
                                                    ),
                                                    name="desc",
                                                ),
                                                # Any response message
                                                rx.text(
                                                    State.update_lost_item_response,
                                                    color="red",
                                                ),
                                                # Submit & Cancel buttons
                                                rx.hstack(
                                                    rx.button(
                                                        "SUBMIT",
                                                        color_scheme="green",
                                                        on_click=[
                                                            State.call_update_lost_item(
                                                                State.editing_iid
                                                            ),
                                                            State.cancel_edit(),
                                                        ],
                                                    ),
                                                    rx.button(
                                                        "CANCEL",
                                                        variant="outline",
                                                        on_click=State.cancel_edit,
                                                    ),
                                                    spacing="4",
                                                ),
                                                spacing="4",
                                            ),
                                            reset_on_submit=False,
                                        ),
                                    ),
                                    mt="6",
                                    width="100%",
                                )
                            ),
                        ),
                        spacing="8",
                        width="100%",
                    ),
                    width="100%",
                    max_w="700px",
                    padding="50px",
                    bg="#1a202c",
                    border_radius=9,
                )
            ),
            flex=1,
            min_height=0,
            overflow="auto",
            width="100vw",
            style=bg_style,
        ),
        # 3) Footer
        footer(),
        direction="column",
        height="100vh",
        width="100vw",
        justify="between",

        on_mount=State.redirect_if_bad_auth(required_role="USER"),
    )


# ----------------------------------
# The Worker dashboard page
# ----------------------------------
def WorkerDashBoard() -> rx.Component:
    return rx.flex(
        # 1) Navbar
        navbar_worker(),
        # 2) Main area (fills the rest of the screen)
        rx.flex(
            # Left action panel
            rx.box(
                rx.vstack(
                    rx.heading("Ready for work today?", font_size="4xl", color="white"),
                    rx.text("Select a task:", color="gray.200"),
                    rx.button(
                        "Submit Found Item",
                        on_click=rx.redirect("/submit-found"),
                        color_scheme=button_style_1,
                        color="white",
                        _hover={"bg": "purple"},
                        width="100%",
                        font_weight="bold",
                    ),
                    rx.button(
                        "Match Found Items",
                        on_click=rx.redirect("/match-items"),
                        color_scheme=button_style_1,
                        color="white",
                        _hover={"bg": "purple"},
                        width="100%",
                        font_weight="bold",
                    ),
                    rx.button(
                        "Confirm Return",
                        on_click=rx.redirect("/confirm-return"),
                        color_scheme=button_style_1,
                        color="white",
                        _hover={"bg": "purple"},
                        width="100%",
                        font_weight="bold",
                    ),
                    spacing="4",
                ),
                style={
                    "background": "rgba(255,255,255,0.05)",
                    "borderRadius": "1rem",
                    "padding": "2rem",
                    "boxShadow": "0 6px 20px rgba(0,0,0,0.3)",
                },
                max_width="20em",
                flex="0 0 auto",
            ),
            # Right illustration
            rx.image(
                src="/navworker.png",
                alt="Worker Illustration",
                max_width="460px",
                width="100%",
                object_fit="contain",
            ),
            wrap="wrap",
            align="center",
            justify="center",
            spacing="8",
            flex="1",
            pt=NAV_H,
            style=bg_style,
            width="100%",
        ),
        footer(),
        direction="column",
        width="100vw",
        height="100vh",

        on_mount=State.redirect_if_bad_auth(required_role="WORKER"),
    )


# ----------------------------------
# Page : The Worker SubmitFoundItem
# ----------------------------------
def SubmitFoundItemPage() -> rx.Component:
    return rx.flex(
        # 1) Navbar
        navbar_worker(),
        rx.box(height=NAV_H),
        # 2) Form  Area
        rx.box(
            rx.center(
                rx.card(
                    rx.vstack(
                        # Header
                        rx.hstack(
                            rx.badge(
                                rx.icon(tag="clipboard-list", size=32),
                                color_scheme=button_style_2,
                                radius="full",
                                padding="0.5rem",
                            ),
                            rx.heading("Report Found Item", size="5", weight="bold"),
                            spacing="2",
                            align_items="center",
                        ),
                        # The form
                        rx.form.root(
                            rx.vstack(
                                # 1) Image upload
                                rx.form.field(
                                    rx.form.label("Image"),
                                    rx.upload(
                                        rx.button(
                                            "Select Image (JPG/JPEG)",
                                            color_scheme=button_style_2,
                                        ),
                                        rx.text(rx.selected_files("upload1")),
                                        id="upload1",
                                        accept={"image/jpeg": [".jpg", ".jpeg"]},
                                        multiple=False
                                    ),
                                    name="image",
                                ),
                                # upload / clear buttons
                                rx.hstack(
                                    rx.button(
                                        "Upload",
                                        color_scheme=button_style_2,
                                        on_click=State.handle_upload(
                                            rx.upload_files(upload_id="upload1")
                                        ),
                                    ),
                                    rx.button(
                                        "Clear",
                                        color_scheme=button_style_2,
                                        variant="outline",
                                        on_click=rx.clear_selected_files("upload1"),
                                    ),
                                    spacing="3",
                                ),
                                # 2) Category
                                rx.form.field(
                                    rx.form.label("Category"),
                                    rx.select(
                                        items=categories,
                                        value=State.category,
                                        on_change=State.set_category,
                                        placeholder="Choose…",
                                    ),
                                    name="category",
                                ),
                                # 3) Type – one cond per category
                                rx.cond(
                                    State.category == "Personal Items",
                                    rx.form.field(
                                        rx.form.label("Type of Personal Item"),
                                        rx.select(
                                            items=personal_item_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_personal",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Jewelry",
                                    rx.form.field(
                                        rx.form.label("Type of Jewelry"),
                                        rx.select(
                                            items=jewelry_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_jewelry",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Accessories",
                                    rx.form.field(
                                        rx.form.label("Type of Accessory"),
                                        rx.select(
                                            items=accessory_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_accessory",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Travel Items",
                                    rx.form.field(
                                        rx.form.label("Type of Travel Item"),
                                        rx.select(
                                            items=travel_item_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_travel",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Electronic Devices",
                                    rx.form.field(
                                        rx.form.label("Type of Electronic Device"),
                                        rx.select(
                                            items=electronic_device_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_electronic",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Clothing",
                                    rx.form.field(
                                        rx.form.label("Type of Clothing"),
                                        rx.select(
                                            items=clothing_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_clothing",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Office Items",
                                    rx.form.field(
                                        rx.form.label("Type of Office Item"),
                                        rx.select(
                                            items=office_item_types,
                                            value=State.it,
                                            on_change=State.set_it,
                                            placeholder="Choose…",
                                        ),
                                        name="type_office",
                                    ),
                                ),
                                rx.cond(
                                    State.category == "Other Items",
                                    rx.form.field(
                                        rx.form.label("Type of Other Item"),
                                        rx.input(
                                            placeholder="Type of Other Item",
                                            on_change=State.set_it,
                                        ),
                                        name="type_other",
                                    ),
                                ),
                                # 4) Size (Jewelry OR Travel OR Clothing OR Office OR Other)
                                rx.cond(
                                    (State.category == "Jewelry")
                                    | (State.category == "Travel Items")
                                    | (State.category == "Clothing")
                                    | (State.category == "Office Items")
                                    | (State.category == "Other Items"),
                                    rx.form.field(
                                        rx.form.label("Size"),
                                        rx.select(
                                            items=sizes,
                                            value=State.size,
                                            on_change=State.set_size,
                                            placeholder="Choose…",
                                        ),
                                        name="size",
                                    ),
                                ),
                                # 5) Material (Accessories OR Travel OR Electronic OR Clothing OR Office OR Other)
                                rx.cond(
                                    (State.category == "Accessories")
                                    | (State.category == "Travel Items")
                                    | (State.category == "Electronic Devices")
                                    | (State.category == "Clothing")
                                    | (State.category == "Office Items")
                                    | (State.category == "Other Items"),
                                    rx.form.field(
                                        rx.form.label("Material"),
                                        rx.select(
                                            items=materials,
                                            value=State.material,
                                            on_change=State.set_material,
                                            placeholder="Choose…",
                                        ),
                                        name="material",
                                    ),
                                ),
                                # 6) Brand (same OR-chain as above)
                                rx.cond(
                                    (State.category == "Accessories")
                                    | (State.category == "Travel Items")
                                    | (State.category == "Electronic Devices")
                                    | (State.category == "Clothing")
                                    | (State.category == "Office Items")
                                    | (State.category == "Other Items"),
                                    rx.form.field(
                                        rx.form.label("Brand"),
                                        rx.input(
                                            placeholder="Brand",
                                            on_change=State.set_brand,
                                        ),
                                        name="brand",
                                    ),
                                ),
                                # 7) Name (Other Items)
                                rx.cond(
                                    State.category == "Other Items",
                                    rx.form.field(
                                        rx.form.label("Name"),
                                        rx.input(
                                            placeholder="Name",
                                            on_change=State.set_name,
                                        ),
                                        name="name",
                                    ),
                                ),
                                # 8) Color
                                rx.form.field(
                                    rx.form.label("Color"),
                                    rx.select(
                                        items=colors,
                                        value=State.color,
                                        on_change=State.set_color,
                                        placeholder="Choose…",
                                    ),
                                    name="color",
                                ),
                                # 9) Description
                                rx.form.field(
                                    rx.form.label("Description"),
                                    rx.form.control(
                                        rx.input(
                                            placeholder="Optional description…",
                                            on_change=State.set_desc,
                                        ),
                                        as_child=True,
                                    ),
                                    name="desc",
                                ),
                                # 10) Final SUBMIT
                                rx.form.submit(
                                    rx.button(
                                        "SUBMIT",
                                        color_scheme=button_style_1,
                                        width="100%",
                                        font_weight="bold",
                                        on_click=State.call_submit_item()
                                    ),
                                    as_child=True,
                                ),
                                spacing="4",
                            ),
                            # on_submit=lambda data: [
                            #     State.call_submit_item(),
                            #     rx.clear_selected_files("upload1"),
                            # ],
                            reset_on_submit=False,
                        ),
                        rx.text(State.submit_item_response, color="green"),
                        spacing="6",
                    ),
                    width="100%",
                    max_width="700px",
                    padding="30px",
                )
            ),
            flex=1,
            overflow="auto",
            style=bg_style,
            width="100%",
        ),
        # 3) Footer at the bottom
        footer(),
        direction="column",
        height="100vh",
        justify="between",
        width="100vw",

        on_mount=State.redirect_if_bad_auth(required_role="WORKER"),
    )


# ----------------------------------
# Match Details
# ----------------------------------
def MatchDetailsModal() -> rx.Component:
    return rx.modal.root(
        rx.modal.content(
            rx.modal.header(
                rx.heading(f"Match {State.unconfirmed_match_id}", size="4")
            ),
            rx.modal.body(
                rx.text(f"Score: {State.unconfirmed_match_score}", mb="4"),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Field"),
                            rx.table.column_header_cell("Lost"),
                            rx.table.column_header_cell("Found"),
                        )
                    ),
                    rx.table.body(
                        *[
                            rx.table.row(
                                rx.table.cell(label),
                                rx.table.cell(value_lost),
                                rx.table.cell(value_found),
                            )
                            for label, value_lost, value_found in [
                                (
                                    "ID",
                                    State.unconfirmed_match_lost_id,
                                    State.unconfirmed_match_found_id,
                                ),
                                (
                                    "Category",
                                    State.unconfirmed_match_lost_category,
                                    State.unconfirmed_match_found_category,
                                ),
                                (
                                    "Type",
                                    State.unconfirmed_match_lost_it,
                                    State.unconfirmed_match_found_it,
                                ),
                                (
                                    "Description",
                                    State.unconfirmed_match_lost_desc,
                                    State.unconfirmed_match_found_desc,
                                ),
                                (
                                    "Color",
                                    State.unconfirmed_match_lost_color,
                                    State.unconfirmed_match_found_color,
                                ),
                                (
                                    "Size",
                                    State.unconfirmed_match_lost_size,
                                    State.unconfirmed_match_found_size,
                                ),
                                (
                                    "Material",
                                    State.unconfirmed_match_lost_material,
                                    State.unconfirmed_match_found_material,
                                ),
                                (
                                    "Brand",
                                    State.unconfirmed_match_lost_brand,
                                    State.unconfirmed_match_found_brand,
                                ),
                                (
                                    "Name",
                                    State.unconfirmed_match_lost_name,
                                    State.unconfirmed_match_found_name,
                                ),
                                # image row
                                (
                                    "Image",
                                    rx.cond(
                                        State.unconfirmed_match_lost_picture_data
                                        == "data:image/jpeg;base64,",
                                        rx.text("No Image"),
                                        rx.image(
                                            src=State.unconfirmed_match_lost_picture_data,
                                            max_width="150px",
                                        ),
                                    ),
                                    rx.cond(
                                        State.unconfirmed_match_found_picture_data
                                        == "data:image/jpeg;base64,",
                                        rx.text("No Image"),
                                        rx.image(
                                            src=State.unconfirmed_match_found_picture_data,
                                            max_width="150px",
                                        ),
                                    ),
                                ),
                            ]
                        ]
                    ),
                    variant="simple"
                ),
            ),
            rx.modal.footer(
                rx.button(
                    "Close",
                    variant="outline",
                    on_click=rx.close_modal("MatchDetailsModal"),
                ),
                rx.button(
                    "Confirm Match",
                    color_scheme=button_style_2,
                    on_click=State.call_confirm_match,
                ),
            ),
        ),
        size="lg",
        close_on_overlay_click=True,

        on_mount=State.redirect_if_bad_auth(required_role="WORKER"),
    )


# ----------------------------------
# Page: MatchItemPage (Unconfirmed Matches)
# ----------------------------------
def MatchItemPage() -> rx.Component:
    return rx.flex(
        # 1) Navbar
        navbar_worker(),
        rx.box(height=NAV_H),
        # 2) Main scrollable area
        rx.box(
            rx.vstack(
                rx.heading("Unconfirmed Matches", size="6", color="white"),
                rx.button(
                    "REFRESH",
                    color_scheme=button_style_1,
                    on_click=State.load_unconfirmed_matches,
                ),
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Match ID"),
                            rx.table.column_header_cell("Synopsis"),
                            rx.table.column_header_cell("Details"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            State.unconfirmed_matches,
                            lambda match: rx.table.row(
                                rx.table.cell(match["match_id"]),
                                rx.table.cell(match["synopsis"]),
                                rx.table.cell(
                                    rx.popover.root(
                                        rx.popover.trigger(
                                            rx.button(
                                                "Details ▶",
                                                size="3",
                                                on_click=[
                                                    State.load_unconfirmed_match(
                                                        match["match_id"]
                                                    )
                                                ],
                                            )
                                        ),
                                        rx.popover.content(
                                            rx.box(
                                                rx.vstack(
                                                    # Header
                                                    rx.hstack(
                                                        rx.text(
                                                            "MATCH ID:",
                                                            font_weight="bold",
                                                        ),
                                                        rx.text(
                                                            State.unconfirmed_match_id
                                                        ),
                                                        mb="4",
                                                    ),
                                                    # Comparison table
                                                    rx.table.root(
                                                        rx.table.header(
                                                            rx.table.row(
                                                                rx.table.column_header_cell(
                                                                    ""
                                                                ),
                                                                rx.table.column_header_cell(
                                                                    "LOST"
                                                                ),
                                                                rx.table.column_header_cell(
                                                                    "FOUND"
                                                                ),
                                                            )
                                                        ),
                                                        rx.table.body(
                                                            # ID row
                                                            rx.table.row(
                                                                rx.table.cell("ID"),
                                                                rx.table.cell(
                                                                    State.unconfirmed_match_lost_id
                                                                ),
                                                                rx.table.cell(
                                                                    State.unconfirmed_match_found_id
                                                                ),
                                                            ),
                                                            # IMAGE
                                                            rx.table.row(
                                                                rx.table.cell("IMAGE"),
                                                                rx.table.cell(
                                                                    rx.cond(
                                                                        State.unconfirmed_match_lost_picture_data
                                                                        == "",
                                                                        rx.text(
                                                                            "No Image"
                                                                        ),
                                                                        rx.image(
                                                                            src=State.unconfirmed_match_lost_picture_data,
                                                                            max_w="100px",
                                                                            object_fit="contain",
                                                                        ),
                                                                    )
                                                                ),
                                                                rx.table.cell(
                                                                    rx.cond(
                                                                        State.unconfirmed_match_found_picture_data
                                                                        == "",
                                                                        rx.text(
                                                                            "No Image"
                                                                        ),
                                                                        rx.image(
                                                                            src=State.unconfirmed_match_found_picture_data,
                                                                            max_w="100px",
                                                                            object_fit="contain",
                                                                        ),
                                                                    )
                                                                ),
                                                            ),
                                                            # PERSONAL ITEMS
                                                            rx.cond(
                                                                State.unconfirmed_match_lost_category
                                                                == "Personal Items",
                                                                rx.vstack(
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Type"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_it
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_it
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Color"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_color
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_color
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Description"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_desc
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_desc
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                            # JEWELRY
                                                            rx.cond(
                                                                State.unconfirmed_match_lost_category
                                                                == "Jewelry",
                                                                rx.vstack(
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Type"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_it
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_it
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Size"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_size
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_size
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Color"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_color
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_color
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Description"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_desc
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_desc
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                            # ACCESSORIES
                                                            rx.cond(
                                                                State.unconfirmed_match_lost_category
                                                                == "Accessories",
                                                                rx.vstack(
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Type"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_it
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_it
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Material"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_material
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_material
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Brand"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_brand
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_brand
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Color"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_color
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_color
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Description"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_desc
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_desc
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                            # TRAVEL ITEMS
                                                            rx.cond(
                                                                State.unconfirmed_match_lost_category
                                                                == "Travel Items",
                                                                rx.vstack(
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Type"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_it
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_it
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Size"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_size
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_size
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Material"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_material
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_material
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Color"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_color
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_color
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Description"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_desc
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_desc
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                            # ELECTRONIC DEVICES
                                                            rx.cond(
                                                                State.unconfirmed_match_lost_category
                                                                == "Electronic Devices",
                                                                rx.vstack(
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Type"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_it
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_it
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Material"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_material
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_material
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Brand"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_brand
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_brand
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Color"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_color
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_color
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Description"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_desc
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_desc
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                            # CLOTHING
                                                            rx.cond(
                                                                State.unconfirmed_match_lost_category
                                                                == "Clothing",
                                                                rx.vstack(
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Type"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_it
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_it
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Size"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_size
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_size
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Material"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_material
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_material
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Color"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_color
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_color
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Description"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_desc
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_desc
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                            # OFFICE ITEMS
                                                            rx.cond(
                                                                State.unconfirmed_match_lost_category
                                                                == "Office Items",
                                                                rx.vstack(
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Type"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_it
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_it
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Material"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_material
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_material
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Color"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_color
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_color
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Description"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_desc
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_desc
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                            # OTHER ITEMS
                                                            rx.cond(
                                                                State.unconfirmed_match_lost_category
                                                                == "Other Items",
                                                                rx.vstack(
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Name"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_name
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_name
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Color"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_color
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_color
                                                                        ),
                                                                    ),
                                                                    rx.table.row(
                                                                        rx.table.cell(
                                                                            "Description"
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_lost_desc
                                                                        ),
                                                                        rx.table.cell(
                                                                            State.unconfirmed_match_found_desc
                                                                        ),
                                                                    ),
                                                                ),
                                                            ),
                                                        ),
                                                        variant="surface",
                                                        # width="100%",
                                                    ),
                                                    # Popover footer
                                                    rx.hstack(
                                                        rx.text(
                                                            "MATCH SCORE:",
                                                            font_weight="bold",
                                                        ),
                                                        rx.text(
                                                            State.unconfirmed_match_score
                                                        ),
                                                        rx.spacer(),
                                                        rx.popover.close(
                                                            rx.button(
                                                                "CONFIRM MATCH",
                                                                color_scheme=button_style_2,
                                                                size="2",
                                                                on_click=State.call_confirm_match,
                                                            ),
                                                        ),
                                                    ),
                                                ),  # end VStack
                                                width="100%",
                                                overflow_y="scroll",
                                                max_height="40vh",
                                            ),  # end scrollable Box
                                        ),  # end popover.content
                                        use_portal=True,
                                        placement="right-start",
                                    )  # end popover.root
                                ),  # end cell
                            ),  # end row
                        ),  # end foreach
                        rx.text(State.confirm_match_response),
                    ),  # end body
                    variant="surface",
                    width="100%",
                    overflow_y="scroll",
                    max_h="200px",
                ),
                spacing="6",
                width="100%",
            ),
            padding="50px",
            flex=1,
            overflow_y="auto",
            bg=bg_style["background"],
        ),
        # 3) Footer
        footer(),
        direction="column",
        height="100vh",
        width="100vw",

        on_mount=State.redirect_if_bad_auth(required_role="WORKER"),
    )


# ----------------------------------
# Page: ConfirmMatchPage (Confirmed Matches)
# ----------------------------------
def ConfirmMatchPage() -> rx.Component:
    return rx.flex(
        # Navbar
        navbar_worker(),
        rx.box(height=NAV_H),
        # Main scrollable area
        rx.box(
            rx.vstack(
                rx.heading("Confirmed Matches", size="6", color="white"),
                rx.button(
                    "REFRESH",
                    color_scheme=button_style_1,
                    on_click=State.load_confirmed_matches_with_owner_info,
                ),
                rx.text(
                    State.hand_over_and_archive_match_response, color="red.300", mb="4"
                ),
                # PESEL input
                rx.hstack(
                    rx.text("Claimer’s PESEL:", font_weight="bold"),
                    rx.input(
                        placeholder="PESEL",
                        on_change=State.set_claimer_pesel,
                        width="200px",
                    ),
                ),
                # Table of confirmed matches
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("ID"),
                            rx.table.column_header_cell("Category"),
                            rx.table.column_header_cell("Type"),
                            rx.table.column_header_cell("Description"),
                            rx.table.column_header_cell("Color"),
                            rx.table.column_header_cell("Size"),
                            rx.table.column_header_cell("Material"),
                            rx.table.column_header_cell("Brand"),
                            rx.table.column_header_cell("Name"),
                            rx.table.column_header_cell("Email"),
                            rx.table.column_header_cell("First Name"),
                            rx.table.column_header_cell("Last Name"),
                            rx.table.column_header_cell("Actions"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            State.confirmed_matches_with_owner_info,
                            lambda item_and_info: rx.table.row(
                                rx.table.cell(item_and_info["id"]),
                                rx.table.cell(item_and_info["category"]),
                                rx.table.cell(item_and_info["it"]),
                                rx.table.cell(item_and_info["desc"]),
                                rx.table.cell(item_and_info["color"]),
                                rx.table.cell(item_and_info["size"]),
                                rx.table.cell(item_and_info["material"]),
                                rx.table.cell(item_and_info["brand"]),
                                rx.table.cell(item_and_info["name"]),
                                rx.table.cell(item_and_info["email"]),
                                rx.table.cell(item_and_info["firstname"]),
                                rx.table.cell(item_and_info["surname"]),
                                rx.table.cell(
                                    rx.hstack(
                                        rx.button(
                                            "HAND OVER",
                                            size="2",
                                            color_scheme="green",
                                            on_click=[
                                                State.call_hand_over_and_archive_match(
                                                    item_and_info["match_id"]
                                                )
                                            ],
                                        ),
                                        rx.button(
                                            "HAND OVER & PRINT RECEIPT",
                                            size="2",
                                            color_scheme="blue",
                                            on_click=[
                                                State.call_hand_over_and_archive_match_print_receipt(
                                                    item_and_info["match_id"]
                                                )
                                            ],
                                        ),
                                        spacing="2",
                                    )
                                ),
                            ),
                        )
                    ),
                    variant="surface",
                    width="100%",
                    overflow_y="auto",
                    max_h="60vh",
                ),
                spacing="6",
                width="100%",
            ),
            padding="50px",
            flex=1,
            overflow_y="auto",
            bg=bg_style["background"],
        ),
        # Footer
        footer(),
        direction="column",
        height="100vh",
        width="100vw",

        on_mount=State.redirect_if_bad_auth(required_role="WORKER"),
    )


# ----------------------------------
# Page : Policy  Page
# ----------------------------------
def PolicyPage() -> rx.Component:

    return rx.flex(
        navbar_user(),
        rx.box(height=NAV_H),
        # 2) Main content
        rx.box(
            rx.center(
                rx.card(
                    rx.vstack(
                        rx.heading("Company Policy", size="8", weight="bold", mb="4"),
                        rx.markdown(
                            State.policy,
                            white_space="pre-wrap",
                            font_size="md",
                        ),
                    ),
                    border_radius="lg",
                    box_shadow="lg",
                    width="100%",
                    padding="50px",
                    max_width="800px",
                ),
            ),
            flex=1,
            overflow_y="auto",
            mt=NAV_H,
            padding="50px",
            bg=bg_style["background"],
        ),
        # 3) Footer
        footer(),
        direction="column",
        width="100vw",
        height="100vh",

        on_mount=State.redirect_if_bad_auth(required_role="USER"),
    )


# ----------------------------------
# Page : User Setting
# ----------------------------------
def SettingsUserPage() -> rx.Component:
    mode = rx.color_mode

    return rx.flex(
        navbar_user(),
        rx.box(height=NAV_H),
        # ── 2) Main area ──
        rx.hstack(
            rx.box(
                rx.vstack(
                    rx.text("Settings", size="6", font_weight="bold", mb="4"),
                    # theme toggle
                    rx.icon_button(
                        rx.cond(
                            mode == "light",
                            rx.icon("moon", box_size=5),
                            rx.icon("sun", box_size=5),
                        ),
                        aria_label="Toggle theme",
                        variant="ghost",
                        on_click=rx.toggle_color_mode,
                        mb="4",
                    ),
                    rx.button(
                        "Profile",
                        on_click=State.set_settings_tab("profile"),
                        variant=rx.cond(
                            State.settings_tab == "profile", "solid", "ghost"
                        ),
                        color_scheme=button_style_2,
                        width="100%",
                        _hover={"bg": rx.cond(mode == "light", "blue.300", "blue.600")},
                    ),
                    spacing="3",
                    p="4",
                    bg=rx.cond(mode == "light", "blue.200", "gray.900"),
                    border_radius="8",
                    box_shadow="sm",
                ),
                flex="0 0 25%",
            ),
            rx.box(
                rx.cond(
                    State.settings_tab == "profile",
                    # —— PROFILE VIEW ——
                    rx.card(
                        rx.vstack(
                            rx.heading("Your Profile", size="4", mb="4"),
                            rx.text(f"📧 Email: {State.email}"),
                            rx.text(f"👤 Name: {State.firstname} {State.surname}"),
                            spacing="3",
                        ),
                        p="6",
                        max_w="600px",
                        mx="auto",
                        bg=rx.cond(mode == "light", "white", "gray.700"),
                        box_shadow="md",
                        border_radius="8",
                    ),
                ),
                flex="1 1 60%",
                p="6",
                bg=rx.cond(mode == "light", "white", "gray.800"),
                border_radius="8",
                box_shadow="md",
            ),
            spacing="6",
            flex="1",
        ),
        # ── 3) Footer ──
        footer(),
        direction="column",
        height="100vh",
        width="100vw",
        bg=bg_style["background"],

        on_mount=State.redirect_if_bad_auth(required_role="USER"),
    )


# ----------------------------------
# Page : Worker Setting
# ----------------------------------
def SettingsWorkerPage() -> rx.Component:
    mode = rx.color_mode

    return rx.flex(
        navbar_worker(),
        rx.box(height=NAV_H),
        # ── 2) Main area ──
        rx.hstack(
            rx.box(
                rx.vstack(
                    rx.text("Settings", size="6", font_weight="bold", mb="4"),
                    # theme toggle
                    rx.icon_button(
                        rx.cond(
                            mode == "light",
                            rx.icon("moon", box_size=5),
                            rx.icon("sun", box_size=5),
                        ),
                        aria_label="Toggle theme",
                        variant="ghost",
                        on_click=rx.toggle_color_mode,
                        mb="4",
                    ),
                    rx.button(
                        "Profile",
                        on_click=State.set_settings_tab("profile"),
                        variant=rx.cond(
                            State.settings_tab == "profile", "solid", "ghost"
                        ),
                        color_scheme=button_style_2,
                        width="100%",
                        _hover={"bg": rx.cond(mode == "light", "blue.300", "blue.600")},
                    ),
                    spacing="3",
                    p="4",
                    bg=rx.cond(mode == "light", "blue.200", "gray.900"),
                    border_radius="8",
                    box_shadow="sm",
                ),
                flex="0 0 25%",
            ),
            rx.box(
                rx.cond(
                    State.settings_tab == "profile",
                    # —— PROFILE VIEW ——
                    rx.card(
                        rx.vstack(
                            rx.heading("Your Profile", size="4", mb="4"),
                            rx.text(f"📧 Email: {State.email}"),
                            rx.text(f"👤 Name: {State.firstname} {State.surname}"),
                            spacing="3",
                        ),
                        p="6",
                        max_w="600px",
                        mx="auto",
                        bg=rx.cond(mode == "light", "white", "gray.700"),
                        box_shadow="md",
                        border_radius="8",
                    ),
                ),
                flex="1 1 60%",
                p="6",
                bg=rx.cond(mode == "light", "white", "gray.800"),
                border_radius="8",
                box_shadow="md",
            ),
            spacing="6",
            flex="1",
        ),
        # ── 3) Footer ──
        footer(),
        direction="column",
        height="100vh",
        width="100vw",
        bg=bg_style["background"],

        on_mount=State.redirect_if_bad_auth(required_role="WORKER"),
    )


# ----------------------------------
# The footer
# ----------------------------------
def footer() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(src=logo, width="2em", border_radius="25%"),
                rx.heading(app_name, size="6", weight="bold", color="white"),
                spacing="2",
                align="start",
            ),
            rx.text("© 2025 BackToU, Inc", color="white"),
            spacing="8",
            align="center",
            justify="center",
        ),
        bg="#20263e",
        width="100%",
        as_="footer",
        justify="end",
    )


app = rx.App()
app.add_page(index, route="/")
app.add_page(AdminDashboard, route="/admin-dashboard")
app.add_page(UserDashboard, route="/user-dashboard")
app.add_page(SubmitLostItemPage, route="/submit-lost")
app.add_page(ViewLostReportPage, route="/view-lost")
app.add_page(WorkerDashBoard, route="/worker-dashboard")
app.add_page(SubmitFoundItemPage, route="/submit-found")
app.add_page(MatchItemPage, route="/match-items")
app.add_page(ConfirmMatchPage, route="/confirm-return")
app.add_page(PolicyPage, route="/policy")
app.add_page(SettingsUserPage, route="/setting-user")
app.add_page(SettingsWorkerPage, route="/setting-worker")
