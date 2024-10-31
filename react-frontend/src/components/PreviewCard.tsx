import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { useGetPreviewImageQuery } from '@/store/api';

interface PreviewCardProps {
  url: string;
}

export function PreviewCard({ url }: PreviewCardProps) {
  const { data: previewData, isLoading, error } = useGetPreviewImageQuery(url, {
    skip: !url,
  });


  return (
    <Card className="w-full overflow-hidden">
      <CardContent className="p-0">
        {isLoading ? (
          <Skeleton className="w-full aspect-video" />
        ) : error ? (
          <div className="w-full aspect-video bg-muted flex items-center justify-center border-2 border-dashed border-gray-300">
            <p className="text-muted-foreground">Failed to load preview</p>
          </div>
        ) : previewData?.image ? (
          <img
            src={previewData.image}
            alt="Website preview"
            className="w-full aspect-video object-cover"
            loading="lazy"
          />
        ) : (
          <div className="w-full aspect-video bg-muted flex items-center justify-center border-2 border-dashed border-gray-300">
            <div className="text-center">
              <p className="text-muted-foreground">No preview available</p>
              <p className="text-sm text-muted-foreground mt-1">Image will appear here</p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}