import fitz


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Safely extract text from a Streamlit uploaded PDF file using PyMuPDF.

    Handles:
    - Streamlit UploadedFile objects
    - PDF byte streams
    - encrypted/protected PDFs
    - empty/scanned PDFs
    - page-level extraction errors
    """

    try:
        if uploaded_file is None:
            return ""

        # Streamlit UploadedFile works best with getvalue()
        file_bytes = uploaded_file.getvalue()

        if not file_bytes:
            return "[PDF_EXTRACTION_ERROR] Uploaded PDF file is empty."

        doc = fitz.open(stream=file_bytes, filetype="pdf")

        try:
            if doc.is_encrypted:
                # Try opening PDFs that have empty password protection
                unlocked = doc.authenticate("")
                if not unlocked:
                    doc.close()
                    return (
                        "[PDF_EXTRACTION_ERROR] This PDF is encrypted or password-protected. "
                        "Please upload an unlocked PDF."
                    )

            text_parts = []

            for page_number in range(len(doc)):
                try:
                    page = doc.load_page(page_number)
                    page_text = page.get_text("text")

                    if page_text:
                        text_parts.append(page_text)

                except Exception as page_error:
                    text_parts.append(
                        f"\n[PAGE_EXTRACTION_WARNING] Could not read page {page_number + 1}: {page_error}\n"
                    )

            doc.close()

            extracted_text = "\n".join(text_parts).strip()

            if not extracted_text:
                return (
                    "[PDF_EXTRACTION_ERROR] No readable text was found in this PDF. "
                    "The file may be scanned/image-based. OCR support is required for scanned PDFs."
                )

            return extracted_text

        except Exception as inner_error:
            try:
                doc.close()
            except Exception:
                pass

            return f"[PDF_EXTRACTION_ERROR] Could not extract text from PDF: {inner_error}"

    except Exception as error:
        return f"[PDF_EXTRACTION_ERROR] Could not process uploaded PDF: {error}"