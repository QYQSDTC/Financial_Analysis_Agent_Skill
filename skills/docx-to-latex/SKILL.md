---
name: docx-to-latex
description: Convert Word documents (.docx) to LaTeX format with full support for OMML mathematical formulas, images, tables, and text formatting. Use when the user wants to convert a Word document to LaTeX, particularly documents containing mathematical equations, formulas, or scientific content.
---

# DOCX to LaTeX Converter

Convert Word documents to LaTeX with accurate math formula conversion.

## Quick Start

Run the conversion script:

```bash
python scripts/docx_to_latex.py input.docx output.tex --images-dir images
```

## Workflow

### 1. Basic Conversion

```bash
python scripts/docx_to_latex.py document.docx document.tex
```

This extracts:
- Text content with formatting (bold, italic, underline)
- Headings → `\section`, `\subsection`, etc.
- Lists → `itemize`/`enumerate`
- Tables → `tabular` environment
- Images → extracted to `images/` folder
- Math formulas (OMML) → LaTeX math notation

### 2. Review Math Formulas

After conversion, verify complex formulas in the output `.tex` file. The converter handles:

- Fractions: `\frac{a}{b}`
- Subscripts/superscripts: `x_{i}^{2}`
- Radicals: `\sqrt{x}`, `\sqrt[n]{x}`
- Integrals/sums: `\int_{a}^{b}`, `\sum_{i=1}^{n}`
- Matrices: `pmatrix` environment
- Greek letters and math symbols
- Delimiters with auto-sizing: `\left( \right)`

For OMML element details, see [references/omml_conversion.md](references/omml_conversion.md).

### 3. Compile LaTeX

```bash
pdflatex output.tex
```

Required packages (auto-included in preamble):
- `amsmath`, `amsfonts`, `amssymb` - math support
- `graphicx` - images
- `hyperref` - links
- `booktabs` - tables

## Manual Adjustments

After automatic conversion, may need manual fixes for:

| Issue | Solution |
|-------|----------|
| Complex nested formulas | Verify bracket matching |
| Custom macros in original | Define in preamble |
| Equation numbering | Add `\label{}` and use `equation` environment |
| Figure captions | Update auto-generated "Image" captions |
| Table alignment | Adjust column specs in `tabular` |

## Example

Input (Word with OMML):
- Equation: "The quadratic formula is x = (-b ± √(b²-4ac)) / 2a"

Output (LaTeX):
```latex
The quadratic formula is $x = \frac{-b \pm \sqrt{b^{2} - 4ac}}{2a}$
```
