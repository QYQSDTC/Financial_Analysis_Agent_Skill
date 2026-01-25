#!/usr/bin/env python3
"""
DOCX to LaTeX Converter with OMML Math Support

Converts Word documents (.docx) to LaTeX format, handling:
- Text content and formatting (bold, italic, underline)
- Paragraphs and headings
- Images (extracted and referenced)
- OMML mathematical formulas (converted to LaTeX math)
- Tables
- Lists (numbered and bulleted)

Usage:
    python docx_to_latex.py input.docx output.tex [--images-dir images]
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

# XML namespaces used in DOCX
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
}

# Register namespaces
for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)


class OmmlToLatexConverter:
    """Converts Office Math Markup Language (OMML) to LaTeX math notation."""

    def __init__(self):
        self.m = '{http://schemas.openxmlformats.org/officeDocument/2006/math}'
        self.w = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

    def convert(self, omml_element):
        """Convert an OMML element to LaTeX string."""
        return self._process_element(omml_element)

    def _process_element(self, elem):
        """Process any OMML element and return LaTeX."""
        if elem is None:
            return ''

        tag = elem.tag.replace(self.m, '').replace(self.w, '')

        handlers = {
            'oMathPara': self._handle_math_para,
            'oMath': self._handle_math,
            'r': self._handle_run,
            't': self._handle_text,
            'f': self._handle_fraction,
            'rad': self._handle_radical,
            'sSup': self._handle_superscript,
            'sSub': self._handle_subscript,
            'sSubSup': self._handle_subsup,
            'nary': self._handle_nary,
            'd': self._handle_delimiter,
            'func': self._handle_function,
            'm': self._handle_matrix,
            'mr': self._handle_matrix_row,
            'e': self._handle_element,
            'num': self._handle_numerator,
            'den': self._handle_denominator,
            'deg': self._handle_degree,
            'sup': self._handle_sup,
            'sub': self._handle_sub,
            'lim': self._handle_limit,
            'fName': self._handle_func_name,
            'acc': self._handle_accent,
            'bar': self._handle_bar,
            'box': self._handle_box,
            'groupChr': self._handle_group_char,
            'limLow': self._handle_lim_low,
            'limUpp': self._handle_lim_upp,
            'eqArr': self._handle_eq_array,
            'sPre': self._handle_pre_sub_sup,
        }

        handler = handlers.get(tag, self._handle_default)
        return handler(elem)

    def _handle_math_para(self, elem):
        """Handle math paragraph (display math)."""
        content = self._process_children(elem)
        return content

    def _handle_math(self, elem):
        """Handle math element."""
        return self._process_children(elem)

    def _handle_run(self, elem):
        """Handle run element (text run in math)."""
        result = []
        for child in elem:
            result.append(self._process_element(child))
        return ''.join(result)

    def _handle_text(self, elem):
        """Handle text element."""
        text = elem.text or ''
        # Convert special characters
        text = self._escape_latex(text)
        return text

    def _escape_latex(self, text):
        """Escape special LaTeX characters and convert symbols."""
        if not text:
            return ''

        # Greek letters mapping
        greek_map = {
            'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma', 'δ': r'\delta',
            'ε': r'\varepsilon', 'ζ': r'\zeta', 'η': r'\eta', 'θ': r'\theta',
            'ι': r'\iota', 'κ': r'\kappa', 'λ': r'\lambda', 'μ': r'\mu',
            'ν': r'\nu', 'ξ': r'\xi', 'π': r'\pi', 'ρ': r'\rho',
            'σ': r'\sigma', 'τ': r'\tau', 'υ': r'\upsilon', 'φ': r'\varphi',
            'χ': r'\chi', 'ψ': r'\psi', 'ω': r'\omega',
            'Α': r'A', 'Β': r'B', 'Γ': r'\Gamma', 'Δ': r'\Delta',
            'Ε': r'E', 'Ζ': r'Z', 'Η': r'H', 'Θ': r'\Theta',
            'Ι': r'I', 'Κ': r'K', 'Λ': r'\Lambda', 'Μ': r'M',
            'Ν': r'N', 'Ξ': r'\Xi', 'Π': r'\Pi', 'Ρ': r'P',
            'Σ': r'\Sigma', 'Τ': r'T', 'Υ': r'\Upsilon', 'Φ': r'\Phi',
            'Χ': r'X', 'Ψ': r'\Psi', 'Ω': r'\Omega',
            'ϕ': r'\phi', 'ϵ': r'\epsilon', 'ϑ': r'\vartheta',
            'ϖ': r'\varpi', 'ϱ': r'\varrho', 'ς': r'\varsigma',
        }

        # Math symbols mapping
        symbol_map = {
            '∞': r'\infty', '∂': r'\partial', '∇': r'\nabla',
            '∑': r'\sum', '∏': r'\prod', '∫': r'\int',
            '∮': r'\oint', '∬': r'\iint', '∭': r'\iiint',
            '√': r'\sqrt', '∛': r'\sqrt[3]', '∜': r'\sqrt[4]',
            '±': r'\pm', '∓': r'\mp', '×': r'\times', '÷': r'\div',
            '·': r'\cdot', '∘': r'\circ', '⊗': r'\otimes', '⊕': r'\oplus',
            '≤': r'\leq', '≥': r'\geq', '≠': r'\neq', '≈': r'\approx',
            '≡': r'\equiv', '∝': r'\propto', '∼': r'\sim', '≃': r'\simeq',
            '≅': r'\cong', '≪': r'\ll', '≫': r'\gg',
            '∈': r'\in', '∉': r'\notin', '⊂': r'\subset', '⊃': r'\supset',
            '⊆': r'\subseteq', '⊇': r'\supseteq', '∪': r'\cup', '∩': r'\cap',
            '∅': r'\emptyset', '∀': r'\forall', '∃': r'\exists', '¬': r'\neg',
            '∧': r'\land', '∨': r'\lor', '⇒': r'\Rightarrow', '⇔': r'\Leftrightarrow',
            '→': r'\to', '←': r'\leftarrow', '↔': r'\leftrightarrow',
            '⇐': r'\Leftarrow', '↑': r'\uparrow', '↓': r'\downarrow',
            '′': r"'", '″': r"''", '‴': r"'''",
            '°': r'^\circ', '‰': r'\permil',
            'ℕ': r'\mathbb{N}', 'ℤ': r'\mathbb{Z}', 'ℚ': r'\mathbb{Q}',
            'ℝ': r'\mathbb{R}', 'ℂ': r'\mathbb{C}',
            '⟨': r'\langle', '⟩': r'\rangle',
            '⌈': r'\lceil', '⌉': r'\rceil', '⌊': r'\lfloor', '⌋': r'\rfloor',
            '|': r'\vert', '‖': r'\Vert',
            '…': r'\ldots', '⋯': r'\cdots', '⋮': r'\vdots', '⋱': r'\ddots',
            'ℓ': r'\ell', 'ℏ': r'\hbar', '℘': r'\wp', 'ℑ': r'\Im', 'ℜ': r'\Re',
        }

        result = []
        for char in text:
            if char in greek_map:
                result.append(greek_map[char] + ' ')
            elif char in symbol_map:
                result.append(symbol_map[char] + ' ')
            elif char in '#$%&_{}':
                result.append('\\' + char)
            elif char == '\\':
                result.append(r'\backslash ')
            elif char == '^':
                result.append(r'\hat{}')
            elif char == '~':
                result.append(r'\tilde{}')
            else:
                result.append(char)

        return ''.join(result).strip()

    def _handle_fraction(self, elem):
        """Handle fraction: num/den."""
        num = ''
        den = ''
        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'num':
                num = self._process_element(child)
            elif tag == 'den':
                den = self._process_element(child)
        return r'\frac{' + num + '}{' + den + '}'

    def _handle_radical(self, elem):
        """Handle radical (square root or nth root)."""
        degree = ''
        base = ''

        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'radPr':
                # Check for degree hide property
                deg_hide = child.find(f'{self.m}degHide')
                if deg_hide is not None:
                    val = deg_hide.get(f'{self.m}val', '1')
                    if val == '1':
                        degree = ''  # Square root
            elif tag == 'deg':
                degree = self._process_element(child)
            elif tag == 'e':
                base = self._process_element(child)

        if degree and degree.strip():
            return r'\sqrt[' + degree + ']{' + base + '}'
        else:
            return r'\sqrt{' + base + '}'

    def _handle_superscript(self, elem):
        """Handle superscript: base^sup."""
        base = ''
        sup = ''
        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'e':
                base = self._process_element(child)
            elif tag == 'sup':
                sup = self._process_element(child)
        return base + '^{' + sup + '}'

    def _handle_subscript(self, elem):
        """Handle subscript: base_sub."""
        base = ''
        sub = ''
        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'e':
                base = self._process_element(child)
            elif tag == 'sub':
                sub = self._process_element(child)
        return base + '_{' + sub + '}'

    def _handle_subsup(self, elem):
        """Handle subscript and superscript: base_sub^sup."""
        base = ''
        sub = ''
        sup = ''
        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'e':
                base = self._process_element(child)
            elif tag == 'sub':
                sub = self._process_element(child)
            elif tag == 'sup':
                sup = self._process_element(child)
        return base + '_{' + sub + '}^{' + sup + '}'

    def _handle_nary(self, elem):
        """Handle n-ary operators (sum, product, integral, etc.)."""
        operator = r'\int'  # Default
        sub = ''
        sup = ''
        base = ''

        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'naryPr':
                # Get the operator character
                chr_elem = child.find(f'{self.m}chr')
                if chr_elem is not None:
                    char = chr_elem.get(f'{self.m}val', '∫')
                    operator_map = {
                        '∑': r'\sum',
                        '∏': r'\prod',
                        '∫': r'\int',
                        '∬': r'\iint',
                        '∭': r'\iiint',
                        '∮': r'\oint',
                        '⋃': r'\bigcup',
                        '⋂': r'\bigcap',
                        '⋁': r'\bigvee',
                        '⋀': r'\bigwedge',
                        '⨁': r'\bigoplus',
                        '⨂': r'\bigotimes',
                    }
                    operator = operator_map.get(char, r'\int')
            elif tag == 'sub':
                sub = self._process_element(child)
            elif tag == 'sup':
                sup = self._process_element(child)
            elif tag == 'e':
                base = self._process_element(child)

        result = operator
        if sub:
            result += '_{' + sub + '}'
        if sup:
            result += '^{' + sup + '}'
        result += ' ' + base
        return result

    def _handle_delimiter(self, elem):
        """Handle delimiters (parentheses, brackets, braces, etc.)."""
        beg_char = '('
        end_char = ')'
        content = ''

        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'dPr':
                beg = child.find(f'{self.m}begChr')
                end = child.find(f'{self.m}endChr')
                if beg is not None:
                    beg_char = beg.get(f'{self.m}val', '(')
                if end is not None:
                    end_char = end.get(f'{self.m}val', ')')
            elif tag == 'e':
                content = self._process_element(child)

        # Map delimiter characters to LaTeX
        delim_map = {
            '(': (r'\left(', r'\right)'),
            ')': (r'\left)', r'\right)'),
            '[': (r'\left[', r'\right]'),
            ']': (r'\left]', r'\right]'),
            '{': (r'\left\{', r'\right\}'),
            '}': (r'\left\}', r'\right\}'),
            '|': (r'\left|', r'\right|'),
            '‖': (r'\left\|', r'\right\|'),
            '⟨': (r'\left\langle', r'\right\rangle'),
            '⟩': (r'\left\rangle', r'\right\rangle'),
            '⌈': (r'\left\lceil', r'\right\rceil'),
            '⌉': (r'\left\rceil', r'\right\rceil'),
            '⌊': (r'\left\lfloor', r'\right\rfloor'),
            '⌋': (r'\left\rfloor', r'\right\rfloor'),
            '': (r'\left.', r'\right.'),
        }

        left = delim_map.get(beg_char, (r'\left' + beg_char, ''))[0]
        right = delim_map.get(end_char, ('', r'\right' + end_char))[1] if end_char else r'\right.'

        if not beg_char:
            left = r'\left.'
        if not end_char:
            right = r'\right.'

        return left + ' ' + content + ' ' + right

    def _handle_function(self, elem):
        """Handle function (sin, cos, log, etc.)."""
        func_name = ''
        argument = ''

        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'fName':
                func_name = self._process_element(child)
            elif tag == 'e':
                argument = self._process_element(child)

        # Standard function names
        std_funcs = ['sin', 'cos', 'tan', 'cot', 'sec', 'csc',
                     'sinh', 'cosh', 'tanh', 'coth',
                     'arcsin', 'arccos', 'arctan',
                     'log', 'ln', 'exp', 'lim', 'max', 'min',
                     'sup', 'inf', 'det', 'dim', 'ker', 'deg',
                     'gcd', 'lcm', 'arg', 'mod']

        func_clean = func_name.strip()
        if func_clean.lower() in std_funcs:
            return '\\' + func_clean.lower() + ' ' + argument
        else:
            return r'\mathrm{' + func_clean + '} ' + argument

    def _handle_matrix(self, elem):
        """Handle matrix."""
        rows = []
        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'mr':
                rows.append(self._handle_matrix_row(child))

        return r'\begin{pmatrix}' + ' \\\\ '.join(rows) + r'\end{pmatrix}'

    def _handle_matrix_row(self, elem):
        """Handle matrix row."""
        cells = []
        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'e':
                cells.append(self._process_element(child))
        return ' & '.join(cells)

    def _handle_element(self, elem):
        """Handle generic element container."""
        return self._process_children(elem)

    def _handle_numerator(self, elem):
        """Handle numerator."""
        return self._process_children(elem)

    def _handle_denominator(self, elem):
        """Handle denominator."""
        return self._process_children(elem)

    def _handle_degree(self, elem):
        """Handle degree (for radicals)."""
        return self._process_children(elem)

    def _handle_sup(self, elem):
        """Handle superscript content."""
        return self._process_children(elem)

    def _handle_sub(self, elem):
        """Handle subscript content."""
        return self._process_children(elem)

    def _handle_limit(self, elem):
        """Handle limit content."""
        return self._process_children(elem)

    def _handle_func_name(self, elem):
        """Handle function name."""
        return self._process_children(elem)

    def _handle_accent(self, elem):
        """Handle accents (hat, bar, vec, etc.)."""
        accent_char = '^'  # Default hat
        base = ''

        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'accPr':
                chr_elem = child.find(f'{self.m}chr')
                if chr_elem is not None:
                    accent_char = chr_elem.get(f'{self.m}val', '^')
            elif tag == 'e':
                base = self._process_element(child)

        accent_map = {
            '^': r'\hat',
            '̂': r'\hat',
            '¯': r'\bar',
            '̄': r'\bar',
            '→': r'\vec',
            '⃗': r'\vec',
            '˙': r'\dot',
            '̇': r'\dot',
            '¨': r'\ddot',
            '̈': r'\ddot',
            '˜': r'\tilde',
            '̃': r'\tilde',
            '˘': r'\breve',
            '̆': r'\breve',
            'ˇ': r'\check',
            '̌': r'\check',
        }

        accent_cmd = accent_map.get(accent_char, r'\hat')
        return accent_cmd + '{' + base + '}'

    def _handle_bar(self, elem):
        """Handle bar/overline."""
        base = ''
        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'e':
                base = self._process_element(child)
        return r'\overline{' + base + '}'

    def _handle_box(self, elem):
        """Handle box."""
        return self._process_children(elem)

    def _handle_group_char(self, elem):
        """Handle group character (underbrace, overbrace, etc.)."""
        char = '⏟'  # Default underbrace
        base = ''

        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'groupChrPr':
                chr_elem = child.find(f'{self.m}chr')
                if chr_elem is not None:
                    char = chr_elem.get(f'{self.m}val', '⏟')
            elif tag == 'e':
                base = self._process_element(child)

        if char in ['⏟', '︸']:
            return r'\underbrace{' + base + '}'
        elif char in ['⏞', '︷']:
            return r'\overbrace{' + base + '}'
        else:
            return base

    def _handle_lim_low(self, elem):
        """Handle limit with subscript (e.g., lim_{x->0})."""
        base = ''
        limit = ''

        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'e':
                base = self._process_element(child)
            elif tag == 'lim':
                limit = self._process_element(child)

        return base + '_{' + limit + '}'

    def _handle_lim_upp(self, elem):
        """Handle limit with superscript."""
        base = ''
        limit = ''

        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'e':
                base = self._process_element(child)
            elif tag == 'lim':
                limit = self._process_element(child)

        return base + '^{' + limit + '}'

    def _handle_eq_array(self, elem):
        """Handle equation array (aligned equations)."""
        equations = []
        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'e':
                equations.append(self._process_element(child))

        return r'\begin{aligned}' + ' \\\\ '.join(equations) + r'\end{aligned}'

    def _handle_pre_sub_sup(self, elem):
        """Handle pre-subscript and pre-superscript (e.g., tensor notation)."""
        pre_sub = ''
        pre_sup = ''
        base = ''

        for child in elem:
            tag = child.tag.replace(self.m, '')
            if tag == 'sub':
                pre_sub = self._process_element(child)
            elif tag == 'sup':
                pre_sup = self._process_element(child)
            elif tag == 'e':
                base = self._process_element(child)

        return '{}_{' + pre_sub + '}^{' + pre_sup + '}' + base

    def _handle_default(self, elem):
        """Default handler for unknown elements."""
        return self._process_children(elem)

    def _process_children(self, elem):
        """Process all children of an element."""
        result = []
        for child in elem:
            result.append(self._process_element(child))
        return ''.join(result)


class DocxToLatexConverter:
    """Converts DOCX files to LaTeX format."""

    def __init__(self, docx_path, images_dir='images'):
        self.docx_path = Path(docx_path)
        self.images_dir = images_dir
        self.image_counter = 0
        self.extracted_images = []
        self.omml_converter = OmmlToLatexConverter()
        self.relationships = {}

    def convert(self):
        """Convert the DOCX file to LaTeX."""
        with zipfile.ZipFile(self.docx_path, 'r') as docx:
            # Load relationships
            self._load_relationships(docx)

            # Extract images
            self._extract_images(docx)

            # Parse document
            document_xml = docx.read('word/document.xml')
            root = ET.fromstring(document_xml)

            # Convert content
            body = root.find('.//w:body', NAMESPACES)
            content = self._process_body(body)

            # Generate LaTeX document
            return self._generate_latex_document(content)

    def _load_relationships(self, docx):
        """Load document relationships (for images)."""
        try:
            rels_xml = docx.read('word/_rels/document.xml.rels')
            rels_root = ET.fromstring(rels_xml)
            for rel in rels_root:
                rel_id = rel.get('Id')
                target = rel.get('Target')
                if rel_id and target:
                    self.relationships[rel_id] = target
        except KeyError:
            pass

    def _extract_images(self, docx):
        """Extract images from the DOCX file."""
        output_dir = Path(self.images_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for name in docx.namelist():
            if name.startswith('word/media/'):
                image_data = docx.read(name)
                image_name = os.path.basename(name)
                output_path = output_dir / image_name
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                self.extracted_images.append(image_name)

    def _process_body(self, body):
        """Process the document body."""
        if body is None:
            return ''

        content = []
        in_list = False
        list_type = None

        for elem in body:
            tag = elem.tag.replace('{' + NAMESPACES['w'] + '}', '')

            if tag == 'p':
                para_content, para_style = self._process_paragraph(elem)

                # Handle lists
                numPr = elem.find('.//w:numPr', NAMESPACES)
                if numPr is not None:
                    numId = numPr.find('w:numId', NAMESPACES)
                    if numId is not None:
                        new_list_type = 'enumerate' if int(numId.get('{' + NAMESPACES['w'] + '}val', '0')) % 2 == 1 else 'itemize'
                        if not in_list:
                            content.append(f'\\begin{{{new_list_type}}}')
                            in_list = True
                            list_type = new_list_type
                        content.append(f'    \\item {para_content}')
                        continue

                # End list if we were in one
                if in_list:
                    content.append(f'\\end{{{list_type}}}')
                    in_list = False
                    list_type = None

                # Handle headings
                if para_style:
                    if para_style.startswith('Heading'):
                        level = int(para_style[-1]) if para_style[-1].isdigit() else 1
                        section_cmd = self._get_section_command(level)
                        content.append(f'{section_cmd}{{{para_content}}}')
                        continue
                    elif para_style == 'Title':
                        content.append(f'\\title{{{para_content}}}')
                        continue

                if para_content.strip():
                    content.append(para_content + '\n')

            elif tag == 'tbl':
                if in_list:
                    content.append(f'\\end{{{list_type}}}')
                    in_list = False
                content.append(self._process_table(elem))

        # Close any open list
        if in_list:
            content.append(f'\\end{{{list_type}}}')

        return '\n'.join(content)

    def _process_paragraph(self, para):
        """Process a paragraph element."""
        content = []
        style = None

        # Get paragraph style
        pPr = para.find('w:pPr', NAMESPACES)
        if pPr is not None:
            pStyle = pPr.find('w:pStyle', NAMESPACES)
            if pStyle is not None:
                style = pStyle.get('{' + NAMESPACES['w'] + '}val')

        for elem in para:
            tag = elem.tag.replace('{' + NAMESPACES['w'] + '}', '').replace('{' + NAMESPACES['m'] + '}', '')

            if tag == 'r':
                content.append(self._process_run(elem))
            elif tag == 'oMathPara' or tag == 'oMath':
                # Handle math
                latex_math = self.omml_converter.convert(elem)
                if elem.tag.endswith('oMathPara'):
                    content.append(f'\n\\[\n{latex_math}\n\\]\n')
                else:
                    content.append(f'${latex_math}$')
            elif tag == 'hyperlink':
                content.append(self._process_hyperlink(elem))

        return ''.join(content), style

    def _process_run(self, run):
        """Process a run element."""
        content = []
        formatting = {'bold': False, 'italic': False, 'underline': False, 'strike': False}

        # Check formatting
        rPr = run.find('w:rPr', NAMESPACES)
        if rPr is not None:
            if rPr.find('w:b', NAMESPACES) is not None:
                formatting['bold'] = True
            if rPr.find('w:i', NAMESPACES) is not None:
                formatting['italic'] = True
            if rPr.find('w:u', NAMESPACES) is not None:
                formatting['underline'] = True
            if rPr.find('w:strike', NAMESPACES) is not None:
                formatting['strike'] = True

        for elem in run:
            tag = elem.tag.replace('{' + NAMESPACES['w'] + '}', '').replace('{' + NAMESPACES['m'] + '}', '')

            if tag == 't':
                text = elem.text or ''
                text = self._escape_latex_text(text)
                content.append(text)
            elif tag == 'drawing':
                content.append(self._process_drawing(elem))
            elif tag == 'oMath':
                latex_math = self.omml_converter.convert(elem)
                content.append(f'${latex_math}$')

        result = ''.join(content)

        # Apply formatting
        if formatting['strike']:
            result = f'\\sout{{{result}}}'
        if formatting['underline']:
            result = f'\\underline{{{result}}}'
        if formatting['italic']:
            result = f'\\textit{{{result}}}'
        if formatting['bold']:
            result = f'\\textbf{{{result}}}'

        return result

    def _escape_latex_text(self, text):
        """Escape special LaTeX characters in regular text."""
        # Order matters - backslash must be first
        replacements = [
            ('\\', r'\textbackslash{}'),
            ('&', r'\&'),
            ('%', r'\%'),
            ('$', r'\$'),
            ('#', r'\#'),
            ('_', r'\_'),
            ('{', r'\{'),
            ('}', r'\}'),
            ('~', r'\textasciitilde{}'),
            ('^', r'\textasciicircum{}'),
        ]
        for old, new in replacements:
            text = text.replace(old, new)
        return text

    def _process_drawing(self, drawing):
        """Process a drawing element (image)."""
        # Find the image reference
        blip = drawing.find('.//a:blip', NAMESPACES)
        if blip is not None:
            embed = blip.get('{' + NAMESPACES['r'] + '}embed')
            if embed and embed in self.relationships:
                image_path = self.relationships[embed]
                image_name = os.path.basename(image_path)
                return f'\n\\begin{{figure}}[htbp]\n    \\centering\n    \\includegraphics[width=0.8\\textwidth]{{{self.images_dir}/{image_name}}}\n    \\caption{{Image}}\n\\end{{figure}}\n'
        return ''

    def _process_hyperlink(self, hyperlink):
        """Process a hyperlink element."""
        content = []
        for run in hyperlink.findall('w:r', NAMESPACES):
            content.append(self._process_run(run))

        text = ''.join(content)
        r_id = hyperlink.get('{' + NAMESPACES['r'] + '}id')

        if r_id and r_id in self.relationships:
            url = self.relationships[r_id]
            return f'\\href{{{url}}}{{{text}}}'
        return text

    def _process_table(self, table):
        """Process a table element."""
        rows = table.findall('.//w:tr', NAMESPACES)
        if not rows:
            return ''

        # Count columns
        first_row_cells = rows[0].findall('.//w:tc', NAMESPACES)
        num_cols = len(first_row_cells)

        latex_rows = []
        for row in rows:
            cells = row.findall('.//w:tc', NAMESPACES)
            cell_contents = []
            for cell in cells:
                cell_text = []
                for para in cell.findall('.//w:p', NAMESPACES):
                    para_content, _ = self._process_paragraph(para)
                    cell_text.append(para_content)
                cell_contents.append(' '.join(cell_text))
            latex_rows.append(' & '.join(cell_contents) + ' \\\\')

        col_spec = '|' + 'c|' * num_cols
        table_content = '\n    '.join(latex_rows)

        return f'''
\\begin{{table}}[htbp]
    \\centering
    \\begin{{tabular}}{{{col_spec}}}
    \\hline
    {table_content}
    \\hline
    \\end{{tabular}}
    \\caption{{Table}}
\\end{{table}}
'''

    def _get_section_command(self, level):
        """Get the appropriate section command for the heading level."""
        commands = {
            1: '\\section',
            2: '\\subsection',
            3: '\\subsubsection',
            4: '\\paragraph',
            5: '\\subparagraph',
        }
        return commands.get(level, '\\paragraph')

    def _generate_latex_document(self, content):
        """Generate the complete LaTeX document."""
        preamble = r'''\documentclass[12pt,a4paper]{article}

% Encoding and fonts
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% Math packages
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{mathtools}

% Graphics
\usepackage{graphicx}
\usepackage{float}

% Tables
\usepackage{booktabs}
\usepackage{array}

% Links
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
}

% Text formatting
\usepackage{ulem}  % For strikethrough with \sout

% Page layout
\usepackage{geometry}
\geometry{margin=1in}

'''

        document = preamble + '\\begin{document}\n\n' + content + '\n\\end{document}\n'
        return document


def main():
    parser = argparse.ArgumentParser(
        description='Convert DOCX files to LaTeX format with math support'
    )
    parser.add_argument('input', help='Input DOCX file')
    parser.add_argument('output', help='Output LaTeX file')
    parser.add_argument('--images-dir', default='images',
                        help='Directory to extract images (default: images)')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)

    converter = DocxToLatexConverter(args.input, args.images_dir)
    latex_content = converter.convert()

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(latex_content)

    print(f"Successfully converted '{args.input}' to '{args.output}'")
    if converter.extracted_images:
        print(f"Extracted {len(converter.extracted_images)} images to '{args.images_dir}/'")


if __name__ == '__main__':
    main()
