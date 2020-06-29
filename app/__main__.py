import sys
from typing import Optional

from app.task import Task

args = sys.argv[1:]

funcs = {
    'reset': (0, Task, Task.reset),
    'save': (2, Task, Task.save_to_db),
    'backup': (0, Task, Task.backup_db),
    'top': (0, Task, Task.export_top_earthquakes),
    'plot': (0, Task, Task.plot_count_by_mag)
}


def request() -> Optional[str]:
    """get the input request string, which will be then mapped as key to get
    main method

    :return:
    """
    try:
        return str(args[0])
    except IndexError:
        return None


def arg1() -> Optional[str]:
    try:
        return str(args[1])
    except (IndexError, ValueError):
        return None


def arg2() -> Optional[str]:
    try:
        return str(args[2])
    except (IndexError, ValueError):
        return None


def main() -> None:
    if request() is None:
        raise TypeError('expect at least one input')

    n_args, cls, func = funcs.get(request(), (None, None, None))

    if func is None:
        raise TypeError('input request is not valid, accept only {}'.format(
            list(funcs.keys())))

    if n_args == 0:
        instance = cls()
        func(instance)
    elif n_args == 2 and (arg1() is None or arg2() is None):
        raise TypeError(
            'yyyy-mm-dd formatted start / end date should be provided')
    elif n_args == 2:
        instance = cls()
        func(instance, arg1(), arg2())
    else:
        raise TypeError('input error')


if __name__ == '__main__':
    main()
