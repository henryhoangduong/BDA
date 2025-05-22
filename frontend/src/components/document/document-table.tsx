import React, { useEffect } from 'react'
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Card, CardHeader } from '../ui/card'
import { embeddingDocumentByIdMutationFn, ingestionQueryFn } from '@/lib/api'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import FileActions from './file-actions'
import { Switch } from '../ui/switch'
import { FileText } from 'lucide-react'
import FileInformation from './file-information'
import ParsingStatus from './parsing-status'
import { toast } from '@/hooks/use-toast'
interface Props {
  uploadButton?: React.ReactNode
}

const DocumentTable = ({ uploadButton }: Props) => {
  const { data, isLoading } = useQuery({
    queryKey: ['ingestion-documents'],
    queryFn: ingestionQueryFn
  })
  const { mutate, isPending } = useMutation({
    mutationFn: embeddingDocumentByIdMutationFn
  })
  const queryClient = useQueryClient()
  const handleEmbedding = (value: string) => {
    if (isPending) return

    mutate(value, {
      onSuccess: () => {
        toast({
          variant: 'default',
          title: 'Successsful',
          description: 'Document embedded'
        })
        queryClient.invalidateQueries({
          queryKey: ['ingestion-documents']
        })
      },
      onError: (error) => {
        toast({
          variant: 'destructive',
          title: 'Error',
          description: error.message
        })
      }
    })
  }
  return (
    <Card className='p-6'>
      <CardHeader>{uploadButton}</CardHeader>
      <Table>
        <TableCaption>A list of your documents</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className='w-[100px] text-left'>Name</TableHead>
            <TableHead className='text-center'>Chunk numbers</TableHead>
            <TableHead className='text-center'>Upload Date</TableHead>
            <TableHead className='text-center'>Enable</TableHead>
            <TableHead className='text-center'>Parsing Status</TableHead>
            <TableHead className='text-center'>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data?.map((item, index) => {
            const date = new Date(item.metadata.uploadedAt || '')
            const day = date.getDate() // 22
            const month = date.getMonth() + 1 // 5  (months are zero-indexed)
            const year = date.getFullYear()
            const raw = item.metadata.file_path
            const fsPath = raw.replace(/^.*(\/Users\/.*)$/, '$1')
            const fileUrl = `file://${raw}`

            return (
              <TableRow key={index}>
                <FileInformation
                  trigger={
                    <TableCell className='flex flex-row items-center gap-2 font-semibold text-left cursor-pointer hover:underline'>
                      <FileText />
                      {item.metadata.filename}
                    </TableCell>
                  }
                  doc_id={item.id}
                />

                <TableCell className='text-center'>{item.metadata.chunk_number}</TableCell>
                <TableCell className='text-center'>{`${day}/${month}/${year}`}</TableCell>
                <TableCell className='text-center'>
                  <Switch
                    onCheckedChange={() => {
                      if (item.metadata.enabled) return
                      handleEmbedding(item.id)
                    }}
                    checked={item.metadata.enabled}
                  />
                </TableCell>
                <TableCell className='text-center'>
                  <ParsingStatus status={(item.metadata.parsing_status as string) || ''} />
                </TableCell>
                <TableCell className='text-center'>
                  <FileActions />
                </TableCell>
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </Card>
  )
}

export default DocumentTable
