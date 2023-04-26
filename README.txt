README
Rusu Ioana 336CC


1. Organizare

Am folosit două dicţionare, unul pentru produceri şi unul pentru carturi;

	Dicţionarul pentru producători are drept key-uri id-urile producerilor şi fiecare key are ca valoare o lista de produse asociate producerului cu id-ul = key, formată din id-urile respectivelor produse. 

	Dicţionarul pentru carts are drept key-uri id-urile consumerilor şi fiecare key are ca valoare o lista de perechi de tip (product, producer_id).

 Dictionar carts -> { 
		 id1:	 [  [product1, producer_id], [product2, producer_id]  ],
	                 id2:	 [  [product3, producer_id], [product4, producer_id]  ]
		}

 Dicitionar producers => { 
		          id1:	      [prod1, prod2, prod3], 
		          id2:	      [prod4, prod5, prod6] 
		        }

	În cazul dicţionarului cart-urilor, valorile sunt liste de elemente de tip pereche, pentru ca aveam nevoie ca pentru fiecare produs să pus în coş să-i reţin şi id-ul producătorul de la care aparţine. Asta pentru că la apelarea funcţiei remove_from_cart() trebuia să readaug produsul în lista producătorului de care aparţine.


2. Implementare

	În implementare am folosit elemente de sincronizare de tip Lock ca să delimitez zone critice precum asocierea id-ului pentru produceri si carts, publicarea produselor şi adăugarea unui produs într-un coş.

	Pe parcursul temei am întâmpinat probleme precum:
	-	Enunţ superficial - prezintă prea în ansamblu ideea a ceea ce aveam de facut. Citind mi s-a parut destul de clar, dar cand m-am apucat efectiv de lucru mi-am dat seama ca nu ştiam cum sa pun cerinţa în practică pentru că explică doar conceptual ce avem de făcut. Aveam nevoie de indicaţii mai precise având în vedere că trebuia să respect şi structura temei.
	-	nu foloseam elemente de sincronizare atunci când cream un nou producer/cart
	-	în metoda run() din consumer.py cream un nou cart la început, în afara structurilor repetitive

	Metoda run() din producers.py:
	-	generez un id pentru producator
	-	parcurg lista de produse pe care trebuie să le public
	-	se incearcă publicarea produselor producerului curent in limita nr de produse pe care le are, apelând
funcţia publish() din marketplace.py

	Metoda run() din consumer.py:
	-	generez un id pentru cart
	-	parcurg câmpurile din fişierul json (type, product, quantity)
	-	extrag tipul de comandă (add sau remove)
	-	în funcţie de comandă primită apelez functiile add_to_cart(), respectiv remove_from_cart din marketplace.py şi adaug produsele în coş în funcţie de cantitatea precizată
	-	apelez functia print_cart() care primeste ca parametru coşul curent şi printeaza produsele existente în coş la finalul apelurilor de funcţii


3. Resurse
-	tutoriale python
-	site-uri pe care se explica threading si synchronization in python
-	laboratoare 1, 2, 3









