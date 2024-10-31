import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2 } from "lucide-react";
import { QuestionItem } from "./QuestionItem";
import { RootState } from "@/store/store";
import { setUserAnswer } from "@/store/features/url/urlSlice";

export default function Questions() {
  const dispatch = useDispatch();
  const { 
    questions, 
    userAnswers, 
    isGenerating, 
    error,
    currentUrl 
  } = useSelector((state: RootState) => state.url);

  // Auto-scroll to new questions as they come in
  useEffect(() => {
    if (questions.length > 0) {
      const lastQuestion = document.querySelector('[data-question]:last-child');
      lastQuestion?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }, [questions.length]);

  const handleAnswerChange = (questionIndex: number, value: string) => {
    dispatch(setUserAnswer({ questionIndex, answer: value }));
  };

  if (!currentUrl) return null;

  return (
    <Card className="w-full mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          Generated Questions
          {isGenerating && !error && (
            <Loader2 className="w-4 h-4 animate-spin ml-2" />
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {error &&  !questions? (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        ) : questions.length === 0 && isGenerating ? (
          <div className="text-center py-8 text-muted-foreground">
            <p>Questions will appear here as they're generated...</p>
          </div>
        ) : questions.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            <p>No questions could be generate :( try again please</p>
          </div>
        ) : (
            <div className="space-y-6">
              {questions.map((question, index) => (
                <div key={index} data-question>
                  <QuestionItem
                    question={question}
                    index={index}
                    value={userAnswers.find(a => a.questionIndex === index)?.answer || ''}
                    onChange={(value) => handleAnswerChange(index, value)}
                  />
                  {index < questions.length - 1 && (
                    <div className="h-px bg-border my-6" />
                  )}
                </div>
              ))}
              {isGenerating && (
                <div className="flex items-center justify-center py-4 text-sm text-muted-foreground">
                  <Loader2 className="w-4 h-4 animate-spin mr-2" />
                  Generating more questions...
                </div>
              )}
            </div>
        )}
      </CardContent>
    </Card>
  );
}
