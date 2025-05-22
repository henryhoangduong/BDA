import React, { useState } from 'react'
import { Button } from '../ui/button'
import { PlusIcon } from 'lucide-react'
import { FileUploadModal } from './file-upload-document'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { ingestionMutationFn, ingestionQueryFn } from '@/lib/api'
import { toast } from '@/hooks/use-toast'
import DocumentTable from './document-table'

const DocumentManagement = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const { mutate, isPending } = useMutation({
    mutationFn: ingestionMutationFn
  })
  const queryClient = useQueryClient()
  const handleModal = () => {
    setIsModalOpen(!isModalOpen)
  }
  const onSubmit = async (values: FileList) => {
    if (isPending) return
    mutate(values, {
      onSuccess: () => {
        toast({
          variant: 'default',
          title: 'Success',
          description: 'File uploaded'
        })
        handleModal()
        queryClient.invalidateQueries({ queryKey: ['ingestion-documents'] })
      },
      onError: (error) => {
        toast({
          variant: 'destructive',
          title: 'Error',
          description: `Error uploading: ${error}`
        })
      }
    })
  }
  return (
    <>
      <DocumentTable
        uploadButton={
          <Button onClick={handleModal} className='w-max ml-auto'>
            <PlusIcon />
            <span>Upload Document</span>
          </Button>
        }
      />

      <FileUploadModal isOpen={isModalOpen} onClose={handleModal} isUploading={isPending} onUpload={onSubmit} />
    </>
  )
}

export default DocumentManagement
