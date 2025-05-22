import React, { useEffect } from 'react'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow
} from '@/components/ui/table'
import { Card, CardHeader } from '../ui/card'
import { ingestionQueryFn } from '@/lib/api'
import { useQuery } from '@tanstack/react-query'
import FileActions from './file-actions'
import { Switch } from '../ui/switch'
import { FileText } from 'lucide-react'

interface Props {
  uploadButton?: React.ReactNode
}

const DocumentTable = ({ uploadButton }: Props) => {
  const { data, isLoading } = useQuery({
    queryKey: ['ingestion-documents'],
    queryFn: ingestionQueryFn
  })

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
            return (
              <TableRow key={index}>
                <TableCell className='flex flex-row items-center gap-2 font-semibold text-left cursor-pointer'>
                  <FileText />
                  {item.metadata.filename}
                </TableCell>
                <TableCell className='text-center'>{item.metadata.chunk_number}</TableCell>
                <TableCell className='text-center'>{`${day}/${month}/${year}`}</TableCell>
                <TableCell className='text-center'>
                  <Switch checked={item.metadata.enabled} />
                </TableCell>
                <TableCell className='text-center'>{`${day}/${month}/${year}`}</TableCell>
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
