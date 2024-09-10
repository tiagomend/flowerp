def pascal_case_to_text(case):
    return ''.join(f' {char}' if char.isupper() else char for char in case).strip()

def snake_case_to_text(case):
    return case.replace('_', ' ').title()

def format_decimal_to_hours(decimal):
    values = f"{decimal:.2f}".split('.')
    minutes = int(int(values[1]) * 0.6)
    if minutes < 10:
        values[1] = f'{0}{minutes}'
    else:
        values[1] = str(minutes)
    if int(values[0]) < 10:
        hours = f'0{values[0]}:{values[1]}'
    else:
        hours = f'{values[0]}:{values[1]}'
    return hours
