import json

areas = {
    "Putatan Lot 1": 11,
    "Putatan Lot 2": 10,

    "Segama - 2nd Floor": 13,
    "Segama - 3rd Floor": 12,

    "Beverly - 1st Floor": 13,
    "Beverly - 2nd Floor": 13,

    "CFC - 1st Floor": 18,
    "CFC - 2nd Floor": 16,
    "CFC - 3rd Floor": 16,

    "Asia City - 1st Floor": 14,
    "Asia City - 2nd Floor": 14,

    "Mart - 1st Floor": 17,
    "Mart - 2nd Floor": 16,
    "Mart - 3rd Floor": 16,

    "Damai": 15,

    "Pizza - 3rd Floor": 12,
    "Pizza - 4th Floor": 13,

    "Bandaran - 1st Floor": 19,
    "Bandaran - 2nd Floor": 20,
    "Bandaran - 3rd Floor": 20,

    "Bataras": 17
}

rooms = []

for area, count in areas.items():
    prefix = area.split()[0][:2].upper()
    for i in range(1, count + 1):
        room = {
            "area": area,
            "room": f"{prefix}-{str(i).zfill(2)}",
            "status": "available",
            "phone": "",
            "paid": {
                "Jan": False, "Feb": False, "Mar": False, "Apr": False,
                "May": False, "Jun": False, "Jul": False, "Aug": False,
                "Sep": False, "Oct": False, "Nov": False, "Dec": False
            }
        }
        rooms.append(room)

with open("rooms.json", "w") as f:
    json.dump(rooms, f, indent=2)

print("✅ rooms.json generated successfully!")
