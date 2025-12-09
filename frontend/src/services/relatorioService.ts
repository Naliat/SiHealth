import type {
  DashboardDispensacaoPorMes,
  DashboardItemCritico,
  DashboardMetrics,
  DashboardTopMedication,
} from './dashboardService'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

export interface RelatorioData {
  metrics: DashboardMetrics
  topMedications: DashboardTopMedication[]
  dispensacoesPorMes: DashboardDispensacaoPorMes[]
  proximosAVencer: DashboardItemCritico[]
  baixaQuantidade: DashboardItemCritico[]
}

// Função para converter hex -> RGB
function hexToRgb(hex: string): number[] {
  const bigint = parseInt(hex.replace('#', ''), 16)
  return [(bigint >> 16) & 255, (bigint >> 8) & 255, bigint & 255]
}

export function gerarRelatorioPDF(data: RelatorioData): void {
  const doc = new jsPDF()

  // Configuração de cores
  const primaryColor = hexToRgb('#1976D2')
  const textColor = hexToRgb('#333333')

  let yPosition = 20

  // Cabeçalho
  doc.setFontSize(22)
  doc.setTextColor(...primaryColor)
  doc.text('Relatório de Dashboard - SiHealth', 14, yPosition)

  yPosition += 8
  doc.setFontSize(10)
  doc.setTextColor(100, 100, 100)
  doc.text(`Data de geração: ${new Date().toLocaleString('pt-BR')}`, 14, yPosition)

  yPosition += 15

  // Seção 1: Métricas principais
  doc.setFontSize(14)
  doc.setTextColor(...textColor)
  doc.text('Métricas Principais', 14, yPosition)

  yPosition += 10

  const metricsData = [
    ['Itens com Baixo Estoque', data.metrics.lowStockItems.toString()],
    ['Itens Próximos ao Vencimento', data.metrics.nearExpiryItems.toString()],
    ['Total de Itens em Estoque', data.metrics.totalStockItems.toString()],
    ['Dispensações Mensais', data.metrics.monthlyDispensations.toString()],
  ]

  autoTable(doc, {
    startY: yPosition,
    head: [['Métrica', 'Valor']],
    body: metricsData,
    theme: 'striped',
    headStyles: {
      fillColor: primaryColor,
      textColor: [255, 255, 255],
      fontStyle: 'bold',
    },
    styles: {
      fontSize: 10,
      cellPadding: 5,
    },
    columnStyles: {
      0: { cellWidth: 140 },
      1: { cellWidth: 40, halign: 'center' },
    },
  })

  yPosition = (doc as any).lastAutoTable.finalY + 15

  // Seção 2: Medicamentos mais retirados
  if (data.topMedications.length > 0) {
    doc.setFontSize(14)
    doc.setTextColor(...textColor)
    doc.text('Medicamentos Mais Retirados', 14, yPosition)

    yPosition += 5

    const topMedsData = data.topMedications.map(med => [
      med.nome,
      med.quantidade.toString(),
    ])

    autoTable(doc, {
      startY: yPosition,
      head: [['Medicamento', 'Quantidade']],
      body: topMedsData,
      theme: 'striped',
      headStyles: {
        fillColor: primaryColor,
        textColor: [255, 255, 255],
        fontStyle: 'bold',
      },
      styles: {
        fontSize: 10,
        cellPadding: 5,
      },
      columnStyles: {
        0: { cellWidth: 140 },
        1: { cellWidth: 40, halign: 'center' },
      },
    })

    yPosition = (doc as any).lastAutoTable.finalY + 15
  }

  if (yPosition > 240) {
    doc.addPage()
    yPosition = 20
  }

  // Seção 3: Dispensações por mês
  if (data.dispensacoesPorMes.length > 0) {
    doc.setFontSize(14)
    doc.setTextColor(...textColor)
    doc.text('Frequência de Dispensações por Mês', 14, yPosition)

    yPosition += 5

    const dispData = data.dispensacoesPorMes.map(item => [
      item.mes,
      item.quantidade.toString(),
    ])

    autoTable(doc, {
      startY: yPosition,
      head: [['Mês', 'Quantidade']],
      body: dispData,
      theme: 'striped',
      headStyles: {
        fillColor: primaryColor,
        textColor: [255, 255, 255],
        fontStyle: 'bold',
        halign: 'center',
      },
      styles: {
        fontSize: 10,
        cellPadding: 5,
      },
      columnStyles: {
        0: { cellWidth: 90, halign: 'center' },
        1: { cellWidth: 90, halign: 'center' },
      },
    })

    yPosition = (doc as any).lastAutoTable.finalY + 15
  }

  if (yPosition > 240) {
    doc.addPage()
    yPosition = 20
  }

  // Seção 4: Itens próximos ao vencimento
  if (data.proximosAVencer.length > 0) {
    doc.setFontSize(14)
    doc.setTextColor(...textColor)
    doc.text('Itens Próximos ao Vencimento', 14, yPosition)

    yPosition += 5

    const proxVencData = data.proximosAVencer.map(item => [
      item.nome,
      item.quantidade.toString(),
      item.lote,
      item.status,
    ])

    autoTable(doc, {
      startY: yPosition,
      head: [['Medicamento', 'Qtd', 'Lote', 'Status']],
      body: proxVencData,
      theme: 'striped',
      headStyles: {
        fillColor: primaryColor,
        textColor: [255, 255, 255],
        fontStyle: 'bold',
      },
      styles: {
        fontSize: 9,
        cellPadding: 4,
      },
      columnStyles: {
        0: { cellWidth: 70 },
        1: { cellWidth: 25, halign: 'center' },
        2: { cellWidth: 50, halign: 'center' },
        3: { cellWidth: 35, halign: 'center' },
      },
      didParseCell: data => {
        if (data.column.index === 3 && data.cell.section === 'body') {
          const status = data.cell.raw as string

          if (status === 'Vencido') {
            data.cell.styles.fillColor = [254, 226, 226] // #fee2e2
            data.cell.styles.textColor = [185, 28, 28]   // #b91c1c
          } else if (status === 'Próx. Venc.') {
            data.cell.styles.fillColor = [254, 243, 199] // #fef3c7
            data.cell.styles.textColor = [180, 83, 9]    // #b45309
          }
        }
      },
    })

    yPosition = (doc as any).lastAutoTable.finalY + 15
  }

  if (yPosition > 240) {
    doc.addPage()
    yPosition = 20
  }

  // Seção 5: Itens com baixa quantidade
  if (data.baixaQuantidade.length > 0) {
    doc.setFontSize(14)
    doc.setTextColor(...textColor)
    doc.text('Itens com Baixa Quantidade', 14, yPosition)

    yPosition += 5

    const baixaQtdData = data.baixaQuantidade.map(item => [
      item.nome,
      item.quantidade.toString(),
      item.lote,
    ])

    autoTable(doc, {
      startY: yPosition,
      head: [['Medicamento', 'Quantidade', 'Lote']],
      body: baixaQtdData,
      theme: 'striped',
      headStyles: {
        fillColor: primaryColor,
        textColor: [255, 255, 255],
        fontStyle: 'bold',
      },
      styles: {
        fontSize: 9,
        cellPadding: 4,
      },
      columnStyles: {
        0: { cellWidth: 90 },
        1: { cellWidth: 40, halign: 'center' },
        2: { cellWidth: 50, halign: 'center' },
      },
    })
  }

  // Rodapé
  const pageCount = doc.getNumberOfPages()
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i)
    doc.setFontSize(8)
    doc.setTextColor(150, 150, 150)
    doc.text(
      `Página ${i} de ${pageCount}`,
      doc.internal.pageSize.getWidth() / 2,
      doc.internal.pageSize.getHeight() - 10,
      { align: 'center' },
    )
    doc.text(
      'SiHealth - Sistema de Gerenciamento de Saúde',
      14,
      doc.internal.pageSize.getHeight() - 10,
    )
  }

  // Salvar
  const dataAtual = new Date().toISOString().split('T')[0]
  doc.save(`relatorio-dashboard-${dataAtual}.pdf`)
}
