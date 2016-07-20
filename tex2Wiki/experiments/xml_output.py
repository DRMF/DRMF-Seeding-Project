import xml.etree.ElementTree as ET


def main():
    ET.register_namespace('', 'http://www.mediawiki.org/xml/export-0.10/')
    root = ET.Element('{http://www.mediawiki.org/xml/export-0.10/}mediawiki')
    page = ET.SubElement(root, 'page')
    title = ET.SubElement(page, 'title')
    title.text = 'the Title & stuff'
    ET.dump(root)
    tree = ET.ElementTree(root)
    tree.write(
        "page.xhtml",
        xml_declaration=True,
        encoding='utf-8',
        method='xml')


if __name__ == "__main__":
    main()
