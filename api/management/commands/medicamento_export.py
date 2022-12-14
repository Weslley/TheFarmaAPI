class ApresentacaoExport(object):
    _id = None
    familia = None
    principioAtivo_id = None
    classe = None
    subClasse = None
    laboratorio_id = None
    codbarras = None
    codbarras2 = None
    codbarras3 = None
    tipoPreco = None
    lista = None
    vazio = None
    generico = None
    descricao = None
    apresentacao = None
    dataVigencia = None
    dataDesconhecida = None
    pmf19 = None
    pmf18 = None
    pmf17 = None
    pmf12 = None
    pmc19 = None
    pmc18 = None
    pmc17 = None
    pmc12 = None
    registroMS = None
    portaria = None

    def __init__(self, line, laboratorios, principios):
        self._id = int(line[2:8])
        self.familia = int(line[8:12])
        self.principioAtivo_id = int(line[12:17])
        self.classe = int(line[17:21])
        self.subClasse = int(line[21:25])
        self.laboratorio_id = int(line[25:28])
        self.codbarras = line[28:41].trim()
        self.codbarras2 = line[41:54].trim()
        self.codbarras3 = line[54:67].trim()
        self.tipoPreco = line[67:68].trim()
        self.lista = line[68:69].trim()
        self.vazio = line[69:70].trim()
        self.generico = False if line[70:71] == 'N' else True
        self.descricao = line[71:106].trim()
        self.apresentacao = line[106:151].trim().upper()
        self.dataVigencia = line[151:159].trim()
        self.dataDesconhecida = line[159:167].trim()
        self.pmf19 = line[167:175]
        self.pmf18 = line[175:183]
        self.pmf17 = line[183:191]
        self.pmf12 = line[191:199]
        self.pmc19 = line[199:207]
        self.pmc18 = line[207:215]
        self.pmc17 = line[215:223]
        self.pmc12 = line[223:231]
        self.registroMS = line[231:246].trim()
        self.portaria = line[246:256].trim()
