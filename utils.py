import os


def saveLastJobDate(datetime):
    with open("last_job.txt", "w") as file:
        file.write(datetime)


def readLastJobDate():
    if not os.path.exists("last_job.txt"):
        with open("last_job.txt", "w") as file:
            file.write("")
    with open("last_job.txt", "r") as file:
        return file.read()
