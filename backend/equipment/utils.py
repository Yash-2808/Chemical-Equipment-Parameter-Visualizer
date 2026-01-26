import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np

def generate_dataset_report(dataset, equipment_list, summary_data):
    """
    Generate a PDF report for a dataset
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20
    )
    
    # Build story
    story = []
    
    # Title
    story.append(Paragraph(f"Equipment Dataset Report", title_style))
    story.append(Paragraph(f"{dataset.name}", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    # Dataset Information
    story.append(Paragraph("Dataset Information", heading_style))
    
    dataset_info = [
        ['Field', 'Value'],
        ['Name', dataset.name],
        ['File Name', dataset.file_name],
        ['Upload Date', str(dataset.upload_date)],
        ['Total Equipment Count', str(dataset.total_count)],
        ['Average Flowrate', f"{dataset.avg_flowrate:.2f}" if dataset.avg_flowrate else 'N/A'],
        ['Average Pressure', f"{dataset.avg_pressure:.2f}" if dataset.avg_pressure else 'N/A'],
        ['Average Temperature', f"{dataset.avg_temperature:.2f}" if dataset.avg_temperature else 'N/A'],
    ]
    
    info_table = Table(dataset_info, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 20))
    
    # Type Distribution
    if summary_data and 'type_distribution' in summary_data:
        story.append(Paragraph("Equipment Type Distribution", heading_style))
        
        type_dist_data = [['Equipment Type', 'Count']]
        for eq_type, count in summary_data['type_distribution'].items():
            type_dist_data.append([eq_type, str(count)])
        
        type_table = Table(type_dist_data, colWidths=[3*inch, 1*inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(type_table)
        story.append(Spacer(1, 20))
    
    # Statistical Summary
    if summary_data and 'statistics' in summary_data:
        story.append(Paragraph("Statistical Summary", heading_style))
        
        stats = summary_data['statistics']
        stats_data = [
            ['Parameter', 'Average', 'Minimum', 'Maximum'],
            ['Flowrate', f"{stats['flowrate']['avg']:.2f}", f"{stats['flowrate']['min']:.2f}", f"{stats['flowrate']['max']:.2f}"],
            ['Pressure', f"{stats['pressure']['avg']:.2f}", f"{stats['pressure']['min']:.2f}", f"{stats['pressure']['max']:.2f}"],
            ['Temperature', f"{stats['temperature']['avg']:.2f}", f"{stats['temperature']['min']:.2f}", f"{stats['temperature']['max']:.2f}"],
        ]
        
        stats_table = Table(stats_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 20))
    
    # Equipment Details (first 20 items)
    story.append(Paragraph("Equipment Details (Sample)", heading_style))
    
    equipment_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
    for equipment in equipment_list[:20]:  # Limit to first 20 items
        equipment_data.append([
            equipment.name,
            equipment.type,
            f"{equipment.flowrate:.2f}",
            f"{equipment.pressure:.2f}",
            f"{equipment.temperature:.2f}"
        ])
    
    equipment_table = Table(equipment_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
    equipment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8)
    ]))
    
    story.append(equipment_table)
    
    if len(equipment_list) > 20:
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"... and {len(equipment_list) - 20} more equipment items", styles['Italic']))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF bytes
    buffer.seek(0)
    return buffer.getvalue()

def generate_charts_pdf(dataset, summary_data):
    """
    Generate charts and save them as PDF bytes
    """
    buffer = io.BytesIO()
    
    with PdfPages(buffer) as pdf_pages:
        # Type Distribution Pie Chart
        if summary_data and 'type_distribution' in summary_data:
            fig, ax = plt.subplots(figsize=(8, 6))
            
            types = list(summary_data['type_distribution'].keys())
            counts = list(summary_data['type_distribution'].values())
            
            ax.pie(counts, labels=types, autopct='%1.1f%%', startangle=90)
            ax.set_title(f'Equipment Type Distribution - {dataset.name}')
            
            pdf_pages.savefig(fig, bbox_inches='tight')
            plt.close(fig)
        
        # Parameter Comparison Chart
        if summary_data and 'statistics' in summary_data:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            stats = summary_data['statistics']
            categories = ['Flowrate', 'Pressure', 'Temperature']
            averages = [stats['flowrate']['avg'], stats['pressure']['avg'], stats['temperature']['avg']]
            minimums = [stats['flowrate']['min'], stats['pressure']['min'], stats['temperature']['min']]
            maximums = [stats['flowrate']['max'], stats['pressure']['max'], stats['temperature']['max']]
            
            x = np.arange(len(categories))
            width = 0.25
            
            ax.bar(x - width, minimums, width, label='Minimum', alpha=0.8)
            ax.bar(x, averages, width, label='Average', alpha=0.8)
            ax.bar(x + width, maximums, width, label='Maximum', alpha=0.8)
            
            ax.set_xlabel('Parameters')
            ax.set_ylabel('Values')
            ax.set_title(f'Parameter Comparison - {dataset.name}')
            ax.set_xticks(x)
            ax.set_xticklabels(categories)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            pdf_pages.savefig(fig, bbox_inches='tight')
            plt.close(fig)
    
    buffer.seek(0)
    return buffer.getvalue()
