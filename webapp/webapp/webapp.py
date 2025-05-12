import reflex as rx
from rxconfig import config
from reflex import redirect

from webapp.models.enums import RoleEnum
from webapp.service.account_service import *
from webapp.service.item_service import *
from webapp.service.matches_service import *

#   V------this "apperance" "config" we can read this from a file
app_name="Back2You"
app_desc="Report lost item or turn in what you found."
logo="/BTUw.png"
bg_style={"background": "linear-gradient(to bottom right, #a34fe2, #184ef2)", "padding": "2rem"}
button_style_1="green"
button_style_2="red"

#    V-------for backend. this is just testing code.
#======================================================================================================================================================================

def get_notifications(email):
    print("GET NOTIFICATIONS", email)
    return ["Your item 456 was matched and is ready for pickup"]
def get_stats():
    print("GET STATS")
    return ["Number of lost items: 2"]
#   V------return dictionary with relevant stuff

#==============================================================================================================================================================================

class State(rx.State):
    email: str=""
    password: str=""
    result: str=""
    logged_in_as_user: bool= False
    logged_in_as_worker: bool= False
    logged_in_as_admin: bool= False
    not_logged_in: bool=True
    temp: str=""
    temp2: str=""
    category: str=""
    item_type: str=""
    color: str=""
    desc: str=""
    size: str=""
    material: str=""
    brand: str="" 
    name: str=""
    account_name: str=""
    is_other: bool=False
    show_size: bool=False
    show_material: bool=False
    show_brand: bool= False
    show_name: bool=False
    def set_email(self, email:str):
        self.email=email
    def set_password(self, password:str):
        self.password=password
    def login(self):
        self.result=""
        if "@" not in self.email or "." not in self.email:
            self.result=f"INVALID EMAIL FORMAT"
            return
        temp=login_user(self.email, self.password)
        if temp==None:
            self.result=f"INCORRECT EMAIL OR PASSWORD"
        elif temp==RoleEnum.USER:
            self.logged_in_as_user=True
            self.not_logged_in=False
            self.load_submitted_lost_items()
            self.account_name = get_account_details(self.email)["name"]
            return redirect("/user-dashboard") # I add this
        elif temp==RoleEnum.WORKER:
            self.logged_in_as_worker=True
            self.not_logged_in=False
            self.load_matches()
            self.load_confirmed_matches()
            return redirect("/worker-dashboard") # I add this
        elif temp==RoleEnum.ADMIN:
            self.logged_in_as_admin=True
            self.not_logged_in=False
            return redirect("/") #I add this
    def logout(self):
        self.logged_in_as_user= False
        self.logged_in_as_worker= False
        self.logged_in_as_admin= False
        self.not_logged_in=True
        self.email = ""
        self.password = ""
    def set_category(self, category: str):
        self.category=category
        self.item_type=""
        self.color=""
        self.desc=""
        self.size=""
        self.material=""
        self.brand=""
        self.name=""
    def set_item_type(self, item_type: str):
        self.item_type=item_type
    def set_size(self, size: str):
        self.size=size
    def set_material(self, material: str):
        self.material=material
    def set_brand(self, brand: str):
        self.brand=brand
    def set_name(self, name: str):
        self.name=name
    def set_color(self, color: str):
        self.color=color
    def set_desc(self, desc: str):
        self.desc=desc
    submitted_lost_items: list[dict] = []
    matches: list[dict]=[]
    confirmed_matches: list[dict] =[]
    notifications: list[str]=[]
    def load_submitted_lost_items(self):
        t=get_submitted_lost_items(self.email)
        self.submitted_lost_items = [{"item_id": x.item_id,"category": x.category,"item_type": x.item_type,"color": x.color,"desc": x.desc,"size": x.size,"material": x.material,"brand": x.brand,"name": x.name,"status": x.status} for x in t]
    def call_submit_lost_item(self):
        item=Item(self.category, self.item_type, self.color, self.desc, self.size, self.material, self.brand, self.name)
        self.temp="ITEM SUBMITTED"
        submit_lost_item(self.email, item)
        self.load_submitted_lost_items()
    def call_delete_lost_item(self, item_id, category):
        self.temp2="ITEM DELETED"
        delete_lost_item(self.email, int(item_id), category)
        self.load_submitted_lost_items()
    def call_get_notifications(self):
        self.notifications=get_notifications(self.email)
    def call_submit_found_item(self):
        item=Item(self.category, self.item_type, self.color, self.desc, self.size, self.material, self.brand, self.name)
        self.temp="ITEM SUBMITTED"
        submit_found_item(self.email, item)
        self.load_matches()
    def load_matches(self):
        t=get_matches(self.email)
        self.matches = [{"lost_item_id": x[0].item_id,"lost_item_category": x[0].category,"lost_item_type": x[0].item_type,"lost_item_color": x[0].color,"lost_item_desc": x[0].desc,"lost_item_size": x[0].size,"lost_item_material": x[0].material,"lost_item_brand": x[0].brand,"lost_item_name": x[0].name,"lost_item_status": x[0].status,
        "found_item_id": x[1].item_id,"found_item_category": x[1].category,"found_item_type": x[1].item_type,"found_item_color": x[1].color,"found_item_desc": x[1].desc,"found_item_size": x[1].size,"found_item_material": x[1].material,"found_item_brand": x[1].brand,"found_item_name": x[1].name, "match_score": x[2]} for x in t]
    def call_confirm_match(self,lost_item_id, found_item_id, category):
        confirm_match(int(lost_item_id), int(found_item_id), category)
        self.load_matches()
    def load_confirmed_matches(self):
        t=get_confirmed_matches_with_user_pesel(self.email)
        self.confirmed_matches = [{"found_item_id": x.item_id,"found_item_category": x.category,"found_item_type": x.item_type,"found_item_color": x.color,"found_item_desc": x.desc,"found_item_size": x.size,"found_item_material": x.material,"found_item_brand": x.brand,"found_item_name": x.name, "owner_pesel": x.pesel} for x in t]
    def call_hand_over_and_archive_match(self,found_item_id, category):
        hand_over_and_archive_match(int(found_item_id), category)
        self.load_confirmed_matches()

#Index Admin Page
def index() -> rx.Component:
    return rx.cond(State.not_logged_in,
        LoginPage(),
        rx.cond(State.logged_in_as_admin,
            rx.box(
                rx.vstack(
                    # Navigation Bar
                    rx.hstack(
                        rx.hstack(
                            rx.image(src="/BTUw.png", width="2.5em", style={"filter": "brightness(1.4) saturate(1.5)"}),
                            rx.heading("Back2You", font_size="xl", color="white"),
                            spacing="2",
                            align="center",
                        ),
                        rx.spacer(),
                        rx.hstack(
                            rx.icon(tag="bell", name="bell", color="white", box_size=5),
                            rx.text(State.email, color="white", font_size="md"),
                            rx.button("Logout", on_click=State.logout, variant="outline", color_scheme="gray"),
                            spacing="3",
                            align="center",
                        ),
                        padding_x="6",
                        padding_y="4",
                        width="100%",
                    ),

                    # Main Content
                    rx.center(
                        rx.box(
                            rx.vstack(
                                rx.heading("Admin Dashboard", font_size="3xl", color="white", mb="2"),
                                rx.text("Overview of system statistics", color="gray.300", mb="4"),

                                # Table headers
                                rx.hstack(
                                    *[rx.text(h, font_weight="bold", width="15em", color="white") for h in [
                                        "Stat Info"
                                    ]]
                                ),
                                rx.divider(),

                                # Table rows
                                rx.vstack(
                                    rx.foreach(
                                        get_stats(),
                                        lambda stat: rx.hstack(
                                            rx.text(stat, width="15em", color="gray.100"),
                                            spacing="2",
                                        )
                                    )
                                ),

                                spacing="4",
                            ),
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "borderRadius": "1rem",
                                "boxShadow": "0 8px 30px rgba(0, 0, 0, 0.4)",
                                "padding": "2rem",
                                "width": "100%",
                                "maxWidth": "600px",
                            },
                        ),
                    ),
                    spacing="6",
                    padding="2rem",
                ),
                height="100vh",
                width="100vw",
                style=bg_style,
            )
        )
    )

# ---------------------
#  Page: Login Page
# ---------------------
def LoginPage() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.image(
                src=logo,
                alt=app_name,
                width="15em",
            ),
            rx.heading(app_name, font_size="5xl", color="white", text_align="center"),
            rx.text(app_desc, color="white", mb="6", text_align="center"),
            rx.input(
                placeholder="Email",
                on_change=State.set_email,
                width="100%",
            ),
            rx.input(
                placeholder="Password",
                on_change=State.set_password,
                width="100%",
            ),
            rx.button("Login", color_scheme=button_style_1, on_click=State.login),
            rx.text(State.result, color="red"),
            align_items="center",
        ),
        height="100vh",
        width="100vw",
        style=bg_style,
    )

# ---------------------
#  Page: User Dashboard
# ---------------------

def UserDashboard() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.image(src="/BTUw.png", width="2.5em", style={"filter": "brightness(1.4) saturate(1.5)"}),
                    rx.heading("Back2You", font_size="xl", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon(tag="bell", name="bell", color="white", box_size=5),
                    rx.text(State.email, color="white", font_size="md"),
                    rx.button("Logout", on_click=lambda: [State.logout(), redirect("/")], variant="outline", color_scheme="gray"),
                    spacing="3",
                    align="center",
                ),
                padding_x="6",
                padding_y="4",
                width="100%",
            ),
            rx.hstack(
                rx.box(
                    rx.vstack(
                        rx.heading("Welcome, Back2You User!", font_size="4xl", color="white", mb="2"),
                        rx.text(
                            "Start by submitting a new lost item or checking your notifications.",
                            color="gray.300",
                            font_size="lg",
                            mb="6",
                        ),
                        rx.button(
                            "Submit Lost Item",
                            on_click=lambda: redirect("/submit-lost"),
                            variant="outline",
                            color_scheme="purple",
                            _hover={"bg": "blue.600", "color": "white", "borderColor": "blue.300"},
                            border="2px solid",
                            border_radius="md"
                        ),
                        rx.button(
                            "View Lost Report",
                            on_click=lambda: redirect("/view-lost"),
                            variant="outline",
                            color_scheme="purple",
                            _hover={"bg": "blue.600", "color": "white", "borderColor": "blue.300"},
                            border="2px solid",
                            border_radius="md"
                        ),
                        spacing="6",
                        align_items="center",
                        text_align="center",
                        width="100%",
                    ),
                    width="60%",
                    padding_x="6",
                ),
                rx.image(
                    src="/navigateuser.png",
                    alt="Lost Item Illustration",
                    width="40%",
                    border_radius="xl",
                ),
                spacing="4",
                align_items="center",
                justify="center",
            ),
            spacing="9",
            padding_x="10",
            padding_y="6",
        ),
        height="100vh",
        width="100vw",
        style=bg_style,
    )

# ---------------------
#  Page: SubmitLostItem
# ---------------------
def SubmitLostItemPage() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Navigation bar
            rx.hstack(
                rx.hstack(
                    rx.image(src="/BTUw.png", width="2.5em", style={"filter": "brightness(1.4) saturate(1.5)"}),
                    rx.heading("Back2You", font_size="xl", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon(tag="bell", name="bell", color="white", box_size=5),
                    rx.text(State.email, color="white", font_size="md"),
                    rx.button("Dashboard", on_click=lambda: redirect("/user-dashboard"), variant="ghost", color_scheme="gray"),
                    rx.button("Logout", on_click=lambda: [State.logout(), redirect("/")], variant="outline", color_scheme="gray"),
                    spacing="3",
                    align="center",
                ),
                padding_x="6",
                padding_y="4",
                width="100%",
            ),

            # Page Content
                # Form Fields
                rx.center(
                        rx.box(
                            rx.vstack(
                                    rx.heading("Submit a Lost Item", font_size="3xl", color="white", mb="4"),
                                    rx.text("Please fill out the form below to report a lost item.", color="gray.300"),
                                    rx.divider(),
                                    rx.text("Category"),
                                    rx.select(
                                        items=["personalitems","jewelry","accessories","travelitems","electronicdevices","clothing","officeitems","otheritems"],
                                        value=State.category,
                                        on_change=State.set_category,
                                        placeholder="",
                                        ),
                                        rx.cond((State.category == "personalitems"),
                                        rx.vstack(
                                            rx.text("Type of Personal Item"),
                                            rx.select(
                                                items=["id_card","passport","keys","credit_card","other"],
                                                value=State.item_type,
                                                on_change=State.set_item_type,
                                                placeholder="",
                                            ),
                                        ),
                                        ),
                                        rx.cond((State.category == "jewelry"),
                                        rx.vstack(
                                            rx.text("Type of Jewelry"),
                                            rx.select(
                                                items=["ring","earrings","necklace","piercing","other"],
                                                value=State.item_type,
                                                on_change=State.set_item_type,
                                                placeholder="",
                                            ),
                                        ),
                                        ),
                                        rx.cond((State.category == "accessories"),
                                        rx.vstack(
                                            rx.text("Type of Accessory"),
                                            rx.select(
                                                items=["glasses","sunglasses","wristwatch","other"],
                                                value=State.item_type,
                                                on_change=State.set_item_type,
                                                placeholder="",
                                            ),
                                        ),
                                        ),
                                        rx.cond((State.category == "travelitems"),
                                        rx.vstack(
                                            rx.text("Type of Travel Item"),
                                            rx.select(
                                                items=["suitcase","handbag","backpack","luggage","umbrella","wallet","purse","water_bottle","other"],
                                                value=State.item_type,
                                                on_change=State.set_item_type,
                                                placeholder="",
                                            ),
                                        ),
                                        ),
                                        rx.cond((State.category == "electronicdevices"),
                                        rx.vstack(
                                            rx.text("Type of Electronic Device"),
                                            rx.select(
                                                items=["phone","laptop","tablet","cable","earbuds","headphones","camera","smartwatch","powerbank","other"],
                                                value=State.item_type,
                                                on_change=State.set_item_type,
                                                placeholder="",
                                            ),
                                        ),
                                        ),
                                        rx.cond((State.category == "clothing"),
                                        rx.vstack(
                                            rx.text("Type of Clothing"),
                                            rx.select(
                                                items=["coat","jacket","gloves","scarf","hat","shoes","other"],
                                                value=State.item_type,
                                                on_change=State.set_item_type,
                                                placeholder="",
                                            ),
                                        ),
                                        ),
                                        rx.cond((State.category == "officeitems"),
                                        rx.vstack(
                                            rx.text("Type of Office Item"),
                                            rx.select(
                                                items=["pen","folder","book","other"],
                                                value=State.item_type,
                                                on_change=State.set_item_type,
                                                placeholder="",
                                            ),
                                        ),
                                        ),
                                        rx.cond((State.category == "otheritems"),
                                        rx.vstack(
                                            rx.text("Type of Other Item"),
                                            rx.input(
                                                placeholder="Type of other item",
                                                on_change=State.set_item_type,
                                            ),
                                        ),
                                        ),
                                    rx.cond((State.category == "jewelry") | (State.category == "travelitems") | (State.category == "clothing") | (State.category == "officeitems") | (State.category == "otheritems"),
                                        rx.vstack(
                                            rx.text("Size"),
                                            rx.select(
                                                items=["xs","s","m","l","xl"],
                                                value=State.size,
                                                on_change=State.set_size,
                                                placeholder="",
                                            ),
                                        ),
                                        ),
                                        rx.cond((State.category == "accessories") | (State.category == "travelitems") | (State.category == "electronicdevices") | (State.category == "clothing") | (State.category == "officeitems") | (State.category == "otheritems"),
                                        rx.vstack(
                                            rx.text("Material"),
                                            rx.select(
                                                items=["wood","metal","plastic","glass","ceramic","fabric","leather","rubber","paper","other"],
                                                value=State.material,
                                                on_change=State.set_material,
                                                placeholder="",
                                            ),
                                        ),
                                        ),
                                        rx.cond((State.category == "accessories") | (State.category == "travelitems") | (State.category == "electronicdevices") | (State.category == "clothing") | (State.category == "officeitems") | (State.category == "otheritems"),
                                        rx.vstack(
                                            rx.text("Brand"),
                                            rx.input(
                                                placeholder="Brand",
                                                on_change=State.set_brand,
                                            ),
                                        ),
                                        ),
                                        rx.cond((State.category == "otheritems"),
                                        rx.vstack(
                                            rx.text("Name"),
                                            rx.input(
                                                placeholder="Name",
                                                on_change=State.set_name,
                                            ),
                                        ),
                                        ),
                                        rx.text("Color"),
                                    rx.select(
                                        items=["red","green","blue","yellow","orange","purple","pink","brown","black","white","gray","cyan","maroon","navy","beige","other"],
                                        value=State.color,
                                        on_change=State.set_color,
                                        placeholder="",
                                        ),
                                        rx.text("Description"),
                                        rx.input(
                                        placeholder="Description",
                                        on_change=State.set_desc,
                                        ),
                                        rx.button("SUBMIT", color_scheme=button_style_1, on_click=State.call_submit_lost_item),
                                        rx.text(State.temp),
                            ),
                            style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "borderRadius": "1rem",
                                "boxShadow": "0 8px 30px rgba(0, 0, 0, 0.4)",
                                "padding": "2rem",
                                "width": "100%",
                                "maxWidth":"650px",
                            }
                        ),
                        spacing="6",
                        width="100vw",
                        height="100vh",
                    ),


            #spacing="6",
            #padding="2rem",
            style=bg_style,
        ),
        
    )

# ---------------------
#  Page: ViewLostReport
# ---------------------
def ViewLostReportPage() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Navigation bar
            rx.hstack(
                rx.hstack(
                    rx.image(src="/BTUw.png", width="2.5em", style={"filter": "brightness(1.4) saturate(1.5)"}),
                    rx.heading("Back2You", font_size="xl", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon(tag="bell", name="bell", color="white", box_size=5),
                    rx.text(State.email, color="white", font_size="md"),
                    rx.button("Dashboard", on_click=lambda: redirect("/user-dashboard"), variant="ghost", color_scheme="gray"),
                    rx.button("Logout", on_click=lambda: [State.logout(), redirect("/")], variant="outline", color_scheme="gray"),
                    spacing="3",
                    align="center",
                ),
                padding_x="6",
                padding_y="4",
                width="100%",
            ),

            # Reported lost items box
            rx.center(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Your Reported Lost Items", size="3", color="white"),
                            rx.spacer(),
                            rx.button("Refresh", color_scheme=button_style_1, on_click=State.load_submitted_lost_items),
                        ),

                        # Header Row
                        rx.hstack(
                            *[rx.text(h, font_weight="bold", width="6.5em", color="white", white_space="nowrap") for h in [
                                "ID", "Category", "Type", "Color", "Desc", "Size", "Material", "Brand", "Name", "Status", "Action"
                            ]]
                        ),

                        rx.divider(),

                        # Data Rows
                        rx.vstack(
                            rx.foreach(
                                State.submitted_lost_items,
                                lambda item: rx.hstack(
                                    rx.text(item["item_id"], width="7em", color="gray.100"),
                                    rx.text(item["category"], width="7em", color="gray.100"),
                                    rx.text(item["item_type"], width="7em", color="gray.100"),
                                    rx.text(item["color"], width="7em", color="gray.100"),
                                    rx.text(item["desc"], width="7em", color="gray.100"),
                                    rx.text(item["size"], width="7em", color="gray.100"),
                                    rx.text(item["material"], width="7em", color="gray.100"),
                                    rx.text(item["brand"], width="7em", color="gray.100"),
                                    rx.text(item["name"], width="7em", color="gray.100"),
                                    rx.text(item["status"], width="7em", color="green.200"),
                                    rx.button("Delete", color_scheme=button_style_2, 
                                              on_click=[State.call_delete_lost_item(item["item_id"], item['category'])]),
                                    spacing="1"
                                )
                            )
                        ),
                        rx.text(State.temp2, color="red"),
                        spacing="4"
                    ),
                    style={
                        #"background": "rgba(255, 255, 255, 0.05)",
                        #"borderRadius": "1rem",
                        #"boxShadow": "0 8px 30px rgba(0, 0, 0, 0.4)",
                        "padding": "2rem",
                        "width": "95%",
                        "maxWidth": "1200px",
                        #"overflowX": "auto",
                    }
                ),
                padding_top="4"
            ),

            spacing="6",
            padding="2rem"
        ),
        height="100vh",
        width="100vw",
        style=bg_style,
    )

# ---------------------
#  Page: WorkerDashboard
# ---------------------
def WorkerDashboard() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Navbar
            rx.hstack(
                rx.hstack(
                    rx.image(src="/BTUw.png", width="2.5em", style={"filter": "brightness(1.4) saturate(1.5)"}),
                    rx.heading("Back2You", font_size="xl", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon(tag="bell", name="bell", color="white", box_size=5),
                    rx.text(State.email, color="white", font_size="md"),
                    rx.button("Logout", on_click=lambda: [State.logout(), redirect("/")], variant="outline", color_scheme="gray"),
                    spacing="3",
                    align="center",
                ),
                padding_x="6",
                padding_y="4",
                width="100%",
            ),

            # Main section
            rx.flex(
                rx.box(
                    rx.vstack(
                        rx.heading("Welcome!", font_size="2xl", color="white"),
                        rx.text("Choose a task you want to perform today:", color="gray.300", mb="4"),
                        #rx.button("Submit Found Item", on_click=lambda: redirect("/submit-found"), color_scheme="blue", width="100%"),
                        rx.button(
                            "Submit Found Item",
                            on_click=lambda: redirect("/submit-found"),
                            bg="blue.500",
                            color="white",
                            _hover={"bg": "blue.600"},
                            width="100%",
                            border_radius="md",
                            font_weight="bold",
                            box_shadow="md",
                        ),
                        rx.button(
                            "Match Found Items",
                            on_click=lambda: redirect("/match-items"),
                            bg="blue.500",
                            color="white",
                            _hover={"bg": "blue.600"},
                            width="100%",
                            border_radius="md",
                            font_weight="bold",
                            box_shadow="md",
                        ),
                        rx.button(
                            "Confirm Return",
                            on_click=lambda: redirect("/confirm-return"),
                            bg="blue.500",
                            color="white",
                            _hover={"bg": "blue.600"},
                            width="100%",
                            border_radius="md",
                            font_weight="bold",
                            box_shadow="md",
                        ),
                        spacing="4",
                        align_items="stretch",
                    ),
                    style={
                        "background": "rgba(255, 255, 255, 0.05)",
                        "borderRadius": "1rem",
                        "boxShadow": "0 6px 20px rgba(0,0,0,0.3)",
                        "padding": "2rem",
                        "width": "100%",
                        "maxWidth": "20em",
                    },
                ),
                rx.image(
                    src="/navworker.png",
                    alt="Worker Dashboard Illustration",
                    width="100%",
                    max_width="460px",
                    height="auto",
                    border_radius="xl",
                ),
                spacing="8",
                wrap="wrap",
                justify="center",
                align="center",
                width="100%",
                height="100%",
            ),
            spacing="9",
            height="100%",
            grow="1",
        ),
        height="100vh",
        width="100vw",
        style=bg_style,
    )

# ---------------------
#  Page:SubmitFoundItemPage
# ---------------------
def SubmitFoundItemPage() -> rx.Component:
        return rx.box(
        rx.vstack(
            # Navigation bar
            rx.hstack(
                rx.hstack(
                    rx.image(src="/BTUw.png", width="2.5em", style={"filter": "brightness(1.4) saturate(1.5)"}),
                    rx.heading("Back2You", font_size="xl", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon(tag="bell", name="bell", color="white", box_size=5),
                    rx.text(State.email, color="white", font_size="md"),
                    rx.button("Dashboard", on_click=lambda: redirect("/worker-dashboard"), variant="ghost", color_scheme="gray"),
                    rx.button("Logout", on_click=lambda: [State.logout(), redirect("/")], variant="outline", color_scheme="gray"),
                    spacing="3",
                    align="center",
                ),
                padding_x="6",
                padding_y="4",
                width="100%",
            ),

             rx.center(
                    rx.box(
                        rx.heading("Submit New Found Item", font_size="3xl",color="white",mb="4",text_align="center"),
                        rx.divider(),
                        rx.vstack(
                            rx.text("Category"),
                            rx.select(
                                items=["personalitems","jewelry","accessories","travelitems","electronicdevices","clothing","officeitems","otheritems"],
                                value=State.category,
                                on_change=State.set_category,
                                placeholder="",
                            ),
                            rx.cond(State.category == "personalitems", rx.vstack(
                                rx.text("Type of Personal Item"),
                                rx.select(items=["id_card","passport","keys","credit_card","other"], value=State.item_type, on_change=State.set_item_type),
                            )),
                            rx.cond(State.category == "jewelry", rx.vstack(
                                rx.text("Type of Jewelry"),
                                rx.select(items=["ring","earrings","necklace","piercing","other"], value=State.item_type, on_change=State.set_item_type),
                            )),
                            rx.cond(State.category == "accessories", rx.vstack(
                                rx.text("Type of Accessory"),
                                rx.select(items=["glasses","sunglasses","wristwatch","other"], value=State.item_type, on_change=State.set_item_type),
                            )),
                            rx.cond(State.category == "travelitems", rx.vstack(
                                rx.text("Type of Travel Item"),
                                rx.select(items=["suitcase","handbag","backpack","luggage","umbrella","wallet","purse","water_bottle","other"], value=State.item_type, on_change=State.set_item_type),
                            )),
                            rx.cond(State.category == "electronicdevices", rx.vstack(
                                rx.text("Type of Electronic Device"),
                                rx.select(items=["phone","laptop","tablet","cable","earbuds","headphones","camera","smartwatch","powerbank","other"], value=State.item_type, on_change=State.set_item_type),
                            )),
                            rx.cond(State.category == "clothing", rx.vstack(
                                rx.text("Type of Clothing"),
                                rx.select(items=["coat","jacket","gloves","scarf","hat","shoes","other"], value=State.item_type, on_change=State.set_item_type),
                            )),
                            rx.cond(State.category == "officeitems", rx.vstack(
                                rx.text("Type of Office Item"),
                                rx.select(items=["pen","folder","book","other"], value=State.item_type, on_change=State.set_item_type),
                            )),
                            rx.cond(State.category == "otheritems", rx.vstack(
                                rx.text("Type of Other Item"),
                                rx.input(placeholder="Type of other item", on_change=State.set_item_type),
                            )),
                            rx.cond((State.category == "jewelry") | (State.category == "travelitems") | (State.category == "clothing") | (State.category == "officeitems") | (State.category == "otheritems"), rx.vstack(
                                rx.text("Size"),
                                rx.select(items=["xs","s","m","l","xl"], value=State.size, on_change=State.set_size),
                            )),
                            rx.cond((State.category == "accessories") | (State.category == "travelitems") | (State.category == "electronicdevices") | (State.category == "clothing") | (State.category == "officeitems") | (State.category == "otheritems"), rx.vstack(
                                rx.text("Material"),
                                rx.select(items=["wood","metal","plastic","glass","ceramic","fabric","leather","rubber","paper","other"], value=State.material, on_change=State.set_material),
                            )),
                            rx.cond((State.category == "accessories") | (State.category == "travelitems") | (State.category == "electronicdevices") | (State.category == "clothing") | (State.category == "officeitems") | (State.category == "otheritems"), rx.vstack(
                                rx.text("Brand"),
                                rx.input(placeholder="Brand", on_change=State.set_brand),
                            )),
                            rx.cond(State.category == "otheritems", rx.vstack(
                                rx.text("Name"),
                                rx.input(placeholder="Name", on_change=State.set_name),
                            )),
                            rx.text("Color"),
                            rx.select(
                                items=["red","green","blue","yellow","orange","purple","pink","brown","black","white","gray","cyan","maroon","navy","beige","other"],
                                value=State.color,
                                on_change=State.set_color,
                                placeholder="",
                            ),
                            rx.text("Description"),
                            rx.input(placeholder="Description", on_change=State.set_desc),
                            rx.button("SUBMIT", color_scheme=button_style_1, on_click=State.call_submit_found_item),
                        ),
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "borderRadius": "1rem",
                            "boxShadow": "0 8px 30px rgba(0, 0, 0, 0.4)",
                            "padding": "2rem",
                            "width": "100%",
                            "maxWidth": "650px",
                        }
                    ),
                    spacing="6",
                    width="100vw",
                    height="100vh",
            ),
            style=bg_style,
        ),
    )

# ---------------------
#  Page:MatchItemPage
# ---------------------
import reflex as rx

import reflex as rx
from reflex import redirect

def MatchItemPage() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Navigation bar
            rx.hstack(
                rx.hstack(
                    rx.image(src="/BTUw.png", width="2.5em", style={"filter": "brightness(1.4) saturate(1.5)"}),
                    rx.heading("Back2You", font_size="xl", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon(tag="bell", name="bell", color="white", box_size=5),
                    rx.text(State.email, color="white", font_size="md"),
                    rx.button("Dashboard", on_click=lambda: redirect("/worker-dashboard"), variant="ghost", color_scheme="gray"),
                    rx.button("Logout", on_click=lambda: [State.logout(), redirect("/")], variant="outline", color_scheme="gray"),
                    spacing="3",
                    align="center",
                ),
                padding_x="6",
                padding_y="4",
                width="100%",
            ),

            # Table section
            rx.center(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Matched Lost & Found Items", size="3", color="white"),
                            rx.spacer(),
                            rx.button("Refresh", color_scheme=button_style_1, on_click=State.load_matches),
                        ),
                        # Table headers
                        rx.hstack(
                            *[rx.text(h, font_weight="bold", width="8em", color="white") for h in [
                                "Lost ID", "Lost Type", "Lost Desc",
                                "Found ID", "Found Type", "Found Desc",
                                "Match %", "Action"
                            ]]
                        ),
                        rx.divider(),

                        # Table rows
                        rx.vstack(
                            rx.foreach(
                                State.matches,
                                lambda item: rx.hstack(
                                    rx.text(item["lost_item_id"], width="8em", color="gray.100"),
                                    rx.text(item["lost_item_type"], width="8em", color="gray.100"),
                                    rx.text(item["lost_item_desc"], width="8em", color="gray.100"),
                                    rx.text(item["found_item_id"], width="8em", color="gray.100"),
                                    rx.text(item["found_item_type"], width="8em", color="gray.100"),
                                    rx.text(item["found_item_desc"], width="8em", color="gray.100"),
                                    rx.text(f"{item['match_score']}%", width="6em", color="green.200"),
                                    rx.button("Confirm", color_scheme=button_style_2,
                                        on_click=[State.call_confirm_match(
                                            item["lost_item_id"],
                                            item["found_item_id"],
                                            item["found_item_category"]
                                        )]),
                                    spacing="2",
                                )
                            )
                        ),
                        spacing="4",
                    ),
                    style={
                        #"background": "rgba(255, 255, 255, 0.05)",
                        #"borderRadius": "1rem",
                        #"boxShadow": "0 8px 30px rgba(0, 0, 0, 0.4)",
                        "padding": "2rem",
                        "width": "100%",
                        "maxWidth": "1000px",
                        #"overflowX": "auto",
                    },
                ),
                padding_top="4"
            ),
            spacing="6",
            padding="2rem"
        ),
        height="100vh",
        width="100vw",
        style=bg_style,
    )


# ---------------------
#  Page:ConfirmRetrunPage
# ---------------------
def ConfirmReturnPage() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Navigation bar
            rx.hstack(
                rx.hstack(
                    rx.image(src="/BTUw.png", width="2.5em", style={"filter": "brightness(1.4) saturate(1.5)"}),
                    rx.heading("Back2You", font_size="xl", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon(tag="bell", name="bell", color="white", box_size=5),
                    rx.text(State.email, color="white", font_size="md"),
                    rx.button("Dashboard", on_click=lambda: redirect("/worker-dashboard"), variant="ghost", color_scheme="gray"),
                    rx.button("Logout", on_click=lambda: [State.logout(), redirect("/")], variant="outline", color_scheme="gray"),
                    spacing="3",
                    align="center",
                ),
                padding_x="6",
                padding_y="4",
                width="100%",
            ),

            # Confirmed Matches Section
            rx.center(
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.heading("Confirmed Matches and Owner PESEL", size="3", color="white"),
                            rx.button("Refresh", color_scheme=button_style_1, on_click=State.load_confirmed_matches),
                        ),
                        # Simulated table header
                        rx.hstack(
                            *[rx.text(h, font_weight="bold", width="8em", color="white") for h in [
                                "Item ID", "Category", "Type", "Color", "Size", "Brand", "Owner PESEL", "Action"
                            ]]
                        ),
                        rx.divider(),
                        # Simulated table body
                        rx.vstack(
                            rx.foreach(
                                State.confirmed_matches,
                                lambda item: rx.hstack(
                                    rx.text(item["found_item_id"], width="8em", color="gray.100"),
                                    rx.text(item["found_item_category"], width="8em", color="gray.100"),
                                    rx.text(item["found_item_type"], width="8em", color="gray.100"),
                                    rx.text(item["found_item_color"], width="8em", color="gray.100"),
                                    rx.text(item["found_item_size"], width="8em", color="gray.100"),
                                    rx.text(item["found_item_brand"], width="8em", color="gray.100"),
                                    rx.text(item["owner_pesel"], width="8em", color="gray.100"),
                                    rx.button("Hand Over", color_scheme=button_style_2,
                                              on_click=[State.call_hand_over_and_archive_match(item["found_item_id"], item["found_item_category"])]),
                                    spacing="2",
                                )
                            )
                        ),
                        spacing="4",
                    ),
                    style={
                        #"background": "rgba(255, 255, 255, 0.05)",
                        #"borderRadius": "1rem",
                        #"boxShadow": "0 8px 30px rgba(0, 0, 0, 0.4)",
                        "padding": "2rem",
                        "width": "100%",
                        "maxWidth": "1000px",
                        #"overflowX": "auto",
                    },
                ),
                padding_top="4"
            ),
            spacing="6",
            padding="2rem"
        ),
        height="100vh",
        width="100vw",
        style=bg_style,
    )

# ---------------------
# App Setup
# ---------------------

app = rx.App()
app.add_page(index)
app.add_page(LoginPage, route="/login")
app.add_page(UserDashboard, route="/user-dashboard")
app.add_page(SubmitLostItemPage, route="/submit-lost")
app.add_page(ViewLostReportPage, route="/view-lost")
app.add_page(WorkerDashboard, route="/worker-dashboard")
app.add_page(SubmitFoundItemPage, route="/submit-found")
app.add_page(MatchItemPage, route="/match-items")
app.add_page(ConfirmReturnPage, route="/confirm-return")

