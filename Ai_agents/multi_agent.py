from pydantic import BaseModel


class Identifier(BaseModel):
  is_search: bool
  is_Tripplan: bool



#user_input = input("Hello I'm Tripify Ask Me Your Query:")

IDENTIFIER_PROMPT = """
  User's query: {user_input}

  You are an agent specialized in query classification.
  Your task is to determine if the user's query requires an rag search.
  
  Guidelines:
  - Classify as search true if the query is general knowledge (e.g. "Who is...", "What is...", "When did...","How is...")
  - Classify as search if the query asks about facts, history, or current events
  - Classify as Trip if They Said i am Travelling to Some Place
  - Classify as Trip if They ask you to Create Vacation/Itinerary Plan for the place that the user asks to create
  - Classify as Trip if They ask you to Suggest Vacation/trip Places to visit
  - Classify as Trip if They entered Name of Any Place 
  - Classify as Trip if They ask you to Suggest Hotel to stay/accomodate in place they ask
  - Classify as Trip if They ask you to Give route inside the Vacation/Trip Place They want to visit
  - Classify as Trip if They ask you to Check Travelling Tickets for the travel to the vacation/trip place
  - Classify as Trip if They ask you to Suggest Best Month/Season to Visit the Vacation/trip Places
  Analyze the query and determine if it requires searching."""
  
  

def mood_finder(user_input: str):
  from openai import OpenAI
  
  client = OpenAI(base_url="https://openrouter.ai/api/v1", 
                  api_key="<OpenAI API-Key>")
  
  response = client.beta.chat.completions.parse(
      model="openai/gpt-4o-mini",
      messages=[
        {
          'role': 'user',
          'content': user_input,
        }
      ],
      response_format=Identifier,
  )
  
  filtered_response = Identifier.model_validate_json(response.choices[0].message.content)
  return filtered_response
 
 
 
 
# print(filtered_response)


# identifier = mood_finder(IDENTIFIER_PROMPT.format(user_input=query))
# print(identifier)

# if identifier.is_search:
#   rag_response = Rag_chat(query)

# if identifier.is_Tripplan:
#   Trip_response = Trip_searching(user_input)
#   Agent_response(question=query, output=Trip_response)




