import React from 'react'
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet'
import { useQuery } from '@tanstack/react-query'
import { ingestionByIdQueryFn } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'

import { ChunkViewer } from './chunk-viewer'
import { Separator } from '@/components/ui/separator'

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
      <SheetContent className='overflow-y-auto flex flex-col items-start'>
        <SheetHeader>
          <SheetTitle>File Information</SheetTitle>
          <SheetDescription>File information including name, chunk, size ...</SheetDescription>
        </SheetHeader>

        <Card className='w-full max-w-md  mt-5'>
          <CardHeader>
            <CardTitle className='text-lg'>Document Metadata</CardTitle>
          </CardHeader>
          <CardContent>
            <dl className='grid grid-cols-2 gap-x-4 gap-y-2'>
              <dt className='font-medium text-sm text-gray-700'>ID</dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.id}</dd>

              <dt className='font-medium text-sm text-gray-700'>Filename</dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.metadata.filename}</dd>

              <dt className='font-medium text-sm text-gray-700'>Type</dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.metadata.type}</dd>

              <dt className='font-medium text-sm text-gray-700'>Chunk #</dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.metadata.chunk_number}</dd>

              <dt className='font-medium text-sm text-gray-700'>Parsing Status</dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.metadata.parsing_status}</dd>

              <dt className='font-medium text-sm text-gray-700'>Size</dt>
              <dd className='text-sm font-semibold text-muted-foreground'>{data?.metadata.size}</dd>
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
