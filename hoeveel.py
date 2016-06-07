#hoeveel-vragen

import socket
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
from lxml import etree

def main(argv):
    sentence = input("Type uw vraag: ")
    u = hoeveel(sentence)
    if sentence != "":
        main(argv)
    else:
        exit
        
#beantwoorden van de vraag
def answerQuestion(uri,x):
    query = "SELECT STR(?output) WHERE { <"+uri+"> " + "prop-nl:"+x + " ?output }"
    sparql = SPARQLWrapper("http://nl.dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

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

def hoeveel(sentence):
    xml = alpino_parse(sentence)

    root = xml.xpath('//node[@cat="np" and @rel="obj1"]/node[@rel]/node[@word]')
    listy = []
    for node in root:
        if "word" in node.attrib:
            if node.attrib["word"] != "de":
                listy.append(node.attrib["word"])
    y = ' '.join(map(str, listy))
    print(y)
    
    root = xml.xpath('//node[@cat="np" and @rel="whd"]/node[@pt="n"]')
    for node in root:
        x = node.attrib["word"]
        print(x)

    try:
        sentence = sentence.split()
        page = ["url",0]
        for pair in open("pairCounts"):
            if y in pair:
                pair = pair.split('\t')
                if int(pair[2]) > page[1]:
                    page[0] = pair[1]
                    page[1] = int(pair[2])			
        resource = page[0]
        print(resource)
        uri = resource
        results = answerQuestion(uri,x.lower())
        i = 0
        for result in results["results"]["bindings"]:
            for arg in result:
                print(result[arg]["value"])
                i+=1
        if i == 0:
            print("Ik kan het niet vinden")
    except:
        print("Niet gevonden")


if __name__ == "__main__":
    main(sys.argv)
