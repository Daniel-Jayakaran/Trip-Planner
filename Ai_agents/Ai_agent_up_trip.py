from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from openai import OpenAI
import uuid
import textwrap

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url="https://a97589e9-aa15-490f-9f45-087a4c1739cc.us-east4-0.gcp.cloud.qdrant.io", 
    api_key="",
)

qdrant_client.delete_collection(collection_name="Trip_planner_data")
# Initialize OpenAI client
openai_client = OpenAI(base_url="https://openrouter.ai/api/v1", 
                       api_key="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")

# Collection name
COLLECTION_NAME = "Trip_planner_dataset"


def create_collection(COLLECTION_NAME):
# def create_collection_if_not_exist():
    """Create a collection if it doesn't exist"""
    collections = qdrant_client.get_collections().collections
    collection_names = [collection.name for collection in collections]

    if COLLECTION_NAME not in collection_names:

        uploading = qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE))

        if (uploading == True):   
            print(f"Collection '{COLLECTION_NAME}' created.")
        else:
            print(f"Collection '{COLLECTION_NAME}' already exists.")


def get_embedding(text):
    """Get embedding for a text using SentenceTransformer"""
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # If text is a single string, wrap it in a list
    if isinstance(text, str):
        embedding_vector = model.encode([text])[0]
    else:
        embedding_vector = model.encode(text)[0]
    
    return embedding_vector


def upload_document(document, chunk_size=1000):
#     """Upload a document by splitting it into chunks and storing in Qdrant"""
#     # Create collection if it doesn't exist
#     # create_collection_if_not_exists()
    
    # Split document into chunks
    chunks = textwrap.wrap(document, chunk_size, break_long_words=False, replace_whitespace=False)
    
    points = []
    for i, chunk in enumerate(chunks):
        chunk_id = str(uuid.uuid4())
        embedding = get_embedding(chunk)
        
        points.append(PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={"text": chunk, "chunk_index": i, "document_id": str(uuid.uuid4())}
        ))
    
    # Upload chunks to Qdrant
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    
    print(f"Uploaded {len(chunks)} chunks to Qdrant")
    # return len(chunks)


def retrieve_chunks(query):
    """Retrieve relevant document chunks based on a query"""
    query_embedding = get_embedding(query)
    
    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=5
    )
    
    results = []
    for result in search_result:
        results.append({
            "text": result.payload["text"],
            "score": result.score,
            "chunk_index": result.payload["chunk_index"],
            "document_id": result.payload["document_id"]
        })
    
    return results

sample_document = """ 1. Define the Purpose
                            Is it for:

                            A vacation? 

                            A business trip?

                            A daily event (e.g., conference)?



                         2.) Add Basic Info

                            Include:

                            Name of traveler(s)

                            Trip title or purpose

                            Dates and locations

                            Emergency contacts or booking references (if needed)

                         4. Structure the Plans of itinerary Day-by-Day with Timimgs:

                            For each day, use this format:


                            Day 1:  [Date], [Location]

                            08:00 AM - Depart from [City A]
                            10:30 AM - Arrive at [City B]
                            11:00 AM - Hotel check-in at [Hotel Name]
                            12:30 PM - Lunch at [Provide Options of Restaurant Name]
                            02:00 PM - Visit [Tourist Spot or Meeting]
                            09:00 PM - Return to hotel
                            
                            You can repeat this structure for each day of your itinerary.

                         5.) Add Maps, Links, or Notes (Optional)
                            Google Maps links,Add Sequential Guiding Routes

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
                                        Route:(For Example: A -> B -> C -> Fisherman's wharf )
                                        Google Map Link:
                            03:00 PM - Beach at Baga
                            08:00 PM - Dinner at Ritz Classic,Mama Misom,Thalassa,Bomras [Provide 4,5 Restaurant Options]
                                        Route:(For Example: A -> B -> C -> Ritz Classics )
                                        Google Map Link:
                            10.00 PM - Swimmimg at Hotel Swimmimg Pool

                            Instructions:
                            i.)    Always be Professional
                            ii.)   make a Itinerary Day wise, include time also,events
                            iii.)  Always provide options 
                            iv.)   Give Guiding Routes for Hotels,Restaurant
                            v.)    Attach and Give Google Map Links (if possible) """


# # Example usage
if __name__ == "__main__":
                          
    create_collection(COLLECTION_NAME)
    upload_document(sample_document,1000)



