from app.messages.environment import environment

CONTRACT_INFO = environment.from_string("""
<b>ПІБ:</b> {{ contract.last_name }} {{ contract.first_name }} {{ contract.middle_name|default('', true) }}
<b>Спеціальність:</b> {{ contract.speciality|default('', true) }}
<b>Номер контракту:</b> {{ contract.contract_number|default('', true) }}
<b>Конкурсний бал:</b> {{ contract.competitive_point|default('', true) }}
<b>Дата:</b> {{ contract.date|default('', true) }}
""")

REGISTER_USER = environment.from_string("""
{{ message }}

<b>ПІБ:</b> <code>{{ user.last_name }} {{ user.first_name }} {{ user.surname|default('', true) }}</code>
<b>Юзернейм:</b> {% if user.username %}@{{ user.username }}{% else %}<a href='tg://user?id={{ user.telegram_id }}'>{{ user.first_name }}</a>{% endif %} ({{ user.telegram_id }})
<b>Телефон:</b> {{ user.phone }}
<b>Пошта:</b> {{ user.email }}
<b>Спеціальність:</b> {{ user.speciality }}
<b>Гуртожиток:</b> {{ 'Так' if user.is_dorm else 'Ні' }}
<b>Підтвердив місце навчання:</b> {{ 'Так' if user.confirm_edbo else 'Ні' }}
<b>Роздрукував заяву:</b> {{ 'Так' if user.printed_edbo else 'Ні' }}
""")
