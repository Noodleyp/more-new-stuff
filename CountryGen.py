### tombricks
### [TAG, country name (generic), adjective, ideology, capital, rrr ggg bbb, common/countries file]

countries = [
	{
		"tag":				"DON",
		"name":				"Donbass",
		"adj":				"Donbass",
		"ideology":			"Marxism_Leninism",
		"capital":			"227",
		"colour":			"91 51 83",
		"culture":			"Eastern_European",
		"long_name":		"Federal State of Donbass",
		"long_name_def":	"the Federal State of Donbass",
		"parties":			{
		},
		"characters":		{
		}
	}
]

from shutil import copyfile
import os.path
import codecs
FileTags  = open("common/country_tags/00_countries.txt", "a+", encoding="utf8")
FileColor = open("common/countries/colors.txt", "a+", encoding="utf8")

for country in countries:
	if "long_name" not in country:
		country["long_name"] = country["name"]
	if "long_name_def" not in country:
		country["long_name_def"] = "the " + country["long_name"]

	FileTags.write(F'\n{country["tag"]} = "countries/{country["culture"]}.txt" ')
	FileLoc   = open("localisation/english/countries/Country_"+country["tag"]+"_l_english.yml", "w", encoding="utf8")

	FileLoc.write('\ufeff')
	FileLoc.write(F"""l_english:
### Country Names and Cosmetics
 {country["tag"]}: "{country["name"]}"
 {country["tag"]}_DEF: "{country["name"]}"
 {country["tag"]}_ADJ: "{country["adj"]}" 
 
 {country["tag"]}_fascism: "{country["long_name"]}"
 {country["tag"]}_fascism_DEF: "{country["long_name_def"]}"
 {country["tag"]}_communism: "{country["long_name"]}"
 {country["tag"]}_communism_DEF: "{country["long_name_def"]}"
 {country["tag"]}_democratic: "{country["long_name"]}"
 {country["tag"]}_democratic_DEF: "{country["long_name_def"]}"
 {country["tag"]}_neutrality: "{country["long_name"]}"
 {country["tag"]}_neutrality_DEF: "{country["long_name_def"]}"

 """)
	
	parties = {
		"fascism_party": "$Fascism_party$",
		"fascism_party_long": "$Fascism_party_long$",
		"Marxism_Leninism_party": "$Marxism_Leninism_party$",
		"Marxism_Leninism_party_long": "$Marxism_Leninism_party_long$",
		"New_Marxism_party": "$New_Marxism_party$",
		"New_Marxism_party_long": "$New_Marxism_party_long$",
		"Socialism_party": "$Socialism_party$",
		"Socialism_party_long": "$Socialism_party_long$",
		"Reactionism_party": "$Reactionism_party$",
		"Reactionism_party_long": "$Reactionism_party_long$"
	}

	for party in country["parties"]:
		parties[party+"_party"] = country["parties"][party][0]
		parties[party+"_party_long"] = country["parties"][party][1]
	
	for party in parties:
		FileLoc.write(F'{country["tag"]}_{party}: "{parties[party]}"\n ')

	FileColor.write(F"""
{country["tag"]} = {{
	color = rgb {{ {country["colour"]} }}
	color_ui = rgb {{ {country["colour"]} }}
}}""")

	path = F'history/countries/{country["tag"]} - {country["name"]}.txt'
	with open(path, "w", encoding="utf8") as FileHistory:
		FileHistory.write(F"""capital = {country["capital"]}
set_stability = 0.6
set_war_support = 0.6

# Starting tech
tech_setup_generic = yes

set_politics = {{
	ruling_party = {country["ideology"]}
	last_election = "1978.1.1"
	election_frequency = 48
	elections_allowed = no
}}

set_popularities = {{
	{country["ideology"]} = 100
}}

""")
		for character in country["characters"]:
			FileHistory.write(F'recruit_character = {country["tag"]}_{character}\n')
			FileLoc.write(F'\n {country["tag"]}_{character}: "{country["characters"][character]["name"]}"\n {country["tag"]}_{character}_desc: ""')

	path = F'common/characters/{country["tag"]}.txt'
	with open(path, "w", encoding="utf8") as FileCharacters:
		FileCharacters.write("characters = {")
		for character in country["characters"]:
			FileCharacters.write(F"""
	{country["tag"]}_{character} = {{
		name = {country["tag"]}_{character}

		allowed_civil_war = {{
		}}

		portraits = {{
			civilian = {{
				large = "GFX_Portrait_Generic_Leader"
			}}
			army = {{
				small = "GFX_Minister_Generic_Leader"
			}}
		}}
		
		""")
			for ideology in country["characters"][character]["ideologies"]:
				FileCharacters.write(F"""
		country_leader = {{
			ideology = {ideology}_ideology
			traits = {{ TITLE_{country["characters"][character]["title"]} IDEOLOGY_{country["characters"][character]["subideology"]} }}
			desc = {country["tag"]}_{character}_desc
		}}
""")
			FileCharacters.write("\n	}")
		FileCharacters.write("\n}")

	if not os.path.isfile(F'gfx/flags/{["tag"]}.tga'):
		copyfile("gfx/flags/ZZZ.tga", F'gfx/flags/{country["tag"]}.tga')
		copyfile("gfx/flags/medium/ZZZ.tga", F'gfx/flags/medium/{country["tag"]}.tga')
		copyfile("gfx/flags/small/ZZZ.tga", F'gfx/flags/small/{country["tag"]}.tga')

FileTags.seek(0)
print(FileTags.read())
FileColor.seek(0)
print(FileColor.read())
