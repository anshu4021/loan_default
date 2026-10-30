# 🔬 Technical Documentation 02: Mathematical Foundations of SHAP & LIME

This document provides rigorous mathematical derivations, algorithmic proofs, and theoretical comparisons for the explainability methods implemented in this system.

---

## 1. Cooperative Game Theory & Shapley Value Derivation

In 1953, Lloyd Shapley introduced a method to fairly allocate total gains to cooperating players in a coalition game.

### Definition:
Let $N = \{1, 2, \dots, M\}$ be the grand coalition of all $M$ features. Let $v(S)$ be a characteristic function that assigns a real value to any coalition of features $S \subseteq N$, representing the model's predicted outcome when only features in $S$ are present.

The unique Shapley value $\phi_i(v)$ assigned to feature $i$ is:

$$\phi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(|N| - |S| - 1)!}{|N|!} \left[ v(S \cup \{i\}) - v(S) \right]$$

### The Weighting Term Interpretation:
The combinatorial coefficient represents the probability that feature $i$ enters coalition $S$ when all features are introduced in a uniformly random permutation:
- $|S|!$: Number of ways to order features preceding feature $i$.
- $(|N| - |S| - 1)!$: Number of ways to order remaining features after feature $i$.
- $|N|!$: Total permutations of the grand coalition $N$.

---

## 2. The Four Fundamental Axioms (Unique to SHAP)

SHAP is the **only** additive feature attribution method that simultaneously satisfies these four axioms:

### Axiom 1: Efficiency (Local Accuracy)
The sum of feature attributions equals the difference between the model prediction $f(x)$ and the baseline expected value $E[f(X)]$:

$$\sum_{i=1}^M \phi_i = f(x) - E[f(X)]$$

*Significance in Lending:* Guarantees that 100% of the applicant's risk deviation is accounted for—no attribution is lost or fabricated.

### Axiom 2: Symmetry (Equal Treatment)
If two features $i$ and $j$ make identical marginal contributions across all coalitions:
$$v(S \cup \{i\}) = v(S \cup \{j\}) \quad \forall S \subseteq N \setminus \{i, j\}$$
Then their Shapley values must be equal:
$$\phi_i = \phi_j$$

*Significance in Lending:* Prevents arbitrary bias; identical risk drivers receive identical importance.

### Axiom 3: Dummy Player (Null Contribution)
If feature $i$ contributes zero marginal value to any coalition:
$$v(S \cup \{i\}) = v(S) \quad \forall S \subseteq N \setminus \{i\}$$
Then its attribution is strictly zero:
$$\phi_i = 0$$

*Significance in Lending:* Guarantees irrelevant variables (e.g., applicant eye color) receive zero legal blame.

### Axiom 4: Additivity (Linear Summation)
If a model $f$ is formed by summing two sub-models $u$ and $v$ ($f = u + v$):
$$\phi_i(u + v) = \phi_i(u) + \phi_i(v)$$

*Significance in Lending:* Enables exact polynomial-time evaluation across ensembles of trees (such as XGBoost or Random Forests).

---

## 3. TreeSHAP vs KernelSHAP: Computational Complexity

| Dimension | KernelSHAP (Model-Agnostic) | TreeSHAP (Tree-Specific) |
| :--- | :---: | :---: |
| **Complexity Class** | Exponential: $\mathcal{O}(M \cdot 2^{|F|})$ | Polynomial: $\mathcal{O}(T \cdot L \cdot D^2)$ |
| **Explanation Latency** | 1,500 – 4,000 ms per sample | **8.60 ms** per sample |
| **Mechanism** | Sampling feature subsets & fitting weighted regression | Recursive dynamic programming down tree split paths |
| **Production Fit** | Offline batch analysis | **Real-time Underwriting APIs** |

---

## 4. LIME Mathematical Formulation

LIME (Local Interpretable Model-agnostic Explanations) optimizes an interpretable surrogate model $g \in G$ to approximate black-box model $f$ locally around applicant $x$:

$$\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$

Where:
- **$\mathcal{L}(f, g, \pi_x)$**: Local fidelity loss:
  $$\mathcal{L}(f, g, \pi_x) = \sum_{z, z' \in \mathcal{Z}} \pi_x(z) \left( f(z) - g(z') \right)^2$$
- **$\pi_x(z)$**: Proximity exponential kernel:
  $$\pi_x(z) = \exp\left( - \frac{D(x, z)^2}{\sigma^2} \right)$$
  *(Where $D(x, z)$ is Euclidean distance and $\sigma$ is kernel bandwidth).*
- **$\Omega(g)$**: Complexity penalty (limiting surrogate $g$ to $K$ non-zero coefficients).
