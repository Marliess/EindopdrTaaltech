
def properties():
#alle properties
	properties = {
			'evenementen':"prop-nl:evenementen",
			
			'motto':"prop-nl:motto",
			'spreuk':"prop-nl:motto",
			'eed':["prop-nl:atleteneed", "prop-nl:eed"],

			'opening':["prop-nl:opening","dbpedia-owl:officialOpenedBy"],
			'startdatum':"prop-nl:opening",
			'geopend':"prop-nl:opening",
			'begin':"prop-nl:opening",
			'sluiting':"prop-nl:sluiting",
			'einddatum': "prop-nl:sluiting",
			'einde':"prop-nl:sluiting",
			'eind':"prop-nl:sluiting",
			'plaats':"prop-nl:plaats",
			'locatie': "prop-nl:plaats",
			'gehouden':"prop-nl:plaats",
			'land':["prop-nl:plaats","dbpedia-owl:location"],

			'opener': "prop-nl:opener",
			'vlam':["dbpedia-owl:torchBearer","prop-nl:vlam"],
			'vlamdragers': ["dbpedia-owl:torchBearer","prop-nl:vlam"],
			'fakkeldragers': ["dbpedia-owl:torchBearer" "prop-nl:vlam"],
			'vlaggendrager':"prop-nl:vlaggendrager",
			'vlaggendragers':"prop-nl:vlaggendrager",
			'fakkel':["prop-nl:vlam", "dbpedia-owl:torchBearer"],

			'eerste':"prop-nl:eerste",
			'volgende':["dbpedia-owl:nextEvent","prop-nl:volgende"],
			'eerstvolgende':["dbpedia-owl:nextEvent","prop-nl:volgende"],
			'vorige':["dbpedia-owl:previousEvent","prop-nl:vorige"],
			'hoeveelste':"prop-nl:spelen",

			'atleten':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'bronzen':["prop-nl:totaalBrons","dbpedia-owl:numberOfBronzeMedalsWon"],
			'deelnemers':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'sporten':["dbpedia-owl:numberOfSports","prop-nl:sporten", "prop-nl:sport"],
			'landen':["prop-nl:landen","dbpedia-owl:numberOfParticipatingNations"],
			'wintersporten':"prop-nl:sport",
			'onderdelen':"prop-nl:disciplines",
			'sporters':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'zomersporten':"prop-nl:sport",
			'gouden':"prop-nl:olympischKampioen",
			'wereldkampioen':"dbpedia-owl:currentWorldChampion",

			'sport':"prop-nl:discipline",
			'discipline':"prop-nl:discipline",

			'trainer':["prop-nl:trainer","dbpedia-owl:coach","prop-nl:coach","dbpedia-owl:trainer"],
			'begeleider':"prop-nl:trainer",
			'gecoacht':["prop-nl:trainer","dbpedia-owl:coach","prop-nl:coach","dbpedia-owl:trainer"],
			'coach':["prop-nl:trainer","dbpedia-owl:coach","prop-nl:coach","dbpedia-owl:trainer"],

			'weegt':["prop-nl:gewicht", "dbpedia-owl:weight"],
			'gewicht':["prop-nl:gewicht", "dbpedia-owl:weight"],
			'lengte':["prop-nl:lengte","dbpedia-owl:height"],
			'lang':["prop-nl:lengte","dbpedia-owl:height"],
			'hoogte':["prop-nl:lengte","dbpedia-owl:height"],
			'geboren':"prop-nl:geboortedatum",
			'verjaardag':"prop-nl:geboortedatum",
			'bijnaam':"prop-nl:bijnaam",
			'bijnamen':"prop-nl:bijnaam",
			
			'gespecialiseerd':["prop-nl:specialisatie", "dbpedia-owl:speciality", "dbpedia-owl:sportSpecialty"],
			'specialisatie':["prop-nl:specialisatie", "dbpedia-owl:speciality", "dbpedia-owl:sportSpecialty"],
			'zwemstijl':"dbpedia-owl:swimmingStyle",
			'zwemstijlen':"dbpedia-owl:swimmingStyle"
			'meegedaan':"dbpedia-owl:olympicGames",

			'georganiseerd':["prop-nl:organisator","dbpedia-owl:organisation"],
			'organiseert':["prop-nl:organisator","dbpedia-owl:organisation"],
			'voorzitter':"prop-nl:voorzitter",
			
			}

	return properties
