from flask import Flask, request, redirect, render_template_string
import json, os

app = Flask(__name__)
DATA_FILE = "rooms.json"

def load_rooms():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save_rooms(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET","POST"])
def index():
    rooms = load_rooms()

    selected_area = request.args.get("area")
    areas = sorted(set(r["area"] for r in rooms))

    if not selected_area and areas:
        selected_area = areas[0]

    if request.method == "POST":
        room_no = request.form.get("room_no")
        room_area = request.form.get("area")
        month = request.form.get("month")
        status = request.form.get("status")
        phone = request.form.get("phone")

        for r in rooms:
            if r["room"] == room_no and r["area"] == room_area:
                if month:
                    r["paid"][month] = not r["paid"][month]
                if status:
                    r["status"] = status
                if phone is not None:
                    r["phone"] = phone
                break

        save_rooms(rooms)
        return redirect(f"/?area={selected_area}")

    # Filter rooms for selected area
    area_rooms = [r for r in rooms if r["area"] == selected_area]

    # Assign display numbers per area
    numbered_rooms = []
    for idx, r in enumerate(area_rooms, start=1):
        r_copy = r.copy()
        r_copy["display_number"] = idx
        numbered_rooms.append(r_copy)

    # --- Calculate per-area summary ---
    total_area = len(area_rooms)
    available_area = sum(1 for r in area_rooms if r["status"] == "available")

    # --- Calculate overall summary ---
    total_rooms_all = len(rooms)
    total_available_all = sum(1 for r in rooms if r["status"] == "available")

    html = """
    <style>
    body {font-family: 'Segoe UI', Tahoma, sans-serif; background:#f0f4f8; margin:20px;}
    h2 {color:#1E90FF; margin-bottom:15px;}
    .summary-top {
        background:#1E90FF; color:white; padding:15px; border-radius:8px;
        font-weight:bold; margin-bottom:20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .tabs {margin-bottom:20px;}
    .tab {
        display:inline-block; padding:10px 18px; margin:4px;
        border-radius:25px; background:#4682B4; color:white; font-weight:bold;
        text-decoration:none; transition:0.3s;
    }
    .tab:hover {background:#5A9BD5;}
    .active {background:#1E90FF; color:white;}
    .main-container {display:flex; flex-wrap:wrap; align-items:flex-start;}
    table.main {border-collapse:collapse; width:70%; background:white; border-radius:6px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.1);}
    table.main th, table.main td {
        border:1px solid #ddd;  /* restore borders */
        padding:10px;
        text-align:center;
    }
    table.main th {background:#1E90FF; color:white;}
    table.main tr:nth-child(even){background:#f9f9f9;}
    table.side {
        border-collapse:collapse; width:20%; margin-left:20px; background:#e6f2ff; border-radius:6px;
        font-size:14px; text-align:center; padding:5px; box-shadow:0 2px 5px rgba(0,0,0,0.05);
    }
    table.side th, table.side td {border:1px solid #99ccff; padding:6px;}
    table.side th {background:#3399FF; color:white; font-size:15px;}
    button {border:none; border-radius:6px; cursor:pointer;}
    input[type=text]{padding:4px; width:90%; border-radius:6px; border:1px solid #ccc;}
    .paid-btn {font-size:12px; padding:4px 6px; border-radius:6px; color:white;}
    .paid-container {display:flex; flex-wrap:nowrap; overflow-x:auto; justify-content:center; gap:4px;}
    </style>

    <!-- Overall summary -->
    <div class="summary-top">
        Overall Total Rooms: {{total_rooms_all}} &nbsp;&nbsp; | &nbsp;&nbsp;
        Overall Available: {{total_available_all}}
    </div>

    <!-- Island tabs -->
    <div class="tabs">
    {% for a in areas %}
        <a class="tab {% if a==selected_area %}active{% endif %}" href="/?area={{a}}">
            {{a}}
        </a>
    {% endfor %}
    </div>

    <div class="main-container">
    <!-- Main table -->
    <table class="main">
        <tr>
            <th>Room</th>
            <th>Status</th>
            <th>Paid (Jan–Dec)</th>
            <th>Phone</th>
        </tr>
        {% for r in numbered_rooms %}
        <tr>
            <td>{{r.display_number}}</td>
            <td>
                <form method="post">
                    <input type="hidden" name="room_no" value="{{r.room}}">
                    <input type="hidden" name="area" value="{{r.area}}">
                    <select name="status" onchange="this.form.submit()" style="padding:4px; border-radius:6px;">
                        <option value="available" {% if r.status=='available' %}selected{% endif %}>Available</option>
                        <option value="occupied" {% if r.status=='occupied' %}selected{% endif %}>Occupied</option>
                        <option value="booking" {% if r.status=='booking' %}selected{% endif %}>Booking</option>
                    </select>
                </form>
            </td>
            <td>
                <div class="paid-container">
                {% for month, paid in r.paid.items() %}
                    <form method="post" style="display:inline;">
                        <input type="hidden" name="room_no" value="{{r.room}}">
                        <input type="hidden" name="area" value="{{r.area}}">
                        <input type="hidden" name="month" value="{{month}}">
                        <button class="paid-btn" style="
                            background:{% if paid %}#28a745{% else %}#dc3545{% endif %};
                        ">
                            {{month}}
                        </button>
                    </form>
                {% endfor %}
                </div>
            </td>
            <td>
                <form method="post">
                    <input type="hidden" name="room_no" value="{{r.room}}">
                    <input type="hidden" name="area" value="{{r.area}}">
                    <input type="text" name="phone" value="{{r.phone}}" placeholder="Enter phone">
                    <button type="submit" style="padding:4px 8px; margin-left:4px; background:#1E90FF; color:white;">Save</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>

    <!-- Compact per-area summary -->
    <table class="side">
        <tr><th>Area Summary</th></tr>
        <tr><td>Total: {{total_area}}</td></tr>
        <tr><td>Available: {{available_area}}</td></tr>
    </table>
    </div>
    """

    return render_template_string(
        html,
        numbered_rooms=numbered_rooms,
        areas=areas,
        selected_area=selected_area,
        total_area=total_area,
        available_area=available_area,
        total_rooms_all=total_rooms_all,
        total_available_all=total_available_all
    )

if __name__ == "__main__":
    app.run()

