"""
Hostel Service.
Manages hostel data initialization, filtering by gender, room and bed queries,
bed allocation, and bed deallocation.
Uses Encapsulation, Models, and JSONHandler.
"""

import os
from typing import List, Dict, Any, Optional
from models.hostel import Hostel
from models.room import Room
from models.bed import Bed
from utilities.json_handler import JSONHandler


class HostelService:
    """Service handling all hostel, room, and bed operations."""

    def __init__(self, data_file_path: Optional[str] = None):
        if data_file_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.__file_path = os.path.join(base_dir, "data", "hostels.json")
        else:
            self.__file_path = data_file_path

        self.initialize_default_data()

    def get_file_path(self) -> str:
        """Get file path to hostels.json."""
        return self.__file_path

    def initialize_default_data(self) -> None:
        """Initialise default hostels, rooms, and beds if hostels.json is absent or empty."""
        data = JSONHandler.read_json(self.__file_path, default_data=None)
        if not data:
            default_hostels = self.__generate_seed_hostels()
            JSONHandler.write_json(self.__file_path, default_hostels)

    def __generate_seed_hostels(self) -> List[Dict[str, Any]]:
        """Generate predefined hostels, rooms, and beds data structure."""
        hostel_configs = [
            {
                "hostel_id": "HST-M01",
                "hostel_name": "Hostel A",
                "gender_category": "Male",
                "location": "North Campus - Block A",
                "total_rooms": 4,
                "warden_id": "STF001",
                "status": "Active",
                "rooms": [
                    {"room_number": "A101", "capacity": 2},
                    {"room_number": "A102", "capacity": 2},
                    {"room_number": "A201", "capacity": 4},
                    {"room_number": "A202", "capacity": 4},
                ],
            },
            {
                "hostel_id": "HST-M02",
                "hostel_name": "Hostel B",
                "gender_category": "Male",
                "location": "North Campus - Block B",
                "total_rooms": 4,
                "warden_id": "STF001",
                "status": "Active",
                "rooms": [
                    {"room_number": "B101", "capacity": 2},
                    {"room_number": "B102", "capacity": 2},
                    {"room_number": "B201", "capacity": 4},
                    {"room_number": "B202", "capacity": 4},
                ],
            },
            {
                "hostel_id": "HST-F01",
                "hostel_name": "Hostel C",
                "gender_category": "Female",
                "location": "South Campus - Block C",
                "total_rooms": 4,
                "warden_id": "STF002",
                "status": "Active",
                "rooms": [
                    {"room_number": "C101", "capacity": 2},
                    {"room_number": "C102", "capacity": 2},
                    {"room_number": "C201", "capacity": 4},
                    {"room_number": "C202", "capacity": 4},
                ],
            },
            {
                "hostel_id": "HST-F02",
                "hostel_name": "Hostel D",
                "gender_category": "Female",
                "location": "South Campus - Block D",
                "total_rooms": 4,
                "warden_id": "STF002",
                "status": "Active",
                "rooms": [
                    {"room_number": "D101", "capacity": 2},
                    {"room_number": "D102", "capacity": 2},
                    {"room_number": "D201", "capacity": 4},
                    {"room_number": "D202", "capacity": 4},
                ],
            },
        ]

        result = []
        for h in hostel_configs:
            hostel_dict = {
                "hostel_id": h["hostel_id"],
                "hostel_name": h["hostel_name"],
                "gender_category": h["gender_category"],
                "location": h["location"],
                "total_rooms": h["total_rooms"],
                "warden_id": h["warden_id"],
                "status": h["status"],
                "rooms": [],
            }
            for r in h["rooms"]:
                beds = []
                for b_idx in range(1, r["capacity"] + 1):
                    beds.append({
                        "bed_number": f"Bed {b_idx}",
                        "room_number": r["room_number"],
                        "status": "Available",
                    })
                room_dict = {
                    "room_number": r["room_number"],
                    "hostel_id": h["hostel_id"],
                    "capacity": r["capacity"],
                    "occupied_beds": 0,
                    "room_status": "Empty",
                    "available_beds": r["capacity"],
                    "beds": beds,
                }
                hostel_dict["rooms"].append(room_dict)
            result.append(hostel_dict)

        return result

    def get_all_hostels_raw(self) -> List[Dict[str, Any]]:
        """Return raw data structure of all hostels."""
        data = JSONHandler.read_json(self.__file_path, default_data=[])
        if not data:
            self.initialize_default_data()
            data = JSONHandler.read_json(self.__file_path, default_data=[])
        return data

    def get_hostels_by_gender(self, gender: str) -> List[Hostel]:
        """Filter hostels by gender category ('Male' or 'Female')."""
        raw_list = self.get_all_hostels_raw()
        matching_hostels: List[Hostel] = []
        for item in raw_list:
            if (
                item.get("status", "Active").strip().lower() == "active"
                and item.get("gender_category", "").strip().lower() == gender.strip().lower()
            ):
                matching_hostels.append(Hostel.from_dict(item))
        return matching_hostels

    def get_hostel_by_id(self, hostel_id: str) -> Optional[Hostel]:
        """Find and return a Hostel model instance by ID."""
        raw_list = self.get_all_hostels_raw()
        for item in raw_list:
            if item.get("hostel_id") == hostel_id:
                return Hostel.from_dict(item)
        return None

    def get_available_rooms(self, hostel_id: str) -> List[Room]:
        """Get list of rooms in a hostel that have at least 1 available bed."""
        raw_list = self.get_all_hostels_raw()
        rooms: List[Room] = []
        for h in raw_list:
            if h.get("hostel_id") == hostel_id and h.get("status", "Active").lower() == "active":
                for r in h.get("rooms", []):
                    if r.get("available_beds", 0) > 0:
                        rooms.append(Room.from_dict(r))
                break
        return rooms

    def get_available_beds(self, hostel_id: str, room_number: str) -> List[Bed]:
        """Get list of available beds in a specific room."""
        raw_list = self.get_all_hostels_raw()
        beds: List[Bed] = []
        for h in raw_list:
            if h.get("hostel_id") == hostel_id:
                for r in h.get("rooms", []):
                    if r.get("room_number") == room_number:
                        for b in r.get("beds", []):
                            if b.get("status") == "Available":
                                beds.append(Bed.from_dict(b))
                        break
                break
        return beds

    def allocate_bed(self, hostel_id: str, room_number: str, bed_number: str) -> bool:
        """
        Allocate a bed to a student:
        Mark chosen bed as Occupied and recalculate room occupancy.
        """
        raw_list = self.get_all_hostels_raw()
        allocated = False

        for h in raw_list:
            if h.get("hostel_id") == hostel_id:
                for r in h.get("rooms", []):
                    if r.get("room_number") == room_number:
                        for b in r.get("beds", []):
                            if b.get("bed_number") == bed_number and b.get("status") == "Available":
                                b["status"] = "Occupied"
                                allocated = True
                                break
                        if allocated:
                            # Recalculate room occupancy
                            total_occupied = sum(1 for b in r.get("beds", []) if b.get("status") == "Occupied")
                            capacity = r.get("capacity", len(r.get("beds", [])))
                            available = max(0, capacity - total_occupied)
                            r["occupied_beds"] = total_occupied
                            r["available_beds"] = available
                            r["room_status"] = "Filled" if available == 0 else ("Empty" if total_occupied == 0 else "Available")
                        break
                break

        if allocated:
            JSONHandler.write_json(self.__file_path, raw_list)
        return allocated

    def release_bed(self, hostel_id: str, room_number: str, bed_number: str) -> bool:
        """
        Deallocate a bed (when account is deleted):
        Mark bed as Available and update room occupancy.
        """
        raw_list = self.get_all_hostels_raw()
        released = False

        for h in raw_list:
            if h.get("hostel_id") == hostel_id:
                for r in h.get("rooms", []):
                    if r.get("room_number") == room_number:
                        for b in r.get("beds", []):
                            if b.get("bed_number") == bed_number and b.get("status") == "Occupied":
                                b["status"] = "Available"
                                released = True
                        if released:
                            total_occupied = sum(1 for b in r.get("beds", []) if b.get("status") == "Occupied")
                            capacity = r.get("capacity", len(r.get("beds", [])))
                            available = max(0, capacity - total_occupied)
                            r["occupied_beds"] = total_occupied
                            r["available_beds"] = available
                            r["room_status"] = "Empty" if total_occupied == 0 else ("Filled" if available == 0 else "Available")
                        break
                break

        if released:
            JSONHandler.write_json(self.__file_path, raw_list)
        return released
