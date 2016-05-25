import sys
from SPARQLWrapper import SPARQLWrapper, JSON

def exampleQuestions():
    print("Voorbeeldvragen:")
    print("Wat was de startdatum van de Olympische Zomerspelen 2008?")
    print("Wat was het motto van de Olympische Zomerspelen 2004?")
    print("Wie is de coach van Michael Phelps?")
    print("Wat is de bijnaam van Bradley Wiggins?")
    print("Wat is de lengte van Usain Bolt?")
    print("Wat is het gewicht van Sam Willoughby?")
    print("Wat is de geboorteplaats van Chris Hoy?")
    print("Wat is de geboortedatum van Sven Kramer?")
    print("Wat zijn de disciplines van Atletiek?")
    print("Wat is de specialisatie van Margot Boer?")
    print("")
    print("Stel een vraag:")
    
def readPairCounts():
    with open('pairCounts', 'r') as p:
        anchor = []
        for line in p.readlines():
            anchor.append(line.split('\t'))
        return anchor


def getResource(entity,anchor):
    if isinstance(entity, list):
        entity = " ".join(entity)
    highest = 0
    for row.lower() in anchor:
        if row[0] == entity:
            if int(row[2]) > highest:
                highest = int(row[2])
                resource = row[1]
    resource = "<" + resource + ">"
    return resource

def getQuery(question,anchor):
    queryShell = """
        SELECT STR(?result) as ?result
        WHERE{{{}}}
        ORDER BY ?result"""
    if question[-1] == "?":
        question = question[:-1]
    question = question.split()

    if question[5] == "de" or question[5] == "het":
        resource = getResource(question[6:],anchor)
    else:
        resource = getResource(question[5:],anchor)
    
    if question[2:5] == ["de","startdatum","van"]:
        queryContent = resource + " prop-nl:opening ?result ."
        
    if question[2:5] == ["het","motto","van"]:
        queryContent = resource + " prop-nl:motto ?result ."
        
    if question[2:5] == ["de","coach","van"]:
        queryContent = resource + " prop-nl:coach ?result ."
        
    if question[2:5] == ["de","bijnaam","van"]:
        queryContent = resource + " foaf:nick ?result ."
        
    if question[2:5] == ["de","lengte","van"]:
        queryContent = resource + " prop-nl:lengte ?result ."
        
    if question[2:5] == ["het","gewicht","van"]:
        queryContent = resource + " prop-nl:gewicht ?result ."
        
    if question[2:5] == ["de","geboorteplaats","van"]:
        queryContent = "{" + resource + " prop-nl:geboorteplaats ?result .} UNION {" + resource + "prop-nl:geboortestad ?result .}"

    if question[2:5] == ["de","geboortedatum","van"]:
        queryContent = resource + " prop-nl:geboortedatum ?result ."
        
    if question[2:5] == ["de","disciplines","van"]:
        queryContent = resource + " prop-nl:disciplines ?result ."
        
    if question[2:5] == ["de","specialisatie","van"]:
        queryContent = resource + " prop-nl:specialisatie ?result ."
        
    query = queryShell.format(queryContent)
    return query

def runQuestion(question,anchor):
    query = getQuery(question,anchor)
    
    sparql= SPARQLWrapper("http://nl.dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if results != []:
        for result in results["results"]["bindings"]:
            for arg in result:
                answer = arg + " : " + result[arg]["value"]
                print(answer)
    else:
        print("Deze informatie staat niet in de database.")

def main(argv):
    exampleQuestions()
    anchor = readPairCounts()
    for line in sys.stdin:
        line = line.rstrip()
        try:
            runQuestion(line.lower(),anchor)
        except:
            print("Deze vraag kan niet worden beantwoord.")

if __name__ == "__main__":
    main(sys.argv)
