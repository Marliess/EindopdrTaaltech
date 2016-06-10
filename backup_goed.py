#!/usr/bin/env python3
# Anouk Broer, Moniek Nieuwenhuis, Karel Beckeringh, Marlies Quekel
# eindopdracht

import socket
import sys
from lxml import etree
from SPARQLWrapper import SPARQLWrapper, JSON

# open het bestand paircounts en lees alle zinnen in, split de zinnen op de tab en voeg deze toe aan de lijst anchors
# de lijst anchors bevat van iedere zin een lijst met drie: elementen anchor, URI, frequentie
def getPaircounts():
	anchors = []
	with open('pairCounts', 'r', encoding='utf-8') as data:
	    pairCounts = data.readlines()

	    for line in pairCounts:
	        anchors.append(line.split('\t'))

	# lees alle vragen in die moeten worden beantwoord 
	# stop al deze vragen in een lijst // een element in de lijst is een vraag
	vragen = []
	with open('vragen.txt', 'r', encoding='utf-8') as data2:
		vraag = data2.readlines()

		# aan het eind van elke vraag staat een newline teken, verwijder deze
		for line in vraag:
			vragen.append(line.strip('\n'))

	# return lijst met alle anchors (= naam van bv persoon), return een lijst met alle vragen 
	return anchors, vragen

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
	entities = xml.xpath('//node[(@pos="name" and not(@rel="mwp") or (@spectype="deeleigen") or (@cat="mwu" and node[@pos="name"]))]')
	ents = []
	
	for ent in entities:
		ents.append(tree_yield(ent))

	#print(ents)
	return ents

# deze fuctie vindt het vraagwoord
def get_whd(xml):

	root = xml.xpath('.//node[@rel="whd"]')
	woorden = []
	for node in root:
		tree_y = tree_yield(node)
		woorden.append(tree_y.lower())

	if "hoeveel" in woorden:
		#get_properties_hoeveel()
	elif "wanneer" in woorden:
		#get_properties_wat()
	elif "wat" in woorden:
		#get_properties_wat()
	elif "welke" in woorden:
		#get_properties_wat()
	elif "wat" in woorden:
		#get_properties_wat()
	elif "hoe" in woorden:
		#get_properties_wat()

def tree_yield(xml):
    leaves = xml.xpath('descendant-or-self::node[@word]')
    words = []
    for l in leaves :
        words.append(l.attrib["word"])
    return " ".join(words)

def create_query(line, entity, anchors):	

	# als de input van de gebruiker eindigt op een '?', haal deze dan weg.
	# geen idee waarom dit er nog bij staat, maar als ik het weg haal werkt
	# het niet meer :)
	if line[-1] == "?":
			line = line[:-1].split(" ")

	resource = "<" + get_resource(entity, anchors) + ">"
	print(resource)

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

# zoek de resource URL (URI) die bij de anchor hoort in de lijst anchors
def get_resource(entity, anchors):
	#entity = " ".join(entity)
	highestFreq = 0
	for line in anchors:
		if line[0].lower() == entity:
			if int(line[2]) > highestFreq:
				highestFreq = int(line[2])
				link = line[1]	
				return link

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

def answerQuestion(uri,x):
    query = "SELECT STR(?output) WHERE { <"+uri+"> " + "prop-nl:"+x + " ?output }"
    sparql = SPARQLWrapper("http://nl.dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def hoeveel(line):
        xml = alpino_parse(line)

        root = xml.xpath('//node[@cat="np" and @rel="obj1"]/node[@rel]/node[@word]')
        listy = []
        for node in root:
                if "word" in node.attrib:
                        if node.attrib["word"] != "de":
                                listy.append(node.attrib["word"])
        y = ' '.join(map(str, listy))
        
        root = xml.xpath('//node[@cat="np" and @rel="whd"]/node[@pt="n"]')
        for node in root:
                x = node.attrib["word"]

        try:
                line = line.split()
                page = ["url",0]
                for pair in open("pairCounts"):
                        if y in pair:
                                pair = pair.split('\t')
                                if int(pair[2]) > page[1]:
                                        page[0] = pair[1]
                                        page[1] = int(pair[2])			
                resource = page[0]
                uri = resource
                results = answerQuestion(uri,x.lower())
                i = 0
                for result in results["results"]["bindings"]:
                        for arg in result:
                                print(result[arg]["value"],"\n")
                                i+=1
        except:
                return 1

def main():

	anchors, vragen = getPaircounts()

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
		get_whd(xml)
		
		# try/except, als het niet mogelijk is om een antwoord te vinden
		# dan 'faalt' try en wordt geprint dat de vraag niet beantwoord kan worden
		try:
			entity = enti[0].lower()
			query = create_query(line, entity, anchors)
			answer = fire_query(query)
			print(answer, "\n")

		except:
                        answer2 = hoeveel(line)
                        if answer2 == 1:
                                print("Deze vraag kan helaas niet worden beantwoord.\n")

if __name__ == "__main__":
	main()
