import AnalyticSection from '@/components/document/analytic-section'
import DocumentManagement from '@/components/document/document-management'
const DocumentPage = () => {
  return (
    <div className=' flex flex-col gap-2'>
      <header className='p-4 w-full shadow-sm mb-5'>
        <p className='font-medium text-2xl'>Documents</p>
      </header>
      <div className='p-6 flex flex-col gap-6'>
        <AnalyticSection />
        <DocumentManagement />
      </div>
    </div>
  )
}

export default DocumentPage
