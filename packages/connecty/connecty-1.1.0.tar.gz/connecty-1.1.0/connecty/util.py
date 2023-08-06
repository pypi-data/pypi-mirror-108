
import datetime
import typing
import doctest

def days_elapsed_since(yr:int=2021) -> typing.Callable[[],int]:
    """
    Return a function that returns how many days have elapsed since the beginning of yr and today

     >>> days_elapsed_since()()
     153
    """
    def days_elapsed() -> int:
        start_date = datetime.date(yr, 1, 1)
        now_date = datetime.date.today()
        delta = now_date - start_date
        return delta.days
    return days_elapsed

if __name__ == '__main__':
    doctest.testmod(verbose=True)