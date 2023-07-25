def combine_results(ner_results: list) -> list:
    """ Takes the output of a huggingface ner model pipeline and 
    combines the outpu named entities into meaningful entities e.g. 
    
    "[{'entity':B-ORG,'word':"Barnes"},{'entity':I-ORG,'word':"&"},{'entity':I-ORG,'word':"Noble"}]"

        ----->

    "[(Barnes & Noble, ORG)]"
    
    
    """


    combined_results = []
    current_string = ""
    curret_type = ""
    for result in ner_results:
        entity = result['entity']
        entity_prefix, entity_type = entity.split("-")
        word = result['word']

        join_char = " "
        if "##" in word:
            join_char = ""
            word = word.replace("##","")




        if "B" == entity_prefix:
            if current_string and curret_type:
                combined_results.append((current_string,curret_type))

            curret_type = entity_type
            current_string = word
            continue

        if "I" == entity_prefix and entity_type == curret_type:
            current_string = join_char.join([current_string,word])
            continue
        

        if "I" == entity_prefix:
            curret_type = entity_type
            current_string = word
            combined_results.append((current_string,curret_type))

    return combined_results



def get_relevant_entities(combined_ner_results: list) -> dict:
    """extracts the name of the purchasing customer and
    the name of the vendor from the input results
    """

    customer = ''
    company = ''


    for result in combined_ner_results:

        if customer and company:
            break


        if not customer:
            if result[1] == "PER":
                customer = result[0]


        if not company:
            if result[1] == "ORG":
                company = result[0]   

    
    return {"company":company, "customer": customer }