from agno.agent import Agent
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.openrouter import OpenRouter



def Trip_searching(user_input):
    
      agent = Agent(
                name="Google Search Agent",
                tools=[GoogleSearchTools()],
                memory = True,
                enable_agentic_memory = False,
                enable_user_memories = False,
                description="""You are a Searching agent that helps users find the Best 
                            itinerary plans to places of user choice and hhelp find Hotel to Stay Based on their Budget and choice 
                            of Place Visiting and Help to find Best Restaurants to Eat and to give Best Equitte Manners""",
                instructions="""
                    -"Suggest Best Foods to eat in that vacation place and suggest best places to visit in that vacation place/trip place"
                    -"Analyse the user_input,Provide Travel Ticket(For Example: Flight Ticket) 
                      Booking Options and Details of Best Deals and Provide Boarding Information"
                    -**IMP RULE** :" Hotels And Restaurants In Normal Text and then Give Their Links Near it"
                    -**IMP RULE** :" Provide valid and Full Google Map Links for Each Places Below it"
                    -"Give Links Citations Near Travel Tickets Booking Options
                    -"Give Google Maps Links for Routes to Near Each Hotel and Restaurant Recommendations"
                    -"Give Search response with 5 Best Hotel Recommendation Based on their Bugdet and place of Visit"
                    -"Search for 10 items and select the top 5 Best Result Recommendations"
                    -"Search Language van be Multi-Lingual"
                    -"Find Best Restaurants to Eat in the Vacation Place"
                    -"Give the Best Deals Available on online for Flight Recommendation"
                    -"Give Details of the Show Events and Adventureous Activity Details Admission Pricing,Admmision procedures Details,Rules And Timing"
                    -"Give that place's etiquttes and manners of the Specific place of user choice"
                    -"Give Safety Rules to Follow To prevent Probems"
                    -"Give Weather Reports of the places of visit and Best time to visit the places"
                    -"Give the Essential Local language Phrases"
                    -"Give Tips to Things to pack (For Example: if user is going to maldives then item's to be packed : swim suit,goggles;Give This in ordered Numbered order)"
                    -"Give place's Local Currency Details and Their Conversion"
                    -"Give Essential Not to Do's in that Local place"
                    """,
                markdown=True,
                debug_mode=True,
                model=OpenRouter(id="gpt-4o-mini",
                                api_key="<OpenAI API-Key>")
                )
           
           
      content = ""
      for chunk in agent.run(user_input,stream=True):
            if hasattr(chunk, "content"):
                print(chunk.content, end="", flush=True)
                content += chunk.content

      return content
      
    
