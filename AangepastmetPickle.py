#!/usr/bin/env python3
# s2331373 - Anouk Broer
# eindopdracht

import pickle
import socket
import sys
from lxml import etree
from SPARQLWrapper import SPARQLWrapper, JSON

# open het bestand paircounts en lees alle zinnen in, split de zinnen op de tab en voeg deze toe aan de lijst anchors
# de lijst anchors bevat van iedere zin een lijst met drie: elementen anchor, URI, frequentie
def getQuestions():
	vragen = []
	with open('vragen.txt', 'r', encoding='utf-8') as data2:
		vraag = data2.readlines()

		# aan het eind van elke vraag staat een newline teken, verwijder deze
		for line in vraag:
			vragen.append(line.strip('\n'))

	# return lijst met alle anchors (= naam van bv persoon), return een lijst met alle vragen 
	return vragen

# parse input sentence and return alpino output as an xml element tree
# code komt rechtstreeks uit de slides 
def alpino_parse(sent, host='zardoz.service.rug.nl', port=42424):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))
	sent = sent + "\n\n"
	sentbytes= sent.encode('utf-8')
	s.sendall(sentbytes)
	bytes_received= b''
	while True:
		byte = s.recv(8192)
		if not byte:
			break
		bytes_received += byte
	#print(bytes_received.decode('utf-8'), file=sys.stderr)
	xml = etree.fromstring(bytes_received)
	return xml

# verkrijg X, Y (namen van personen, en bv Olympische Spelen)
def get_entity(xml):
	entities = xml.xpath('.//node[(@pos="name" and not(@rel="mwp") or (@spectype="deeleigen") or (@cat="mwu" and node[@pos="name"]))]')
	ents = []
	
	for ent in entities:
		ents.append(tree_yield(ent))

	#print(ents)
	return ents

def tree_yield(xml):
    leaves = xml.xpath('descendant-or-self::node[@word]')
    words = []
    for l in leaves :
        words.append(l.attrib["word"])
    return " ".join(words)

def create_query(line, entity, data):	

	# als de input van de gebruiker eindigt op een '?', haal deze dan weg.
	# geen idee waarom dit er nog bij staat, maar als ik het weg haal werkt
	# het niet meer :)
	if line[-1] == "?":
			line = line[:-1].split(" ")

	resource = data[y][1]
	uri ="<" + resource + ">"
	#print(resource)

	# de basis van de query
	basis = """
        SELECT STR(?result) as ?result
        WHERE  {{
            {}
        }}ORDER BY ?result
        """
	
	#alle properties
	properties = {'motto':"prop-nl:motto",
	              'spreuk':"prop-nl:motto",
	              'opening':"prop-nl:opening",
	              'startdatum':"prop-nl:opening",
	              'begin':"prop-nl:opening",
	              'plaats':"prop-nl:plaats",
	              'locatie': "prop-nl:plaats",
	              'opener': "prop-nl:opener",
	              'officiele opener':"prop-nl:opener",
	              'sluiting':"prop-nl:sluiting",
	              'einddatum': "prop-nl:sluiting",
	              'einde':"prop-nl:sluiting",
	              'eind':"prop-nl:sluiting",
	              'geboren':["prop-nl:geboortedatum","prop-nl:geboortedatum"],
	              'verjaardag':"prop-nl:geboortedatum",
	              'aantal atleten':"prop-nl:atleten",
	              'aantal sporters':"prop-nl:atleten",
	              'lengte':["prop-nl:lengte","dbpedia-owl:height"],
	              'lang':["prop-nl:lengte","dbpedia-owl:height"],
	              'hoogte':"prop-nl:lengte",
	              'sport':"prop-nl:discipline",
	              'discipline':"prop-nl:discipline",
	              'onderdeel':"prop-nl:discipline",
	              'trainer':"prop-nl:trainer",
	              'begeleider':"prop-nl:trainer",
	              'gecoacht':"dbpedia-owl:coach",
	              'sport':"prop-nl:discipline",
	              'gespecialiseerd':["dbpedia-owl:speciality", "dbpedia-owl:sportSpecialty", "prop-nl:specialisatie"],
	              'weegt':["prop-nl:gewicht", "dbpedia-owl:weight"],
	              'bijnaam':"prop-nl:bijnaam"}


	for item in line:
		if item in properties:

			# Kijk of de value van een key in de dictionary met properties een lijst is
			if type(properties[item]) is list:
				propList = properties[item]

				# als de lengte van de lijst groter is dan 2 --> voor UNION
				if len(propList) == 2:
					query = basis.format("{{" + resource + " " + propList[0] +" ?result} UNION {" + resource + " " + propList[1] + " ?result}}")

				# als de lengte van de lijst groter is dan 3
				elif len(propList) == 3:
					query = basis.format("{{" + resource + " " + propList[0] +" ?result} UNION {" + resource + " " + propList[1] + " ?result} UNION {" + resource + " " + propList[2] + " ?result}}")

			# als de value van de dictionary geen lijst is			
			else:
				query = basis.format("{{" + resource + " " + properties[item] +" ?result}}")

	#print(query)
	return(query)

# stuur de query naar dbpedia en geef het antwoord terug
# --> geeft op dit moment slechts één antwoord terug (dus ook als er meerdere
# antwoorden mogelijk zijn)
def fire_query(query):
	sparql = SPARQLWrapper("http://nl.dbpedia.org/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	count = 0
	for result in results["results"]["bindings"]:
		count += 1
	if count == 0:
		raise Exception()
	for result in results["results"]["bindings"]:
		for arg in result :
			answer = result[arg]["value"]
			return answer

def main():

	data = pickle.load(open('pairCounts.pickle','rb'))

	vragen = getQuestions()

	goed = 0
	fout = 0

	print()

	for line in vragen:
		print(line)

		# als een vraag niet eindigt met een ? voeg deze dan toe
		# geen idee of dit nodig is met de uiteindelijke vragen, maar als een vraag niet eindigt
		# op een ? dan werkt het programma niet 
		if line[-1] != "?":
			line = line + "?"

		# parse de vraag met xml 
		xml = alpino_parse(line)

		# verkrijg de entitiy uit de parse (dus de anchor, bv naam van persoon)
		enti = get_entity(xml)

		
		# try/except, als het niet mogelijk is om een antwoord te vinden
		# dan 'faalt' try en wordt geprint dat de vraag niet beantwoord kan worden
		try:
			#entity = enti[0].lower()

			query = create_query(line, entity, data)
			answer = fire_query(query)
			print(answer, "\n")
			goed += 1

		except:
			print("Deze vraag kan helaas niet worden beantwoord.\n")
			fout += 1

	# even om te testen hoeveel antwoorden er gevonden kunnen worden 
	print("Aantal vragen kunnen beantwoorden {}. Aantal vragen niet kunnen beantwoorden {}".format(goed,fout))

if __name__ == "__main__":
	main()