from enum import Enum
import time
import uuid

# ---------------- ENUMS ----------------

class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3

class SpotSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class SpotStatus(Enum):
    FREE = 1
    OCCUPIED = 2

# ---------------- VEHICLE ----------------

class Vehicle:
    def __init__(self, number, vehicle_type):
        self.number = number
        self.type = vehicle_type

# ---------------- PARKING SPOT ----------------

class ParkingSpot:
    def __init__(self, spot_id, size):
        self.spot_id = spot_id
        self.size = size
        self.status = SpotStatus.FREE

    def can_fit(self, vehicle):
        if vehicle.type == VehicleType.MOTORCYCLE:
            return True
        if vehicle.type == VehicleType.CAR:
            return self.size in (SpotSize.MEDIUM, SpotSize.LARGE)
        if vehicle.type == VehicleType.BUS:
            return self.size == SpotSize.LARGE

# ---------------- PARKING FLOOR ----------------

def find_spots(self, vehicle):
    if vehicle.type != VehicleType.BUS:
        return next(
            ([s] for s in self.spots if s.status == SpotStatus.FREE and s.can_fit(vehicle)),
            None
        )

    prev = None
    for s in self.spots:
        if s.status == SpotStatus.FREE and s.size == SpotSize.LARGE:
            if prev:
                return [prev, s]
            prev = s
        else:
            prev = None
    return None

# ---------------- TICKET ----------------

class ParkingTicket:
    def __init__(self, vehicle, spots):
        self.ticket_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.spots = spots
        self.entry_time = time.time()
        self.exit_time = None

    def close(self):
        self.exit_time = time.time()

    def calculate_fee(self):
        hours = int((self.exit_time - self.entry_time) / 3600) + 1
        rates = {
            VehicleType.MOTORCYCLE: 10,
            VehicleType.CAR: 20,
            VehicleType.BUS: 50
        }
        return hours * rates[self.vehicle.type]

# ---------------- PARKING LOT ----------------

class ParkingLot:
    def __init__(self, floors):
        self.floors = floors
        self.active_tickets = {}

    def park_vehicle(self, vehicle):
        for floor in self.floors:
            spots = floor.find_spots(vehicle)
            if spots:
                for spot in spots:
                    spot.status = SpotStatus.OCCUPIED
                ticket = ParkingTicket(vehicle, spots)
                self.active_tickets[ticket.ticket_id] = ticket
                return ticket
        print("No spot available")
        return None

    def exit_vehicle(self, ticket_id):
        ticket = self.active_tickets.pop(ticket_id)
        ticket.close()
        for spot in ticket.spots:
            spot.status = SpotStatus.FREE
        return ticket.calculate_fee()

# ---------------- DISPLAY BOARD ----------------

class DisplayBoard:
    def show(self, floors):
        print("\n--- Parking Status ---")
        for floor in floors:
            free = sum(1 for s in floor.spots if s.status == SpotStatus.FREE)
            print(f"Floor {floor.floor_id}: Free Spots = {free}")

# ---------------- MAIN ----------------

if __name__ == "__main__":
    # Create floors
    floor1_spots = [ParkingSpot(i, SpotSize.MEDIUM) for i in range(5)]
    floor2_spots = [ParkingSpot(i, SpotSize.LARGE) for i in range(6)]

    floor1 = ParkingFloor(1, floor1_spots)
    floor2 = ParkingFloor(2, floor2_spots)

    parking_lot = ParkingLot([floor1, floor2])
    display = DisplayBoard()

    # Vehicles
    car = Vehicle("KA-01-1234", VehicleType.CAR)
    bus = Vehicle("KA-02-9999", VehicleType.BUS)

    # Park vehicles
    ticket1 = parking_lot.park_vehicle(car)
    ticket2 = parking_lot.park_vehicle(bus)

    display.show(parking_lot.floors)

    # Exit vehicles
    time.sleep(1)
    fee1 = parking_lot.exit_vehicle(ticket1.ticket_id)
    fee2 = parking_lot.exit_vehicle(ticket2.ticket_id)

    print("\nCar Fee:", fee1)
    print("Bus Fee:", fee2)

    display.show(parking_lot.floors)
