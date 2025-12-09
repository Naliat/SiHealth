declare module 'jspdf-autotable' {
  import type { jsPDF } from 'jspdf'

  export interface RowInput {
    [key: string]: any
  }

  export interface UserOptions {
    includeHiddenHtml?: boolean
    useCss?: boolean
    theme?: 'striped' | 'grid' | 'plain'
    startY?: number | false
    margin?: number | { top?: number, right?: number, bottom?: number, left?: number }
    pageBreak?: 'auto' | 'avoid' | 'always'
    rowPageBreak?: 'auto' | 'avoid'
    tableWidth?: 'auto' | 'wrap' | number
    showHead?: 'everyPage' | 'firstPage' | 'never'
    showFoot?: 'everyPage' | 'lastPage' | 'never'
    tableLineWidth?: number
    tableLineColor?: number | number[]

    head?: RowInput[]
    body?: RowInput[]
    foot?: RowInput[]

    headStyles?: Partial<CellDef>
    bodyStyles?: Partial<CellDef>
    footStyles?: Partial<CellDef>
    alternateRowStyles?: Partial<CellDef>
    columnStyles?: { [key: string]: Partial<CellDef> }
    styles?: Partial<CellDef>

    didParseCell?: (data: CellHookData) => void
    willDrawCell?: (data: CellHookData) => void
    didDrawCell?: (data: CellHookData) => void
    didDrawPage?: (data: any) => void
  }

  export interface CellDef {
    cellPadding: number
    fontSize: number
    font: string
    textColor: number | number[] | string
    fillColor: number | number[] | string
    lineWidth: number
    lineColor: number | number[] | string
    fontStyle: 'normal' | 'bold' | 'italic' | 'bolditalic'
    overflow: 'linebreak' | 'ellipsize' | 'visible' | 'hidden'
    valign: 'top' | 'middle' | 'bottom'
    halign: 'left' | 'center' | 'right' | 'justify'
    cellWidth: 'auto' | 'wrap' | number
    minCellHeight: number
    minCellWidth: number
  }

  export interface CellHookData {
    cell: Cell
    row: Row
    column: Column
    section: 'head' | 'body' | 'foot'
  }

  export interface Cell {
    raw: string | number
    text: string[]
    styles: Partial<CellDef>
    section: 'head' | 'body' | 'foot'
    x: number
    y: number
    width: number
    height: number
    textPos: { x: number, y: number }
  }

  export interface Row {
    index: number
    raw: RowInput
    cells: { [key: string]: Cell }
    section: 'head' | 'body' | 'foot'
    height: number
  }

  export interface Column {
    index: number
    dataKey: string | number
    width: number
  }

  export default function autoTable (doc: jsPDF, options: UserOptions): jsPDF
}
