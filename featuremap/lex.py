from lark import Lark

parser = Lark("""
start: context
     | link entity
     | context link entity
     | noswitch context link entity

context: CONTEXT -> context
link: LINK -> link
entity: ENTITY -> entity
noswitch: NOSWITCH -> noswitch

CONTEXT: PREFIX ":" TYPE
LINK: " "* "->" " "* 
    | " "+ SYMBOL " "+
ENTITY: PREFIX ":" TYPE
NOSWITCH: " "* "!" " "*

PREFIX: SYMBOL
TYPE: SYMBOL

LOWER: ("a".."z")+
UPPER: ("A".."Z")+
NUMBER: ("0".."9")+
SYMBOL: (LOWER | UPPER | NUMBER)+
""")