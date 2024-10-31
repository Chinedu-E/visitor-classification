import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Question as QuestionType } from "@/store/types";
import { Card, CardContent } from "@/components/ui/card";

interface QuestionItemProps {
  question: QuestionType;
  index: number;
  value: string;
  onChange: (value: string) => void;
}

export function QuestionItem({ question, index, value, onChange }: QuestionItemProps) {
    console.log(question)
  const isMultipleChoice = question.options.length > 0;

  return (
    <Card className="border-none shadow-none">
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <h3 className="text-lg font-semibold">
            Question {index + 1}
          </h3>
          <p className="text-gray-700 dark:text-gray-300">{question.question}</p>
        </div>

        {isMultipleChoice ? (
          <RadioGroup
            value={value}
            onValueChange={onChange}
            className="space-y-3"
          >
            {question.options.map((option, optionIndex) => (
              <div key={optionIndex} className="flex items-center space-x-2">
                <RadioGroupItem 
                  value={option} 
                  id={`q${index}-option${optionIndex}`}
                />
                <Label 
                  htmlFor={`q${index}-option${optionIndex}`}
                  className="text-sm font-normal cursor-pointer"
                >
                  {option}
                </Label>
              </div>
            ))}
          </RadioGroup>
        ) : (
          <Input
            placeholder="Type your answer here..."
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="max-w-md"
          />
        )}
      </CardContent>
    </Card>
  );
}