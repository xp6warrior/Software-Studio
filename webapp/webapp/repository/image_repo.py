import os
# TODO Handle situation when filename is None or contains /../ in it
def get_image(filename: str) -> bytes:
    file_path = os.getenv("IMAGE_STORE_PATH")
    if file_path is None or not isinstance(file_path, str):
        raise Exception("IMAGE_STORE_PATH not set to string path!")

    file_path += "/" + filename
    with open(file_path, "rb") as f:
        image_bytes = f.read()
    
    return image_bytes

def save_image(filename: str, image_bytes: bytes):
    file_path = os.getenv("IMAGE_STORE_PATH")
    if file_path is None or not isinstance(file_path, str):
        raise Exception("IMAGE_STORE_PATH not set to string path!")
    
    file_path += "/" + filename
    if os.path.exists(file_path):
        raise Exception(f"File {file_path} already exists!")

    with open(file_path, "wb") as f:
        f.write(image_bytes)

def update_image(filename: str, image_bytes: bytes):
    file_path = os.getenv("IMAGE_STORE_PATH")
    if file_path is None or not isinstance(file_path, str):
        raise Exception("IMAGE_STORE_PATH not set to string path!")
    
    file_path += "/" + filename
    if not os.path.exists(file_path):
        raise Exception(f"File {file_path} doesn't exist!")

    os.remove(file_path)
    with open(file_path, "wb") as f:
        f.write(image_bytes)

def delete_image(filename: str):
    file_path = os.getenv("IMAGE_STORE_PATH")
    if file_path is None or not isinstance(file_path, str):
        raise Exception("IMAGE_STORE_PATH not set to string path!")
    
    file_path += "/" + filename
    if not os.path.exists(file_path):
        raise Exception(f"File {file_path} doesn't exist!")

    os.remove(file_path)