# Výpočet účinnosti pomocí pístu a jakosti oscilátoru

Minimální výkon oscilátoru odpovídá energii potřebné na překonání tlumení oscilátoru samotného. Jakost oscilátoru _(Q faktor)_ určíme pomocí [definice skrze uloženou energii](https://en.wikipedia.org/wiki/Q_factor#Stored_energy_definition):

$$
Q \stackrel{\text{def}}{=}
2\pi \cdot \frac{\text{energy stored}}{\text{energy dissipated per cycle}}
= 2\pi \cdot \frac{E_{max}}{E_{max} - E_1}
$$

Energii vloženou do systému před začátkem oscilací označíme $E_{max}$ nebo $E_0$. Energii po jedné periodě označíme $E_1$.

Energii pístu můžeme jednoduše vypočítat pomocí kinetické energie:

$$
E_0 = \frac{1}{2}mv^2 = \frac{1}{2}m \cdot (\omega \cdot y_0)^2
$$

Zde je $y_0$ amplituda na začátku oscilace a $\omega$ je úhlová rychlost oscilátoru. Analogicky můžeme vypočítat i $E_1$.

Z videa jsme schopni vyčíst relativní výchylky a periodu oscilací. Pro vyčtení ze 40x zpomaleného videa (25 fps) využijeme:

$$
1px = \frac{( 0.0206 \pm 1 \cdot 10^{-5} ) \ m}{( 976.0 \pm 1.0 ) - ( 792.0 \pm 1.0 )} = ( 0.000112 \pm 1.27 \cdot 10^{-6} ) \ m            \\
f = \frac{1}{25 * 40} s = 0.001 \ s                     \\
m = ( 0.0265 \pm 1 \cdot 10^{-5} ) \ kg                                      \\
$$

$$
y_0 = (( 658.0 \pm 1.0 ) - ( 621.0 \pm 1.0 ))px = ( 0.00415 \pm 0.000271 ) \ m                              \\
y_1 = (( 658.0 \pm 1.0 ) - ( 633.0 \pm 1.0 ))px = ( 0.0028 \pm 0.000256 ) \ m                              \\
T = (( 52.0 \pm 1.0 ) - ( 15.0 \pm 1.0 ))f = ( 0.037 \pm 0.002 ) \ s                        \\
\omega = \frac{2\pi}{T}= ( 169.816 \pm 9.179 ) \ \frac{rad}{s}                       \\
$$

Dopočet Q faktoru:

$$
Q = 2\pi \cdot \frac{E_{max}}{E_{max} - E_1} \\ \ \\
Q = 2\pi \cdot \frac{\frac{1}{2}m\omega^2 y_0^2}{\frac{1}{2}m\omega^2 (y_0^2 - y_1^2)}  \\ \ \\
Q = 2\pi \cdot \frac{y_0^2}{y_0^2 - y_1^2}  \\ \ \\
Q = ( 11.56 \pm 6.07 )
$$

Dále můžeme dopočítat [(viz)](https://en.wikipedia.org/wiki/Q_factor#Stored_energy_definition) ztracený výkon systému, tedy minimální výkon buzeného pístu $P$ je:

$$
Q = \omega \cdot \frac{E_{max}}{P_{min}} \\ \ \\
P_{min} = \frac{\frac{1}{2} m \omega^3 y_0^2 }{Q} \\ \ \\
P_{min} = \frac{1}{4\pi} m \omega^3 (y_0^2 - y_1^2)  \\ \ \\
P_{min} = ( 0.097 \pm 0.054 ) \ W 
$$

Do systému dodaný příkon $P_0$ vypočítáme z proudu a napětí dodávaného do zahřívací cívky:

$$
U = ( 4.7 \pm 0.1 ) \ V \\
I = ( 4.9 \pm 0.1 ) \ A \\
P_0 = U \cdot I = ( 23.03 \pm 0.96 ) \ W
$$

Konečně dopočítáme minimální účinnost $\eta_{min}$:

$$
\eta \geq \eta_{min} = \frac{P_{min}}{P_0} = ( 0.42 \pm 0.25 ) \ \%
$$

# Výpočet akustické účinnosti

Při zahřívání zkumavky s průměrem $d = ( 20.63 \pm 0.01 ) \ mm$ (zároveň chlazené) and kahanem můžeme změřit intenzitu zvuku. Při meření ve vzdálenosti $l = ( 0.2 \pm 0.025 ) \ m$ jsme sledovali, že intenzita před zkumavkou a po stranách zkumaky (> 50dB) je přibližně stejná, ale z zkumavkou je značně nižší (cca 40 dB). Aproximujeme tedy tvar šířících se zvukových vln na tvar polokoule s povrchem $A$:

$$
A = 2\pi \cdot l^2 = ( 0.08 \pm 0.02 ) \ m^2 
$$

Měření byla provedena sjemnou a hrubou vatou. Ze zvukové intenzity také vypočítáme odpovídající výkon:

U jemné vaty:
$$
I_{fine} = ( 50.0 \pm 2.0 ) \ dB \\
I_{fine} = 9.8 \cdot 10^{-8} \ \frac{W}{m^2} \\
P_{fine} = I_{fine} \cdot A = ( 7.84 \cdot 10^{-9} \pm 1.96 \cdot 10^{-9} ) \ W
$$

U hrubé vaty:
$$
I_{coarse} = ( 55.0 \pm 2.0 ) \ dB \\
I_{coarse} = 3.1 \cdot 10^{-7} \ \frac{W}{m^2} \\
P_{coarse} = I_{coarse} \cdot A = ( 2.48 \cdot 10^{-8} \pm 6.2 \cdot 10^{-9} ) \ W
$$

Zdrojem tepla byl propan-butanový kahan. Naměřený průtok $Q$:

$$
Q = \frac{100.0 \ ml}{( 12.3 \pm 0.5 ) \ s} = ( 8.13 \pm 0.33 ) \ \frac{ml}{s}
$$

Použijeme průměrnou výhřevnost $H$ podle: [zdroj 1](https://www.motoobchod.cz/plynova-kartuse-coleman-c300-240g-propan-butan-p65085/) a [zdroj 2](https://www.primagas.cz/co-je-lpg). Průmernou hustotu podle: [zdroj 3](https://cs.wikipedia.org/wiki/Propan) a [zdroj 4](https://cs.wikipedia.org/wiki/Butan). Celkový příkon $P_0$ je tedy:

$$
P_0 = H \cdot Q \cdot \rho \\
P_0 = (H_{prop} \cdot 0.3 +  H_{but} \cdot 0.7) \cdot Q \cdot (\rho_{prop} \cdot 0.3 +  \rho_{but} \cdot 0.7) \\
P_0 = (46350.0 \ \frac{kJ}{kg} \cdot 0.3 + 45726.0 \ \frac{kJ}{kg} \cdot 0.7) \cdot ( 8.13 \pm 0.33 ) \ \frac{ml}{s} \cdot (1.91 \ \frac{kg}{m^3} \cdot 0.3 + 2.48 \ \frac{kg}{m^3} \cdot 0.7) \\
P_0 = ( 861.899 \pm 35.0365 ) \ W
$$

Účinnosti jsou tedy:

$$
\eta_{fine}   = \frac{P_{fine}}{P_0} = ( 9.1 \cdot 10^{-10} \pm 2.64 \cdot 10^{-10} ) \ \%\\
\eta_{coarse} = \frac{P_{coarse}}{P_0} = ( 2.88 \cdot 10^{-9} \pm 8.36 \cdot 10^{-10} ) \ \%
$$