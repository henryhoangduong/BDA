import { useMutation, useQuery } from '@tanstack/react-query'
import { Badge } from '../ui/badge'
import { ingestionByIdQueryFn, parseDocMutationFn, getParsingTaskStatusByIdQueryFn } from '@/lib/api'
import { toast } from '@/hooks/use-toast'
import { useEffect, useState } from 'react'
import { Loader2 } from 'lucide-react'

const ParsingStatus = ({ document_id }: { document_id: string }) => {
  const [isParsing, setIsParsing] = useState(false)
  const [taskId, setTaskId] = useState<string | null>(null)

  const { mutate: parse, isPending } = useMutation({
    mutationFn: parseDocMutationFn
  })

  const {
    data: parseStatus,
    isLoading: isGettingParseStatus,
    refetch: refetchParseStatus
  } = useQuery({
    queryKey: ['parse-status', taskId],
    queryFn: () => getParsingTaskStatusByIdQueryFn(taskId!),
    enabled: Boolean(taskId),
    refetchInterval: (latestData) => {
      if (!latestData) return false
      return latestData?.status === 'PENDING' ? 5000 : false
    }
  })

  const { data, isLoading } = useQuery({
    queryKey: ['ingestion-documents', document_id],
    queryFn: () => ingestionByIdQueryFn(document_id)
  })

  const handleParsing = () => {
    parse(document_id, {
      onSuccess: (data) => {
        setIsParsing(true)
        setTaskId(data.task_id)
        toast({
          variant: 'default',
          title: 'Successful',
          description: 'Document is parsing'
        })
      },
      onError: (error: any) => {
        toast({
          variant: 'destructive',
          title: 'Error',
          description: error.message
        })
      }
    })
  }

  useEffect(() => {
    if (parseStatus?.status === 'SUCCESS') {
      setIsParsing(false)
    }
  }, [parseStatus])

  return (
    <>
      {isLoading && (
        <div className='flex items-center justify-center'>
          <Loader2 className='animate-spin' />
        </div>
      )}

      {data?.metadata.parsing_status === 'Unparsed' && !isParsing && (
        <div onClick={handleParsing} className='cursor-pointer'>
          <Badge variant='warning' className='w-max'>
            {data.metadata.parsing_status}
          </Badge>
        </div>
      )}
      {data?.metadata.parsing_status === 'FAILED' && !isParsing && (
        <div onClick={handleParsing} className='cursor-pointer'>
          <Badge variant='destructive' className='w-max'>
            {data.metadata.parsing_status}
          </Badge>
        </div>
      )}
      {data?.metadata.parsing_status === 'SUCCESS' && !isParsing && (
        <Badge variant='success' className='w-max'>
          {data.metadata.parsing_status}
        </Badge>
      )}

      {/* While parsing is in progress, show a “Pending” badge with spinner */}
      {isParsing && (
        <Badge variant='secondary' className='w-max gap-2'>
          <Loader2 className='animate-spin' size={16} />
          {'Pending'}
        </Badge>
      )}
    </>
  )
}

export default ParsingStatus
