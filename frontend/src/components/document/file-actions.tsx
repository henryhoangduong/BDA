import { Button } from '@/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { ingestionDeleteMutationFn } from '@/lib/api'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Loader2, Trash2Icon } from 'lucide-react'
import { toast } from '@/hooks/use-toast'
interface Props {
  doc_id: string
}
const FileActions = ({ doc_id }: Props) => {
  const { mutate, isPending } = useMutation({
    mutationFn: ingestionDeleteMutationFn
  })
  const queryClient = useQueryClient()
  const onDelete = () => {
    if (isPending) return
    mutate([doc_id], {
      onSuccess: () => {
        toast({
          variant: 'default',
          description: `Document ${doc_id} deleted`
        })
        queryClient.invalidateQueries({
          queryKey: ['ingestion-documents']
        })
      },
      onError: () => {
        toast({
          variant: 'destructive',
          description: `Error deleting document ${doc_id}`
        })
      }
    })
  }
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant='outline'>Open</Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className='w-56'>
        <DropdownMenuItem onClick={onDelete} disabled={isPending}>
          {isPending ? <Loader2 className='animate-spin' /> : <Trash2Icon />}
          Delete
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

export default FileActions
