/**
 * v0 by Vercel.
 * @see https://v0.dev/t/ZwUgB7JLnFz
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card'
import { Document } from '@/types/document'
interface Props {
  documents: Document[]
}
export const ChunkViewer = ({ documents }: Props) => {
  return (
    <Card className='max-w-4xl'>
      <CardHeader>
        <CardTitle>Chunk Viewer</CardTitle>
        <CardDescription>View and copy your JSON data.</CardDescription>
      </CardHeader>
      <CardContent>
        {documents.map((doc) => {
          return (
            <pre className='bg-gray-100 p-4 mt-5 rounded-md text-sm font-mono dark:bg-gray-800 dark:text-gray-200 overflow-auto'>
              {JSON.stringify(doc, null, 2)}
            </pre>
          )
        })}
      </CardContent>
    </Card>
  )
}
