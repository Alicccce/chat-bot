import PyPDF2



def merge_pdf(src_filenames, dest_filename):
    merger = PyPDF2.PdfMerger()

    for src_filename in src_filenames:
        merger.append(src_filename)

    merger.write(dest_filename)

src_filenames = ["pdf_file/numder13.pdf", "pdf_file/numder14.pdf"]
dest_filename = "pdf_file/merged.pdf"

merge_pdf(src_filenames, dest_filename)