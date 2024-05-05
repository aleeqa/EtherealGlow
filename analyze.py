import re

comedogenic_ingredients = [ "Acetylated Lanolin",
    "Acetylated Lanolin Alcohol",
    "Acetylated wool fat",
    "Acetylated wool wax",
    "Adansonia digitata l.",
    "Agar",
    "Ahnfeltiopsis concinna extract",
    "Alaria esculenta extract",
    "Alga bladderwrack",
    "Algae",
    "Algae Extract",
    "Algin",
    "Alginate",
    "Alginic acid",
    "Algea",
    "Aphanothece sacrum polysaccharide",
    "Arthrospira plantensis",
    "Ascophyllum nodosum extract",
    "Asparagopsis armata extract",
    "Baobab",
    "Beeswax",
    "Bismuth",
    "Bryopsis africana",
    "Butyl Stearate",
    "Butyrospermum",
    "Cacao seed butter",
    "Capea biruncinata var. denuda sonder",
    "Capea biruncinata var. elongata sonder",
    "Carageenan gum",
    "Carastay c",
    "Caulerpa lentillifera extract",
    "Caulerpa filiformis",
    "Carrageenan",
    "Carrageenan Moss",
    "Cera alba",
    "Cera bianca",
    "Cera flava",
    "Cera olea",
    "Cetearyl Alcohol + Ceteareth 20",
    "Chaetomorpha linum (aerea) cladophora radiosa",
    "Chlamydomonas reinhardtii extract",
    "Chlorella",
    "Chlorophyceae",
    "Chondrus Crispus (aka Irish Moss or Carageenan Moss)",
    "Cladophora cf. subsimplex",
    "Cladosiphon okamuranus extract",
    "Coal Tar",
    "Coco-caprylate",
    "Cocoa Butter",
    "Coconut Alkanes",
    "Coconut Butter",
    "Coconut Extract",
    "Coconut Nucifera extract",
    "Coconut Oil",
    "Cocos nucifera oil",
    "cocos nucifera seed butter",
    "Coenochloris signiensis extract",
    "Colloidal Sulfur",
    "Cotton Awws Oil",
    "Cotton Seed Oil",
    "Corallina officinalis extract",
    "Corn",
    "Corn oil",
    "Creosote",
    "Cystoseira tamariscifolia extract",
    "D & C Red # 17",
    "D & C Red # 21",
    "D & C Red # 3",
    "D & C Red # 30",
    "D & C Red # 36",
    "Decyl Oleate",
    "Dictyopteris membranacea",
    "Dictyopteris polypodioides",
    "Dilsea carnosa extract",
    "Dioctyl Succinate",
    "Disodium Monooleamido",
    "Dodecanoic acid",
    "Dunaliella salina extract",
    "Durvillaea antarctica extract",
    "Ecklonia cava",
    "Ecklonia cava extract",
    "Ecklonia radiata",
    "Enteromorpha compressa extract",
    "Ethoxylated Lanolin",
    "Ethylhexyl Palmitate",
    "Eucheuma spinosum extract",
    "Fucoxanthin",
    "Fucus serratus",
    "Fucus vesiculosus",
    "Gamtae extract",
    "Gelidiella acerosa extract",
    "Gelidium amansii extract",
    "Gigartina stellata extract",
    "Glyceryl Stearate SE",
    "Glyceryl-3 Diisostearate",
    "Glycine soja oil",
    "Glycine max",
    "Gracilariopsis chorda extract",
    "Haematococcus pluvialis extract",
    "Haematococcus pluvialis",
    "Haslea ostrearia extract",
    "Hexadecyl Alcohol",
    "Himanthalia elongata extract",
    "Hizikia fusiforme extract",
    "Hydrogenated Vegetable Oil",
    "Hydrolyzed rhodophycea extract",
    "Hydrous magnesium silicate",
    "Hypnea musciformis extract",
    "Hypneaceae extract",
    "Irish Moss",
    "Isocetyl Alcohol",
    "Isocetyl Stearate",
    "Isodecyl Oleate",
    "Isopropyl Isostearate",
    "Isopropyl Linolate",
    "Isopropyl Myristate",
    "Isopropyl Palmitate",
    "Isostearyl Isostearate",
    "Isostearyl Neopentanoate",
    "Jania rubens extract",
    "Jojoba wax",
    "Kappaphycus alvarezii extract",
    "Karite",
    "Kelp",
    "Kousou ekisu",
    "Laminaria",
    "Laminaria Digitata Extract",
    "Laminaria Saccharina Extract (Laminaria Saccharine)",
    "Laureth-23",
    "Laureth-4",
    "Lauric Acid",
    "Linolate",
    "Liquor picis carbonis",
    "Lithothamnium calcareum powder",
    "Lpc",
    "Macroalgae",
    "Macrocystis pyrifera extract",
    "Mangifera indica seed butter",
    "Mango Butter",
    "Marula",
    "Marula oil",
    "Mink Oil",
    "Moringa Oil",
    "Moss",
    "Myristate",
    "Myristic Acid",
    "Myristyl",
    "Myristyl Lactate",
    "Myristyl Myristate",
    "Myristyl Propionate",
    "Octyl Stearate",
    "Oleth-3",
    "Oleyl Alcohol",
    "Palmaria palmata extract",
    "Palm Oil",
    "Parkii",
    "PEG 2 Sulfosuccinate",
    "PEG 16 Lanolin",
    "PEG 200 Dilaurate",
    "PEG 8 Stearate",
    "Pelvetia canaliculata extract",
    "Phaeodactylum tricornutum extract",
    "Phaeophyceae",
    "Pix carbonis",
    "PG Monostearate",
    "PPG-2 Myristyl",
    "PPG 2 Myristyl Propionate",
    "PPG 2 Myristyl Ether Propionate",
    "Plankton",
    "Polysiphonia elongata extract",
    "Polyglyceryl-3 Di" ]

def analyzer_tool(ingredients):
    ingredients_lower = ingredients.lower()
    comedogenic_detected = []

    for ingredient in comedogenic_ingredients:
        #creates regular exp pattern for each ingredient/ re.escape() is used to ensure pattern match the literal string
        pattern = re.escape(ingredient.lower())
        #search ingredient pattern within the input
        if re.search(r'\b' + pattern + r'\b', ingredients_lower) or re.search(pattern, ingredients_lower):
            comedogenic_detected.append(ingredient)

    #display comedogenic ingredients found
    if comedogenic_detected:
        return "Oh NO! The following ingredients are comedogenic: {}".format(','.join(comedogenic_detected))       
    
    else:
    #when ingredient doesnt exist in comedogenic_ingredients
        return "Yeay! None of the ingredients are comedogenic."    