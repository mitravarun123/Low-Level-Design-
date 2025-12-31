from abc import ABC, abstractmethod
from enum import Enum


# -------------------- ENUM --------------------
class ChannelType(Enum):
    SMS = "SMS"
    EMAIL = "EMAIL"
    PUSH = "PUSH"
    INSTAGRAM = "INSTAGRAM"


# -------------------- ENTITY --------------------
class Notification:
    def __init__(self, user_name, message):
        self.user_name = user_name
        self.message = message

    def get_user_name(self):
        return self.user_name

    def get_message(self):
        return self.message


# -------------------- OBSERVER --------------------
class Observer(ABC):
    @abstractmethod
    def update(self, notification: Notification):
        pass


# -------------------- STRATEGY --------------------
class ChannelStrategy(Observer, ABC):
    @abstractmethod
    def send_notification(self, notification: Notification):
        pass

    def update(self, notification: Notification):
        return self.send_notification(notification)


# -------------------- CONCRETE CHANNELS --------------------
class EmailChannel(ChannelStrategy):
    def send_notification(self, notification: Notification):
        print(f"[EMAIL] Sent to {notification.user_name}: {notification.message}")


class SMSChannel(ChannelStrategy):
    def send_notification(self, notification: Notification):
        print(f"[SMS] Sent to {notification.user_name}: {notification.message}")


class PushChannel(ChannelStrategy):
    def send_notification(self, notification: Notification):
        print(f"[PUSH] Sent to {notification.user_name}: {notification.message}")


class InstagramChannel(ChannelStrategy):
    def send_notification(self, notification: Notification):
        print(f"[INSTAGRAM] Sent to {notification.user_name}: {notification.message}")


# -------------------- FACTORY --------------------
class ChannelFactory:
    @staticmethod
    def get_channel(channel_type: ChannelType) -> ChannelStrategy:
        if channel_type == ChannelType.EMAIL:
            return EmailChannel()
        elif channel_type == ChannelType.SMS:
            return SMSChannel()
        elif channel_type == ChannelType.PUSH:
            return PushChannel()
        elif channel_type == ChannelType.INSTAGRAM:
            return InstagramChannel()
        else:
            raise ValueError("Invalid Channel Type")


# -------------------- USER PREFERENCES --------------------
class UserPreferences:
    def __init__(self):
        self.preferences = {}

    def set_preferences(self, user_name, channels):
        self.preferences[user_name] = channels

    def get_preferences(self, user_name):
        return self.preferences.get(user_name, [ChannelType.EMAIL])


# -------------------- SUBJECT --------------------
class NotificationService:
    def __init__(self):
        self.observers = []

    def attach(self, observer: Observer):
        self.observers.append(observer)

    def detach(self, observer: Observer):
        self.observers.remove(observer)

    def notify(self, notification: Notification):
        for observer in self.observers:
            observer.update(notification)


# -------------------- CLIENT --------------------
if __name__ == "__main__":

    # User preferences
    user_preferences = UserPreferences()
    user_preferences.set_preferences(
        "Varun",
        [ChannelType.EMAIL, ChannelType.SMS, ChannelType.PUSH]
    )

    # Notification
    notification = Notification("Varun", "Your order has been shipped 🚚")

    # Notification Service (Subject)
    service = NotificationService()

    # Attach observers based on user preferences
    channels = user_preferences.get_preferences("Varun")
    for channel_type in channels:
        channel = ChannelFactory.get_channel(channel_type)
        service.attach(channel)

    # Notify all observers
    service.notify(notification)
