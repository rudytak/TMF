# Osnova

1. Úvod
    1. Nomenklatura
    2. Motivace
    3. Určení základních myšlenek a relevantní parametrů

2. Kap 1: Spinnery
    1. Úvodní kvalitativní sledování
    2. Teoretické vzorce
        1. Magnetické dipóly 
            1. Aproximace na "větší" vzdálenosti
            2. Magnetický moment přes remanenci
            3. Síla $F$
            4. $B$ pole
            5. Moment síly
        2. Otáčivý pohyb
            Působení momentů síly na spinner jakožto tuhé těleso
    3. Měření základních parametrů spinnerů pro simulaci a vzorce
        1. Rozměry
        2. $J$
        3. $B_r$
    4. Vývoj simulace (RK4)
        1. Datová struktury
        2. RK
        3. $\omega$-stavy a $\varphi$-stavy
        4. komplexita
    5. Tření bez magnetů
        1. Úvaha hlavních třecích sil
        2. Analytické řešení
            1. _důkaz maximálního časového průběhu systému ???_
        3. Měření dat
        4. Potvrzení měření a určení $\alpha$ a $\gamma$ pro všechny spinnery
        5. Implementace do simulace
            1. webové rozhraní
    6. Potvrzování simulace
        1. 1 spinner, pouze tření
            1. vysvětlení aparatury s Vernier magnetometrem
            2. vysvětlení algoritmu pro přibližné $\omega$ z peaků
            3. porovnání se simulací
        2. 1 spinner, pouze tření v quasi-homogenním magnetickém poli
            1. porovnání se simulací
        3. slow motion video
            1. 1 spinner, oscilace v quasi-homogenním magnetickém poli (slow-mo C0000)
            2. 1 spinner, rotace v quasi-homogenním magnetickém poli; pomalé a rychlé otáčky (slow-mo C0002, C0004, C0007)
            3. porovnání se simulací
        4. 2 spinners, magnetic coupling of different orders
            1. určení "možných poměrů" vzheldem k rozměrům spinneru
            2. vysvětlen aparatury s hnaným osc. a Vernier magnetometrem
                1. _měření závislosti RPM vrtačky/motoru na napětí ???_
            3. vysvětlení algoritmu pro získání detailnějšího průběhu $\varphi$ v čase
                1.zmínit úskalí jako prostost apod.
            4. **! porovnání se simulací !**
        5. 2 spinners, laserové moduly, magnetic coupling
            1. vysvětlení laserového modulu pro kvalitnější snímání $\omega$
            2. vysvětlení úprav algoritmu
            2. **! porovnání se simulací !**
    7. Přenos momentu síly
        1. vysvětlení aparatury
            1. využití odporu vzduchu pro generovnání zátěže
            2. potvrzení kvadratické závislosti
        2. úskalí používání spinnerů pro přenos momentu síly
        3. možná řešení těchto problémů
        4. *porovnání se simulací ???*
    8. _Heatmap stavů ze simulace ???_

3. Kap 2: magnetické převodovky

# TODO
1. ~~RK implementace~~
2. Stabilní webové rozhraní
3. ~~určení remanance magnetů~~
4. rerun simulací (vše s _todo...) a výtažek plotů
    1. ~~spinner decay rate~~
    2. ~~decay rate in magnetic field~~
    3. ~~slowmotion spinner in magnetic field~~
    4. ~~magnetically coupled spinners vernier ??~~
    5. magentically coupled spinners laser
    6. ~~torque transfer~~
5. ~~predefinování $c_1$, aby bylo kladné~~
6. ~~$\alpha\beta\gamma$ damping~~
7. ~~Add RK optimisation for spinners that should be ignored~~
8. ~~Add sim selectable output parameters => retrofit everything ofc~~
9. **PŘEVODOVKY!!!**
10. **Doměření přenosu momentu síly!!!**
