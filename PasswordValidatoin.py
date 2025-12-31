# Design a low-level system for validating passwords that can apply different validation rules based on user roles (e.g., admin, regular user, super admin).
#
# Your design should prioritize extensibility, allowing for easy addition of new roles and corresponding password rules without modifying existing code. Consider common password complexity requirements (minimum length, special characters, numbers, uppercase/lowercase).
#
# Requirements:
# Role-Based Validation: Implement different password validation logic for at least three distinct user roles (e.g., 'admin', 'regular', 'super_admin').
# Extensibility: The system should be easy to extend with new roles and their specific validation rules.
# Configurable Rules: Individual validation rules (e.g., minimum length, requirement for special characters, numbers) should be configurable per role.
# Clear API: Design an intuitive API for performing password validation given a password string and a user role.
# Feedback: The system should return clear feedback on which rules were violated if validation fails.




from abc import ABC, abstractmethod
from enum import Enum



class User:
    def __init__(self, name, password, user_role):
        self.name = name
        self.password = password
        self.user_role = user_role

    def get_name(self):
        return self.name

    def get_role(self):
        return self.user_role

    def get_password(self):
        return self.password



class UserRoles(Enum):
    Admin = "Admin"
    Regular = "Regular"
    SuperAdmin = "SuperAdmin"



class RoleValidation(ABC):
    @abstractmethod
    def validate_password(self, user: User) -> bool:
        pass


class AdminValidation(RoleValidation):
    def validate_password(self, user: User) -> bool:
        result = ConfigurableRules(user.get_password()).is_validpassword()
        if result != "Password is valid":
            print(result)
            return False

        for char in user.get_password():
            if char in "!@#$%^&*()":
                print("It is valid password for Admin role")
                return True

        print("Include at least one special character")
        return False


class RegularValidation(RoleValidation):
    def validate_password(self, user: User) -> bool:
        result = ConfigurableRules(user.get_password()).is_validpassword()
        print(result)
        return result == "Password is valid"


class SuperAdminValidation(RoleValidation):
    def validate_password(self, user: User) -> bool:
        result = ConfigurableRules(user.get_password()).is_validpassword()
        if result != "Password is valid":
            print(result)
            return False

        special_count = 0
        for char in user.get_password():
            if char in "!@#$%^&*()":
                special_count += 1

        if special_count >= 2:
            print("Password valid for SuperAdmin")
            return True

        print("Include at least 2 special characters")
        return False


class ValidationFactory:
    @staticmethod
    def Validate_Role(user: User) -> RoleValidation:
        if user.user_role == UserRoles.Regular.value:
            return RegularValidation()
        elif user.user_role == UserRoles.Admin.value:
            return AdminValidation()
        elif user.user_role == UserRoles.SuperAdmin.value:
            return SuperAdminValidation()
        else:
            raise ValueError("Unknown user role")



class ConfigurableRules:
    def __init__(self, password):
        self.password = password

    def is_validpassword(self):
        missing = []

        if len(self.password) < 8:
            missing.append("minimum length 8")

        has_upper = has_lower = has_num = False

        for char in self.password:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_num = True

        if not has_upper:
            missing.append("uppercase letter")
        if not has_lower:
            missing.append("lowercase letter")
        if not has_num:
            missing.append("number")

        if not missing:
            return "Password is valid"
        return "Password is missing: " + ", ".join(missing)



class PasswordManger:
    def __init__(self, user: User):
        self.user = user
        self.user_password = {}

    def set_password(self):
        validator = ValidationFactory.Validate_Role(self.user)

        if not validator.validate_password(self.user):
            print("Password NOT set due to validation failure")
            return

        if self.user.name in self.user_password:
            print("Password already taken")
            return

        self.user_password[self.user.name] = self.user.get_password()
        print("Password set successfully")

    def reset_password(self, password):
        validator = ValidationFactory.Validate_Role(self.user)

        old_password = self.user.password
        self.user.password = password

        if not validator.validate_password(self.user):
            self.user.password = old_password
            print("Password reset failed due to validation")
            return

        self.user_password[self.user.name] = password
        print("Password reset successfully")



if __name__ == "__main__":
    user = User("Varun", "Aaabbaa1", UserRoles.Admin.value)

    manager = PasswordManger(user)
    manager.set_password()

    print("-" * 40)

    user.password = "Abcdef1@"
    manager.set_password()

    user1 = User("mitra","Mitra@1232#",UserRoles.SuperAdmin.value)
    manager1 = PasswordManger(user1)
    manager1.set_password()
