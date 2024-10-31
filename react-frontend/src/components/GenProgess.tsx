// src/components/GenProgress/GenProgress.tsx
import { useEffect, useState, useRef } from 'react';
import { useSelector } from 'react-redux';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Loader2 } from 'lucide-react';
import { RootState } from '@/store/store';
import { cn } from '@/lib/utils';

interface ProcessingStatus {
  processed: number;
  total: number;
}

export default function GenProgress() {
    const [progressValue, setProgressValue] = useState(0);
    const timerRef = useRef<NodeJS.Timeout | null>(null);
    const startTimeRef = useRef<number>(0);
    
    const { 
      links, 
      isGenerating, 
      questions, 
      error 
    } = useSelector((state: RootState) => state.url);
  
    // Handle the progress animation
    useEffect(() => {
      if (!isGenerating) {
        if (timerRef.current) {
          clearInterval(timerRef.current);
        }
        setProgressValue(0);
        return;
      }
  
      startTimeRef.current = Date.now();
      let lastProgress = 0;
  
      timerRef.current = setInterval(() => {
        const elapsedTime = Date.now() - startTimeRef.current;
        const duration = 20000; // 20 seconds
  
        // If questions are defined, complete the progress
        if (questions?.length > 0) {
          setProgressValue(100);
          if (timerRef.current) {
            clearInterval(timerRef.current);
          }
          return;
        }
  
        // Calculate progress based on time
        if (elapsedTime >= duration) {
          // Hold at 99% if questions aren't defined after 15 seconds
          setProgressValue(99);
          if (timerRef.current) {
            clearInterval(timerRef.current);
          }
        } else {
          // Smooth progression up to 99% over 15 seconds
          const progress = Math.min(99, (elapsedTime / duration) * 99);
          // Ensure progress only increases
          if (progress > lastProgress) {
            setProgressValue(progress);
            lastProgress = progress;
          }
        }
      }, 50); // Update every 50ms for smooth animation
  
      return () => {
        if (timerRef.current) {
          clearInterval(timerRef.current);
        }
      };
    }, [isGenerating, questions]);
  
    // Don't show if we haven't started
    if (!isGenerating && progressValue === 0) return null;
  
    const isComplete = progressValue === 100;
  
    return (
      <Card className="w-full mx-auto">
        <CardHeader>
          <CardTitle className="flex gap-2 items-center">
            <div className="flex items-center gap-2">
              {!isComplete && (
                <Loader2 className="h-4 w-4 animate-spin" />
              )}
              Generating Content
            </div>
            <p 
              className={cn(
                "italic text-sm truncate ml-auto",
                isComplete && "text-green-600 font-medium"
              )}
            >
              {isComplete 
                ? "Processing complete!" 
                : "(This might take a minute)"}
            </p>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Progress 
              value={progressValue}
              className="transition-all duration-500 ease-in-out"
            />
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>Processing content...</span>
              <span>{Math.round(progressValue)}%</span>
            </div>
          </div>
          
          {!isComplete && (
            <div className="text-sm text-muted-foreground animate-pulse">
              Analyzing and generating questions...
            </div>
          )}
        </CardContent>
      </Card>
    );
  }


