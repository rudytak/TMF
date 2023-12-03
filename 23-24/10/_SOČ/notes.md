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

### Omega decay:
<!-- 
https://www.wolframalpha.com/input?i2d=true&i=y%27%5C%2840%29t%5C%2841%29+%3D+-a-c*y%5C%2840%29t%5C%2841%29**2
-->
$$
\omega'(t) = - \alpha - \gamma \omega(t)^2 \\
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

### Magnetic dipole interactions

$$
F_m (r,m_1,m_2) = \frac{3\mu_0}{4\pi ||r||^5} 
\bigg[
    (m_1\cdot r) m_2 +
    (m_2\cdot r) m_1 +
    (m_1\cdot m_2) r -
    \frac{5(m_1\cdot r)(m_2\cdot r)}{||r||^2} r
\bigg] \\

B (r, m) = \frac{\mu_0}{4\pi}\frac{3 \hat{r}(\hat{r}\cdot m) - m}{|r|^3}
$$

### Change of angular velocity

$$
\frac{dL}{dt} = I\frac{d\omega}{dt} = \tau_F + \tau_{mag} \\
\tau_F = \sum_{j=0}^{n} F_m(P_{external}- P(j), m(j), m_{external}) \times (P(i) - S)\\
\tau_{mag} = \sum_{j=0}^{n} m(j) \times B(P(j)-P_{external},m_{external})\\
$$

### Better omega decay:

<!-- 
https://www.wolframalpha.com/input?i2d=true&i=y%27%5C%2840%29t%5C%2841%29+%3D+-a-b*y%5C%2840%29t%5C%2841%29-c*y%5C%2840%29t%5C%2841%29**2 
-->
$$
\omega'(t) = - \alpha -\beta \omega(t) - \gamma \omega(t)^2 \\
\omega(t) = -\frac{\sqrt{4\alpha\gamma - \beta^2} \tan{(\frac{1}{2}\sqrt{4\alpha\gamma - \beta^2}(t-c_1)})-\beta}{2\gamma}
$$