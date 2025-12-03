from io import BytesIO
from datetime import date
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak

class PDFService:
    def gerar_relatorio_gerencial(self, estoque: list, dispensacoes: list, inicio: date, fim: date) -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=landscape(A4),
            rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20
        )
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos Personalizados
        style_title = styles['Title']
        style_heading = styles['Heading2']
        style_cell = ParagraphStyle('CellStyle', parent=styles['Normal'], fontSize=8, leading=10)
        style_cell_warn = ParagraphStyle('CellWarn', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.red)

        # =========================================================
        # CABEÇALHO GERAL
        # =========================================================
        titulo = Paragraph(f"Relatório Gerencial do Sistema SiHealth", style_title)
        subtitulo = Paragraph(f"Período de Análise de Dispensação: {inicio.strftime('%d/%m/%Y')} a {fim.strftime('%d/%m/%Y')}", styles['Normal'])
        elements.append(titulo)
        elements.append(subtitulo)
        elements.append(Spacer(1, 20))

        # =========================================================
        # SEÇÃO 1: POSIÇÃO DE ESTOQUE ATUAL
        # =========================================================
        elements.append(Paragraph("1. Posição Atual de Estoque (Lotes Ativos)", style_heading))
        elements.append(Spacer(1, 10))

        headers_estoque = ["Medicamento / Princípio", "Tarja", "Lote / Fabr.", "Validade", "Qtd Atual", "Status"]
        data_estoque = [headers_estoque]
        total_itens_estoque = 0

        hoje = date.today()

        for item in estoque:
            # Formatação
            med_txt = f"<b>{item['nome_medicamento']}</b><br/><i>{item['principio_ativo'] or ''}</i>"
            lote_txt = f"<b>{item['lote']}</b><br/>{item['fabricante'] or ''}"
            validade_str = item['validade'].strftime("%d/%m/%Y")
            
            # Lógica de Status Visual para o PDF
            dias_venc = (item['validade'] - hoje).days
            status_txt = "OK"
            estilo_uso = style_cell

            if dias_venc < 0:
                status_txt = "VENCIDO"
                estilo_uso = style_cell_warn # Texto Vermelho
            elif dias_venc < 30:
                status_txt = "ALERTA"
            
            row = [
                Paragraph(med_txt, style_cell),
                Paragraph(item['tarja'] or "-", style_cell),
                Paragraph(lote_txt, style_cell),
                Paragraph(validade_str, estilo_uso),
                str(item['quantidade_atual']),
                Paragraph(status_txt, estilo_uso)
            ]
            data_estoque.append(row)
            total_itens_estoque += item['quantidade_atual']

        # Configura Tabela de Estoque (Verde)
        col_widths_est = [250, 80, 150, 80, 60, 80]
        t1 = Table(data_estoque, colWidths=col_widths_est, repeatRows=1)
        t1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.1, 0.5, 0.3)), # Verde Escuro
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (4, 0), (5, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(t1)
        elements.append(Paragraph(f"<b>Total em Estoque: {total_itens_estoque} unidades</b>", styles['Normal']))
        
        # QUEBRA DE PÁGINA (Para separar Estoque de Dispensação)
        elements.append(PageBreak())

        # =========================================================
        # SEÇÃO 2: HISTÓRICO DE DISPENSAÇÕES
        # =========================================================
        elements.append(Paragraph("2. Histórico de Dispensações (Período Selecionado)", style_heading))
        elements.append(Spacer(1, 10))

        headers_disp = ["Data/Hora", "CNS Paciente", "Medicamento", "Lote", "Qtd", "Tipo"]
        data_disp = [headers_disp]
        total_dispensado = 0

        for item in dispensacoes:
            dt = item['data_hora'].strftime("%d/%m %H:%M")
            med_txt = f"<b>{item['nome_medicamento']}</b>"
            lote_txt = item['lote']
            
            row = [
                Paragraph(dt, style_cell),
                Paragraph(item['cns_paciente'], style_cell),
                Paragraph(med_txt, style_cell),
                Paragraph(lote_txt, style_cell),
                str(item['quantidade_dispensada']),
                Paragraph(item['tipo_saida'], style_cell)
            ]
            data_disp.append(row)
            total_dispensado += item['quantidade_dispensada']

        # Configura Tabela de Dispensação (Azul)
        col_widths_disp = [90, 100, 250, 100, 50, 110]
        t2 = Table(data_disp, colWidths=col_widths_disp, repeatRows=1)
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.2, 0.4, 0.6)), # Azul Escuro
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (4, 0), (4, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(t2)
        elements.append(Paragraph(f"<b>Total Dispensado: {total_dispensado} unidades</b>", styles['Normal']))

        doc.build(elements)
        buffer.seek(0)
        return buffer