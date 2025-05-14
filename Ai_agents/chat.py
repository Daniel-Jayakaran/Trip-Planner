from qdrant_client import QdrantClient
from openai import OpenAI
from Ai_agent_up_trip import get_embedding,COLLECTION_NAME


qdrant_client = QdrantClient(
    url="https://a97589e9-aa15-490f-9f45-087a4c1739cc.us-east4-0.gcp.cloud.qdrant.io", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzQ5MjI3NjcyfQ.KEUgkxkY_o4JAdHyRg_02opN1jg7i8Hq4T-uqPDXtSg",
)
client = OpenAI(base_url="https://openrouter.ai/api/v1", 
                api_key="<OpenAI API-Key>")

def retrieve_chunks(query):
    """Retrieve relevant document chunks based on a query"""
    query_embedding = get_embedding(query)
    
    context_search = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=5
    )
    
    res_contexts = []
    for context in res_contexts:
        context_search.append({
            "text": context.payload["text"],
            "score": context.score,
            "chunk_index": context.payload["chunk_index"],
            "document_id": context.payload["document_id"]}
        )
    return res_contexts      
        

def Rag_chat(question):
    
    Context = retrieve_chunks(question)

    prompt = f"""
        question: {question}
        context: {Context[0]["text"]}
        answer the question based on the context
    """   

    response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
            {
                "role": "user",
                "content": prompt,
            },
            {
                "role": "system",
                "content": """You are a Intelligent Assistant who answer general question like answer about current affair,
                            facts, news , Hisory, scientific questions""",
            },
        ],
        stream=True,
    )

    for chunk in response:
        yield chunk.choices[0].delta.content

def Agent_response(question: str, Agent: str):
    prompt = f"""
        question: {question}
        output: {Agent}
        answer the question based on the output
    """

    stream = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
            {
                "role": "user",
                "content": prompt,
            },
            {
                "role": "system",
                "content": """You are a helpful Tourist Planner assistant that Help people to plan their Vacation
                              And Follow These Instructions to Create The Itinerary:
                              - Your name is Tripify
                              - Give A bif Title in Bold Letters On the Trip ot Itinerary
                              - First Congratulate them On their Vacation
                              - Appreciate their Choice of choosing the place for Vacation
                              - You Always Give response in a Professional Manner
                              - create itinerary and tours Plans based on User inputs and queries 
                              - Answer Questions Asked Politely to the User
                              - Structure the plan in Day wise with 'Time'
                              - Give Times of the Days in Bold
                              - Give Total Budget Estimation if Budget was not given
                              - Give Details of the Show Event places and Adventureous Activities to do and visit, 
                                Give Their Details like Admission Pricing,Admmision procedures Details,Rules 
                                And Timings [Note:Give the Details In Formal Structure]
                              - Guide User by Giving Routes to Each place in a sequantial Manner 'USE the Format I gave In Example'
                                (For Example:'Route: Go to Location A -> Location B -> Destinnations Location')
                              - Suggest Famous Restaurants to eat 
                              - You have to Find Best Hotel Recommendations Based Location Places to Visit
                              - Give Famous Foods Recommendations to Eat in Nearby place in that Location 
                              - Give Total Budget Overview
                              - Finally Wish Them Safe Journey.
                             
                             User's query:
                             Plan: Devise the plan Day by day With Timing
                             Route: Give Sequential Manner,Example: Go to Location A -> Location B -> Final Destinations Location
                             Restaurants: Give 4 - 5 options
                             Hotels: give 4 - 5  options
                             Adventurous Activities Admmision Tickets and Timings Details:Tickets: Use Search and Give Details and Give the Travelling Medium and Guide The User how they GO
                             and Operate inside the vacation place(integrate this while the Guiding Routes)
                             
                             Structure the Plans of itinerary Day-by-Day

                                For each day, use this format:


                                Day 1:  [Date], [Location]

                                08:00 AM - Depart from [City A]
                                10:30 AM - Arrive at [City B]
                                11:00 AM - Hotel check-in at [Hotel Name]
                                           Route: Go to Location A -> Location B -> Destinnations Location
                                12:30 PM - Lunch at [Provide Options of Restaurant Name]
                                02:00 PM - Visit [Tourist Spot or Meeting]
                                           Route: Go to Location A -> Location B -> Destinnations Location
                                09:00 PM - Return to hotel
                                
                                You can repeat this structure for each day of your itinerary.

                                Add Sequential Guiding Routes

                                Options of Restaurant and  hotel and Their confirmations

                                Event tickets or reservation codes

                                Sample Simple Itinerary (Vacation):

                                Trip to Goa: May 15-17, 2025

                                * Travellers: J. Daniel and Friends
                                * Emergency Contact: +91-9876543210

                                ----------------------------------------------------------------------------------------------------------------------

                                Day 1: May 15
                                Plan:
                                06:00 AM - Flight from Chennai to Goa
                                08:30 AM - Arrive and take taxi to Hotel Taj
                                09:30 AM - Check-in and rest
                                12:00 PM - Lunch at Fisherman’s Wharf,Britto's Restauarnt,Maka Zai Goan Restaurant [Provide 4,5 Restaurant Options]
                                            * Route:(For Example: A -> B -> C -> Fisherman's wharf )
                                03:00 PM - Beach at Baga
                                           * Route:(For Example: A -> B -> C -> Fisherman's wharf )
                                           * Adventurous Events:
                                               1.) Event A: Admission price : 5$
                                                   Event Timing : 2.00PM
                                                   Rules : Stand in que Till Reaching Your Seat
                                               2.) Place B: Admission price : 2$
                                                   Event Timing : 4.00PM
                                                   Rules : Don't Push other while standing.
                                08:00 PM - Dinner at Ritz Classic,Mama Misom,Thalassa,Bomras [Provide 4,5 Restaurant Options]
                                           * Route:(For Example: A -> B -> C -> Ritz Classics )
                                10.00 PM - Swimmimg at Hotel Swimmimg Pool
                                 """
            },
        ],
        stream=True,
    )

    for chunk in stream:
        yield chunk.choices[0].delta.content
