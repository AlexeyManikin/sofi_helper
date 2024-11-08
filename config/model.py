__author__ = 'Alexey Y Manikin'

from datetime import date

# Определение JSON-схемы для ответа
json_schema = {
    "type": "object",
    "properties": {   
        "description":  {"type": "string"},
        "group":        {"type": "string"},
        "summ":         {"type": "number"},
        "type_s":       {"type": "string"},
        "date":         {"type": "string"},
        "reasoning":    {"type": "string"}
    },
    "required": ["description", "group", "summ", "type_s"]
}

def get_content_for_llm(today: date) -> str:
    content = "You are a helper who converts text about cafe expenses or income into json. " + \
        "Provide accurate and concise information in accordance with the requested structure. " + \
        "Current date %s. " % today + "The summ field is always a positive number, " + \
        "if it says food products, bread, name of grocery store, " + \
        "ice cream, lard and so on group=grocery_shopping and type_s=del, " + \
        "if the cost is related to alcohol, the value group=grocery_alco and type_s=del, " + \
        "if the cost is related to repairs, purchase of equipment, purchase of gas, payment for something, " + \
        "purchases related to interior improvement, household goods group=fixed_assets and type_s=del, " + \
        "if salary is indicated then group=salary and type_s=del, " + \
        "if any other receipt of money other than salary is indicated group=add and type_s=add, " + \
        "in the reasoning justification briefly indicate why a specific value of the group field was chosen, " + \
        "the reasoning field must be in Russian. check the json structure"
    return content

# URL вашего vLLM сервера
openai_api_url = "http://5.101.159.18:8000/v1/chat/completions"
model_name = "Qwen"