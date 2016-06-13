#!/usr/bin/env python3
# eindopdracht.py
# Dit programma is geschreven voor de eindopdracht van Taaltechnologie 2016
# Door: Anouk Broer, Moniek Nieuwenhuis, Karel Beckeringh en Marlies Quekel 

import socket
import properties
import sys
from lxml import etree
from SPARQLWrapper import SPARQLWrapper, JSON

########################################
# getQuestion  
# De functie get_questions opent het bestand met alle vragen die beantwoord moeten worden. 
# Vervolgens worden alle vragen in een lijst gezet, ieder item in die lijst is een regel uit het bestand.
########################################

def get_questions():

	questionList = []
	with open('vragen.txt', 'r', encoding='utf-8') as data:
		questions = data.readlines()

		for line in questions:
			questionList.append(line.strip('\n'))

	return questionList

########################################
# get_paircounts
# De functie get_paircounts opent het bestand paircounts en laadt de regels van het bestand in de lijst 'anchors'.
# De lijst anchors bestaat uit verschillende lijsten. Elke lijst representeert een regel van het bestand
# paircounts. Elke regel-lijst bestaat uit drie elementen: anchor, URI, frequentie. 
########################################

def get_paircounts():

	anchors = []
	with open('pairCounts', 'r', encoding='utf-8') as data:
	    pairCounts = data.readlines()

	    for line in pairCounts:
	        anchors.append(line.split('\t'))

	return anchors

########################################
# alpino_parse
# De functie alpino_parse haalt de vraag door de Alpino Parser. Dit resulteert in een parsetree van de zin
# waarin de syntactische structuur van de zin beschreven is. De syntactische structuur wordt gerepresenteert
# in een hierarchische structuur in XML. De functie geeft de XML structuur terug. (Deze code komt
# rechtstreeks uit de slides van week 4.)
########################################

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
	xml = etree.fromstring(bytes_received)
	return xml

########################################
# get_entity
# De functie get_entity verkrijgt de entiteit uit de vraag. Dit is bijvoorbeeld de naam van een sporter of de naam
# van een Olympische Spelen. De entiteit wordt verkregen door in de XML structuur te zoeken op bepaalde relaties
# tussen woorden en nodes. --> zie de zoekopdracht bij xml.xpath. De gevonden entities worden toegevoegd aan de lijst entitie.
########################################

def get_entity(xml):
	entitie = []

	entitieList = xml.xpath('.//node[(@pos="name" and not(@rel="mwp") or (@spectype="deeleigen") or (@cat="mwu" and node[@pos="name"]))]')
	
	for ent in entitieList:
		entitie.append(tree_yield(ent))

	return entitie

########################################
# get_olympic
# De functie get_olympic is bijna hetzelfde als de functie get_entity. get_olympic is echter bedoeld voor zinnen waarin de entitie
# een Olympische Spelen is waarbij het woord "van" voor het jaartal van de Spelen staat. De entiteit wordt verkregen door in de 
# XML structuur te zoeken op bepaalde relaties tussen woorden en nodes. --> zie de zoekopdracht bij xml.xpath. De gevonden 
# entiteiten worden toegevoegd aan de lijst entitie.
########################################

def get_olympic(xml):
	entities = []

	entitieList = xml.xpath('//node[@cat="np" and @rel="obj1"]/node[@rel]/node[@word]')

	for ent in entitieList:
		if "word" in ent.attrib:
			if ent.attrib["word"] != "de":
				entities.append(ent.attrib["word"])

	entitie = [' '.join(map(str, entities))]

	return entitie

########################################
# tree_yield
# De functie tree_yield zoekt het bijbehoorde woord van een relatie/node. 
# Deze functie wordt aangeroepen in get_entity.
########################################

def tree_yield(xml):
    leaves = xml.xpath('descendant-or-self::node[@word]')
    words = []
    for l in leaves :
        words.append(l.attrib["word"])
    return " ".join(words)

########################################
# create_query
# De functie create_query maakt een sparql query op basis van de entity, URI en een bijbehorende propertie.
# In het bestand properties.py staat een dictionary met woorden (key) en bijbehorende properties (values). Voor elke vraag
# wordt gekeken of een key uit de properties dictionary voorkomt in de vraag. Als een key voorkomt, wordt de bijbehorende
# propertie gezocht. Sommige keys hebben meerdere properties. Er worden verschillende properties getest in de query,
# net zo lang totdat er een antwoordt komt. De juiste query wordt uitgevoerd door de functie fire_query.
########################################

def create_query(line, entity, anchors, propertieList):

	line = line[:-1].split(" ")

	resource = "<" + get_resource(entity, anchors) + ">"
	#print(resource)

	# de basis van de query
	basis = """
        SELECT STR(?result) as ?result
        WHERE  {{
            {}
        }}ORDER BY ?result
        """
	
	for item in line:

		if item in propertieList:

			if type(propertieList[item]) is list:
				propList = propertieList[item]
				
				try:
					query = basis.format("{{" + resource + " " + propList[0] +" ?result}}")
					answer = fire_query(query)
					if answer == False:
						break					
				except:
					try:
						query = basis.format("{{" + resource + " " + propList[1] +" ?result}}")
						answer = fire_query(query)
						if answer == False:
							break
					except:
						try:
							query = basis.format("{{" + resource + " " + propList[2] +" ?result}}")
							answer = fire_query(query)
							if answer == False:
								break							
						except:
							try:
								query = basis.format("{{" + resource + " " + propList[3] +" ?result}}")
								answer = fire_query(query)
								if answer == False:
									break
							except:
								break
			else:
				query = basis.format("{{" + resource + " " + propertieList[item] +" ?result}}")
				fire_query(query)

	return(query)

########################################
# get_resource
# De functie get_resource zoekt de URI die bij de entitiy hoort. Deze functie wordt aangeroepen in de functie
# create_query, en geeft de juiste URI voor de query aan de functie terug. 
########################################

def get_resource(entity, anchors):
	highestFreq = 0
	for line in anchors:
		if line[0].lower() == entity:
			if int(line[2]) > highestFreq:
				highestFreq = int(line[2])
				link = line[1]	
	return link

########################################
# fire_query
# De functie fire_query stuurt de query naar dpbedia en geeft(print) het antwoord.
########################################

def fire_query(query):
	sparql = SPARQLWrapper("http://nl.dbpedia.org/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	if results != []:
		for result in results["results"]["bindings"]:
			for arg in result:
				answer = result[arg]["value"]
				print(answer)
	else:
		answer = False 

	return answer


########################################
# main
# De functie main 
########################################

def main():

	# verkrijg de dictionary met properties
	propertieList = properties.properties()	

	# verkrijg de vragen die beantwoord moeten worden
	questions = get_questions()

	# verkrijg een lijst met anchors uit het bestand pairCounts
	anchors = get_paircounts()

	# placeholder voor het aantal antwoorden dat wel en niet beantwoord kunnen worden
	goed = 0
	fout = 0

	# open een bestand waar de antwoorden in komen die niet beantwoord kunnen worden
	# f = open('foute_vragen.txt', 'a', encoding='utf-8')

	# voor iedere vraag in de lijst met vragen
	for line in questions:
		enti = []
		# print de vraag
		print(line)

		# parse de vraag met alpino  
		xml = alpino_parse(line)

		# verkrijg de entitiy uit de parse 
		# als het woord Olympische in de vraag staat en deze wordt gevolgd door ... "van"
		# verkrijg dan de entitie met behulp van de functie get_olympic. Zo niet, verkrijgt
		# de entitie dan met behulp van de functie get_entity


		olymp = ["Olympische Spelen van",
				 "Olympische Winterspelen van",
				 "Olympische Zomerspelen van",
				 "Olympische Spelen in", 
				 "Olympische Winterspelen in", 
				 "Olympische Zomerspelen in"]


		if olymp[0] in line:
			enti = get_olympic(xml)	
		elif olymp[1] in line:
			enti = get_olympic(xml)
		elif olymp[2] in line:
			enti = get_olympic(xml)
		elif olymp[3] in line:
			enti = get_olympic(xml)
		elif olymp[4] in line:
			enti = get_olympic(xml)
		elif olymp[5] in line:
			enti = get_olympic(xml)
		else:
			enti = get_entity(xml)


		# probeer een antwoord op de vraag te vinden. Als dit niet lukt,
		# dan is de poging gefaalt en kan de vraag niet beantwoord worden.
		try:
			entity = enti[0].lower()
			query = create_query(line, entity, anchors, propertieList)
			goed += 1	
			print()
		except:
                        print(">>> Deze vraag kan helaas niet worden beantwoord.\n")
			# schrijf alle vragen die niet beantwoord kunnen worden naar "f"
			# f.write(line + "\n")
                        fout += 1

	print("Er zijn {} die beantwoord konden worden. {} konden niet worden beantwoord".format(goed,fout))

	# f.close()

if __name__ == "__main__":
	main()
