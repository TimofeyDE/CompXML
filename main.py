import xml.etree.ElementTree as ET
import sys
import os


def __main__():
    curr_dir = os.getcwd()

    if not is_input_valid(sys.argv):
        print("Files were not specified or files have an incorrect extensions!")
        print()
        print(help_function())
        exit(1)

    file_1 = os.path.join(curr_dir, sys.argv[1])
    file_2 = os.path.join(curr_dir, sys.argv[2])

    if not os.path.exists(file_1) or not os.path.exists(file_2):
        print("One of the given files does not exist!")
        print()
        print(help_function())
        exit(1)

    differences = compare_xml(file_1, file_2)

    if differences:
        print_difference(differences, file_1, file_2)
    else:
        print("Both files are either identical or there are not identical tags!")


def print_difference(similar_tags, f1, f2):
    tree1 = ET.parse(f1)
    tree2 = ET.parse(f2)

    for tag_name in similar_tags:
        tags1 = tree1.findall('.//{}'.format(tag_name))  # Finds all occurrences in tree1
        tags2 = tree2.findall('.//{}'.format(tag_name))  # Finds all occurrences in tree2

        if tree1.getroot().tag == tag_name and tree2.getroot().tag == tag_name:
            r1 = tree1.getroot()
            r2 = tree2.getroot()
            print("Root:", r1.tag)
            print("file 1:", r1.attrib, r1.text, (r1.tail if r1.tail is not None else ""))
            print("file 2:", r2.attrib, r2.text, (r2.tail if r2.tail is not None else ""))

        for tag1, tag2 in zip(tags1, tags2):
            if tag1 is not None and tag2 is not None:
                print("Tag:", tag1.tag)
                print("file 1:", tag1.attrib, tag1.text, (tag1.tail if tag1.tail is not None else ""))
                print("file 2:", tag2.attrib, tag2.text, (tag2.tail if tag2.tail is not None else ""))


def compare_elements(element1, element2):
    """Recursively compare two XML elements."""
    similar_tags = []

    if element1.tag == element2.tag:
        if (element1.attrib != element2.attrib or element1.text != element2.text):
            similar_tags.append(element1.tag)

        for child1, child2 in zip(element1, element2):
            similar_tags.extend(compare_elements(child1, child2))

    return similar_tags


def compare_xml(f1, f2):
    tree1 = ET.parse(f1)
    tree2 = ET.parse(f2)

    root1 = tree1.getroot()
    root2 = tree2.getroot()

    return compare_elements(root1, root2)


def traverse(root, depth = 0):
    print(root.tag, root.attrib, root.text)

    for child in root:
        traverse(child, depth + 2)


def help_function() -> str:
    return "This program compares two XML files between each other.\n\
It is necessary for you to run this program the following way:\n\
    python3 program.py file_1.xml file_2.xml\n\
You should make sure that both files are on the same directory where the executable file of program is located."


def is_input_valid(input: list[str]) -> bool:

    if len(sys.argv) == 0 or len(sys.argv) < 3:
        return False

    if not sys.argv[1].endswith(".xml") or not sys.argv[2].endswith(".xml"):
        return False
    
    return True


def is_path_valid(path: str) -> bool:

    return os.path.exists(path)


if __name__ == '__main__':
    __main__()
