import { useSelector } from 'react-redux';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { ScrollArea } from '@/components/ui/scroll-area';
import { PreviewCard } from '@/components/PreviewCard';
import { RootState } from '@/store/store';
import { Link } from 'lucide-react';

export default function Links() {
  const { currentUrl, sessionId } = useSelector((state: RootState) => state.url);
  const { data: generateData, isLoading } = useSelector((state: RootState) => ({
    data: state.url.links,
    isLoading: state.url.isGenerating,
  }));
  const uniqueLinks = Array.from(new Set(generateData))

  const showLoading =  (currentUrl && !generateData);
  const hasLinks = generateData && generateData.length > 0;

  return (
    <div className="space-y-6 lg:space-y-0 lg:grid lg:grid-cols-2 lg:gap-6 w-full">
    {/* Preview card section */}
    <div className="w-full">
        <PreviewCard url={currentUrl} />
    </div>

    {/* Links section */}
    <Card className="w-full mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Link className="h-5 w-5" />
          Found Links
        </CardTitle>
      </CardHeader>
      <CardContent>
        {showLoading ? (
          <div className="space-y-3">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-5/6" />
          </div>
        ) : !hasLinks ? (
          <p className="text-muted-foreground italic">
            {currentUrl ? 'No links found' : 'Links will appear here'}
          </p>
        ) : (
          <ScrollArea className="h-[300px] pr-4">
            <ul className="space-y-2">
              {uniqueLinks.map((link, index) => (
                <li key={`${link}-${index}`}>
                  <a
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:text-blue-700 hover:underline break-all"
                  >
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </ScrollArea>
        )}
      </CardContent>
    </Card>
  </div>
  );
}