from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Frame, PageTemplate, Flowable
)
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from datetime import datetime
import logging
import json

class PDFGenerator:
    """Class to handle PDF generation for class schedules"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Initialize custom paragraph styles"""
        self.custom_styles = {
            'subtitle': ParagraphStyle(
                'Subtitle',
                parent=self.styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                spaceAfter=20,
                textColor=colors.HexColor('#666666')
            ),
            'class_code': ParagraphStyle(
                'ClassCode',
                parent=self.styles['Normal'],
                leading=12
            ),
            'special_cell': ParagraphStyle(
                'SpecialCell',
                parent=self.styles['Normal'],
                fontSize=10,
                alignment=TA_CENTER,
                textColor=colors.black,
                leading=12
            ),
            'lunch_break': ParagraphStyle(
                'LunchBreak',
                parent=self.styles['Normal'],
                textColor=colors.gray,
                fontSize=8,
                alignment=TA_CENTER,
                leading=10,
                spaceBefore=0,
                spaceAfter=0
            ),
            'notes': ParagraphStyle(
                'Notes',
                parent=self.styles['Normal'],
                fontSize=8,
                alignment=TA_LEFT,
                spaceBefore=15,
                textColor=colors.HexColor('#666666')
            )
        }

    def generate_qr_code(self, data):
        """Generate QR code for document metadata"""
        qr_code = qr.QrCodeWidget(data)
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        drawing = Drawing(45, 45, transform=[45./width, 0, 0, 45./height, 0, 0])
        drawing.add(qr_code)
        return drawing

    def create_header_footer(self, canvas, doc):
        """Create header and footer for each page"""
        canvas.saveState()
        width, height = landscape(A4)
        
        # Watermark
        canvas.setFont('Helvetica-Bold', 60)
        canvas.setFillColor(colors.Color(0, 0, 0, alpha=0.1))
        canvas.translate(width/2, height/2)
        canvas.rotate(45)
        canvas.drawCentredString(0, 0, "Cahier de Texte")
        canvas.rotate(-45)
        canvas.translate(-width/2, -height/2)
        
        # Header
        current_date = datetime.now().strftime("%Y-%m-%d")
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(colors.black)
        canvas.drawString(
            doc.leftMargin,
            height - doc.topMargin + 15,
            f"Generated: {current_date}"
        )
        
        # QR Code
        qr_data = {
            "document": "Class Schedule",
            "date": current_date,
            "type": "Academic Document"
        }
        qr_drawing = self.generate_qr_code(json.dumps(qr_data))
        qr_drawing.drawOn(
            canvas,
            width - doc.rightMargin - 45,
            height - doc.topMargin
        )
        
        # Footer
        canvas.setFont('Helvetica', 8)
        canvas.drawString(
            doc.leftMargin,
            doc.bottomMargin - 15,
            "Academic Institution"
        )
        canvas.drawRightString(
            width - doc.rightMargin,
            doc.bottomMargin - 15,
            f"Page {canvas.getPageNumber()}"
        )
        
        canvas.restoreState()

    def create_legend(self):
        """Create schedule legend"""
        legend_data = [
            ["Légende:", ""],
            ["⏰ Horaire régulier", "📚 Cours normal"],
            ["🍽️ Pause déjeuner", "📋 Notes spéciales"],
        ]
        
        legend_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#1B2631')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ])
        
        return Table(
            legend_data,
            colWidths=[3*cm, 3*cm],
            style=legend_style
        )

    def format_cell_content(self, content):
        """Format cell content with appropriate styling"""
        if not content:
            return ''
            
        if isinstance(content, str):
            content = content.strip()
            if '\n' in content:
                lines = content.split('\n')
                if lines[0].startswith('TCSF'):
                    return Paragraph(
                        f'''<para align='center'>
                            <font name="Helvetica-Bold" size="10">{lines[0]}</font>
                            <br/>
                            <font color="#666666" size="9">
                                {' '.join(lines[1:])}
                            </font>
                        </para>''',
                        self.custom_styles['class_code']
                    )
            return Paragraph(
                f'<para align="center">{content}</para>',
                self.styles['Normal']
            )
            
        if isinstance(content, dict) and content.get('type') in ['vacation', 'holiday', 'absence']:
            cell_type = content['type'].capitalize()
            return Paragraph(
                f'''<para align="center">
                    <b>{cell_type}</b><br/>{content.get("text", "")}
                </para>''',
                self.custom_styles['special_cell']
            )
            
        return content

    def create_table_style(self, table_data):
        """Create table styling including vacation cells"""
        base_style = [
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1B2631')),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B2631')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ]
        
        # Add alternating row colors
        base_style.extend([
            ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8F9F9'))
            for i in range(1, len(table_data), 2)
        ])
        
        return TableStyle(base_style)

    def generate_pdf(self, data, filename):
        """Generate PDF from schedule data"""
        try:
            logging.info("Starting PDF generation")
            
            if not data or len(data) < 2:
                raise ValueError("Insufficient data for PDF generation")
                
            # Setup document
            doc = SimpleDocTemplate(
                filename,
                pagesize=landscape(A4),
                rightMargin=1.5*cm,
                leftMargin=1.5*cm,
                topMargin=2*cm,
                bottomMargin=2*cm,
                title="Class Schedule",
                author="Academic System",
                subject="Weekly Schedule",
                keywords=["schedule", "academic", "classes"]
            )
            
            # Create page template
            content_frame = Frame(
                doc.leftMargin,
                doc.bottomMargin,
                doc.width,
                doc.height,
                id='content'
            )
            template = PageTemplate(
                id='basic',
                frames=[content_frame],
                onPage=self.create_header_footer
            )
            doc.addPageTemplates([template])
            
            # Generate content
            story = []
            
            # Add subtitle
            current_week = datetime.now().strftime("Semaine du %d %B %Y")
            story.append(
                Paragraph(current_week, self.custom_styles['subtitle'])
            )
            
            # Process table data
            table_data = self._process_table_data(data)
            
            # Create and style table
            col_widths = self._calculate_column_widths(
                doc.width,
                len(table_data[0])
            )
            table = Table(table_data, colWidths=col_widths)
            table.setStyle(self.create_table_style(table_data))
            
            story.append(table)
            story.append(Spacer(1, 10))
            story.append(self.create_legend())
            
            # Add notes
            notes = """Notes: 
            • Les horaires sont susceptibles de modifications
            • En cas d'absence, veuillez prévenir l'administration
            • Consultez régulièrement les mises à jour du planning"""
            story.append(
                Paragraph(notes, self.custom_styles['notes'])
            )
            
            # Build PDF
            doc.build(story)
            logging.info("PDF generation completed successfully")
            
        except Exception as e:
            logging.error(f"Error in generate_pdf: {str(e)}", exc_info=True)
            raise

    def _process_table_data(self, data):
        """Process and format table data"""
        table_data = []
        
        # Add header row
        header_row = data[1]
        num_columns = len(header_row)
        table_data.append([
            self.format_cell_content(cell) for cell in header_row
        ])
        
        # Process remaining rows
        for row in data[2:]:
            # Ensure correct number of columns
            row = row[:num_columns] if len(row) > num_columns else row + [''] * (num_columns - len(row))
            styled_row = []
            
            for i, cell in enumerate(row):
                if i == 0:  # Time column
                    styled_row.append(self.format_cell_content(cell))
                elif isinstance(cell, dict) and cell.get('type') in ['vacation', 'holiday', 'absence']:
                    styled_row.append(self.format_cell_content(cell))
                elif cell and "Pause Déjeuner" in str(cell):
                    styled_row.append(
                        Paragraph(
                            f'<para align="center">{cell}</para>',
                            self.custom_styles['lunch_break']
                        )
                    )
                else:
                    styled_row.append(self.format_cell_content(cell))
                    
            table_data.append(styled_row)
            
        return table_data

    def _calculate_column_widths(self, total_width, num_columns):
        """Calculate column widths for the table"""
        time_col_width = total_width * 0.15  # 15% for time column
        remaining_width = total_width - time_col_width
        other_col_width = remaining_width / (num_columns - 1)
        
        return [time_col_width] + [other_col_width] * (num_columns - 1)

# Usage example:
if __name__ == "__main__":
    try:
        generator = PDFGenerator()
        schedule_data = [
            ["Cahier de Texte - Class A (Level 1 - 2024)"],
            ["Horaire", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"],
            # Add your schedule data here
        ]
        generator.generate_pdf(schedule_data, "class_schedule.pdf")
    except Exception as e:
        logging.error(f"Failed to generate PDF: {e}", exc_info=True)