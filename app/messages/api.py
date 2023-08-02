from app.messages.environment import environment

CONTRACT_INFO = environment.from_string("""
<b>ПІБ:</b> {{ contract.last_name }} {{ contract.first_name }} {{ contract.middle_name }}
<b>Спеціальність:</b> {{ contract.speciality }}
<b>Номер контракту:</b> {{ contract.contract_number }}
<b>Конкурсний бал:</b> {{ contract.competitive_point }}
<b>Дата:</b> {{ contract.date }}
""")
