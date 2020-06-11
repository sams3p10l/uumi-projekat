from lxml import etree

def main():
    xmlDoc = etree.parse("karton.xml")

    rezultat = xmlDoc.xpath("/zdravstveni_karton/pregledi/pregled")
    for pregled in rezultat:
        atributi = pregled.attrib
        for atribut in atributi:
            print(atribut + ":", atributi[atribut])
        for podelement in pregled:
            print(podelement.tag + ":", podelement.text)
        print()

    anamneza = xmlDoc.xpath("/zdravstveni_karton/anamneza")[0]
    if True:
        oboljenje = etree.Element("oboljenje")
        if True:
            dijagnoza = etree.Element("dijagnoza")
            dijagnoza.append(etree.Element("naziv"))
            if True:
                datumDijagnoze = etree.Element("datum_dijagnoze")
                datumDijagnoze.text = "2015-01-01"
            dijagnoza.append(datumDijagnoze)
            dijagnoza.append(etree.Element("lekar"))
        oboljenje.append(dijagnoza)
        if True:
            terapije = etree.Element("terapije")
            if True:
                atributi = {"tip_terapije":""}
                terapija = etree.Element("terapija", atributi)
                terapija.append(etree.Element("opis"))
                if True:
                    datumPocetka = etree.Element("datum_početka")
                    datumPocetka.text = "2015-01-01"
                terapija.append(datumPocetka)
            terapije.append(terapija)
        oboljenje.append(terapije)
    anamneza.append(oboljenje)

    schemaDoc = etree.parse("karton.xsd")
    schema = etree.XMLSchema(schemaDoc)
    if schema.validate(xmlDoc):
        print("Dokument je validan.")
    else:
        print(schema.error_log)

    file = open("karton01.xml", "wb")
    xmlDoc.write(file, encoding="UTF-8", xml_declaration=True, pretty_print=True)
    file.close()

    # dopuna da bi i dodati element bio pretty_print-ovan
    # sacuvano stablo mora da se reparse-uje i ponovo sacuva
    # parser-u se mora naznaciti da obrise visak whitespace-ova
    parser = etree.XMLParser(remove_blank_text=True)
    xmlDoc = etree.parse("karton01.xml", parser)
    file = open("karton01.xml", "wb")
    xmlDoc.write(file, encoding="UTF-8", xml_declaration=True, pretty_print=True)
    file.close()

main()