import AnalyticSection from '@/components/document/analytic-section'
import DocumentManagement from '@/components/document/document-management'
const DocumentPage = () => {
  return (
    <div className='p-6 flex flex-col gap-2'>
      <AnalyticSection />
      <DocumentManagement />
    </div>
  )
}

export default DocumentPage
