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
1px = \frac{@0@}{@1@ - @2@} = @3@            \\
f = \frac{1}{25 * 40} s = @4@                     \\
m = @5@                                      \\
$$

$$
y_0 = (@6@ - @7@)px = @9@                              \\
y_1 = (@6@ - @8@)px = @10@                              \\
T = (@11@ - @12@)f = @13@                        \\
\omega = \frac{2\pi}{T}= @14@                       \\
$$

Dopočet Q faktoru:

$$
Q = 2\pi \cdot \frac{E_{max}}{E_{max} - E_1} \\ \ \\
Q = 2\pi \cdot \frac{\frac{1}{2}m\omega^2 y_0^2}{\frac{1}{2}m\omega^2 (y_0^2 - y_1^2)}  \\ \ \\
Q = 2\pi \cdot \frac{y_0^2}{y_0^2 - y_1^2}  \\ \ \\
Q = @15@
$$

Dále můžeme dopočítat [(viz)](https://en.wikipedia.org/wiki/Q_factor#Stored_energy_definition) ztracený výkon systému, tedy minimální výkon buzeného pístu $P$ je:

$$
Q = \omega \cdot \frac{E_{max}}{P_{min}} \\ \ \\
P_{min} = \frac{\frac{1}{2} m \omega^3 y_0^2 }{Q} \\ \ \\
P_{min} = \frac{1}{4\pi} m \omega^3 (y_0^2 - y_1^2)  \\ \ \\
P_{min} = @16@ 
$$

Do systému dodaný příkon $P_0$ vypočítáme z proudu a napětí dodávaného do zahřívací cívky:

$$
U = @17@ \\
I = @18@ \\
P_0 = U \cdot I = @19@
$$

Konečně dopočítáme minimální účinnost $\eta_{min}$:

$$
\eta \geq \eta_{min} = \frac{P_{min}}{P_0} = @20@
$$

# Výpočet akustické účinnosti

Při zahřívání zkumavky s průměrem $d = @21@$ (zároveň chlazené) and kahanem můžeme změřit intenzitu zvuku. Při meření ve vzdálenosti $l = @22@$ jsme sledovali, že intenzita před zkumavkou a po stranách zkumaky (> 50dB) je přibližně stejná, ale z zkumavkou je značně nižší (cca 40 dB). Aproximujeme tedy tvar šířících se zvukových vln na tvar polokoule s povrchem $A$:

$$
A = 2\pi \cdot l^2 = @23@ 
$$

Měření byla provedena sjemnou a hrubou vatou. Ze zvukové intenzity také vypočítáme odpovídající výkon:

U jemné vaty:
$$
I_{fine} = @24@ \\
I_{fine} = @25@ \\
P_{fine} = I_{fine} \cdot A = @26@
$$

U hrubé vaty:
$$
I_{coarse} = @27@ \\
I_{coarse} = @28@ \\
P_{coarse} = I_{coarse} \cdot A = @29@
$$

Zdrojem tepla byl propan-butanový kahan. Naměřený průtok $Q$:

$$
Q = \frac{@30@}{@31@} = @32@
$$

Použijeme průměrnou výhřevnost $H$ podle: [zdroj 1](https://www.motoobchod.cz/plynova-kartuse-coleman-c300-240g-propan-butan-p65085/) a [zdroj 2](https://www.primagas.cz/co-je-lpg). Průmernou hustotu podle: [zdroj 3](https://cs.wikipedia.org/wiki/Propan) a [zdroj 4](https://cs.wikipedia.org/wiki/Butan). Celkový příkon $P_0$ je tedy:

$$
P_0 = H \cdot Q \cdot \rho \\
P_0 = (H_{prop} \cdot @33@ +  H_{but} \cdot @36@) \cdot Q \cdot (\rho_{prop} \cdot @33@ +  \rho_{but} \cdot @36@) \\
P_0 = (@34@ \cdot @33@ + @37@ \cdot @36@) \cdot @32@ \cdot (@35@ \cdot @33@ + @38@ \cdot @36@) \\
P_0 = @39@
$$

Účinnosti jsou tedy:

$$
\eta_{fine}   = \frac{P_{fine}}{P_0} = @40@\\
\eta_{coarse} = \frac{P_{coarse}}{P_0} = @41@
$$