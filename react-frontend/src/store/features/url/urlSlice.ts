import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Question, UserAnswer } from '@/store/types';

interface UrlState {
  currentUrl: string;
  sessionId: string | null;
  questions: Question[];
  userAnswers: UserAnswer[];
  isGenerating: boolean;
  error: string | null;
  links: string[];
}

const initialState: UrlState = {
  currentUrl: '',
  sessionId: null,
  questions: [],
  userAnswers: [],
  links: [],
  isGenerating: false,
  error: null,
};

const urlSlice = createSlice({
  name: 'url',
  initialState,
  reducers: {
    setCurrentUrl: (state, action: PayloadAction<string>) => {
      state.currentUrl = action.payload;
      state.questions = [];
      state.userAnswers = [];
      state.links = []
      state.error = null;
    },
    setSessionId: (state, action: PayloadAction<string>) => {
      state.sessionId = action.payload;
    },
    setLinks: (state, action: PayloadAction<string[]>) => {  // Added this reducer
        state.links = action.payload;
    },
    addQuestions: (state, action: PayloadAction<Question[]>) => {
      state.questions.push(...action.payload);
    },
    setUserAnswer: (state, action: PayloadAction<UserAnswer>) => {
      const existingAnswerIndex = state.userAnswers.findIndex(
        (ans) => ans.questionIndex === action.payload.questionIndex
      );
      
      if (existingAnswerIndex !== -1) {
        state.userAnswers[existingAnswerIndex] = action.payload;
      } else {
        state.userAnswers.push(action.payload);
      }
    },
    setGenerating: (state, action: PayloadAction<boolean>) => {
      state.isGenerating = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const {
  setCurrentUrl,
  setSessionId,
  addQuestions,
  setUserAnswer,
  setLinks,
  setGenerating,
  setError,
} = urlSlice.actions;
export default urlSlice.reducer;