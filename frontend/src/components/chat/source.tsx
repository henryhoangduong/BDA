import React from 'react'
import { Badge } from '../ui/badge'
import { FileText } from 'lucide-react'

interface Source {
  file_name: string
}

interface SourcesProps {
  sources: Source[]
}
export const Sources: React.FC<SourcesProps> = ({ sources }) => {
  if (!sources || sources.length == 0) return null
  const uniqueSources = Array.from(new Set(sources.map((s) => s.file_name))).map((fileName) => ({
    file_name: fileName
  }))
  return (
    <div className='mt-2'>
      <div className='text-xs text-gray-500 mb-1'>Sources:</div>
      <div className='flex flex-wrap gap-2'>
        {uniqueSources.map((source, index) => {
          // Extract just the filename from the full path
          const fileName = source.file_name.split('/').pop() || source.file_name

          return (
            <Badge key={index} variant='secondary' className='flex items-center gap-1 text-xs py-1 px-2'>
              <FileText className='h-3 w-3' />
              {fileName}
            </Badge>
          )
        })}
      </div>
    </div>
  )
}
