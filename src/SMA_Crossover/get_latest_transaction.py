import firebase

"""
This script is used to get all latest transactions of each instrument for easy reference.
"""


def main():
    db_list = firebase.get_all_db_user()
    for user in db_list:
        for item in user["instruments"]:
            print("*************************************")
            print(item["instrument"])
            print(item["config"])
            print(item["transactions"][-1])
            print("\n")


if __name__ == '__main__':
    main()
