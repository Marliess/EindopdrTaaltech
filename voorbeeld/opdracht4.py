#!/usr/bin/env python3
# s2331373 - Anouk Broer
# opdracht 4 Taaltechnologie 
# versie 1 - niet af

import socket
import sys
from lxml import etree
from SPARQLWrapper import SPARQLWrapper, JSON

# open het bestand paircounts en lees alle zinnen in, split de zinnen op de tab en voeg deze toe aan de lijst anchors
# de lijst anchors bevat van iedere zin een lijst met drie: elementen anchor, URI, frequentie
def getPaircounts():
	anchors = []
	with open('pairCounts.txt', 'r') as data:
	    pairCounts = data.readlines()

	    for line in pairCounts:
	        anchors.append(line.split('\t'))

	return anchors

# print een overzicht met alle voorbeeld vragen
def print_example_queries():
	print('1.  Door wie wordt Michael Phelps gecoacht?')
	print('2.  Wanneer is Bradley Wiggins geboren?')
	print('3.  Hoeveel weegt Michael Phelps?')
	print('4.  Welke lengte heeft Aleksandr Vinkoerov?')
	print('5.  Waar is Fabian Cancellara in gespecialiseerd?')
	print("")

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
	entities = xml.xpath('.//node[(@pos="name" and not(@rel="mwp") or (@spectype="deeleigen") or (@cat="mwu" and node[@pos="name"]))]')
	ents = []
	for ent in entities:
		ents.append(tree_yield(ent))
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

	# de basis van de query
	basis = """
        SELECT STR(?result) as ?result
        WHERE  {{
            {}
        }}ORDER BY ?result
        """
	
	coach = ['coach', 'coacht','gecoacht']
	geboren = ['geboortedatum', 'geboren', 'geboorte', 'verjaardag']
	gewicht = ['gewicht', 'zwaar', 'weegt']
	lengte = ['hoogte', 'lengte', 'lang', 'hoog']	
	specialisatie = ['specialisatie', 'specialiseert', 'gespecialiseerd', 'specialiseerde']	


	for item in line:

		if item in coach:
			query = basis.format(resource + " dbpedia-owl:coach ?result ")

		elif item in geboren:
			query = basis.format("{{" + resource + " dbpedia-owl:birthDate ?result} UNION {" + resource + " prop-nl:geboortedatum ?result}}")

		elif item in gewicht:
			query = basis.format("{{" + resource + " prop-nl:gewicht ?result} UNION {" + resource + " dbpedia-owl:weight ?result}}")

		elif item in lengte:
			query = basis.format("{{" + resource + " dbpedia-owl:height ?result} UNION {" + resource + " prop-nl:lengte ?result}}")

		elif item in specialisatie:
			query = basis.format("{{" + resource + " dbpedia-owl:speciality ?result} UNION {" + resource + " dbpedia-owl:sportSpecialty ?result} UNION {" + resource + " prop-nl:specialisatie ?result}}")

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

def main(argv):
	print_example_queries()
	anchors = getPaircounts()

	for line in sys.stdin:
		lower = line.lower()
		line = lower.rstrip()
		if line[-1] != "?":
			line = line + "?"

		xml = alpino_parse(line)
		entity = get_entity(xml)

		for ent in entity:
			entity = ent

		try:
			query = create_query(line, entity, anchors)
			answer = fire_query(query)
			print(answer, "\n")

		except:
			print("Deze vraag kan helaas niet worden beantwoord.\n")

if __name__ == "__main__":
	main(sys.argv)
