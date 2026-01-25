# OMML to LaTeX Conversion Reference

This document describes the mapping between Office Math Markup Language (OMML) and LaTeX mathematical notation.

## OMML Element Mappings

### Fractions (`m:f`)

```xml
<m:f>
  <m:num>numerator</m:num>
  <m:den>denominator</m:den>
</m:f>
```

**LaTeX:** `\frac{numerator}{denominator}`

### Superscripts (`m:sSup`)

```xml
<m:sSup>
  <m:e>base</m:e>
  <m:sup>exponent</m:sup>
</m:sSup>
```

**LaTeX:** `base^{exponent}`

### Subscripts (`m:sSub`)

```xml
<m:sSub>
  <m:e>base</m:e>
  <m:sub>subscript</m:sub>
</m:sSub>
```

**LaTeX:** `base_{subscript}`

### Combined Sub/Superscripts (`m:sSubSup`)

```xml
<m:sSubSup>
  <m:e>base</m:e>
  <m:sub>subscript</m:sub>
  <m:sup>superscript</m:sup>
</m:sSubSup>
```

**LaTeX:** `base_{subscript}^{superscript}`

### Radicals (`m:rad`)

```xml
<m:rad>
  <m:radPr>
    <m:degHide m:val="1"/>  <!-- Square root when val="1" -->
  </m:radPr>
  <m:deg>n</m:deg>
  <m:e>expression</m:e>
</m:rad>
```

**LaTeX:**
- Square root: `\sqrt{expression}`
- Nth root: `\sqrt[n]{expression}`

### N-ary Operators (`m:nary`)

```xml
<m:nary>
  <m:naryPr>
    <m:chr m:val="∑"/>
  </m:naryPr>
  <m:sub>lower</m:sub>
  <m:sup>upper</m:sup>
  <m:e>expression</m:e>
</m:nary>
```

**LaTeX:** `\sum_{lower}^{upper} expression`

Supported operators:
| OMML | LaTeX |
|------|-------|
| ∑ | `\sum` |
| ∏ | `\prod` |
| ∫ | `\int` |
| ∬ | `\iint` |
| ∭ | `\iiint` |
| ∮ | `\oint` |
| ⋃ | `\bigcup` |
| ⋂ | `\bigcap` |

### Delimiters (`m:d`)

```xml
<m:d>
  <m:dPr>
    <m:begChr m:val="("/>
    <m:endChr m:val=")"/>
  </m:dPr>
  <m:e>content</m:e>
</m:d>
```

**LaTeX:** `\left( content \right)`

### Functions (`m:func`)

```xml
<m:func>
  <m:fName>
    <m:r><m:t>sin</m:t></m:r>
  </m:fName>
  <m:e>argument</m:e>
</m:func>
```

**LaTeX:** `\sin argument`

Standard functions: sin, cos, tan, log, ln, exp, lim, max, min, etc.

### Matrices (`m:m`)

```xml
<m:m>
  <m:mr>
    <m:e>a</m:e>
    <m:e>b</m:e>
  </m:mr>
  <m:mr>
    <m:e>c</m:e>
    <m:e>d</m:e>
  </m:mr>
</m:m>
```

**LaTeX:**
```latex
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
```

### Accents (`m:acc`)

```xml
<m:acc>
  <m:accPr>
    <m:chr m:val="^"/>
  </m:accPr>
  <m:e>x</m:e>
</m:acc>
```

| OMML | LaTeX |
|------|-------|
| ^ | `\hat{x}` |
| ¯ | `\bar{x}` |
| → | `\vec{x}` |
| ˙ | `\dot{x}` |
| ¨ | `\ddot{x}` |
| ˜ | `\tilde{x}` |

### Equation Arrays (`m:eqArr`)

```xml
<m:eqArr>
  <m:e>equation1</m:e>
  <m:e>equation2</m:e>
</m:eqArr>
```

**LaTeX:**
```latex
\begin{aligned}
equation1 \\
equation2
\end{aligned}
```

## Greek Letters

| Unicode | LaTeX |
|---------|-------|
| α | `\alpha` |
| β | `\beta` |
| γ | `\gamma` |
| δ | `\delta` |
| ε | `\varepsilon` |
| θ | `\theta` |
| λ | `\lambda` |
| μ | `\mu` |
| π | `\pi` |
| σ | `\sigma` |
| φ | `\varphi` |
| ω | `\omega` |
| Γ | `\Gamma` |
| Δ | `\Delta` |
| Θ | `\Theta` |
| Λ | `\Lambda` |
| Σ | `\Sigma` |
| Φ | `\Phi` |
| Ω | `\Omega` |

## Mathematical Symbols

| Unicode | LaTeX |
|---------|-------|
| ∞ | `\infty` |
| ∂ | `\partial` |
| ∇ | `\nabla` |
| ± | `\pm` |
| × | `\times` |
| ÷ | `\div` |
| · | `\cdot` |
| ≤ | `\leq` |
| ≥ | `\geq` |
| ≠ | `\neq` |
| ≈ | `\approx` |
| ≡ | `\equiv` |
| ∈ | `\in` |
| ∉ | `\notin` |
| ⊂ | `\subset` |
| ⊆ | `\subseteq` |
| ∪ | `\cup` |
| ∩ | `\cap` |
| ∅ | `\emptyset` |
| ∀ | `\forall` |
| ∃ | `\exists` |
| → | `\to` |
| ⇒ | `\Rightarrow` |
| ⇔ | `\Leftrightarrow` |

## Troubleshooting

### Common Issues

1. **Missing symbols**: Ensure the LaTeX document includes `\usepackage{amssymb}` and `\usepackage{amsmath}`

2. **Inline vs Display math**:
   - `m:oMathPara` → Display math: `\[ ... \]`
   - `m:oMath` (in paragraph) → Inline math: `$ ... $`

3. **Nested structures**: The converter handles arbitrarily nested elements (e.g., fractions within fractions)

4. **Unknown characters**: Characters not in the mapping table are passed through unchanged
