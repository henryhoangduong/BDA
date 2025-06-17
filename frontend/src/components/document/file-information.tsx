import React from 'react'
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet'
import { useQuery } from '@tanstack/react-query'
import { ingestionByIdQueryFn } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import PDF from '../../assets/files/PDF.svg'

import { ChunkViewer } from './chunk-viewer'
import { Separator } from '@/components/ui/separator'
import ParsingStatus from './parsing-status'

interface Props {
  trigger: React.ReactNode
  doc_id: string
}
const FileInformation = ({ trigger, doc_id }: Props) => {
  const { data, isLoading } = useQuery({
    queryKey: ['ingestion-documents', doc_id],
    queryFn: () => ingestionByIdQueryFn(doc_id)
  })
  return (
    <Sheet>
      <SheetTrigger>{trigger}</SheetTrigger>
      <SheetContent className='overflow-y-auto flex flex-col items-start md:w-[70%] w-full'>
        <SheetHeader>
          <SheetTitle>File Information</SheetTitle>
          <SheetDescription>File information including name, chunk, size ...</SheetDescription>
        </SheetHeader>

        <Card className='w-[70%] max-w-[100vw]  mt-5'>
          <CardHeader>
            <CardTitle className='text-lg'>Document Metadata</CardTitle>
          </CardHeader>
          <CardContent>
            <dl className='grid grid-cols-2 gap-x-4 gap-y-4'>
              <dt className='font-medium text-sm text-gray-700'>ID: </dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.id}</dd>

              <dt className='font-medium text-sm text-gray-700'>Filename: </dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.metadata.filename}</dd>

              <dt className='font-medium text-sm text-gray-700'>Type: </dt>
              {/* <dd className='text-sm font-semibold text-muted-foreground'>{data?.metadata.type == '.pdf'}</dd> */}
              <img src={PDF} alt='' className='w-6' />

              <dt className='font-medium text-sm text-gray-700'>Chunk: </dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.metadata.chunk_number}</dd>

              <dt className='font-medium text-sm text-gray-700'>Parsing Status: </dt>
              <ParsingStatus document_id={doc_id} />

              <dt className='font-medium text-sm text-gray-700'>Size: </dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.metadata.size}</dd>

              <dt className='font-medium text-sm text-gray-700'>Public URL: </dt>
              <a
                href={data?.metadata.file_path}
                target='_blank'
                rel='noopener noreferrer'
                className='text-sm font-semibold text-muted-foreground block w-full truncate hover:underline'
                title={data?.metadata.file_path} // Tooltip on hover
              >
                {data?.metadata.file_path}
              </a>

              <dt className='font-medium text-sm text-gray-700'>Total Chunks: </dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.documents.length}</dd>

              <dt className='font-medium text-sm text-gray-700'>Page Numbers: </dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.metadata.page_number}</dd>
            </dl>
          </CardContent>
        </Card>
        <Separator className='mt-5' />
        <div className='mt-5'>
          <ChunkViewer documents={data?.documents || []} />
        </div>
      </SheetContent>
    </Sheet>
  )
}

export default FileInformation
