import os
from django.test import TestCase

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
FIXTURES_DIR = os.path.join(CURRENT_DIR, "fixtures")

FIXTURES = [
    os.path.join(FIXTURES_DIR, "product.json"),
    os.path.join(FIXTURES_DIR, "discount.json"),
    os.path.join(FIXTURES_DIR, "shop.json"),
    os.path.join(FIXTURES_DIR, "attribute.json"),
]

TEST_ID = 1

PRODUCT_DATA = {
    1: {
        "info":
            {
                "title": "Acer Nitro 5 AN515-55-53E5 Gaming Laptop",
                "short_description": "Traditional Laptop Computers by Acer",
                "short_description_en": "Traditional Laptop Computers by Acer",
                "category": 5,
                "tags": [1, 2, 3],
            },
        "attributes":
            {
                "CPU (speed)": 4.5,
                "CPU (Model)": "Core i5-10300H",
                "Processor Count": 4,
                "CPU (Model Manufacturer)": "Intel",
                "Display Resolution": "1920 x 1080",
                "Graphics": "NVIDIA GeForce RTX 3050",
                "Hard Disk": "SSD",
                "Hard Disk Size": "256",
                "RAM size": "8",
                "RAM Type": "DDR4 SDRAM",
                "USB 3.0 Ports": "4",
                "USB 2.0 Ports": "0",
                "Operating System": "Windows 11 Home",
                "Wireless": "Bluetooth, WiFi",
                "Optical Drive": "No",
                "Voltage": "240",
                "Batteries": "1 Lithium ion batteries required. (included)",
                "Battery Life": "11",
                "Power Source": "Battery Powered",
                "Item Dimension (length)": "14.31",
                "Item Dimensions (height)": "0.94",
                "Item Dimensions (width)": "10.04",
                "Weight": "5.07",
                "Color": "Black",
            },
        "shop":
            {
                ("Computer Shop", "1500.00"),
                ("Universal Shop", "2169.00"),
                ("Electronic Shop", "3795.00"),
                ("Computer Shop", "3143.00"),
            },
    },
    36: {
        "info":
            {
                "title": "CYBERRPOWERPC Gamer Xtreme VR Gaming PC",
                "short_description": "Tower Computers by CyberpowerPC",
                "short_description_en": "Tower Computers by CyberpowerPC",
                "category": 5,
                "tags": [3, 38, 39],
            },
        "attributes":
            {
                "CPU (speed)": 4.5,
                "CPU (Model)": "Core i5-10300H",
                "Processor Count": 4,
                "CPU (Model Manufacturer)": "Intel",
                "Display Resolution": "1920 x 1080",
                "Graphics": "NVIDIA GeForce RTX 3050",
                "Hard Disk": "SSD",
                "Hard Disk Size": "256",
                "RAM size": "8",
                "RAM Type": "DDR4 SDRAM",
                "USB 3.0 Ports": "4",
                "USB 2.0 Ports": "0",
                "Operating System": "Windows 11 Home",
                "Wireless": "Bluetooth, WiFi",
                "Optical Drive": "No",
                "Voltage": "240",
                "Batteries": "1 Lithium ion batteries required. (included)",
                "Battery Life": "11",
                "Power Source": "Battery Powered",
                "Item Dimension (length)": "14.31",
                "Item Dimensions (height)": "0.94",
                "Item Dimensions (width)": "10.04",
                "Weight": "5.07",
                "Color": "Black",
            },
        "shop":
            {
                ("Computer Shop", "3400.00"),
                ("Universal Shop", "417.00"),
                ("Electronic Shop", "3116.00"),
                ("Computer Shop", "2983.00"),
            },
    }
}
USER_DATA = {
    "email": "test@test.test",
    "password": "Qwe123456!",
    "first_name": "Name",
    "last_name": "Surname",
    # "": "",
    # "": "",
}

REVIEW_CNT = 5


class ProductDetailMixin(TestCase):
    base_url = "/products/"
    template_name = "product/product.html"
    fixtures = FIXTURES
