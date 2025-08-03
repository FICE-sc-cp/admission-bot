from app.messages.environment import environment

CONTRACT_INFO = environment.from_string("""
<b>ПІБ:</b> <code>{{ contract.last_name }} {{ contract.first_name }} {{ contract.middle_name|default('', true) }}</code>
<b>Спеціальність:</b> {{ contract.speciality|default('', true) }}
<b>Номер договору:</b> {{ contract.contract_number|default('', true) }}
<b>Конкурсний бал:</b> {{ contract.competitive_point|default('', true) }}
<b>Дата:</b> {{ contract.date|default('', true) }}
""")

REGISTER_USER = environment.from_string("""
Зареєтровано нового користувача

<b>ПІБ:</b> <code>{{ user.last_name }} {{ user.first_name }} {{ user.middle_name|default('', true) }}</code>
<b>Телефон:</b> <code>{{ user.phone }}</code>
<b>Пошта:</b> <code>{{ user.email }}</code>
<b>Спеціальність:</b> <code>{{ user.expected_specialities }}</code>
<b>Гуртожиток:</b> <code>{{ 'Так' if user.is_dorm else 'Ні' }}</code>
<b>Роздрукував заяву:</b> <code>{{ 'Так' if user.printed_edbo else 'Ні' }}</code>
""")

GOING_USER = environment.from_string("""
Користувач зайшов у корпус

<b>ПІБ:</b> <code>{{ user.last_name }} {{ user.first_name }} {{ user.middle_name|default('', true) }}</code>
<b>Телефон:</b> <code>{{ user.phone }}</code>
<b>Пошта:</b> <code>{{ user.email }}</code>
<b>Спеціальність:</b> <code>{{ user.expected_specialities }}</code>
<b>Гуртожиток:</b> <code>{{ 'Так' if user.is_dorm else 'Ні' }}</code>
<b>Роздрукував заяву:</b> <code>{{ 'Так' if user.printed_edbo else 'Ні' }}</code>

""")
