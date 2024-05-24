from pydantic import BaseModel, constr, field_validator
import re
from datetime import datetime

class User(BaseModel):
    id: int
    login: constr(min_length=3, max_length=20)
    password: constr(min_length=3, max_length=50) #и имеется хотя бы одна цифра и буква в верхнем регистре
    email: str = None #опциональное, подходит под шаблон: {a}@{b}.{c}
    date: str = None #опциональное, дата в формате ISO – YYYY-mm-dd
    status: int #обязательное, один из статусов 1,5,7,9,14
    is_moderator: bool = None

    @field_validator("password")
    def check_password_pattern(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError("пароль должен содержать хотя бы одну цифру")
        if not any(c.isupper() for c in v):
            raise ValueError("пароль должен содержать хотя бы одну цифру в верхнем регистре")
        return v

    @field_validator("email")
    def is_correct_email(cls, v):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(pattern, v):
            raise ValueError("email не подходит под шаблон {a}@{b}.{c}")
        return v

    @field_validator("date")
    def is_correct_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except Exception:
            raise ValueError("дата не дата")

    @field_validator("status")
    def check_status(cls, v):
        if v not in (1,5,7,9,14):
            raise ValueError("Некорректный код статуса. Разрешены только 1,5,7,9,14")
        return v

if __name__ == "__main__":
    import json

    results = []

    with open("dataset_853556_9.txt") as f:
        data = json.loads(f.read())
        for user_data in data:
            try:
                user = User(**user_data)
                print(user_data)
                print("OK\n")
                results.append("OK")
            except Exception as e:
                print(user_data)
                print("FAILED", repr(e.errors()[0]), "\n")
                results.append("Failed")

