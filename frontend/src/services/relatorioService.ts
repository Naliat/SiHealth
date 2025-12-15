const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'
export async function baixarRelatorioGeral(inicio: string, fim: string): Promise<void> {
  const url = `${API_BASE_URL}/relatorios/geral/pdf?inicio=${inicio}&fim=${fim}`
  
  const res = await fetch(url, {
    method: 'GET',
    headers: {
    },
  })

  if (!res.ok) {
    const error: any = new Error(`Falha ao baixar relatório: HTTP ${res.status}`)
    error.status = res.status
    throw error
  }

  const blob = await res.blob()
  
  const contentDisposition = res.headers.get('Content-Disposition')
  let nomeArquivo = `relatorio_geral_${inicio}_${fim}.pdf` 
  
  if (contentDisposition) {
    const match = contentDisposition.match(/filename="(.+)"/);
    if (match && match[1]) {
      nomeArquivo = match[1];
    }
  }

  const urlBlob = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = urlBlob
  link.setAttribute('download', nomeArquivo)
  document.body.appendChild(link)
  link.click()
  
  document.body.removeChild(link)
  window.URL.revokeObjectURL(urlBlob)
}