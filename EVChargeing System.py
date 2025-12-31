# Design the low‑level architecture of a multi‑level electric vehicle (EV) charging station. The station will have several charging points spread across multiple floors. Each point can support different charging standards such as Level 1 AC, Level 2 AC, and DC Fast Charging. The system must handle allocation of charging points, monitor charging sessions, enforce safety limits, and allow future expansion to new charging types or additional levels.
#
# Manage multiple charging points on each level.
# Support three charging types with different power requirements.
# Allocate a free point to a vehicle based on the requested charging level.
# Track start time, end time, energy delivered, and cost for each session.
# Enforce maximum current/power per point and per level for safety.
# Provide real‑time status (available, in‑use, fault) for each point.
# Allow addition of new levels or new charging types without major code changes.
# Persist session data for reporting and billing.
# Design a set of classes, interfaces, and relationships that satisfy the above requirements. Indicate which design patterns (for example, Factory, Strategy, Observer) you would use and why. Explain how your design supports scalability, extensibility, and efficient resource management.


from abc import ABC, abstractmethod
from enum import Enum
import time

# ---------------- ENUMS ----------------

class ChargingType(Enum):
    Level1AC = "Level1AC"
    Level2AC = "Level2AC"
    DCFast   = "DCFast"

class Status(Enum):
    Free = 'FREE'
    Fault = 'FAULT'
    Occupied = 'OCCUPIED'

# ---------------- VEHICLE ----------------

class Veichle:
    def __init__(self, curr_charge, charge_type: ChargingType):
        self.curr_charge = curr_charge
        self.charge_type = charge_type

# ---------------- STRATEGY ----------------

class ChargingStarategy(ABC):
    @abstractmethod
    def charge_and_pay(self, vechile: Veichle):
        pass

class Level1ACcharge(ChargingStarategy):
    def charge_and_pay(self, vechile: Veichle):
        unit_price = 5
        charge = vechile.curr_charge
        total_units = 0

        while charge < 100:   # FIXED
            charge += 5
            total_units += 1

        return total_units * unit_price

class Level2ACcharge(ChargingStarategy):
    def charge_and_pay(self, vechile: Veichle):
        unit_price = 10
        charge = vechile.curr_charge
        total_units = 0

        while charge < 100:   # FIXED
            charge += 10
            total_units += 1

        return total_units * unit_price

class DSFastcharge(ChargingStarategy):
    def charge_and_pay(self, vechile: Veichle):
        unit_price = 50
        charge = vechile.curr_charge
        total_units = 0

        while charge < 100:   # FIXED
            charge += 20
            total_units += 1

        return total_units * unit_price

# ---------------- FACTORY ----------------

class ChargingFactory:
    @staticmethod
    def charing_factroy(vechile: Veichle):
        if vechile.charge_type == ChargingType.Level1AC:
            return Level1ACcharge()
        elif vechile.charge_type == ChargingType.Level2AC:
            return Level2ACcharge()
        elif vechile.charge_type == ChargingType.DCFast:
            return DSFastcharge()
        else:
            raise ValueError("Invalid Charging Type")

# ---------------- POINT ----------------

class Point:
    def __init__(self, level_type: ChargingType):
        self.level_type = level_type
        self.status = Status.Free   # FIXED

# ---------------- LEVEL ----------------

class ChargingLevel:
    def __init__(self, cols, level_type: ChargingType):
        self.points = [Point(level_type) for _ in range(cols)]  # FIXED

    def get_free_point(self):
        for point in self.points:
            if point.status == Status.Free:
                return point
        return None

# ---------------- AREA ----------------

class ChargingArea:
    def __init__(self):
        self.levels = []   # FIXED

    def add_level(self, level: ChargingLevel):
        self.levels.append(level)

    def allocate_point(self, charge_type: ChargingType):
        for level in self.levels:
            point = level.get_free_point()
            if point and point.level_type == charge_type:
                point.status = Status.Occupied
                return point
        return None


    def display_area(self):
        print("\n--- Charging Area Status ---")
        for idx, level in enumerate(self.levels):
            level_type = level.points[0].level_type.value
            print(f"Level {idx} ({level_type}): ", end="")

            for point in level.points:
                if point.status == Status.Free:
                    print("F", end=" ")
                elif point.status == Status.Occupied:
                    print("O", end=" ")
                else:
                    print("X", end=" ")
            print()



class EVChargingService:
    def __init__(self, charging_area: ChargingArea, charging_factory: ChargingFactory):
        self.charging_area = charging_area
        self.charging_factory = charging_factory

    def charge_vechile(self, vechile: Veichle):
        point = self.charging_area.allocate_point(vechile.charge_type)

        if not point:
            print("No charging point available")
            return

        strategy = self.charging_factory.charing_factroy(vechile)  # FIXED
        cost = strategy.charge_and_pay(vechile)

        print(f"Charging started for {vechile.charge_type.value}")
        print(f"Total cost: ₹{cost}")

# ---------------- MAIN ----------------

if __name__ == "__main__":
    charging_area = ChargingArea()

    charging_area.add_level(ChargingLevel(10, ChargingType.Level1AC))
    charging_area.add_level(ChargingLevel(10, ChargingType.Level1AC))
    charging_area.add_level(ChargingLevel(8, ChargingType.Level2AC))
    charging_area.add_level(ChargingLevel(5, ChargingType.DCFast))

    charging_factory = ChargingFactory()
    ev_service = EVChargingService(charging_area, charging_factory)

    vechile1 = Veichle(0, ChargingType.Level1AC)
    vechile2 = Veichle(0, ChargingType.DCFast)
    charging_area.display_area()
    ev_service.charge_vechile(vechile1)
    ev_service.charge_vechile(vechile2)

    charging_area.display_area()

