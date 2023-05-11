from openai_functions import ai_complete

#EXAMPLES
#print("OPENAI:" , ai_complete("Il migliore amico dell'uomo è", verbose=False, api_type="openai", max_tokens=100))
print("AZURE OPENAI:" , ai_complete("Il migliore amico dell'uomo è", verbose=False, api_type="azure", max_tokens=100))