from faker import Faker
import time

fake = Faker()

def get_registered_user():
    return {
            "name": fake.name(),
            "address": fake.address(),
            "created_at": fake.year()
            } 


def calculate_thoughput(timing, n_messages, msg_size):
    print("Processed {0} messages in {1:.2f} seconds".format(n_messages, timing))
    print("{0:.2f} MB/s".format((msg_size * n_messages) / timing / (1024*1024)))
    print("{0:.2f} Msgs/s".format(n_messages / timing))