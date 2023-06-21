import openai
import json

class LinkAttatcher:
    prompt = '''
    <context>
    The input is a recommendation of places in a conversational format.
    <context>
    <input>
    {response}
    <input>
    <task>
    From the input text identify the recommended places and answear with only one place per line.
    For each line only include place_name, city, country. Separated by ;
    Everything must be written in english.
    <task>
    <example>
    venice beach;los angeles;USA
    times square;new york;USA
    <example>
    <constrains>
    - Answer only with the lines of places, DO NOT include any more text.
    - Do not respond with code, respond with the result of the task.
    - If there are no places in the input, answer with an empty string.
    <constrains>
    '''

    links_prefix= '''
    {response}

    Also here are some links that might be useful:
    {links_array}
    '''

    def __init__(self, tripAdvisorClient, gpt_deployment) -> None:
        self.tripAdvisorClient = tripAdvisorClient
        self.gpt_deployment = gpt_deployment
    
    def attatch_links(self, response)->str:
        print("prompt", self.prompt.format(response=response))
        completition = openai.Completion.create(
            engine=self.gpt_deployment, 
            prompt=self.prompt.format(response=response), 
            temperature=0.1,
            top_p=0.1,
            max_tokens=1024, 
            n=1)
        try:
            res = completition["choices"][0]["text"]
            print(res)
            if len(res) == 0: raise Exception("No kinks to attatch")
            places = res.split("\n")
            links = []
            for place in places:
                if len(links) >= 3: break # dont overload the response with too much data
                if len(place) == 0 or ";" not in place: continue # dont process empty or broken lines
                if place.endswith(";"): place = place[:-1]
                [place_name, city, country] = place.split(";")

                options = self.tripAdvisorClient.locations_index(
                    place_name.strip(),
                    city.strip() + " " + country.strip()
                    )
                if len(options) == 0: continue # dont process places that trip advisor doesnt know

                relevant_location = options[0] # naively pick the first
                details = self.tripAdvisorClient.location_detail(relevant_location["location_id"])
                if details and len(details["web_url"]) > 0: links.append(details["web_url"])
        except Exception as e:
            print(e)
            return response
        
        if len(links)>0:
            links[0] = "- " + links[0]
            return self.links_prefix.format(
                response=response,
                links_array="\n- ".join(links)
            )
        else:
            return response

        
        
        