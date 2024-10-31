import { AppDispatch } from '../store/store';
import { addQuestions, setError, setGenerating } from '../store/features/url/urlSlice';
import { SSEMessage } from '../store/types';

export class SSEService {
  private eventSource: EventSource | null = null;

  constructor(private dispatch: AppDispatch) {}

  connect(sessionId: string) {
    this.disconnect(); // Ensure any existing connection is closed
    
    this.eventSource = new EventSource(`http://127.0.0.1:5000/stream/${sessionId}`);
    this.dispatch(setGenerating(true));

    this.eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data.questions);
      
      if (data.questions) {
        this.dispatch(addQuestions(JSON.parse(data.questions)));
      }
      
      if (data.status === 'complete') {
        this.dispatch(setGenerating(false));
        this.disconnect();
      }
      
      if (data.error) {
        this.dispatch(setError(data.error));
        this.disconnect();
      }
    };

    this.eventSource.onerror = (e) => {
        console.log(e)
      this.dispatch(setError('Something went wrong, please try again.'));
      this.dispatch(setGenerating(false));
      this.disconnect();
    };
  }

  disconnect() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}

export const createSSEService = (dispatch: AppDispatch) => new SSEService(dispatch);