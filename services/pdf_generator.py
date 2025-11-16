from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Frame,
    PageTemplate, Image, Flowable, NextPageTemplate, PageBreak
)
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.barcode import qr
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import logging
import io
import json
import math

# =============================================================================
# Styling and Formatting Functions (from your provided code)
# =============================================================================

def generate_qr_code(data):
    qr_code = qr.QrCodeWidget(data)
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    drawing = Drawing(45, 45, transform=[45.0/width, 0, 0, 45.0/height, 0, 0])
    drawing.add(qr_code)
    return drawing

def header_footer(canvas, doc):
    """Add header and footer to each page"""
    canvas.saveState()
    width, height = landscape(A4)
    
    # Header
    canvas.setFont('Helvetica-Bold', 10)
    canvas.setFillColor(colors.black)
    current_date = datetime.now().strftime("%Y-%m-%d")
    canvas.drawString(doc.leftMargin, height - doc.topMargin + 15, 
                     f"Generated: {current_date}")
    
    # Add QR Code to top right
    qr_data = {
        "document": "Class Schedule",
        "date": current_date,
        "type": "Academic Document"
    }
    qr_drawing = generate_qr_code(json.dumps(qr_data))
    qr_drawing.drawOn(canvas, width - doc.rightMargin - 45, 
                      height - doc.topMargin)
    
    # Footer
    canvas.setFont('Helvetica', 8)
    footer_text = ("Académie de la région de l'Oriental-Oujda => Délégation de Taourirt, "
                   "lyccé ALMARINYINE")
    canvas.drawString(doc.leftMargin, doc.bottomMargin - 15, footer_text)
    canvas.drawRightString(width - doc.rightMargin, doc.bottomMargin - 15,
                          f"Page {canvas.getPageNumber()}")
    
    canvas.restoreState()

def format_cell_content(content, styles):
    """
    Format cell content with improved styling.
      - For a plain string, center it.
      - For multiline text where the first line starts with "TCSF" or "TCLSHF",
        apply custom formatting.
      - For a dictionary indicating a vacation/holiday/absence, format accordingly.
      - For a dictionary with {"lunch": True}, return an empty Paragraph.
    """
    # Hide content for lunch marker.
    if isinstance(content, dict) and content.get("lunch", False):
        return Paragraph("", styles['Normal'])
    
    if content is None or content == '':
        return ''
        
    if isinstance(content, str):
        content = content.strip()
        if '\n' in content:
            lines = content.split('\n')
            if lines[0].startswith('TCSF') or lines[0].startswith('TCLSHF'):
                # Custom styling for class codes
                return Paragraph(
                    f'''<para align='center'>
                        <font name="Helvetica-Bold" size="10">{lines[0]}</font>
                        <br/>
                        <font color="#666666" size="9">{' '.join(lines[1:])}</font>
                    </para>''',
                    ParagraphStyle(
                        'ClassCode',
                        parent=styles['Normal'],
                        leading=12
                    )
                )
        return Paragraph(
            f'<para align="center">{content}</para>',
            styles['Normal']
        )
    elif isinstance(content, dict) and content.get('type') in ['vacation', 'holiday', 'absence']:
        cell_type = content.get('type').capitalize()  # e.g., "Vacation"
        return Paragraph(
            f'<para align="center">{content.get("text", "")}</para>',
            ParagraphStyle(
                'SpecialCell',
                parent=styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                textColor=colors.black,
                leading=12
            )
        )
    # If content is already a flowable, return it as is.
    return content

# =============================================================================
# Our Advanced PDF Code (with lunch row processing, splitting, merged cells)
# =============================================================================

def create_document(filename):
    """Initialize document with landscape A4 and proper margins/template."""
    page_width, page_height = landscape(A4)
    margins = {'left': 1.5*cm, 'right': 1.5*cm, 'top': 2*cm, 'bottom': 2*cm}
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4),
        rightMargin=margins['right'],
        leftMargin=margins['left'],
        topMargin=margins['top'],
        bottomMargin=margins['bottom'],
        title="Class Schedule",
        author="Academic System",
        subject="Weekly Schedule",
        keywords=["schedule", "academic", "classes"]
    )
    
    content_frame = Frame(
        margins['left'],
        margins['bottom'],
        page_width - (margins['left'] + margins['right']),
        page_height - (margins['top'] + margins['bottom']),
        id='content'
    )
    
    template = PageTemplate(
        id='basic',
        frames=[content_frame],
        onPage=header_footer
    )
    doc.addPageTemplates([template])
    return doc

def extract_schedule_data(data):
    """Extract title, header row, and content rows from data."""
    if len(data) < 3:
        raise ValueError("Insufficient data for schedule")
    title = data[0][0] if data[0] else ""
    header_row = data[1]
    content_rows = data[2:]
    return title, header_row, content_rows

def calculate_layout(header_row):
    """Calculate column widths based on header row count and page size."""
    page_width = landscape(A4)[0] - (1.5*cm + 1.5*cm)
    time_col_width = page_width * 0.15
    remaining_width = page_width - time_col_width
    day_columns = len(header_row) - 1
    other_col_width = remaining_width / day_columns if day_columns > 0 else remaining_width
    return {
        'col_widths': [time_col_width] + [other_col_width] * day_columns,
        'styles': getSampleStyleSheet()  # Use the stylesheet from reportlab
    }

def determine_global_vacation_columns(content_rows, header_row):
    """Scan all rows to record which columns have vacation/holiday/absence info."""
    global_vacation = {}
    for col_idx in range(len(header_row)):
        if col_idx == 0:
            continue
        for row in content_rows:
            cell = row[col_idx]
            if isinstance(cell, dict) and cell.get('type') in ['vacation', 'holiday', 'absence']:
                global_vacation[col_idx] = {'text': cell.get('text', ''), 'type': cell.get('type')}
                break
    return global_vacation

def process_lunch_rows(content_rows, remove=False):
    """
    Process rows containing "Pause Déjeuner".
      - If remove==False: Replace any such row with one where each cell is marked with {"lunch": True}
        (so that later the text is hidden and styled with a dark background).
      - If remove==True: Remove the row entirely.
    """
    new_rows = []
    for row in content_rows:
        if any("Pause Déjeuner" in str(cell) for cell in row):
            if remove:
                continue
            else:
                new_rows.append([{"lunch": True} for _ in row])
        else:
            new_rows.append(row)
    return new_rows

def create_schedule_table(header_row, content_rows, layout, global_vacation_columns=None):
    """
    Build the table data (with cell formatting, merged vacation/holiday cells,
    and special lunch row styling). If global_vacation_columns is provided, inject
    its info into the first content row.
    """
    # Use global vacation info if provided.
    if global_vacation_columns is not None:
        vacation_columns = global_vacation_columns.copy()
        if content_rows and isinstance(content_rows[0], list):
            for col_idx, vac_info in vacation_columns.items():
                content_rows[0][col_idx] = {'text': vac_info['text'], 'type': vac_info['type']}
    else:
        vacation_columns = {}
        for col_idx in range(len(header_row)):
            if col_idx == 0:
                continue
            for row in content_rows:
                cell = row[col_idx]
                if isinstance(cell, dict) and cell.get('type') in ['vacation', 'holiday', 'absence']:
                    vacation_columns[col_idx] = {'text': cell.get('text', ''), 'type': cell.get('type')}
                    break

    # Build formatted rows. The header row (first row) is processed separately.
    formatted_rows = [
        [format_cell_content(cell, layout['styles']) for cell in header_row]
    ]
    for row in content_rows:
        formatted_row = []
        for col_idx, cell in enumerate(row):
            if col_idx in vacation_columns:
                # For vacation/holiday columns, only show the content in the first row.
                if row is content_rows[0]:
                    formatted_row.append(format_cell_content(
                        {'text': vacation_columns[col_idx]['text'],
                         'type': vacation_columns[col_idx]['type']},
                        layout['styles']
                    ))
                else:
                    formatted_row.append('')
            else:
                formatted_row.append(format_cell_content(cell, layout['styles']))
        formatted_rows.append(formatted_row)
    
    table = Table(formatted_rows, colWidths=layout['col_widths'])
    
    # Define table style using the styling from your provided code.
    style = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#9fc5e8')),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9fc5e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        # Alternate row background for rows (starting at index 2)
        *[('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8F9F9'))
          for i in range(2, len(formatted_rows), 2)]
    ]
    
    # Apply dark background to any row marked as a lunch break.
    # (Note: header is row 0, content rows start at index 1)
    for idx, row in enumerate(content_rows, start=1):
        if isinstance(row[0], dict) and row[0].get("lunch", False):
            style.append(('BACKGROUND', (0, idx), (-1, idx), colors.darkgray))
            style.append(('TEXTCOLOR', (0, idx), (-1, idx), colors.whitesmoke))
    
    # Merge vacation/holiday cells vertically.
    for col_idx, vac_info in vacation_columns.items():
        style.extend([
            ('SPAN', (col_idx, 1), (col_idx, len(content_rows))),
            ('BACKGROUND', (col_idx, 1), (col_idx, len(content_rows)), colors.HexColor('#FFE5E5')),
            ('TEXTCOLOR', (col_idx, 1), (col_idx, len(content_rows)), colors.HexColor('#FF0000'))
        ])
    table.setStyle(TableStyle(style))
    return table

def split_table_data(content_rows):
    """Split content rows into two approximately equal halves."""
    half = len(content_rows) // 2
    first_half = content_rows[:half]
    second_half = content_rows[half:]
    return first_half, second_half

def generate_pdf(data, filename):
    """
    Generate PDF schedule.
      - For a single-page PDF, any row containing "Pause Déjeuner" is kept (its text is removed and styled with a dark background).
      - If the table is too large (i.e. splitting is required), the lunch break row is removed.
    Also applies merged vacation/holiday cell logic and our custom styling.
    """
    try:
        logging.info("Starting PDF generation with reportlab")
        doc = create_document(filename)
        title, header_row, content_rows = extract_schedule_data(data)
        layout = calculate_layout(header_row)
        global_vacation = determine_global_vacation_columns(content_rows, header_row)
        
        # First, try generating a single-page PDF.
        # Process lunch rows: mark them (do not remove)
        content_rows_single = process_lunch_rows(content_rows, remove=False)
        story = []
        # Use a subtitle style from our stylesheet
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=getSampleStyleSheet()['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#666666')
        )
        story.append(Paragraph(title, subtitle_style))
        try:
            table = create_schedule_table(header_row, content_rows_single, layout, global_vacation_columns=global_vacation)
            story.append(table)
            doc.build(story)
            logging.info("Successfully generated single-page PDF")
        except Exception as e:
            error_message = str(e)
            if "Flowable <Table" in error_message and "too large on page" in error_message:
                logging.info("Table too large, splitting into two separate pages (lunch row removed)...")
                # For split PDF, remove lunch break rows.
                content_rows_split = process_lunch_rows(content_rows, remove=True)
                first_half, second_half = split_table_data(content_rows_split)
                story = []
                story.append(Paragraph(f"{title} - Part 1", subtitle_style))
                table1 = create_schedule_table(header_row, first_half, layout, global_vacation_columns=global_vacation)
                story.append(table1)
                story.append(PageBreak())
                story.append(Paragraph(f"{title} - Part 2", subtitle_style))
                table2 = create_schedule_table(header_row, second_half, layout, global_vacation_columns=global_vacation)
                story.append(table2)
                doc.build(story)
                logging.info("Successfully generated split (two-page) PDF")
            else:
                raise e
    except Exception as e:
        logging.error(f"Error in generate_pdf: {str(e)}", exc_info=True)
        raise

