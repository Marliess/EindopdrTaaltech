#!/usr/bin/env/python3
import socket
import sys
import csv
from SPARQLWrapper import SPARQLWrapper, JSON
from xml import etree


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
              'geboortedatum':"prop-nl:geboortedatum",
              'verjaardag':"prop-nl:geboortedatum",
              'aantal atleten':"prop-nl:atleten",
              'aantal sporters':"prop-nl:atleten",
              'lengte':"prop-nl:lengte",
              'hoogte':"prop-nl:lengte",
              'sport':"prop-nl:discipline",
              'discipline':"prop-nl:discipline",
              'onderdeel':"prop-nl:discipline",
              'trainer':"prop-nl:trainer",
              'begeleider':"prop-nl:trainer"}


def main(argv):
    examples = print_example_queries()
    hulp = show_help(properties)
    print("\n\nType een vraag met de volgende structuur: \nWie/Wat is/zijn/was/waren <de/het> PROPERTY van <de/het> DOMAIN?")
    sentence = input("Type uw vraag: ")
    sentence = sentence.split()
    [x,y] = getXY(sentence)
    for line in y:
            y = y.strip('?')
    resource = resources(y)
    answer = create_and_fire_query(resource,x)


#voorbeeldvragen
def print_example_queries():
    examples = ["Wat is het motto van de Olympische Zomerspelen 2012?",
                "Wie is de trainer van Usain Bolt?",
                "Wat is het aantal landen bij de Olympische Winterspelen 2018?",
                "Wat is het aantal atleten van de Olympische Zomerspelen 2012?",
                "Wat is de locatie van de Olympische Winterspelen 2018?",
                "Wie is de opener bij de Olympische Winterspelen 2014?",
                "Wat is de geboortedatum van Naomi van As?",
                "Wat is de einddatum van de Olympische Winterspelen 2010?",
                "Wat is de lengte van Yuri van Gelder?",
                "Wat is de sport van Dafne Schippers?"]
    print("Voorbeeld vragen: ")
    for line in examples:
        print(line)
    return examples

#laat mogelijke properties aan gebruiker zien
def show_help(properties):
    print("\nU kunt alleen gebruik maken van de volgende PROPERTIES: ")
    for line in properties:
        print(line,end=", ")

#krijg de X en de Y uit een zin
def getXY(sentence):
    if ("van") in sentence:
        posVan = sentence.index("van")
        x = " ".join(sentence[3:posVan])
        y = " ".join(sentence[posVan+1:])
        y = y.strip()
        if y[:2] == 'de':
            y = " ".join(sentence[posVan+2:])
            return([x,y])
        if y[:3] == 'het':
            y = " ".join(sentence[posVan+2:])
            return([x,y])
        else:
            return([x,y])
    if ("bij") in sentence:
        posBij = sentence.index("bij")
        x = " ".join(sentence[3:posBij])
        y = " ".join(sentence[posBij+1:])
        y = y.strip()
        if y[:2] == 'de':
            y = " ".join(sentence[posBij+2:])
            return([x,y])
        if y[:3] == 'het':
            y = " ".join(sentence[posBij+2:])
            return([x,y])
        else:
            return([x,y])
        


#sorteer op vaakst voorkomende in pairCounts
def resources(y):
    page = ["url",0]
    for pair in open("pairCounts"):
        if str(y) in pair:
            pair = pair.split('\t')
            if int(pair[2]) > page[1]:
                page[0] = pair[1]
                page[1] = int(pair[2])			
    resource = page[0]
    return(resource)
        
#beantwoorden van de vraag
def answerQuestion(uri,x):
    query = "SELECT STR(?output) WHERE { <"+uri+"> " + properties[x] + " ?output }"
    sparql = SPARQLWrapper("http://nl.dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

#geeft antwoord op de vraag
def create_and_fire_query(resource,x):
    uri = resource
    results = answerQuestion(uri,x.lower())
    z = 0
    for result in results["results"]["bindings"]:
        for arg in result:
            print(result[arg]["value"])
            z+=1
    if z == 0:
        print("Niet gevonden")


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

while True:
    sentence = input("Stel uw vraag: ").replace("?","")
    if sentence == "":
        print_example_queries()

    xml = alpino_parse(sentence)
    root = xml.xpath('//node[@spectype="deeleigen"]')
    for node in root :
        print(node.attrib["word"])

    root = xml.xpath('//node[@cat="mwu" and @rel="obj1"]')
    for node in root:
        if "mwu_root" in node.attrib:
           y = node.attrib["mwu_root"]

    root = xml.xpath('//node[@cat="mwu" and @rel="su"]')
    for node in root:
        if "mwu_root" in node.attrib:
            y = node.attrib["mwu_root"]

    root = xml.xpath('//node[@cat="ppart" and @rel="vc"]/node[@rel="obj1"]')
    for node in root:
        if "lemma" in node.attrib:
            y = node.attrib["lemma"]

    root = xml.xpath('//node[@lemma="sport"]')
    for node in root:
        if "lemma" in node.attrib:
            x = node.attrib["lemma"]
        
    root = xml.xpath('//node[@cat="np" and @rel="su"]/node[@word]')
    for node in root:
        if "lemma" in node.attrib:
            if node.attrib["lemma"] != "de":
                x = node.attrib["lemma"]


    if x.lower() in properties:
        sentence = sentence.split()
        page = ["url",0]
        for pair in open("pairCounts"):
            if str(y) in pair:
                pair = pair.split('\t')
                if int(pair[2]) > page[1]:
                    page[0] = pair[1]
                    page[1] = int(pair[2])			
        resource = page[0]
        uri = "http://nl.dbpedia.org/resource/"+resource
        results = answerQuestion(uri,x.lower())
        i = 0
        for result in results["results"]["bindings"]:
            for arg in result:
                print(result[arg]["value"])
                i+=1

        if i == 0:
            print("Ik kan het niet vinden")



if __name__ == "__main__":
    main(sys.argv)
