from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def number_to_words(num, join=True):
    '''Converts a number to words'''
    units = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    teens = ['', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    thousands = ['', 'Thousand', 'Million', 'Billion', 'Trillion', 'Quadrillion', 'Quintillion', 'Sextillion', 'Septillion', 'Octillion', 'Nonillion', 'Decillion', 'Undecillion', 'Duodecillion', 'Tredecillion', 'Quattuordecillion', 'Sexdecillion', 'Septendecillion', 'Octodecillion', 'Novemdecillion', 'Vigintillion']
    words = []
    if num == 0:
        words.append('Zero')
    else:
        num_str = '%d' % num
        num_len = len(num_str)
        groups = int((num_len + 2) / 3)
        num_str = num_str.zfill(groups * 3)
        for i in range(0, groups * 3, 3):
            h = int(num_str[i])
            t = int(num_str[i + 1])
            u = int(num_str[i + 2])
            g = int(groups - (i / 3 + 1))
            if h >= 1:
                words.append(units[h])
                words.append('Hundred')
            if t > 1:
                words.append(tens[t])
                if u >= 1:
                    words.append(units[u])
            elif t == 1:
                if u >= 1:
                    words.append(teens[u])
                else:
                    words.append(tens[t])
            else:
                if u >= 1:
                    words.append(units[u])
            if g >= 1 and (h + t + u) > 0:
                words.append(thousands[g])
    if join:
        return ' '.join(words)
    return words

def convert_to_text(number):
    '''Converts an integer to its equivalent text representation in Indian Rupees'''
    text = number_to_words(number)
    text = text + " Only"
    return text