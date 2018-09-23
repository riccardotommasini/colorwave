# percorso per RW

## durante la lezione

### present the streams 
le sorgenti mettono 1 elemento e poi aspettano un tempo variabile tra 1 e 9 secondi

**red stream (annotated) **

	r1 a Red
	r2 a Red
	...


**green stream (to-be-annotated) **

	g1 a Green
	g2 a Green
	...

**blue stream (to-be-annottated)**
	b1 a Blue
	b2 a Blue
	...

### inspect a stream

### let's annotate the green stream

### EX: your turn to inspect the green stream

### analyse a stream

	SELECT count(?r)
	FROM NAMED WINDOW :rw ON s:blue [RANGE PT15S STEP PT5S]
	WHERE {
		WINDOW :rw { ?r a Red }
	}

discussion on the different types of windows and exercises

### analyse two streams simultaneously

	SELECT count(?r) AS ?cntr, count(?g) AS ?cntg, (?cntr>?cntg) as ?moreRedsThanGreens  
	FROM NAMED WINDOW :rw ON s:red [RANGE PT15S STEP PT5S]
	FROM NAMED WINDOW :gw ON s:green [RANGE PT15S STEP PT5S]
	WHERE {
		WINDOW :rw { ?r a Red }
		WINDOW :gw { ?g a Green }	
	}

### EX: annotate the blue stream and add it to the analysis

### construct a new stream

	CONSTRUCT { UUID() a Yellow; from ?r, ?g .}
	FROM NAMED WINDOW :rw ON s:red [RANGE PT15S STEP PT5S]
	FROM NAMED WINDOW :gw ON s:green [RANGE PT15S STEP PT5S]
	WHERE {
		WINDOW :rw { ?r a Red }
		WINDOW :gw { ?g a Green }	
	}

### EX: construct the Magenta (Red + Blue) stream

### let's add some reasoning

we load an ontology that contains

Blue rdfs:subClassOf ColdColor, PrimaryColor, Color .

Green rdfs:subClassOf ColdColor, PrimaryColor, Color .

Red rdfs:subClassOf WarmColor, PrimaryColor, Color .

Yellow rdfs:subClassOf WarmColor .

from a owl:ObectProperty .

from rdfs:domain DerivedColor .

from rdfs:range Color .

we run the query

	SELECT count(?w) AS ?cntWarm, count(?c) AS ?cntCold, (?cntWarm>?cntCold) as ?moreWarmThanCold  
	FROM NAMED WINDOW :rw ON s:red [RANGE PT15S STEP PT5S]
	FROM NAMED WINDOW :yw ON s:yellow [RANGE PT15S STEP PT5S]
	WHERE {
		WINDOW :rw { ?w a Warm }
		WINDOW :yw { ?c a Cold }	
	}

### EX: primary vs. derivati

domain di from

	SELECT count(?p) AS ?cntPrimary, count(?d) AS ?cntDerived, (?cntPrimary>? cntDerived) as ?morePrimaryThanDerived  
	FROM NAMED WINDOW :rw ON s:red [RANGE PT15S STEP PT5S]
	FROM NAMED WINDOW :gw ON s:green [RANGE PT15S STEP PT5S]
	FROM NAMED WINDOW :bw ON s:blue [RANGE PT15S STEP PT5S]
	FROM NAMED WINDOW :yw ON s:yellow [RANGE PT15S STEP PT5S]
	WHERE {
		WINDOW ?x { ?p a Primary }
		WINDOW ?y { ?d a Derived }	
	}



