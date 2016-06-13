def properties():
#alle properties
    properties = {
            'evenementen':"prop-nl:evenementen",
            
            'motto':["prop-nl:motto","dbpedia-owl:motto"],
            'spreuk':["prop-nl:motto","dbpedia-owl:motto"],
            'eed':["prop-nl:atleteneed", "prop-nl:eed","dbpedia-owl:olympicOathSwornBy"],

            'opening':["prop-nl:opening","dbpedia-owl:officialOpenedBy"],
            'startdatum':["prop-nl:opening","dbpedia-owl:startDate"],
            'geopend':["prop-nl:opening","dbpedia-owl:startDate"],
            'begin':["prop-nl:opening","dbpedia-owl:startDate"],
            'beginnen':["prop-nl:opening","dbpedia-owl:startDate"],
            'begonnen':["prop-nl:opening","dbpedia-owl:startDate"],
            'sluiting':["prop-nl:sluiting","dbpedia-owl:endDate"],
            'einddatum':["prop-nl:sluiting","dbpedia-owl:endDate"],
            'einde':["prop-nl:sluiting","dbpedia-owl:endDate"],
            'eind':["prop-nl:sluiting","dbpedia-owl:endDate"],
            'eindigen':["prop-nl:sluiting","dbpedia-owl:endDate"],
            'eindigden':["prop-nl:sluiting","dbpedia-owl:endDate"],
            'eind':["prop-nl:sluiting","dbpedia-owl:endDate"],
            'plaats':["prop-nl:plaats","dbpedia-owl:location","prop-nl:geboorteplaats"],
            'locatie':["prop-nl:plaats","dbpedia-owl:location"],
            'gehouden':["prop-nl:plaats","dbpedia-owl:location"],
            'land':["prop-nl:plaats","dbpedia-owl:location"],
            'stad':["prop-nl:plaats","dbpedia-owl:location","prop-nl:geboorteplaats","prop-nl:geboortestad"],

            'opener':["prop-nl:opener","dbpedia-owl:officialOpenedBy"],
            'opende':["prop-nl:opener","dbpedia-owl:officialOpenedBy"],
            'fakkel':["prop-nl:vlam", "dbpedia-owl:torchBearer"],
            'vlam':["prop-nl:vlam", "dbpedia-owl:torchBearer"],
            'vlamdragers':["dbpedia-owl:torchBearer","prop-nl:vlam"],
            'fakkeldragers':["dbpedia-owl:torchBearer" "prop-nl:vlam"],
            'vlaggendrager':["prop-nl:vlaggendrager","dbpedia-owl:flagBearer"],
            'vlaggendragers':["prop-nl:vlaggendrager","dbpedia-owl:flagBearer"],

            'eerste':"prop-nl:eerste",
            'volgende':["dbpedia-owl:nextEvent","prop-nl:volgende"],
            'eerstvolgende':["dbpedia-owl:nextEvent","prop-nl:volgende"],
            'vorige':["dbpedia-owl:previousEvent","prop-nl:vorige"],
            'hoeveelste':"prop-nl:spelen",
            'website':["foaf:homepage"],

            'atleten':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
            'deelnemers':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
            'sporten':["dbpedia-owl:numberOfSports","prop-nl:sporten","prop-nl:sport"],
            'landen':["prop-nl:landen","dbpedia-owl:numberOfParticipatingNations"],
            'wintersporten':"prop-nl:sport",
            'onderdelen':"prop-nl:disciplines",
            'sporters':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
            'zomersporten':"prop-nl:sport",
            'gouden':"prop-nl:olympischKampioen",
            'wereldkampioen':"dbpedia-owl:currentWorldChampion",

            'sport':["prop-nl:discipline","dbpedia-owl:sportDiscipline"],
            'discipline':["prop-nl:discipline","dbpedia-owl:sportDiscipline"],
            'disciplines':["prop-nl:discipline","dbpedia-owl:sportDiscipline","prop-nl:disciplines"],
            'beoefent':["prop-nl:discipline","dbpedia-owl:sportDiscipline"],
            'beoefende':["prop-nl:discipline","dbpedia-owl:sportDiscipline"],

            'trainer':["prop-nl:trainer","dbpedia-owl:coach","prop-nl:coach","dbpedia-owl:trainer"],
            'begeleider':["prop-nl:trainer","dbpedia-owl:coach","prop-nl:coach","dbpedia-owl:trainer"],
            'gecoacht':["prop-nl:trainer","dbpedia-owl:coach","prop-nl:coach","dbpedia-owl:trainer"],
            'coach':["prop-nl:trainer","dbpedia-owl:coach","prop-nl:coach","dbpedia-owl:trainer"],

            'weegt':["prop-nl:gewicht","dbpedia-owl:weight"],
            'gewicht':["prop-nl:gewicht","dbpedia-owl:weight"],
            'zwaar':["prop-nl:gewicht","dbpedia-owl:weight"],
            'lengte':["prop-nl:lengte","dbpedia-owl:height"],
            'lang':["prop-nl:lengte","dbpedia-owl:height"],
            'hoogte':["prop-nl:lengte","dbpedia-owl:height"],
            'geboren':["prop-nl:geboortedatum","dbpedia-owl:birthDate","prop-nl:geboorteplaats","prop-nl:geboortestad"],
            'verjaardag':["prop-nl:geboortedatum","dbpedia-owl:birthDate"],
            'geboorteplaats':["prop-nl:geboorteplaats","prop-nl:geboortestad","dbpedia-owl:birthPlace"],
            'geboortedatum':["prop-nl:geboortedatum","dbpedia-owl:birthDate"],
            'bijnaam':["prop-nl:bijnaam","foaf:nick"],
            'bijnamen':["prop-nl:bijnaam","foaf:nick"],
            'volledige':["prop-nl:naam","dbpedia-owl:birthName"],
            
            'gespecialiseerd':["prop-nl:specialisatie","dbpedia-owl:speciality","dbpedia-owl:sportSpecialty"],
            'specialisatie':["prop-nl:specialisatie","dbpedia-owl:speciality","dbpedia-owl:sportSpecialty"],
            'zwemstijl':["prop-nl:slagen","dbpedia-owl:swimmingStyle",],
            'zwemstijlen':["prop-nl:slagen","dbpedia-owl:swimmingStyle",],
            'meegedaan':["dbpedia-owl:olympicGames"],

            'georganiseerd':["prop-nl:organisator","dbpedia-owl:organisation"],
            'organiseert':["prop-nl:organisator","dbpedia-owl:organisation"],
            'voorzitter':["prop-nl:voorzitter","dbpedia-owl:chairperson"],
            'president':["prop-nl:voorzitter","dbpedia-owl:chairperson"],
            'topman':["prop-nl:voorzitter","dbpedia-owl:chairperson"],
            }

    return properties

def propertiesWaar():
    prop = properties()
    prop['geboren'] = ["prop-nl:geboorteplaats","prop-nl:geboortestad","dbpedia-owl:birthPlace"]
    return prop

def propertiesWanneer():
    prop = properties()
    prop['geboren'] = ["prop-nl:geboortedatum","dbpedia-owl:birthDate"]
    return prop
