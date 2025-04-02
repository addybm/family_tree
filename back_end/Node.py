from Person import Person

class Node:
    def __init__(self, person: Person, in_focus : bool, partner_left : bool, partner_right : bool, parents : bool, children_left : bool, children_right : bool):
        self.person = Person("","","","")
        self.in_focus = in_focus
        self.partner_left = partner_left
        self.partner_right = partner_right
        self.parents = parents
        self.children_left = children_left
        self.children_right = children_right


