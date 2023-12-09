# Osnova

1. Úvod
    1. Nomenklatura
    2. Motivace
    3. Určení základních myšlenek a relevantních parametrů

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
            1. Působení momentů síly na spinner jakožto tuhé těleso
    3. Měření základních parametrů spinnerů pro simulaci a vzorce
        1. Rozměry
        2. $I$
        3. $B_r$
    4. Vývoj simulace (RK4)
        1. Datové struktury
        2. RK
        3. $\omega$-stavy a $\varphi$-stavy
        4. komplexita
        5. _Webové rozhraní ??_
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
    1. simulace přes FEMM
    2. 3D model
    3. měření max torque
    4. Možné využití v mikrostrukturách

# TODO
1. ~~RK implementace~~
2. _Stabilní webové rozhraní ???_
3. ~~určení remanance magnetů~~
4. ~~rerun simulací (vše s _todo...) a výtažek plotů~~
    1. ~~spinner decay rate~~
    2. ~~decay rate in magnetic field~~
    3. ~~slowmotion spinner in magnetic field~~
    4. ~~magnetically coupled spinners vernier ??~~
    5. ~~magentically coupled spinners laser~~
    6. ~~torque transfer~~
5. ~~predefinování $c_1$, aby bylo kladné~~
6. ~~$\alpha\beta\gamma$ damping~~
7. ~~Add RK optimisation for spinners that should be ignored~~
8. ~~Add sim selectable output parameters => retrofit everything ofc~~
9. **PŘEVODOVKY!!!**
9. *Heatmap stavů ???*
9. *Magnet grade comparison ???*
10. ~~Doměření přenosu momentu síly!!!~~

<!-- ---------------------------------------------------------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------------------------------------------------------- -->

# SOLUTION

## Spinner properties

$n$ ... total number of magnets \
$r$ ... radius of spinner \
$S$ ... centerpoint of the spinner (also position of axis of rotation)

$\varphi$ ... angle of rotation \
$\omega$ ... angular velocity \
$\alpha$ ... angular acceleration \
$I$ ... moment of inertia of the spinner


The $i$-th magnet is positioned at $P(i)$:

$$
P(i) = S + \biggr(r\cos{\bigg(\varphi + \frac{2\pi i}{n}\bigg)},
r\sin{\bigg(\varphi+\frac{2\pi i}{n}}\bigg), 0 \biggr)
$$

The $i$-th magnetic moment is $m(i)$:

$$
radial: m(i) =\hat{(P(i) - S)}|m_0| \\
vertical: m(i) = (0, 0, |m_0|) \\
tangeng: m(i) = \hat{((0, 0, 1) \times (P(i) - S))}|m_0|
$$

## Omega decay:
<!-- 
https://www.wolframalpha.com/input?i2d=true&i=y%27%5C%2840%29t%5C%2841%29+%3D+-a-c*y%5C%2840%29t%5C%2841%29**2
-->
$$
\omega'(t) = - \alpha - \gamma \omega(t)^2 \\
$$
$$
\omega(t) = -\sqrt{\frac{\alpha}{\gamma}} \tan{(\sqrt{\alpha\gamma}(t-c_1))}
$$

#### Maximum runtime

$$
c_1(\omega_0) = \frac{1}{\sqrt{\alpha\gamma}} \arctan{ \bigg( \sqrt{\frac{\gamma}{\alpha}} \omega_0 \bigg)} \\

c_1(E) = \frac{1}{\sqrt{\alpha\gamma}} \arctan{ \bigg( \sqrt{\frac{2 \gamma E}{\alpha I}} \bigg)} \\
$$

#### Maximum runtime of a system
The maximum runtime of a system of $n$ spinners with starting energies $E_1, E_2 ... E_n$ is: 

$$c_1(E_1+E_2+...+E_n)$$

Proof:
$$
H_{c_1} \in \mathbb{R}^+ \\
c_1 \text{ is a decresing function and represents the runtime $t_{max} = c_1$} \\
E_1, E_2 \in \mathbb{R}^+ \\
\text{WLOG: } E_1>E_2 \\
$$

<!--
$$
E_1 = \frac{1}{2}I\omega_1^2 \\
E_2 = \frac{1}{2}I\omega_2^2 \\
E_1 + E_2 = \frac{1}{2}I\omega_1^2 + \frac{1}{2}I\omega_2^2 = \frac{1}{2}I(\omega_1^2 + \omega_2^2) \\
$$
-->

$$
c_1(E_1+E_2) \stackrel{?}{>} \min(c_1(E_1), c_1(E_2)) \\
$$

$$
c_1(E_1+E_2) > c_1(E_1) \\
\frac{1}{\sqrt{\alpha\gamma}} \arctan{ \bigg( \sqrt{\frac{2 \gamma (E_1+E_2)}{\alpha I}} \bigg)} > \frac{1}{\sqrt{\alpha\gamma}} \arctan{ \bigg( \sqrt{\frac{2 \gamma E_1}{\alpha I}} \bigg)} \\
\arctan{ \bigg( \sqrt{\frac{2 \gamma (E_1+E_2)}{\alpha I}} \bigg)} > \arctan{ \bigg( \sqrt{\frac{2 \gamma E_1}{\alpha I}} \bigg)} \\
\sqrt{\frac{2 \gamma (E_1+E_2)}{\alpha I}} > \sqrt{\frac{2 \gamma E_1}{\alpha I}}\\
\sqrt{\frac{2 \gamma }{\alpha I}} \sqrt{E_1+E_2} > \sqrt{\frac{2 \gamma}{\alpha I}} \sqrt{E_1}\\
\sqrt{E_1+E_2} > \sqrt{E_1}\\
E_1+E_2 > E_1\\
E_2 > 0\\
\text{QED}
$$

<!--
$$
\omega(t) = \omega_0 e^{-\lambda t} \\
\omega(t+dt) = \omega_0 e^{-\lambda(t+dt)} = \omega_0 e^{-\lambda t} e^{-\lambda dt} = \omega(t)e^{-\lambda dt}
$$
-->

### Better? omega decay:

<!-- 
https://www.wolframalpha.com/input?i2d=true&i=y%27%5C%2840%29t%5C%2841%29+%3D+-a-b*y%5C%2840%29t%5C%2841%29-c*y%5C%2840%29t%5C%2841%29**2 
-->
$$
\omega'(t) = - \alpha -\beta \omega(t) - \gamma \omega(t)^2
$$
$$
\omega(t) = -\frac{\sqrt{4\alpha\gamma - \beta^2} \tan{(\frac{1}{2}\sqrt{4\alpha\gamma - \beta^2}(t-c_1)})-\beta}{2\gamma}
$$

## Interactions

### Magnetic dipole interactions

$$
F_m (r,m_1,m_2) = \frac{3\mu_0}{4\pi ||r||^5} 
\bigg[
    (m_1\cdot r) m_2 +
    (m_2\cdot r) m_1 +
    (m_1\cdot m_2) r -
    \frac{5(m_1\cdot r)(m_2\cdot r)}{||r||^2} r
\bigg] \\
$$

$$
B (r, m) = \frac{\mu_0}{4\pi}\frac{3 \hat{r}(\hat{r}\cdot m) - m}{|r|^3} \\
\tau = m_2 \times B(r, m_1)
$$

### Change of angular velocity

$$
\frac{dL}{dt} = I\frac{d\omega}{dt} = \tau_F + \tau_{mag} \\
\tau_F = \sum_{j=0}^{n} F_m(P_{external}- P(j), m(j), m_{external}) \times (P(i) - S)\\
\tau_{mag} = \sum_{j=0}^{n} m(j) \times B(P(j)-P_{external},m_{external})\\
$$

### Magnetic dipole model

$V [m^3]$ ... volume of the magent \
$B_r [T]$ ... remanence / remanent magnetization

$$
m = \frac{1}{\mu_0}B_rV
$$

## Simulation

### Complexity

$T$ ... run time \
$\tau$ ... time interval \
$N$ ... amount of magnets per spinner \
$M$ ... amount of spinners \
$K$ ... RK matrix degree \
$U$ ... the amount of RK integrations we do in each step ($U=2$ in our case, because: $\tau \implies \omega \implies \varphi$)

$\mathcal{O} \bigg( \bigg( \dfrac{S}{\tau} \bigg) \cdot (N M)^2 \cdot K^U \bigg)$

# Transmissions

## 3D model