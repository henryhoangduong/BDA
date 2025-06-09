import { ActiveTable } from 'active-table-react'
import { useQuery } from '@tanstack/react-query'
import { ingestionByIdQueryFn } from '@/lib/api'
import { Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
const DatasetPage = () => {
  const { data: chunkData, isLoading } = useQuery({
    queryKey: ['ingestion-documents', '40df50df-189d-4f94-91fc-4d8cb9966d1c'],
    queryFn: () => ingestionByIdQueryFn('40df50df-189d-4f94-91fc-4d8cb9966d1c')
  })
  const rows = chunkData?.documents.map((doc) => [doc.page_content, '', '']) ?? []

  // data: first element is header row, then each of your rows
  const data = [['Chunk', 'Question', 'Reference Answer'], ...rows]
  if (isLoading) return <Loader2 className='animate-spin' />
  return (
    <div className=' flex flex-col gap-2 items-center'>
      <header className='p-4 w-full shadow-sm mb-5'>
        <p className='font-medium text-2xl'>Dataset Creation</p>
      </header>
      <div className='p-6 flex flex-row items-start w-full'>
        <Button>
          <span className='text-sm font-light'>Create Dataset</span>
        </Button>
      </div>
      <ActiveTable
        data={data}
        headerStyles={{ default: { backgroundColor: '#d6d6d630' } }}
        tableStyle={{ position: 'relative', width: '90%', border: 'box-sizing' }}
      />
    </div>
  )
}

export default DatasetPage
