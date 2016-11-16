from pryo import *

class KB1(KB):

    def tell(self, kw):
        """

        kb.tell(father = ('pap', 'a'))
        kb.tell(['father', ('pap', 'a')])
        
        kb.tell({
            ('sibling', ('?x', '?y')):
            [('father', '?z', )]
        })
        
        """
        


kb = KB()

