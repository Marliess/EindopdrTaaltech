
def properties():
#alle properties
	properties = {
			'motto':"prop-nl:motto",
			'spreuk':"prop-nl:motto",
			'opening':"prop-nl:opening",
			'startdatum':"prop-nl:opening",
			'begin':"prop-nl:opening",
			'plaats':"prop-nl:plaats",

			'locatie': "prop-nl:plaats",
			'evenementen':"prop-nl:evenementen",

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

			'trainer':"prop-nl:trainer",
			'begeleider':"prop-nl:trainer",
			'sport':["prop-nl:discipline", "prop-nl:discipline"],	

			'gespecialiseerd':["prop-nl:specialisatie", "dbpedia-owl:speciality", "dbpedia-owl:sportSpecialty"],


			'weegt':["prop-nl:gewicht", "dbpedia-owl:weight"],
			'bijnaam':"prop-nl:bijnaam",
			'bijnamen':"prop-nl:bijnaam",
			'motto':"prop-nl:motto",
			'spreuk':"prop-nl:motto",

			'opening':["prop-nl:opening","dbpedia-owl:officialOpenedBy"],
			'startdatum':"prop-nl:opening",

			'geopend':"prop-nl:opening",


			'begin':"prop-nl:opening",
			'plaats':"prop-nl:plaats",
			'locatie': "prop-nl:plaats",
			'land':["prop-nl:plaats","dbpedia-owl:location"],

			'opener': "prop-nl:opener",
			'officiele opener':"prop-nl:opener"
			,
			'vlam':["dbpedia-owl:torchBearer","prop-nl:vlam"],
			'vlamdragers': ["dbpedia-owl:torchBearer","prop-nl:vlam"],
			'fakkeldragers': ["dbpedia-owl:torchBearer" "prop-nl:vlam"],
			'vlaggendrager':"prop-nl:vlaggendrager",
			'vlaggendragers':"prop-nl:vlaggendrager",
			'fakkel':["prop-nl:vlam", "dbpedia-owl:torchBearer"],

			'sluiting':"prop-nl:sluiting",
			'einddatum': "prop-nl:sluiting",
			'einde':"prop-nl:sluiting",
			'eind':"prop-nl:sluiting",

			'eerste Olympische':"prop-nl:eerste",
			'eerste zomerspelen':"prop-nl:eerste",
			'eerste winterspelen':"prop-nl:eerste",
			'eerste Olympische Zomerspelen':"prop-nl:eerste",

			'volgende Olympische Spelen':["dbpedia-owl:nextEvent","prop-nl:volgende"],
			'volgende Olympische Zomerspelen':["dbpedia-owl:nextEvent","prop-nl:volgende"],
			'volgende zomerspelen':["dbpedia-owl:nextEvent","prop-nl:volgende"],
			'volgende winterspelen':["dbpedia-owl:nextEvent","prop-nl:volgende"],
			'volgende Olympische Winterspelen':["dbpedia-owl:nextEvent","prop-nl:volgende"],

			'vorige zomerspelen':["dbpedia-owl:previousEvent","prop-nl:vorige"],
			'vorige winterspelen':["dbpedia-owl:previousEvent","prop-nl:vorige"],
			'vorige Olympische Winterspelen':["dbpedia-owl:previousEvent","prop-nl:vorige"],
			'vorige Olympische Zomerspelen':["dbpedia-owl:previousEvent","prop-nl:vorige"],
			'vorige Olympische Spelen':["dbpedia-owl:previousEvent","prop-nl:vorige"],

			'geboren':"prop-nl:geboortedatum",
			'verjaardag':"prop-nl:geboortedatum",

			'aantal atleten':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'atleten':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'aantal atleten':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'Hoeveel atleten':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'aantal sporters':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'atleten':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'bronzen medailles':["prop-nl:totaalBrons","dbpedia-owl:numberOfBronzeMedalsWon"],
			'deelnemers':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'deelnemende atleten':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'sporten':["dbpedia-owl:numberOfSports","prop-nl:sporten"],
			'Hoeveel landen':["prop-nl:landen","dbpedia-owl:numberOfParticipatingNations"],
			'deelnemende landen':["prop-nl:landen","dbpedia-owl:numberOfParticipatingNations"],
			'landen':["prop-nl:landen","dbpedia-owl:numberOfParticipatingNations"],
			'wintersporten':"prop-nl:sport",
			'onderdelen':"prop-nl:disciplines",
			'sporters':["prop-nl:atleten","dbpedia-owl:numberOfParticipatingAthletes"],
			'zomersporten':"prop-nl:sport",

			'hoeveelste':"prop-nl:spelen",

			'lengte':["prop-nl:lengte","dbpedia-owl:height"],
			'lang':["prop-nl:lengte","dbpedia-owl:height"],
			'hoogte':"prop-nl:lengte",

			'sport':"prop-nl:discipline",
			'discipline':"prop-nl:discipline",

			'gouden medialle':"prop-nl:olympischKampioen",
			'wereldkampioen':"dbpedia-owl:currentWorldChampion",

			#'onderdeel':"prop-nl:discipline",

			'trainer':["prop-nl:trainer","dbpedia-owl:coach","prop-nl:coach","dbpedia-owl:trainer"],
			'begeleider':"prop-nl:trainer",
			'gecoacht':["prop-nl:trainer","dbpedia-owl:coach","prop-nl:coach","dbpedia-owl:trainer"],
			'coach':["prop-nl:trainer","dbpedia-owl:coach","prop-nl:coach","dbpedia-owl:trainer"],


			'weegt':["prop-nl:gewicht", "dbpedia-owl:weight"],

			'bijnaam':"prop-nl:bijnaam",

			'meegedaan':"dbpedia-owl:olympicGames",

			'georganiseerd':["prop-nl:organisator","dbpedia-owl:organisation"],
			'organiseert':["prop-nl:organisator","dbpedia-owl:organisation"],

			'gehouden':"prop-nl:plaats",
			'voorzitter':"prop-nl:voorzitter",

			'eed':["prop-nl:atleteneed", "prop-nl:eed"],

			'zwemstijl':"dbpedia-owl:swimmingStyle",
			'zwemstijlen':"dbpedia-owl:swimmingStyle"
			}

	return properties
