BEGIN;

CREATE SCHEMA Lost_Found;
CREATE SCHEMA Accounts;


SET search_path TO Accounts;

CREATE TYPE RoleEnum AS ENUM (
    'user',
    'worker',
    'admin'
);

CREATE TABLE IF NOT EXISTS Accounts (
    email TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role RoleEnum NOT NULL
);


SET search_path TO Lost_Found;

CREATE TYPE ColorEnum AS ENUM (
    'red',
    'green',
    'blue',
    'yellow',
    'orange',
    'purple',
    'pink',
    'brown',
    'black',
    'white',
    'gray',
    'cyan',
    'beige',
    'other'
);

CREATE TYPE StatusEnum AS ENUM ('lost', 'found', 'confirmed');

CREATE TYPE SizeEnum AS ENUM ('xs', 's', 'm', 'l', 'xl');

CREATE TYPE MaterialEnum AS ENUM (
    'wood',
    'metal',
    'plastic',
    'glass',
    'ceramic',
    'fabric',
    'leather',
    'rubber',
    'paper',
    'other'
);

CREATE TYPE PersonalItemType AS ENUM (
    'id_card',
    'passport',
    'keys',
    'credit_debit_card',
    'other'
);

CREATE TYPE JeweleryType AS ENUM (
    'ring',
    'earrings',
    'necklace',
    'piercing',
    'other'
);

CREATE TYPE AccessoryType AS ENUM (
    'glasses',
    'sunglasses',
    'wristwatch',
    'other'
);

CREATE TYPE TravelItemType AS ENUM (
    'suitcase',
    'handbag',
    'backpack',
    'luggage',
    'umbrella',
    'wallet',
    'purse',
    'water_bottle',
    'other'
);

CREATE TYPE ElectronicDeviceType AS ENUM (
    'phone',
    'laptop',
    'tablet',
    'cable',
    'earbuds',
    'headphones',
    'camera',
    'smartwatch',
    'powerbank',
    'other'
);

CREATE TYPE ClothingType AS ENUM (
    'coat',
    'jacket',
    'gloves',
    'scarf',
    'hat',
    'shoes',
    'other'
);

CREATE TYPE OfficeItemType AS ENUM (
    'pen',
    'folder',
    'book',
    'other'
);


-- TABLES
CREATE TABLE IF NOT EXISTS PersonalItems (
    id SERIAL PRIMARY KEY,
    type PersonalItemType NOT NULL,
    color ColorEnum NOT NULL,
    description TEXT,
    status StatusEnum NOT NULL,
    email TEXT REFERENCES Accounts.Accounts NOT NULL
);

CREATE TABLE IF NOT EXISTS Jewelry (
    id SERIAL PRIMARY KEY,
    type JeweleryType NOT NULL,
    color ColorEnum NOT NULL,
    size SizeEnum NOT NULL,
    description TEXT,
    status StatusEnum NOT NULL,
    email TEXT REFERENCES Accounts.Accounts NOT NULL
);

CREATE TABLE IF NOT EXISTS Accessories (
    id SERIAL PRIMARY KEY,
    type AccessoryType NOT NULL,
    color ColorEnum NOT NULL,
    material MaterialEnum NOT NULL,
    brand TEXT,
    description TEXT,
    status StatusEnum NOT NULL,
    email TEXT REFERENCES Accounts.Accounts NOT NULL
);

CREATE TABLE IF NOT EXISTS TravelItems (
    id SERIAL PRIMARY KEY,
    type TravelItemType NOT NULL,
    color ColorEnum NOT NULL,
    size SizeEnum NOT NULL,
    material MaterialEnum NOT NULL,
    brand TEXT,
    description TEXT,
    status StatusEnum NOT NULL,
    email TEXT REFERENCES Accounts.Accounts NOT NULL
);

CREATE TABLE IF NOT EXISTS ElectronicDevices (
    id SERIAL PRIMARY KEY,
    type ElectronicDeviceType NOT NULL,
    color ColorEnum NOT NULL,
    material MaterialEnum NOT NULL,
    brand TEXT,
    description TEXT,
    status StatusEnum NOT NULL,
    email TEXT REFERENCES Accounts.Accounts NOT NULL
);

CREATE TABLE IF NOT EXISTS Clothing (
    id SERIAL PRIMARY KEY,
    type ClothingType NOT NULL,
    color ColorEnum NOT NULL,
    size SizeEnum NOT NULL,
    material MaterialEnum NOT NULL,
    brand TEXT,
    description TEXT,
    status StatusEnum NOT NULL,
    email TEXT REFERENCES Accounts.Accounts NOT NULL
);

CREATE TABLE IF NOT EXISTS OfficeItems (
    id SERIAL PRIMARY KEY,
    type OfficeItemType NOT NULL,
    color ColorEnum NOT NULL,
    size SizeEnum NOT NULL,
    material MaterialEnum NOT NULL,
    name TEXT,
    description TEXT,
    status StatusEnum NOT NULL,
    email TEXT REFERENCES Accounts.Accounts NOT NULL
);

CREATE TABLE IF NOT EXISTS OtherItems (
    id SERIAL PRIMARY KEY,
    type TEXT,
    color ColorEnum NOT NULL,
    size SizeEnum NOT NULL,
    material MaterialEnum NOT NULL,
    brand TEXT,
    name TEXT,
    description TEXT,
    status StatusEnum NOT NULL,
    email TEXT REFERENCES Accounts.Accounts NOT NULL
);

DO $$ BEGIN
    CREATE TYPE matchstatus AS ENUM ('unconfirmed', 'confirmed', 'declined');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS Match (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    lost_item_id INTEGER NOT NULL,
    found_item_id INTEGER NOT NULL,
    status matchstatus NOT NULL
    percentage INTEGER NOT NULL
);

COMMIT;
