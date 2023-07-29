PIC_DIR = 'q_nums'


def get_num(num):
    return f'{PIC_DIR}/{num}.jpg'


def pre_gen_nums(num: int):
    for i in range(num):
        get_num(i)
