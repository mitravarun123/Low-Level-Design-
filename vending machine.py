from abc import ABC, abstractmethod
from enum import Enum


# ================= ENUMS =================
class ProductType(Enum):
    COKE = "Coke"
    PEPSI = "Pepsi"
    WATER = "Water"


# ================= MODELS =================
class Product:
    def __init__(self, product_type: ProductType, price: int):
        self.product_type = product_type
        self.price = price


class Inventory:
    def __init__(self):
        self.stock = {}

    def add_product(self, product: Product, quantity: int):
        self.stock[product.product_type] = {
            "product": product,
            "quantity": quantity
        }

    def is_available(self, product_type):
        return (
            product_type in self.stock
            and self.stock[product_type]["quantity"] > 0
        )

    def dispense(self, product_type):
        if not self.is_available(product_type):
            raise Exception("Product out of stock")

        self.stock[product_type]["quantity"] -= 1
        return self.stock[product_type]["product"]


# ================= PAYMENT STRATEGY =================
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class CashPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid ₹{amount} using Cash")
        return amount


class CardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid ₹{amount} using Card")
        return amount


class PaymentFactory:
    @staticmethod
    def get_payment_method(method):
        if method == "cash":
            return CashPayment()
        elif method == "card":
            return CardPayment()
        else:
            raise Exception("Invalid payment method")


# ================= VENDING MACHINE =================
class VendingMachine:
    def __init__(self):
        self.inventory = Inventory()
        self.selected_product = None
        self.amount_paid = 0

    def select_product(self, product_type: ProductType):
        if not self.inventory.is_available(product_type):
            raise Exception("Product not available")

        self.selected_product = self.inventory.stock[product_type]["product"]
        self.amount_paid = 0
        print(f"Selected {product_type.value} | Price: ₹{self.selected_product.price}")

    def make_payment(self, payment_method):
        if not self.selected_product:
            raise Exception("Select product first")

        payment = PaymentFactory.get_payment_method(payment_method)
        self.amount_paid += payment.pay(self.selected_product.price)

    def dispense(self):
        if not self.selected_product:
            raise Exception("No product selected")

        if self.amount_paid < self.selected_product.price:
            raise Exception("Insufficient payment")

        product = self.inventory.dispense(self.selected_product.product_type)
        print(f"Dispensed {product.product_type.value}")

        change = self.amount_paid - product.price
        if change > 0:
            print(f"Returned change: ₹{change}")

        self._reset()

    def _reset(self):
        self.selected_product = None
        self.amount_paid = 0


# ================= CLIENT =================
if __name__ == "__main__":
    vm = VendingMachine()

    vm.inventory.add_product(Product(ProductType.COKE, 25), 5)
    vm.inventory.add_product(Product(ProductType.WATER, 15), 3)

    vm.select_product(ProductType.COKE)
    vm.make_payment("cash")
    vm.dispense()
