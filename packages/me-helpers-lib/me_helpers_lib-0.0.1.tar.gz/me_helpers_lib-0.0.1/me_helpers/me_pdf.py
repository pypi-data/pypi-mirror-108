from PIL import Image
import PyPDF2
import os
import pandas as pd


def merge_pdfs(pdfs, output_pdf, remove_pdfs=False):
    output_pdf = PyPDF2.PdfFileWriter()
    open_pdfs = []
    for _pdf in pdfs:
        try:
            _x = open(_pdf, 'rb')
            open_pdfs.append(_x)
            x = PyPDF2.PdfFileReader(_x)
            output_pdf.appendPagesFromReader(x)
            if (x.getNumPages() % 2) != 0:
                output_pdf.addBlankPage()
        except Exception as e:
            print(e)

    with open(output_pdf, 'wb') as out_pdf:
        output_pdf.write(out_pdf)

    for y in open_pdfs:
        y.close()

    if remove_pdfs:
        for _pdf in pdfs:
            os.remove(_pdf)


def create_pdf_from_pngs(pngs, output_pdf):
    _pngs = list(map(_modify_rgba_to_rgb, pngs))
    _pngs[0].save(output_pdf, "PDF", resolution=100,
                  save_all=True, append_images=_pngs[1:])
    [os.remove(png) for png in pngs]


def _modify_rgba_to_rgb(png):
    rgba = Image.open(png)
    # white background
    rgb = Image.new('RGB', rgba.size, (255, 255, 255))
    # paste using alpha channel as mask
    rgb.paste(rgba, mask=rgba.split()[3])
    return rgb


def save_pdf(pdf, folder, name):
    path = os.path.join(folder, f'{name}.pdf')
    pdf.output(path)
    return path


def add_df_to_pdf(pdf, df, header, font_size=10, line_height_x=2.5):
    df = df.astype(str)
    columns = df.columns
    records = df.to_records(index=False)
    if header:
        header = df.columns.str.upper()
    else:
        header = []

    pdf.set_font("Times", size=font_size)
    line_height = pdf.font_size * line_height_x
    col_width = pdf.epw / len(df.columns)
    for datum in header:
        pdf.multi_cell(col_width, line_height, datum, border=1,
                       ln=3, max_line_height=pdf.font_size)
    pdf.ln(line_height)

    for row in records:
        for datum in row:
            pdf.multi_cell(col_width, line_height, datum, border=1,
                           ln=3, max_line_height=pdf.font_size)
        pdf.ln(line_height)
    return pdf


def add_lineSpace_to_pdf(pdf, y, ln):
    pdf.ln(ln)
    y += 5+ln
    return pdf, y


def add_date_to_pdf(pdf):
    pdf.set_font('helvetica', '', 12)
    _today = str(pd.Timestamp.today()).split('.')[0]
    today_w = pdf.get_string_width(_today)+6
    doc_w = pdf.w
    pdf.set_x(doc_w-today_w)
    pdf.cell(today_w, txt=_today, ln=True)
    return pdf


def add_title_to_pdf(pdf, title):
    pdf.set_font('helvetica', '', 22)
    pdf.cell(w=pdf.get_string_width(title)+6,
             txt=title, ln=True)
    return pdf
