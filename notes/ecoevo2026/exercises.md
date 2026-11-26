# Ecology & Evolution 2026 — Exercises for the exam

You are *very* encouraged to discuss the exercises with others. Analytic calculations and simulations are both welcome. The oral exam starts from these exercises.

The notation is the one of the lecture notes (L1–L12, S1–S2).

## 1. Is stress mutagenic? Fluctuation tests with cell death

A culture starts from $N_0$ sensitive cells and grows until it has $N\gg N_0$ cells. $N_0$ is large enough that the culture does not go extinct, and small enough that it contains no resistant cell. Every cell divides at rate $b$ and dies at rate $d<b$. A cell born from a sensitive parent is resistant with probability $\mu$, the mutation probability per division of L3. Resistant cells divide and die at the same rates. At the end the whole culture is plated and the resistant cells, $M$, are counted. With $d=0$ this is the setting of L3.

1. On average, how many divisions does the culture go through to reach $N$ cells, and how many mutational events happen?
2. What's the average number of resistant cells $\langle M \rangle$?
3. What's the probability $P_0$ that a culture has no resistant cell? (Each mutational event founds a clone, which is a birth–death process: it counts only if it is still alive at the end.)
4. Show that the tail is still $P(M\ge m)\propto 1/m$, and find its prefactor.
5. A lab wants to know whether streptomycin, a bactericidal antibiotic, is mutagenic at doses too low to stop growth. They run two fluctuation tests as in L3, each with 100 cultures of *E. coli* inoculated with $N_0=10^3$ cells and grown to $N\approx10^8$ cells: one in plain medium, one with a quarter of the minimal inhibitory concentration (MIC) of streptomycin. At the end, each culture is plated whole on agar with rifampicin, and the rifampicin-resistant colonies are counted (resistance to rifampicin comes from mutations in the RNA polymerase, unrelated to streptomycin). Time-lapse microscopy shows that with streptomycin the cells divide as fast as without it, but die at rate $d=0.6\,b$, while without the drug $d\simeq0$. They estimate $\mu$ in the two ways of L3: from the fraction of cultures without resistant colonies, $P_0=e^{-\mu N}$, and from the mean, $\langle M\rangle=\mu N\ln(N/N_0)$. With streptomycin the first estimate is 1.5 times higher and the second 2.5 times higher, and they conclude that streptomycin is mutagenic. Do you agree? What does each estimator actually count? How could a fluctuation test alone measure $d/b$?
6. What changes if, during growth, the drug kills resistant cells less than sensitive ones, as it would if the test scored resistance to streptomycin itself (L7)?

If you want to test with simulations, use (for instance) $b=1$, $d=0.6$, $N_0=50$, $N=2\times10^4$, $\mu=5\times10^{-5}$.

## 2. Rescue or drag down? Two patches with an Allee effect

Two identical patches, each with the strong Allee effect of L5, exchange individuals at rate $\kappa$. In the units of L5,

$$
\frac{du_1}{d\tau}=f(u_1)+\kappa\,(u_2-u_1),\qquad
\frac{du_2}{d\tau}=f(u_2)+\kappa\,(u_1-u_2)
$$
with
$$
f(u)=u\,(u-\alpha)(1-u),\quad 0<\alpha<1 .
$$

Study the phase diagram as a function of $\kappa$ and $\alpha$.
Consider the case where the population is at carrying capacity in one patch and extinct in the other. What happens for $\kappa > 0$?

## 3. One resource, two winners: competition under serial dilution

Two species share a single resource in serial batch culture. At each transfer a fraction $1/D$ of the culture goes into fresh medium with resource $R_0$. Within a cycle nothing dies,

$$
\frac{dN_i}{dt}=b_i\,\phi_i(R)\,N_i,\qquad
\frac{dR}{dt}=-\sum_i\frac{b_i\,\phi_i(R)}{Y_i}\,N_i,\qquad
\phi_i(R)=\frac{R}{K_i+R},
$$

and each cycle lasts until the resource is exhausted. In a chemostat (L11) only the species with the lowest $R^*$ survives.

1. Species $r$ alone, in its periodic state: show that $N_r(t)=Y_r\,\bigl(R_0-R(t)\bigr)$ throughout the cycle.
2. Add a few cells of species $i$. What is the condition for invasion?
3. Is coexistence possible? Is bistability possible?
4. In L6 a daily dilution was *exactly* a mortality $\delta=\ln D/T$, as far as invasion is concerned. Is this still valid? Compare the outcome at $D=10$ with a chemostat at $\delta=\ln 10/(24\ \text{h})$.
5. Does the coexistence of two species on one resource contradict competitive exclusion (L11)? What plays the role of the second resource?

If you want to simulate the system consider a gleaner, $b_g=0.3$/h and $K_g=0.01$ mM, and an opportunist, $b_o=1$/h and $K_o=1$ mM, with $R_0=1$ mM. Simulate many cycles from different starting fractions.

## 4. Genetic draft: when sweeps act as noise

In an asexual population the genome is inherited as one block. A neutral site then rises and falls with the beneficial mutations that happen to sit on the same genome (selection at linked sites, L9; quasi-neutral fixation, L10). This exercise is about what these sweeps do to a neutral site.

**Setting.** A population of $N$ asexual individuals, with time measured in generations. We follow a single neutral site with two alleles, $A$ and $a$, and call $x$ the frequency of $A$. Two kinds of events change $x$.

- *Drift*, as in the Moran model of L9. Each individual reproduces at rate 1. Its offspring carries the allele of its parent and replaces an individual chosen at random.
- *Sweeps*. From time to time a beneficial mutation, with advantage $\sigma$, appears at another site, in an individual chosen at random. A sweep lasts about $2\ln N/\sigma$ generations (L7), much less than the $\sim N$ generations over which drift acts, so we treat it as instantaneous. Sweeps happen at random times, at rate $\lambda$ per generation. In a sweep, the descendants of the individual where the mutation appeared, which all carry its allele at the neutral site, replace a fraction $y$ of the population, chosen at random. In a complete sweep $y=1$, and the whole population descends from that individual. If the sweep is stopped before (for instance by a beneficial mutation in another lineage, as in clonal interference), $y<1$.

For instance, with $N=10$ and $y=0.3$: a sweep starts in individual 7, which carries $a$, and three individuals chosen at random are replaced by copies of individual 7. Treat $y$ as a fixed parameter.

1. What does a sweep do to the mean of $x$, and to its variance? What is the probability that a neutral allele, now at frequency $x$, eventually fixes? Do sweeps change the rate at which neutral mutations are substituted (the molecular clock of L9)?
2. How does the mean heterozygosity $\langle H\rangle$ decay? Now let every newborn carry a new allele with probability $\mu$ (infinitely many alleles, as in L9). Where do mutation, drift and sweeps balance? (Use the equation for $F$ of L9: what does a sweep do to $F$?)
3. Suppose the sweeps are caused by beneficial mutations that appear at rate $U_b$ per genome and escape drift with probability $\sigma$ (L10), so that $\lambda=NU_b\sigma$. How does the neutral diversity depend on $N$? Compare with Lewontin's paradox (L9). Can sweeps dominate drift while they still come one at a time (L10)?

If you want to simulate the system, use for instance $N=1000$, $\lambda=0.02$ and $y=0.2$ or $0.5$.

## 5. Why do phages survive the evolution of resistance?

Consider a chemostat with dilution rate $D$ and glucose $R$ supplied at concentration $R_{\text{in}}$, with sensitive cells $N$, resistant cells $M$ that the phage does not adsorb but that grow more slowly ($b_M<b_N$), and phages $V$ without latent period:

$$
\begin{aligned}
\frac{dR}{dt}&=D\,(R_{\text{in}}-R)-\frac{b_N\,\phi(R)\,N+b_M\,\phi(R)\,M}{Y},\\
\frac{dN}{dt}&=\bigl(b_N\,\phi(R)-D\bigr)N-aNV,\qquad
\frac{dM}{dt}=\bigl(b_M\,\phi(R)-D\bigr)M,\\
\frac{dV}{dt}&=(\beta-1)\,aNV-DV,
\end{aligned}
\qquad \phi(R)=\frac{R}{K_R+R}.
$$

1. Without phages, who wins? Without resistant cells, find the coexistence point of $N$ and $V$, and the minimal $R_{\text{in}}$ for the phage to persist.
2. A resistant mutant appears in the $N$–$V$ chemostat. Under what conditions does it invade?
3. Find the fixed point with all four populations present. What keeps the phage alive? What if resistance were free?
4. Two kinds of bacteria and a phage persist on a single supplied resource. Does this contradict competitive exclusion (L11)?
5. How does the probability that a resistant mutant arises and establishes in the population depend on the mutation rate $\mu$ and on the supplied resource $R_{\text{in}}$?

For simulations you can use $D=0.2$/h, $b_N=0.77$/h, $K_R=0.073$ mg/L, $Y=5\times10^5$ cells/ml per mg/L, $a=3\times10^{-7}$ ml/h, $\beta=80$ and $b_M=0.5$/h.
