import schedule
import time


def job():
    print("I'm working...")




def main():
    schedule.every(1).minutes.do(job)
    number = 0
    while True:
        schedule.run_pending()
        time.sleep(1)
        number += 1
        print(number)

if __name__ == '__main__':

    main()