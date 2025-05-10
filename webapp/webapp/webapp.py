import reflex as rx
from rxconfig import config


#   V------this "apperance" "config" we can read this from a file
app_name="Campus Retriever"
app_desc="Report lost item or turn in what you found."
logo="/CR.png"
bg_style={"background": "linear-gradient(to bottom right, #a34fe2, #184ef2)", "padding": "2rem"}
button_style_1="green"
button_style_2="red"


#    V-------for backend. this is just testing code.
#======================================================================================================================================================================

f=open("./test.txt","w")
f.write(f"145,j,d,h,v,wa,sa,d,j,Pending\n123,p,w,b,w,l,l,o,a,Ready to Pickup")
f.close()

#   V------return account role if creds valid and False if not
def login_user(email, password):
    users={"u@g.c": "p", "w@g.c": "p", "a@g.c": "p"}
    if email in users and users[email]==password:
        if email[0]=="u":
            return "USER"
        elif email[0]=="w":
            return "WORKER"
        elif email[0]=="a":
            return "ADMIN"
    else:
        return False
#   V------return a list of Lost_Item objects
def get_submitted_lost_items(email):
    f=open("./test.txt", "r")
    x=f.readlines()
    ret=[]
    for l in x:
        t=l.strip().split(",")
        if t==[""]:
            continue
        ret.append(Lost_Item(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9]))
    f.close()
    return ret
    
def submit_lost_item(email,item):
    f=open("./test.txt","a")
    f.write(f"345,{item.category},{item.item_type},{item.color},{item.desc},{item.size},{item.material},{item.brand},{item.name},Pending\n")
    f.close()
def delete_lost_item(email,item_id):
    f=open("./test.txt", "r")
    x=f.readlines()
    ret=[]
    for l in x:
        t=l.strip().split(",")
        if t==[""]:
            continue
        if t[0]==item_id:
            continue
        ret.append(l)
    f.close()
    f=open("./test.txt","w")
    for l in ret:
        f.write(l+"\n")
    f.close()
#   V------return list of strings
def get_notifications(email):
    return ["Your item 456 was matched and is ready for pickup"]
    
def submit_found_item(item):
    f=open("./test2.txt","a")
    f.write(f"\n345,{item.category},{item.item_type},{item.color},{item.desc},{item.size},{item.material},{item.brand},{item.name}\n")
    f.close()

#    V------for this function make sure to provide pairs of lost and found items with match score sorted using match scores descending
def get_matches():
    return [
    [Lost_Item("123","p", "w", "b", "w", "l", "l", "o", "a", "Pending"), Found_Item("484","p", "w", "b", "w", "l", "l", "o", "a"), "90%"],
    [Lost_Item("233","d", "s", "b", "w", "l", "l", "o", "a", "Pending"), Found_Item("324","s", "d", "b", "w", "l", "l", "o", "a"), "80%"],
    ]
    
def confirm_match(lost_item_id, found_item_id):
    pass

#    V-----------the found item details with the pesel of the owner
def get_confirmed_matches_with_user_pesel():
    return [Matched_Item("123","p", "w", "b", "w", "l", "l", "o", "a", "1244324")]

#    V------this function is called when worker finally hands over the found item to owner and it will archive the record
def hand_over_and_archive_match(found_item_id):
    pass
#   V------return list of strings
def get_stats():
    return ["Number of lost items: 2"]
#   V------return dictionary with relevant stuff
def get_account_details(email):
    return {"name":"Arin", "pesel": "21312121"}

#==============================================================================================================================================================================

class Item:
    def __init__(self, category="", item_type="", color="", desc="", size="", material="", brand="", name=""):
        self.category=category
        self.item_type=item_type
        self.color=color
        self.desc=desc
        self.size=size
        self.material=material
        self.brand=brand
        self.name=name
    def __repr__(self):
        return f"Category:{self.category} ItemType:{self.item_type} Color:{self.color} Description:{self.desc} Size:{self.size} Material:{self.material} Brand:{self.brand} Name:{self.name}"
class Lost_Item(Item):
    def __init__(self, item_id="", category="", item_type="", color="", desc="", size="", material="", brand="", name="", status=""):
        super().__init__(category, item_type, color, desc, size, material, brand, name)
        self.item_id=item_id
        self.status=status
    def __repr__(self):
        return f"ID:{self.item_id} "+f"Category:{self.category} ItemType:{self.item_type} Color:{self.color} Description:{self.desc} Size:{self.size} Material:{self.material} Brand:{self.brand} Name:{self.name}"+" Status:{self.status}"
class Found_Item(Item):
    def __init__(self, item_id="", category="", item_type="", color="", desc="", size="", material="", brand="", name=""):
        super().__init__(category, item_type, color, desc, size, material, brand, name)
        self.item_id=item_id
    def __repr__(self):
        return f"ID:{self.item_id} "+f"Category:{self.category} ItemType:{self.item_type} Color:{self.color} Description:{self.desc} Size:{self.size} Material:{self.material} Brand:{self.brand} Name:{self.name}"
class Matched_Item(Item):
    def __init__(self, item_id="", category="", item_type="", color="", desc="", size="", material="", brand="", name="", pesel=""):
        super().__init__(category, item_type, color, desc, size, material, brand, name)
        self.item_id=item_id
        self.pesel=pesel
    def __repr__(self):
        return f"ID:{self.item_id} "+f"Category:{self.category} ItemType:{self.item_type} Color:{self.color} Description:{self.desc} Size:{self.size} Material:{self.material} Brand:{self.brand} Name:{self.name}"+" PESEL:{self.pesel}"
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
        if temp==False:
            self.result=f"INCORRECT EMAIL OR PASSWORD"
        elif temp=="USER":
            self.logged_in_as_user=True
            self.not_logged_in=False
            self.load_submitted_lost_items()
        elif temp=="WORKER":
            self.logged_in_as_worker=True
            self.not_logged_in=False
            self.load_matches()
            self.load_confirmed_matches()
        elif temp=="ADMIN":
            self.logged_in_as_admin=True
            self.not_logged_in=False
    def logout(self):
        self.logged_in_as_user= False
        self.logged_in_as_worker= False
        self.logged_in_as_admin= False
        self.not_logged_in=True
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
    def load_submitted_lost_items(self):
        t=get_submitted_lost_items(self.email)
        self.submitted_lost_items = [{"item_id": x.item_id,"category": x.category,"item_type": x.item_type,"color": x.color,"desc": x.desc,"size": x.size,"material": x.material,"brand": x.brand,"name": x.name,"status": x.status} for x in t]
    def call_submit_lost_item(self):
        item=Item(self.category, self.item_type, self.color, self.desc, self.size, self.material, self.brand, self.name)
        self.temp="ITEM SUBMITTED"
        submit_lost_item(self.email, item)
        self.load_submitted_lost_items()
    def call_delete_lost_item(self, item_id):
        self.temp2="ITEM DELETED"
        delete_lost_item(self.email, item_id)
        self.load_submitted_lost_items()
    def call_submit_found_item(self):
        item=Item(self.category, self.item_type, self.color, self.desc, self.size, self.material, self.brand, self.name)
        self.temp="ITEM SUBMITTED"
        submit_found_item(item)
        self.load_found_items()
    def load_matches(self):
        t=get_matches()
        self.matches = [{"lost_item_id": x[0].item_id,"lost_item_category": x[0].category,"lost_item_type": x[0].item_type,"lost_item_color": x[0].color,"lost_item_desc": x[0].desc,"lost_item_size": x[0].size,"lost_item_material": x[0].material,"lost_item_brand": x[0].brand,"lost_item_name": x[0].name,"lost_item_status": x[0].status,
        "found_item_id": x[1].item_id,"found_item_category": x[1].category,"found_item_type": x[1].item_type,"found_item_color": x[1].color,"found_item_desc": x[1].desc,"found_item_size": x[1].size,"found_item_material": x[1].material,"found_item_brand": x[1].brand,"found_item_name": x[1].name, "match_score": x[2]} for x in t]
    def call_confirm_match(self,lost_item_id, found_item_id):
        self.load_matches()
        confirm_match(lost_item_id, found_item_id)
    def load_confirmed_matches(self):
        t=get_confirmed_matches_with_user_pesel()
        self.confirmed_matches = [{"found_item_id": x.item_id,"found_item_category": x.category,"found_item_type": x.item_type,"found_item_color": x.color,"found_item_desc": x.desc,"found_item_size": x.size,"found_item_material": x.material,"found_item_brand": x.brand,"found_item_name": x.name, "owner_pesel": x.pesel} for x in t]
    def call_hand_over_and_archive_match(self,found_item_id):
        self.load_confirmed_matches()
        hand_over_and_archive_match(found_item_id)
def index() -> rx.Component:
    return rx.cond(State.not_logged_in,
        rx.center(
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
                rx.button("Login", color_scheme=button_style_1,on_click=State.login),
                rx.text(State.result, color="red"),
                align_items="center",
            ),
            height="100vh",
            width="100vw",
            style=bg_style,
        ),
        rx.vstack(
            rx.cond(State.logged_in_as_user,
                rx.vstack(
                    rx.flex(
                        rx.heading("Welcome back "+get_account_details(State.email)["name"]+"!", size="7"),
                        rx.spacer(),
                        rx.button("Logout", color_scheme=button_style_2, on_click=State.logout),
                        width="100%",
                    ),
                    rx.flex(
                    rx.box(
                        rx.heading("Report Lost Item", size="3"),
                        rx.vstack(
                                rx.text("Category"),
                                rx.select(
                                    items=["personal_items","jewelry","accessories","travel_items","electronic_devices","clothing","office_items","other_items"],
                                    value=State.category,
                                    on_change=State.set_category,
                                    placeholder="",
                                    ),
                                    rx.cond((State.category == "personal_items"),
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
                                    rx.cond((State.category == "travel_items"),
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
                                    rx.cond((State.category == "electronic_devices"),
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
                                    rx.cond((State.category == "office_items"),
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
                                    rx.cond((State.category == "other_items"),
                                    rx.vstack(
                                        rx.text("Type of Other Item"),
                                        rx.input(
                                            placeholder="Type of other item",
                                            on_change=State.set_item_type,
                                        ),
                                    ),
                                    ),
                                rx.cond((State.category == "jewelry") | (State.category == "travel_items") | (State.category == "clothing") | (State.category == "office_items") | (State.category == "other_items"),
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
                                    rx.cond((State.category == "accessories") | (State.category == "travel_items") | (State.category == "electronic_devices") | (State.category == "clothing") | (State.category == "office_items") | (State.category == "other_items"),
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
                                    rx.cond((State.category == "accessories") | (State.category == "travel_items") | (State.category == "electronic_devices") | (State.category == "clothing") | (State.category == "office_items") | (State.category == "other_items"),
                                    rx.vstack(
                                        rx.text("Brand"),
                                        rx.input(
                                            placeholder="Brand",
                                            on_change=State.set_brand,
                                        ),
                                    ),
                                    ),
                                    rx.cond((State.category == "other_items"),
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
                            "maxWidth": "650px",
                        }
                    ),
                    rx.box(
                        rx.hstack(
                            rx.heading("Your reported lost items", size="3"),
                            rx.button("Refresh", color_scheme=button_style_1, on_click=State.load_submitted_lost_items),
                        ),
                        rx.text("ID Category Type Color Description Size Material Brand Name Status"),
                        rx.vstack(
                            rx.foreach(
                                State.submitted_lost_items,
                                lambda item: rx.hstack(
                                    rx.text(f"{item['item_id']} {item['category']} {item['item_type']} {item['color']} {item['desc']} {item['size']} {item['material']} {item['brand']} {item['name']} {item['status']}"),
                                    rx.button("Delete", color_scheme=button_style_2, on_click=[State.call_delete_lost_item(item["item_id"])])
                                )
                            )
                        ),
                        rx.text(State.temp2, color="red"),
                        style={
                            "background": "rgba(255, 255, 255, 0.05)",
                            "borderRadius": "1rem",
                            "boxShadow": "0 8px 30px rgba(0, 0, 0, 0.4)",
                            "padding": "2rem",
                            "width": "100%",
                            "maxWidth": "650px",
                        }
                    ),
                    rx.box(
                        rx.heading("Your notifications", size="3"),
                        rx.text(repr(get_notifications(State.email))),
                        style={
                                "background": "rgba(255, 255, 255, 0.05)",
                                "borderRadius": "1rem",
                                "boxShadow": "0 8px 30px rgba(0, 0, 0, 0.4)",
                                "padding": "2rem",
                                "width": "100%",
                                "maxWidth": "650px",
                        }
                    ),
                    spacing="2",
                    width="100%",
                    height="100vh",
                    ),
                    height="100vh",
                    width="100vw",
                    style=bg_style,
                )
            ),
            rx.cond(State.logged_in_as_worker,
                rx.vstack(
                    rx.text("WORKER UI"),
                    rx.button("LOGOUT", on_click=State.logout),
                    rx.text("SUBMIT NEW FOUND ITEM FORM HERE"),
                    rx.vstack(
                            rx.text("ITEM TYPE"),
                            rx.select(
                                items=["personal_items","jewelry","accessories","travel_items","electronic_devices","clothing","office_items","other_items"],
                                value=State.category,
                                on_change=State.set_category,
                                placeholder="",
                                ),
                                rx.cond((State.category == "personal_items"),
                                rx.vstack(
                                    rx.text("TYPE OF PERSONAL ITEM"),
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
                                    rx.text("TYPE OF JEWELRY"),
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
                                    rx.text("TYPE OF ACCESSORY"),
                                    rx.select(
                                        items=["glasses","sunglasses","wristwatch","other"],
                                        value=State.item_type,
                                        on_change=State.set_item_type,
                                        placeholder="",
                                    ),
                                ),
                                ),
                                rx.cond((State.category == "travel_items"),
                                rx.vstack(
                                    rx.text("TYPE OF TRAVEL ITEM"),
                                    rx.select(
                                        items=["suitcase","handbag","backpack","luggage","umbrella","wallet","purse","water_bottle","other"],
                                        value=State.item_type,
                                        on_change=State.set_item_type,
                                        placeholder="",
                                    ),
                                ),
                                ),
                                rx.cond((State.category == "electronic_devices"),
                                rx.vstack(
                                    rx.text("TYPE OF ELECTRONIC DEVICE"),
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
                                    rx.text("TYPE OF CLOTHING"),
                                    rx.select(
                                        items=["coat","jacket","gloves","scarf","hat","shoes","other"],
                                        value=State.item_type,
                                        on_change=State.set_item_type,
                                        placeholder="",
                                    ),
                                ),
                                ),
                                rx.cond((State.category == "office_items"),
                                rx.vstack(
                                    rx.text("TYPE OF OFFICE ITEM"),
                                    rx.select(
                                        items=["pen","folder","book","other"],
                                        value=State.item_type,
                                        on_change=State.set_item_type,
                                        placeholder="",
                                    ),
                                ),
                                ),
                                rx.cond((State.category == "other_items"),
                                rx.vstack(
                                    rx.text("TYPE OF OTHER ITEM"),
                                    rx.input(
                                        placeholder="Type of other item",
                                        on_change=State.set_item_type,
                                    ),
                                ),
                                ),
                            rx.cond((State.category == "jewelry") | (State.category == "travel_items") | (State.category == "clothing") | (State.category == "office_items") | (State.category == "other_items"),
                                rx.vstack(
                                    rx.text("SIZE"),
                                    rx.select(
                                        items=["xs","s","m","l","xl"],
                                        value=State.size,
                                        on_change=State.set_size,
                                        placeholder="",
                                    ),
                                ),
                                ),
                                rx.cond((State.category == "accessories") | (State.category == "travel_items") | (State.category == "electronic_devices") | (State.category == "clothing") | (State.category == "office_items") | (State.category == "other_items"),
                                rx.vstack(
                                    rx.text("MATERIAL"),
                                    rx.select(
                                        items=["wood","metal","plastic","glass","ceramic","fabric","leather","rubber","paper","other"],
                                        value=State.material,
                                        on_change=State.set_material,
                                        placeholder="",
                                    ),
                                ),
                                ),
                                rx.cond((State.category == "accessories") | (State.category == "travel_items") | (State.category == "electronic_devices") | (State.category == "clothing") | (State.category == "office_items") | (State.category == "other_items"),
                                rx.vstack(
                                    rx.text("BRAND"),
                                    rx.input(
                                        placeholder="Brand",
                                        on_change=State.set_brand,
                                    ),
                                ),
                                ),
                                rx.cond((State.category == "other_items"),
                                rx.vstack(
                                    rx.text("NAME"),
                                    rx.input(
                                        placeholder="Name",
                                        on_change=State.set_name,
                                    ),
                                ),
                                ),
                                rx.text("COLOR"),
                            rx.select(
                                items=["red","green","blue","yellow","orange","purple","pink","brown","black","white","gray","cyan","maroon","navy","beige","other"],
                                value=State.color,
                                on_change=State.set_color,
                                placeholder="",
                                ),
                                rx.text("DESCRIPTION"),
                                rx.input(
                                placeholder="Description",
                                on_change=State.set_desc,
                            ),
                                rx.button("SUBMIT", on_click=State.call_submit_lost_item),
                                rx.text(State.temp),
                    ),
                    rx.text("FOUND ITEMS AND THEIR MATCHES (TODO: BUTTON HERE FOR EACH MATCH AND CALL FUNCTION)"),
                    rx.vstack(
                        rx.button("Refresh", on_click=State.load_matches),
                            rx.foreach(
                                State.matches,
                                lambda item: rx.vstack(
                                    rx.text(f"{item['lost_item_id']} {item['lost_item_category']} {item['lost_item_type']} {item['lost_item_color']} {item['lost_item_desc']} {item['lost_item_size']} {item['lost_item_material']} {item['lost_item_brand']} {item['lost_item_name']} "),
                                    rx.text(f"{item['found_item_id']} {item['found_item_category']} {item['found_item_type']} {item['found_item_color']} {item['found_item_desc']} {item['found_item_size']} {item['found_item_material']} {item['found_item_brand']} {item['found_item_name']} "),
                                    rx.text(f"{item['match_score']}"),
                                    rx.button("Confirm Match", on_click=[State.call_confirm_match(item["lost_item_id"], item["found_item_id"])]),
                                )
                            )
                    ),
                    rx.text("CONFIRMED MATCHES AND OWNER PESEL"),
                    rx.vstack(
                        rx.button("Refresh", on_click=State.load_confirmed_matches),
                            rx.foreach(
                                State.confirmed_matches,
                                lambda item: rx.hstack(
                                    rx.text(f"{item['found_item_id']} {item['found_item_category']} {item['found_item_type']} {item['found_item_color']} {item['found_item_desc']} {item['found_item_size']} {item['found_item_material']} {item['found_item_brand']} {item['found_item_name']} {item['owner_pesel']}"),
                                    rx.button("Hand Over", on_click=[State.call_hand_over_and_archive_match(item["found_item_id"])]),
                                )
                            )
                    ),
                )
            ),
            rx.cond(State.logged_in_as_admin,
                rx.vstack(
                    rx.text("ADMIN UI"),
                    rx.button("LOGOUT", on_click=State.logout),
                    rx.text("STATS"),
                    rx.text(repr(get_stats())),
                )
            ),
        ),
    )


app = rx.App()
app.add_page(index)
