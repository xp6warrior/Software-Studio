import reflex as rx

from rxconfig import config

#from webapp.backend.service.login_service import create_user, login_user

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

#from webapp.backend.service.lost_item_service import *
	
def get_notifications(email):
	return ["Your item 456 was matched and is ready for pickup"]
	
def submit_found_item(item_json):
	pass

def get_found_items_and_their_matches():
	return [{"Item":{"ID":"123","Name": "Watch", "Color": "Black"}, "Matches": [{"ID":"534","Name": "Watch", "Color": "Black"}]}]
	
def confirm_match(lost_item_json, found_item_json):
	pass

def get_confirmed_matches_with_user_pesel():
	return [{"Item":{"ID":"456","Name": "Pen", "Color": "Blue", "Brand": "ParkerS"}, "PESEL": "123456789"}]

def get_stats():
	return [{"Number of lost items": "2","Number of found items": "2"}, {"Number of matches": "1"}]

class State(rx.State):
	email: str=""
	password: str=""
	result: str=""
	logged_in_as_user: bool= False
	logged_in_as_worker: bool= False
	logged_in_as_admin: bool= False
	not_logged_in: bool=True
	
	temp: str=""
	model: str=""
	item_type: str=""
	size: str=""
	material: str=""
	brand: str="" 
	name: str=""
	color: str=""
	desc: str=""
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
		if len(self.email.split("@"))-1==0 or len(self.email.split("."))-1==0:
			self.result=f"INVALID EMAIL FORMAT"
			return
		temp=login_user(self.email, self.password)
		if temp==False:
			self.result=f"INCORRECT EMAIL OR PASSWORD"
		elif temp=="USER":
			self.logged_in_as_user=True
			self.not_logged_in=False
		elif temp=="WORKER":
			self.logged_in_as_worker=True
			self.not_logged_in=False
		elif temp=="ADMIN":
			self.logged_in_as_admin=True
			self.not_logged_in=False
	def logout(self):
		self.logged_in_as_user= False
		self.logged_in_as_worker= False
		self.logged_in_as_admin= False
		self.not_logged_in=True
	
	def set_model(self, model: str):
		self.model=model
		self.item_type=""
		self.size=""
		self.material=""
		self.brand=""
		self.name=""
		self.color=""
		self.desc=""
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
	
	def call_submit_lost_item(self):
		item={"model": self.model, "type": self.item_type, "size": self.size, "material": self.material, "brand": self.brand, "name": self.name, "color": self.color, "desc":self.desc}
		self.temp=repr(item)
		submit_lost_item(State.email,item)
	def call_submit_found_item(self):
		item={"model": self.model, "type": self.item_type, "size": self.size, "material": self.material, "brand": self.brand, "name": self.name, "color": self.color, "desc":self.desc}
		submit_found_item(item)
def index() -> rx.Component:
	return rx.cond(State.not_logged_in,
		rx.vstack(
			rx.input(
				placeholder="Email",
				on_change=State.set_email,
			),
			rx.input(
				placeholder="Password",
				on_change=State.set_password,
			),
			rx.button("Login", on_click=State.login),
			rx.text(State.result),
		),
		rx.vstack(
			rx.cond(State.logged_in_as_user,
				rx.vstack(
					rx.text("USER UI"),
					rx.button("LOGOUT", on_click=State.logout),
					rx.text("SUBMIT NEW LOST ITEM FORM HERE"),
					rx.vstack(
							rx.text("ITEM TYPE"),
							rx.select(
								items=["personal_items","jewelry","accessories","travel_items","electronic_devices","clothing","office_items","other_items"],
								value=State.model,
								on_change=State.set_model,
								placeholder="",
        						),
        						rx.cond((State.model == "personal_items"),
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
        						rx.cond((State.model == "jewelry"),
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
        						rx.cond((State.model == "accessories"),
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
        						rx.cond((State.model == "travel_items"),
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
        						rx.cond((State.model == "electronic_devices"),
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
        						rx.cond((State.model == "clothing"),
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
        						rx.cond((State.model == "office_items"),
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
        						rx.cond((State.model == "other_items"),
								rx.vstack(
									rx.text("TYPE OF OTHER ITEM"),
									rx.input(
										placeholder="Type of other item",
										on_change=State.set_item_type,
									),
								),
        						),
							rx.cond((State.model == "jewelry") | (State.model == "travel_items") | (State.model == "clothing") | (State.model == "office_items") | (State.model == "other_items"),
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
        						rx.cond((State.model == "accessories") | (State.model == "travel_items") | (State.model == "electronic_devices") | (State.model == "clothing") | (State.model == "office_items") | (State.model == "other_items"),
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
        						rx.cond((State.model == "accessories") | (State.model == "travel_items") | (State.model == "electronic_devices") | (State.model == "clothing") | (State.model == "office_items") | (State.model == "other_items"),
								rx.vstack(
									rx.text("BRAND"),
									rx.input(
										placeholder="Brand",
										on_change=State.set_brand,
									),
								),
        						),
        						rx.cond((State.model == "other_items"),
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
					rx.text(repr(get_submitted_lost_items(State.email))),
					rx.text(repr(get_notifications(State.email))),
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
								value=State.model,
								on_change=State.set_model,
								placeholder="",
        						),
        						rx.cond((State.model == "personal_items"),
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
        						rx.cond((State.model == "jewelry"),
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
        						rx.cond((State.model == "accessories"),
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
        						rx.cond((State.model == "travel_items"),
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
        						rx.cond((State.model == "electronic_devices"),
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
        						rx.cond((State.model == "clothing"),
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
        						rx.cond((State.model == "office_items"),
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
        						rx.cond((State.model == "other_items"),
								rx.vstack(
									rx.text("TYPE OF OTHER ITEM"),
									rx.input(
										placeholder="Type of other item",
										on_change=State.set_item_type,
									),
								),
        						),
							rx.cond((State.model == "jewelry") | (State.model == "travel_items") | (State.model == "clothing") | (State.model == "office_items") | (State.model == "other_items"),
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
        						rx.cond((State.model == "accessories") | (State.model == "travel_items") | (State.model == "electronic_devices") | (State.model == "clothing") | (State.model == "office_items") | (State.model == "other_items"),
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
        						rx.cond((State.model == "accessories") | (State.model == "travel_items") | (State.model == "electronic_devices") | (State.model == "clothing") | (State.model == "office_items") | (State.model == "other_items"),
								rx.vstack(
									rx.text("BRAND"),
									rx.input(
										placeholder="Brand",
										on_change=State.set_brand,
									),
								),
        						),
        						rx.cond((State.model == "other_items"),
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
					rx.text(repr(get_found_items_and_their_matches())),
					rx.text("CONFIRMED MATCHES AND OWNER PESEL"),
					rx.text(repr(get_confirmed_matches_with_user_pesel())),
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
