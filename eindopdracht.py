#!/usr/bin/env python3
# Eindopdracht Taaltechnologie 

import socket
import sys
from lxml import etree
from SPARQLWrapper import SPARQLWrapper, JSON

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

# print een overzicht met alle voorbeeld vragen
def print_example_queries():
	print('1.  Door wie wordt Michael Phelps gecoacht?')
	print('2.  Wanneer is Bradley Wiggins geboren?')
	print('3.  Hoeveel weegt Michael Phelps?')
	print('4.  Welke lengte heeft Aleksandr Vinkoerov?')
	print('5.  Waar is Fabian Cancellara in gespecialiseerd?')
	print("")


if __name__ == "__main__":
	main(sys.argv)
