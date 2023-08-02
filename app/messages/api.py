from app.messages.environment import environment

CONTRACT_INFO = environment.from_string("""
ПІБ: {{ contract.last_name }} {{ contract.first_name }}
""")
