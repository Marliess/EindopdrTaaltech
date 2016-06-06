#!/usr/bin/env python3
# s2331373 - Anouk Broer
# eindopdracht

import socket
import sys
from lxml import etree
from SPARQLWrapper import SPARQLWrapper, JSON

# open het bestand paircounts en lees alle zinnen in, split de zinnen op de tab en voeg deze toe aan de lijst anchors
# de lijst anchors bevat van iedere zin een lijst met drie: elementen anchor, URI, frequentie
def getPaircounts():
	anchors = []
	with open('pairCounts.txt', 'r', encoding='utf-8') as data:
	    pairCounts = data.readlines()

	    for line in pairCounts:
	        anchors.append(line.split('\t'))

	vragen = []
	with open('vragen.txt', 'r', encoding='utf-8') as vraagje:
		vraag = vraagje.readlines()

		for line in vraag:
			vragen.append(line.strip('\n'))

	return anchors, vragen

# parse input sentence and return alpino output as an xml element tree
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

def get_entity(xml):
	entities = xml.xpath('//node[(@spectype="deeleigen")]')
	#or (@spectype="deeleigen") or (@cat="mwu" and node[@pos="name"]))
	ents = []
	
	for ent in entities:
		ents.append(tree_yield(ent))
		#print(ent)

	print(ents)
	return ents

def tree_yield(xml):
    leaves = xml.xpath('descendant-or-self::node[@word]')
    words = []
    for l in leaves :
        words.append(l.attrib["word"])
    return " ".join(words)

def create_query(line, entity, anchors):	

	# als de input van de gebruiker eindigt op een '?', haal deze dan weg.
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


	return(query)

# zoek de resource URL die bij de anchor hoort in de lijst anchors
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

	anchors, vragen = getPaircounts()

	print()

	for line in vragen:
		print(line)
		#lower = line.lower()
		#line = lower.rstrip()
		if line[-1] != "?":
			line = line + "?"

		xml = alpino_parse(line)
		enti = get_entity(xml)
		
		try:
			entity = enti[0]

		#for ent in entity:
		#	entity = ent

			query = create_query(line, entity, anchors)
			answer = fire_query(query)
			print(answer, "\n")

		except:
			print("Deze vraag kan helaas niet worden beantwoord.\n")

if __name__ == "__main__":
	main()