from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self._validate(value)
        super().__init__(value)

    def _validate(self, value):
        if len(value) != 10:
            raise Exception("Number must be 10 digits")

    def set_value(self, value):
        self._validate(value)
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def show_bd(self):
        return f"Date of birthday {self.birthday.value.strftime('%d.%m.%Y')}"

    def add_phone(self, phone: str):
        field = Phone(phone)
        self.phones.append(field)

    def remove_phone(self, phone: str):
        self.phones = [field for field in self.phones if field.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str):
        finded = [field for field in self.phones if field.value == old_phone]
        result = False
        for item in finded:
            item.set_value(new_phone)
            result = True
        return result

    def find_phone(self, phone: str):
        finded = [field for field in self.phones if field.value == phone]
        return finded[0] if len(finded) else None
    
    def add_birthday(self, date):
        self.birthday = Birthday(date)

class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record: Record):
        self.data.update({record.name.value : record})

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            self.data.pop(name)

    def get_upcoming_birthdays(self):
        # current date and years
        today = date.today()
        current_year = datetime.now().year
        next_year = current_year + 1

        result = list()
        for user in self.data.values():
            # parse user birthday date
            # user_birthday = datetime.strptime(user['birthday'], '%Y.%m.%d').date()
            if user.birthday == None:
                continue
            user_month = user.birthday.value.month
            user_day = user.birthday.value.day
            
            # setup next birthdate date
            next_birthday = date(year=current_year, month=user_month, day=user_day)
            if next_birthday < today:
                next_birthday = date(year=next_year, month=user_month, day=user_day)

            diff_days = (next_birthday - today).days
            if diff_days < 7:
                # corrent date if weekends
                if next_birthday.weekday() in [5,6]:
                    days_ahead = 7 - next_birthday.weekday()
                    next_birthday = next_birthday + timedelta(days=days_ahead)
                
                congratulation_date = next_birthday.strftime("%d.%m.%Y")
                
                # add users with birthdays in this week
                data = {'name': user.name.value, 'congratulation_date': congratulation_date}
                result.append(data)

        return result
