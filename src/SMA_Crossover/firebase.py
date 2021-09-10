from firebase_admin import credentials
from firebase_admin import db
import firebase_admin


"""
This is the only script responsible to save and get data from firebase db
"""

cred = credentials.Certificate("")
firebase_admin.initialize_app(cred, {
    'url': 'URL'
})
ref = db.reference('')


def get_all_db_user() -> list:
    docs = ref.get()
    result_list = []
    for item in docs:
        result_list.append(docs[item])
    return result_list


def update_users_table(new_user_list: list):
    for user in new_user_list:
        user_ref = ref.child(user["user_id"])
        user_ref.set(user)


if __name__ == '__main__':
    old = get_all_db_user()
    update_users_table(old)
