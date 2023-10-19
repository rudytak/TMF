## Spinner properties

$n$ ... total number of magnets \
$r$ ... radius of spinner \
$S$ ... centerpoint of the spinner (also position of axis of rotation)

$\varphi$ ... angle of rotation \
$\omega$ ... angular velocity \
$\alpha$ ... angular acceleration \
$I$ ... moment of inertia of the spinner \


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

$$
\omega'(t) = - \alpha - \gamma \omega(t)^2 \\
\omega(t) = -\sqrt{\frac{\alpha}{\gamma}} \tan{(\sqrt{\alpha\gamma}(t+c_1))}
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