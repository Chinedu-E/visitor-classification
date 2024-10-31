"use client"

import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Loader2 } from 'lucide-react';
import { useGenerateContentMutation } from '@/store/api';
import { setCurrentUrl, setSessionId, setLinks } from '@/store/features/url/urlSlice';
import { createSSEService } from '@/services/sseService';
import { AppDispatch } from '@/store/store';


export default function UrlInput() {
  const [url, setUrl] = useState('');
  const [inputError, setInputError] = useState('');
  const dispatch = useDispatch<AppDispatch>();
  
  const [generateContent, { isLoading }] = useGenerateContentMutation();

  const validateUrl = (input: string): boolean => {
    try {
      // Add https:// if not present
      const urlToTest = input.startsWith('http') ? input : `https://${input}`;
      new URL(urlToTest);
      return true;
    } catch {
      setInputError('Please enter a valid URL');
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setInputError('');

    if (!url.trim()) {
      setInputError('Please enter a URL');
      return;
    }

    if (!validateUrl(url)) {
      return;
    }

    const normalizedUrl = url.startsWith('http') ? url : `https://${url}`;
    dispatch(setCurrentUrl(normalizedUrl));
    
    try {
      const response = await generateContent(normalizedUrl).unwrap();
      dispatch(setSessionId(response.session_id));
      dispatch(setLinks(response.links));
      
      // Initialize SSE connection
      const sseService = createSSEService(dispatch);
      sseService.connect(response.session_id);
    } catch (error) {
        console.log(error);
      setInputError('Failed to analyze website. Please try again.');
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Enter Website URL</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <div className="relative">
              <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
                <span className="text-sm text-muted-foreground">https://</span>
              </div>
              <Input
                className="pl-[4.5rem]"
                placeholder="example.com"
                value={url}
                onChange={(e) => {
                  setUrl(e.target.value.replace(/^https?:\/\//, ''));
                  setInputError('');
                }}
                disabled={isLoading}
                aria-invalid={!!inputError}
                aria-describedby={inputError ? "url-error" : undefined}
              />
            </div>
            {inputError && (
              <p className="text-sm text-red-500" id="url-error">
                {inputError}
              </p>
            )}
          </div>
          <Button 
            type="submit" 
            className="w-[200px]"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              'Analyze Website'
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}