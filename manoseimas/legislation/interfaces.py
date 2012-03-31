from sboard.interfaces import INode

class ILegalAct(INode): pass

class ILaw(ILegalAct): pass
class ILawChange(ILegalAct): pass
class ILawProject(ILegalAct): pass
