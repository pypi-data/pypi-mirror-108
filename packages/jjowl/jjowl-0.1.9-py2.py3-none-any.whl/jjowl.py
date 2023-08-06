#!/usr/bin/python3
""" VERY EXPERIMENTAL :  module for opinied command line processing of OWL ontologies

# Synopsis

    owlcat  a.ttl b.owl c.ttl > all.ttl
      -f xml            - define output format
      -n
      -o file           

    owlclass a.ttl      show class taxonomy
      -r                - keep transitive redundances

    owlgrep pattern a.ttl
       -k                  just the IRI (default: term and adjacents)
       pattern :
         intanceRE
         classRE::instanceRE

    owllabel2term a.ttl > new.ttl    - rename IRIRef from rfds:label
       -s nameSpace                  - default http://it/

    owlexpandpp a.ttl   - expand and pretty print

    owlxdxf  a.ttl      - Build a XDXF dictionary (seealso goldendict)
       -o out.xdxf      - redirects output (default stdout)

As a module:

    import jjowl
    ... FIXME

# Description
"""

__version__ = "0.1.9"

from jjcli import *
from unidecode import unidecode
import json
import yaml
import owlrl
from   owlrl import convert_graph, RDFXML, TURTLE, JSON, AUTO, RDFA
import rdflib
from   rdflib.namespace import RDF, OWL, RDFS, SKOS, FOAF

def OFF_best_name_d(g : rdflib.Graph) -> dict :
   """ FIXME: IRIRef -> str based on RDFS.label, id, ??? """
   bestname={}
   for n in g.all_nodes():
       if islit(n): continue
       if name := g.preferredLabel(n) :
           bestname[s]=name[0].strip()
       else:
           txt = term.n3(g.namespace_manager)
           txt = sub(r'^:', '', txt)
           txt = sub(r'_', ' ', txt)
           bestname[s]=txt.strip()
   return bestname
#   for s,p,o in g.triples((None,RDFS.label,None)):
#   return


def get_invs(g: rdflib.Graph) -> dict :
   """Dictionary of inverse relations (based on inverseOf and SymetricProperty"""
   inv = {OWL.sameAs: OWL.sameAs}
   for s,p,o in g.triples((None,OWL.inverseOf,None)):
       inv[s]=o
       inv[o]=s
   for s,p,o in g.triples((None,RDF.type, OWL.SymmetricProperty)):
       inv[s]=s
   return inv

def reduce_graph(g,fixuri=None,fixlit=None)-> rdflib.Graph:
   def fix(item):
        if islit(item) and fixlit:
            return rdflib.term.Literal(fixlit(str(item)))
        if isinstance(item, rdflib.term.URIRef) and fixuri:
            return rdflib.term.URIRef(fixuri(str(item)))
        return item

   fixed= rdflib.Graph()
   fixed.bind('owl',OWL)
   fixed.bind('rdf',RDF)
   fixed.bind('rdfs',RDFS)
   fixed.bind('skos',SKOS)
   fixed.bind('foaf',FOAF)

   fixed+= [ (fix(s), fix(p), fix(o)) for s,p,o in g]
   return fixed

def concatload(files:list, opt: dict) -> rdflib.Graph :
   ns=opt.get("-s",'http://it/')
   g = rdflib.Graph(base=ns)
   g.bind("",rdflib.Namespace(ns))
   g.bind('owl',OWL)
   g.bind('rdf',RDF)
   g.bind('rdfs',RDFS)
   g.bind('skos',SKOS)
   g.bind('foaf',FOAF)
   for f in files:
      if ".n3" in f or ".ttl" in f or "-t" in opt:
         try:
             # g.parse(f,format='turtle')
             g.parse(f,format='n3')
         except Exception as e:
             warn("#### Error in ", f,e)
      else:
         try:
             g.parse(f) #,format='xml')
         except Exception as e:
             warn("#### Error in ", f,e)
   return g

def concat(files:list, opt: dict) -> rdflib.Graph :
   ns=opt.get("-s",'http://it/')
   g=concatload(files, opt)
   def fixu(t):
      if str(RDF) in t or str(OWL) in t or str(RDFS) in t :
          return t
      else:
          return  sub(r'(http|file).*[#/]',ns,t)

   g2=reduce_graph(g, fixuri=fixu)
   g2.bind("",ns)
   return g2

def termcmp(t):
   return  unidecode(sub(r'.*[#/]','',t).lower())

def islit(t):
   return isinstance(t,rdflib.term.Literal)

#== main entry points

def mcat():
   c=clfilter(opt="f:no:s:")
   g=owlproc(c.args,c.opt)
   g.serial()

def mlabel2term():
   c=clfilter(opt="f:kpctno:s:")
   g=owlproc(c.args,c.opt)
   g.rename_label2term()
   g.serial()

def mgrep():   ## using class
   c=clfilter(opt="kpcto:s:")
   pat=c.args.pop(0)
   g=owlproc(c.args,c.opt)
   if v:= match(r'(.+?)::(.+)',pat):
       g.grep2(v[1],v[2])
   else:
       g.grep(pat)

def mexpandpp():
   c=clfilter(opt="kpcto:s:")
   g=owlproc(c.args,c.opt)
   g.pprint()

def mxdxf():   ## using class
   c=clfilter(opt="no:s:")
   g=owlproc(c.args,c.opt)
   g.xdxf()

def mclass():
   c=clfilter(opt="no:rs:")
   g=owlproc(c.args,c.opt)
   g.pptopdown(OWL.Thing)

##=======

class owlproc:
   """ Class for process owl ontologies
      .opt
      .g
      .inv
      .instances : tipo -> indiv
      .subcl   = {}
      .supcl   = {}
      .supcltc = {}

   """
   def __init__(self,ontos,
                     opt={},
                     ):
      self.opt=opt
      if "-s" not in self.opt:    ## default name space
          self.ns='http://it/'
      else:
          self.ns=self.opt["-s"]

      self.g=concat(ontos,opt)
      if "-n" not in self.opt:
          self._infer()
      self.inv=get_invs(self.g)
      self._get_subclass()
      self._instances()

   def serial(self,fmt="turtle"):
      if "-f" in self.opt :
          fmt = self.opt["-f"]
      print(self.g.serialize(format=fmt).decode('utf-8'))

   def _pp(self,term) -> str:
       """ returns a Prety printed a URIRef or Literal """
       return term.n3(self.g.namespace_manager)

   def _instances(self):
      self.instances={}
      for s,p,o in self.g.triples((None,RDF.type, None)):
          self.instances[o]=self.instances.get(o,[]) + [s]

   def _infer(self):
      owlrl.DeductiveClosure(owlrl.OWLRL_Extension_Trimming ).expand(self.g)

   def xdxf(self):
      if "-o" in self.opt:
          f = open(self.opt["-o"],"w",encoding="utf-8")
      else:
          f = sys.stdout
      ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
         OWL.equivalentProperty }

      print(f"""<?xml version="1.0" encoding="UTF-8" ?>
<xdxf lang_from="POR" lang_to="DE" format="logical" revision="033">
    <meta_info>
        <title>Dicionário</title>
        <full_title>Dicionário</full_title>
        <file_ver>001</file_ver>
        <creation_date></creation_date>
    </meta_info>
<lexicon>""",file=f)

      for n in sorted(self.g.all_nodes(), key=termcmp):
          if islit(n): continue
          if n in [OWL.Thing] : continue
          self._term_inf_xdxf(n,f)  ## FIXME
      print("</lexicon>\n</xdxf>",file=f)
      if "-o" in self.opt:
          f.close()

   def grep(self,pat):
       for n in sorted(self.g.all_nodes(), key=termcmp):
           if islit(n): continue
           if n in [OWL.Thing] : continue
           npp = self._pp(n)
           if search( pat, npp, flags=re.I):
               if "-k" in self.opt:
                   print(npp)
               else:
                   self._pterm_inf(n)

   def grep2(self,patc,pati):
       for s,o in self.g.subject_objects(RDF.type):
           opp = self._pp(o)
           if search( patc, opp, flags=re.I):
               spp = self._pp(s)
               if search( pati, spp, flags=re.I):
                   if "-k" in self.opt:
                       print(f'{opp}::{spp}')
                   else:
                       self._pterm_inf(s)

   def _get_subclass(self):
      self.subcl   = {}
      self.supcl   = {}
      self.supcltc = {}
      for s,p,o in self.g.triples((None,RDF.type,None)):
          self.supcl[o]=set()
      for s,p,o in self.g.triples((None,RDFS.subClassOf,None)):
          self.subcl[s]=self.subcl.get(s,set())
          self.supcl[o]=self.supcl.get(o,set())

          self.subcl[o]=self.subcl.get(o,set()) | {s}  ### | subcl.get(s,set())
          self.supcl[s]=self.supcl.get(s,set()) | {o}
      self.subcl[OWL.Thing]=[x for x in self.supcl if not self.supcl[x]]

      for c,up in self.supcl.items():
          if c not in self.supcltc: self.supcltc[c] = up
          for y in up:
              if y not in self.supcltc:
                  self.supcltc[y] = set()
              self.supcltc[c].update(self.supcl[y])
      aux = self.supcltc.items()
      for c,up in aux :
          for y in up:
              self.supcltc[c].update(self.supcltc[y])

   def pptopdown(self,top,vis={},indent=0,max=1000):
       if max <= 0  : return
       if top in vis: return
       vis[top]=1
       print( f'{"  " * indent}{self._pp(top)}' )
       scls=self.subcl.get(top,[])
       if "-r" not in self.opt:
           scls=self._simplify_class(self.subcl.get(top,[]))
       for a in sorted(scls,key=termcmp):
           self.pptopdown(a,vis,indent+2,max-1)

   def _simplify_class(self, cls:list, strat="td") -> list:
       """ FIXME: remove redundant class from a class list"""
       aux = set(cls) - {OWL.Thing, OWL.NamedIndividual}
       for x in aux.copy():
           if strat == "td":
               if self.supcltc.get(x,set()) & aux:
                   aux.remove(x)
           else:    ## "bu"
               aux -= self.supcltc.get(x,set())
       return aux

   def _term_inf_xdxf(self,n,f):
      ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
         OWL.equivalentProperty }

      print("",file=f)
      print(f'<ar><k>{self._xpp(n)}</k><def>',file=f)
      cls = self._simplify_class(self.g.objects(subject=n,predicate=RDF.type),
                                 strat="bu")
      for c in cls:                                     ## class
          print( f"<kref>{self._xpp(c)}</kref>",
                 file=f)
      for p,o in sorted(self.g.predicate_objects(n)):   ## ↓ p o 
          if p in ignore_pred: continue
          if islit(o):
              print(f"   <def>{self._xpp(p)}: {self._xpp(o)}</def>",
                    file=f)
          else:
              print(f"   <def>{self._xpp(p)}: <kref>{self._xpp(o)}</kref></def>",
                    file=f)

      for s,p in sorted(self.g.subject_predicates(n)):   ## s p ↓  
          if p in ignore_pred  or p in self.inv: continue
          print(f"   <def><kref>{self._xpp(s)}</kref>  {self._xpp(p)} *</def>",
                file=f)
      if n in self.instances:
          for i in sorted(self.instances[n],key=termcmp):
              print(f" <def><kref>{self._xpp(i)}</kref></def>",
                    file=f)
      print(f'</def></ar>', file=f)


   def _xpp(self,term) -> str:
       """ returns a xdxf Prety printed URIRef """
       txt = self._pp(term)
       if islit(term):
           if '"""' in txt  or "'''" in txt:
               return "<deftext>"+ sub(r'[<>&]','=',txt).strip("""'" """) + "</deftext>"
           else:
               return "<c>"+sub(r'[<>&]','=',txt).strip("""'" """) + "</c>"
       else:
           txt = sub(r'^:', '', txt)
           txt = sub(r'_', ' ', txt)
           return sub(r'[<>&]','=',txt)

   def rename_label2term(self) -> rdflib.Graph :
       newname = {}

       for s,o in self.g.subject_objects(RDFS.label):
           base = sub(r'(.*[#/]).*',r'\1',str(s))
           newid = sub(r' ','_', str(o).strip())
           newname[str(s)] = base + newid

       for s,o in self.g.subject_objects(SKOS.prefLabel):
           base = sub(r'(.*[#/]).*',r'\1',str(s))
           newid = sub(r' ','_', str(o).strip())
           newname[str(s)] = base + newid

       def rename(t):
          if str(RDF) in t or str(OWL) in t or str(RDFS) in t or str(SKOS) in t:
              return t
          else:
              taux = newname.get(t,t)
              return sub(r'(http|file).*[#/]',self.ns,taux)
       g2=reduce_graph(self.g, fixuri=rename)
       g2.bind("",self.ns)
       self.g = g2

   def _pterm_inf(self,n):
       ignore_pred={ RDF.type, RDFS.subPropertyOf , OWL.topObjectProperty,
          OWL.equivalentProperty }
    
       print("====")
       print(self._pp(n))
       cls = self._simplify_class(self.g.objects(subject=n,predicate=RDF.type),
                                  strat="bu")
       for c in cls:
           print("   ", self._pp(c))
       for p,o in sorted(self.g.predicate_objects(n)):   ## ↓ p o 
           if p in ignore_pred: continue
           print( "       ", self._pp(p), self._pp(o))
       for s,p in sorted(self.g.subject_predicates(n)):   ## s p ↓ 
           if p in ignore_pred: continue
           if p in self.inv: continue
           print( "       ", self._pp(s), self._pp(p), "*")

   def pprint(self):
       for n in sorted(self.g.all_nodes(), key=termcmp):
           if islit(n): continue
           if n in [OWL.Thing] : continue
           self._pterm_inf(n)

## -----------------------------------------------------------------
## === utils importing "pseudo ontology elems"
##   parse tmd   
##   tmd → turtle 

def md2py(c):
    """ markdown with initial yaml metadata → docs = [ doc ] """
    docs=[]
    for txt in c.slurp():
        ex=match(r'\s*---(.*?)---(.*)',txt,flags=re.S)
        if not ex:
            warn("### Erro: no formato de", c.filename(),)
            continue
        meta,body=(ex[1] , ex[2])
        try:
            doc = yaml.safe_load(meta)
        except Exception as e:
            warn("### Erro: nos metadados de", c.filename(),e)
            continue
        doc["__file"]=c.filename()
        doc["__body-type"]="markdown"
        doc["body"]=body
        docs.append(doc)
    return docs 

def t2iri(s):
    """ term 2 IRIref """
    if isinstance(s ,(dict,list,tuple)): 
        warn("???",s)
        return f'"""FIXME: {s}"""'
    if s in {'type','a',} : return f'a'
    if s in {'inverseOf','Class','Thing','sameAs', 'ObjectProperty', 
        'DataProperty'} : return f'owl:{s}'
    if s in {'range','domain','subClassOf'} : return f'rdfs:{s}'
    if search(r'[!?()"\'\n+,.;/]',str(s)): return f'"""{s.strip()}"""'
    return ":"+sub(r'\s+|[:]',r'_',str(s))

def t2iri_or_lit(s):
    """ term 2 IRIref """
    if isinstance(s ,(dict,list,tuple)): 
        warn("???",s)
        return f'"""FIXME: {s}"""'
    if s in {'type','a',} : return f'a'
    if s in {'inverseOf','Class','Thing','sameAs', 'ObjectProperty', 
        'DataProperty'} : return f'owl:{s}'
    if s in {'range','domain','subClassOf'} : return f'rdfs:{s}'
    if search(r'[\n,.;/]',str(s)): return f'"""{s.strip()}"""'
    return ":"+sub(r'\s+|[:]',r'_',str(s))

def docs2ttl(d):
    """ docs → turtle triples """ 
    if isinstance(d,list):
        if len(d)==3 and not isinstance(d[0],(list,dict,tuple)) :
            return docs2ttl_d({d[0]: {d[1]: d[2]}})
        elif ( len(d)==2 and 
               not isinstance(d[0],(list,dict,tuple)) and 
               isinstance(d[1],dict) ) :
            return docs2ttl_d({d[0]: d[1]})
        else:
            return str.join("\n",[docs2ttl(x) for x in d])
    if isinstance(d,dict):
        return docs2ttl_d(d)
    if isinstance(d,tuple):
        if len(d)==3:
            return docs2ttl_d({d[0]: {d[1]: d[2]}})
        else:
            warn("????",d)

def docs2ttl_d(d:dict):
    """ dict doc → turtle triples """ 
    ## { "%id" : "João", "parente" : [ "D", "M"] }
    r=""
    rd= d.copy()
    if "id" in d:
        s = rd.pop("id")
        rd= {s:rd} 
    elif "ID" in d:
        s = rd.pop("ID")
        rd= {s:rd} 
    elif "@id" in d:
        s = rd.pop("@id")
        rd= {s:rd} 
    for s,dd in rd.items():
        if match(r'@?ont(ology|ologia)?$',s,flags=re.I):
            r += docs2ttl(dd)
            continue

        if not isinstance(dd,dict):
            warn("Error: expecting a dictionary, got a ",rd) 
            dd = {"__DEBUG__": dd}

        for p,o in dd.items():
            if p == "ont":
                r += docs2ttl(o)
            elif isinstance(o,(list,set)):
                for oo in o:
                    r += f'{t2iri(s)} {t2iri(p)} {t2iri(oo)} .\n'
            else: 
                r += f'{t2iri(s)} {t2iri(p)} {t2iri(o)} .\n'
    return r 

def mtmd2ttl():
    c=clfilter(opt="do:")     ## option values in c.opt dictionary
    ds = md2py(c)
    print(docs2ttl(ds))

