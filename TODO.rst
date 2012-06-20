Užduotys
========

* Optimizuoti seimo nuomonės puslapį, pavyzdys:

    http://test.manoseimas.lt/visagino-atomine-elektrine/seimo-pozicija/

* Greičiausiai reikės refaktorinti testo kategorijų ir toms
  kategorijoms priskirtų sprendimų dalį.

  Dabar viskas tiesiog saugoma į patį testo nodą, todėl negalima
  kategorijų su kuo nors susieti ir pan.

  Kategorijos buvo saugomos į testo nodą, kad būtų išspręsta
  besidubliuojančių kategorijų pavadinimų problema, tačiau šią
  problemą, ko gero reikės spręsti traversalo būdu.

* Change title handling: title must come from view as context
  variable, this way title can be used in several places, i. e. in
  page title and in page header.

* Kai keičiama Issue objekto antraštę, prasukti ciklą, per visus
  susijusius SolutionIssue objektus ir atnaujinti jų slugus, tą patį
  padaryti ir Solution objekto antraštės keitimo atveju, kadangi
  SolutionIssue objekto slugas padaromas iš Solution ir Issue objekto
  slugų.

* Kaip nors pertvarkyti scrapy.pipelines, kad duomenų bazės
  nustatymai būtų paprastai prieinami ir iš Django.

* Fix bin/couch replicate command, all databases must be created
  automatically and some how, RDBMS also should be replicated.

  Now, if you get only couch data, then unique ID table, that generates
  new keys for couchdb documents, starts from 0, while replicated
  couchdb has much greater keys, what finally leads to Duplicate
  errors in couchdb, when tying to create new records.


Neišspręstos problemos
======================

Sinchronizacijos pertvarkymas
-----------------------------

1. Pasileidžia duomenų indeksavimo skirptas ir suranda pradinius
   adresus indeksavimui.

2. Voras gauna pradinį adresą ir suindeksuoja viską, kas jame yra.

   Suindeksuoti duomenys įrašomi į specialią couchdb duomenų bazę,
   kartu su duomenimis išsaugomas ir visas indeksuojamo puslapio HTML
   kodas, kad esant reikalui būtų galima iš naujo perindeksuoti
   nesikreipiant į svetainę.

   Visų tipų duomenys indeksuojami į vieną ir tą pačią duomenų bazę.

3. Atskirai pasileidžia suindeksuotų duomenų konvertavimo į nodus
   skriptai, jie pasileidžia tam tikra tvarka, kad numatyta eilės
   tvarka būtų sukurti visi priklausomi nodeai ir sujingti ryšiais.

   Pavyzdžiui pirmiausia turi pasileisti seimo narių konvertavimas,
   tada teisės aktų, nes teisės aktai turi nuorodų į seimo narių
   profilius ir galiausiai barsavimai, kadangi balsavimai turi
   nuorodų ir į seimo narių ir į teisės aktų profilius.

   Konvertavimo skriptai visada turėtų konvertuoti tik pasikeitusius
   priminius duomenis, nuo ten, kur paskutinį kartą baigė.

Node'ų trynimas
---------------

Reikia užtikrinti, kad trinant vieną node'ą, būtų ištrinti ir visi
ryšiai esantys kituose node'uose ir rodantys į tą, kuris bus trinamas.

Galimas sprendimas
''''''''''''''''''
Sukurti specialius laukus, kurie nurodo ryšį su kitu node'u ir
vadovaujantis tų laukų informacija, ištrinti viską, kas susiję.


Node'ų one-to-one ryšys
-----------------------

Dažnai iškyla poreikis išplėsti vieną node'ą, pridedant į jį daugiau
informacijos, kuri nėra susijusi su tuo node'u tiesiogiai, bet tos
informacijos reikia kitiems node'ams.

Galimas sprendimas
''''''''''''''''''
Realiai viename node'e galima saugoti ir daug informacijos, o
sąrašuose grąžinti tik reikiamus laukus, per view'us.

Medžio elementų su sutempančiais pavadinimais problema
------------------------------------------------------

Tarkime yra toks medis::

    `- root
       |- A       (ID:1)
       |  `- C    (ID:2)
       `- B       (ID:3)
          `- C    (ID:4)

Pagal šį medį yra tokie du keliai::

    /A/C
    /B/C

Nodeai adrese atvaizduoja tik paskutinį elementa, tai reiškia,
gaunami du elementai su tuo pačiu pavadinimu ``C``.

Galimas sprendimas 1
''''''''''''''''''''
Kiekvienas node'as pasirinktinai turi turėti galimybę saugoti slug'ą su
``/`` simboliu, kuris nurodo pilną kelią.

Pavyzdžiui, node'as ID:2 turi slug'ą ``A/C``, todėl, galutinis
suformuotas adresas yra ``A/C``. Kreipiantis tokiu adresu, pirmiausia
imamas ``A`` ir gaunamas ID:1 node'as, kuris yra ``Category``
node'as, kuris tikisi, kad adrese, antras kelio elementas, bus jo

Galimas sprendimas 2
''''''''''''''''''''
Galima realizuoti kažką panašaus į traversalą. Jis galėtų veikti taip:

Gavus užklausą ``A/C`` ji būtų išanalizuota, kaip ir visos kitos, jei
nebūtų rastas viewas, kuris šią užklausą gali apdoroti, tada bandoma
ieškoti ``C`` nodo, tarp visų tiesioginių ``A`` vaikų.

Kad ``C`` nodas nesimaišytų globalioje nodų vardų erdvėje, jis turi
turėti atributą ``traverse``, kuris nurodo, kad šis nodas, gali būti
pasiekiamas, tik traversalo būdu.


Lanksti navigacijos sistema
---------------------------

Reikia sugalvoti būdą, kaip įvairūs view'ai gali bendrai konstruoti
navigacijos medį.

Pavyzdžiui, jei rodomas view'as A, tada visi kiti view'ai, turi
turėti galimybę, įdėti savo navigacijos elementus į view'o A
navigacijos medį.

Galimas sprendimas
''''''''''''''''''
Realizuoti tai per Django signalus.


Frakcijos
---------

Kaip geriau skaičiuoti frakcijos poziciją, pagal balsavimus ar pagal
seimo narius?

Tarkim yra tokia situacija, svarstomas klausimas, dėl jo buvo
balsuota 3 kartus (2=už, -1=susilaikė, -2=prieš). Seimo narys S1,
dažnai keitė frakcijas ir kiekvieno balsavimo metu, priklausė vis
kitai frakcijai. Šiuo metu seimo narys S1 priklauso frakcijai F3:

 Balsavimas   Balsas   Seimo narys   Frakcija
------------ -------- ------------- ----------
 B1                2   S1            F1
------------ -------- ------------- ----------
 B2               -1   S1            F2
------------ -------- ------------- ----------
 B3               -2   S1            F3
 B3                2   S2            F3
 B3               -1   S3            F3
------------ -------- ------------- ----------

Seimo nario S1 pozicija:

    P(S1) = AVG(B1 + B2 + B3)
    P(S1) = (2 + -1 + -2) / 3 = -0.3

Frakcijos F3 pozicija, pagal seimo narį:

    P(F3) = AVG(P(S1) + P(S2) + P(S3))
    P(F3) = (-0.3 + 2 + -1) / 3 = 0.2

Frakcijos F3 pozicija, pagal balsavimus:

    P(F3) = AVG(S1_B3 + S2_B3 + S3_B3)
    P(F3) = (-2 + 2 + -1) / 3 = -0.3

Skaičiuojant, pagal seimo narį, gaunam 0.2, o pagal balsavimus, -0.3.

Ar svarbiau pateikti frakcijos istorinę poziciją, ar geriau pateikti
dabar frakcijos poziciją, pagal šiuo metu, joje esančių seimo narių
sudėtį ir jų pozicijas?

Skaičiavimo būdai
'''''''''''''''''

Užduočių eilės
--------------

Kai kurie veiksmai vyksta labai ilgai, pavyzdžiui tokie, kaip balsavimo
priskyrimas. Balsavimo priskyrimo metu reikia perskaičiuoti visų seimo
narių, frakcijų ir grupių pozicijas tam sprendimui, kūrimą buvo
priskirtas balsavimas. Iš esmės labai panašiai yra ir su pozicijos
išsakymu.

Kad naudotojui nereikėtų ilgai laukti, kol tai atliekama, tokios
užduotys turi būti dedamos į eilę ir atliekamos vėliau.

Sprendimas 1
''''''''''''

Django Celery:

    http://celeryproject.org/

Demonai
-------

manoseimas.lt projektas naudoja kelis papildomus demonus, pavyzdžiui
tokius, kaip CouchDB duomenų  bazė, anksčiau naudojo ir gal bū vėl
naudos paieškos variklį, taip pat, gal būt bus naudojamas užduočių eilės
demonas.

Visus šiuos demonus reikia paleisti ir kontroliuoti ar jie teisingai
veikia. Tam reikalingas įrankis skirtas demonų valdymui.


Sprendimas 1
''''''''''''

Demonų valdymui galima naudoti Supervisor:

    http://supervisord.org/


CouchDB versija
---------------

Šiuo metu Ubuntu pateikia tik seną 1.0.x CouchDB versiją, kuri turi daug
klaidų, o svarbiausia neveikia replikavimas.

Todėl reikia susikompiliuoti CouchDB rankomis. Reikėtų padaryti
automatinį CouchDB kompiliavimą ir ko gero suintegruoti tai su
Supervisor demonų valdymo įrankiu.
