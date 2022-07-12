

# Composite Pattern

- describes a group of objects that is treated the same way as a single instance of the same type of the objects. The purpose of the Composite Method is to Compose objects into Tree type structures to represent the whole-partial hierarchies.

- <b>composite</b>: made up of various parts or elements.

- <b>Examples</b>: Filesystem: Files / Directories ... directories hold multiple files. Order / Multiple Orders ... Same interface, composites group leaf objects.


``` python

class LeafElement:

    def __init__(self, *args):
        self.position = args[0]

    def showDetails(self):
        print("\t", end ="")
        print(self.position)


class CompositeElement:

    def __init__(self, *args):
        self.position = args[0]
        self.children = []

    def add(self, child):
        self.children.append(child)

    def remove(self, child):
        self.children.remove(child)

    def showDetails(self):
        print(self.position)
        for child in self.children:
            print("\t", end ="")
            child.showDetails()


if __name__ == "__main__":

    topLevelMenu = CompositeElement("GeneralManager")

    subMenuItem1 = CompositeElement("Manager1")
    subMenuItem2 = CompositeElement("Manager2")

    subMenuItem1.add(LeafElement("Developer11"))
    subMenuItem1.add(LeafElement("Developer12"))
    subMenuItem2.add(LeafElement("Developer21"))
    subMenuItem2.add(LeafElement("Developer22"))

    topLevelMenu.add(subMenuItem1)
    topLevelMenu.add(subMenuItem2)

    topLevelMenu.showDetails()

```