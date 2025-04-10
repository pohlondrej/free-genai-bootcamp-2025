import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { firstValueFrom } from 'rxjs';
import { environment } from '@env/environment';
import { StudySessionsService, StudySession } from '../../../services/study-sessions.service';
import { ActivatedRoute, Router } from '@angular/router';
import { ReviewService } from '../../../services/review.service';
import { HttpClient } from '@angular/common/http';

interface VocabularyEntry {
  jp_audio: string;
  en_text: string;
}

interface VocabularyStage {
  stage_id: string;
  entries: VocabularyEntry[];
}

interface ComprehensionStage {
  stage_id: string;
  jp_audio: string;
  question: string;
  correct_answer: boolean;
}

interface RecallStage {
  stage_id: string;
  jp_audio: string;
  options: string[];
  incorrect_option: string;
}

interface QuizSession {
  session_id: number;
  en_intro_audio: string;
  en_outro_audio: string;
  vocabulary_stage: VocabularyStage;
  comprehension_stage: ComprehensionStage;
  recall_stage: RecallStage;
  current_stage: number;
  score: number;
}

@Component({
  selector: 'app-duoradio-game',
  standalone: false,
  templateUrl: './duoradio-game.component.html',
  styleUrls: ['./duoradio-game.component.scss']
})
export class DuoRadioGameComponent implements OnInit {
  session: QuizSession | null = null;
  currentStage = 0;
  isLoading = false;
  loadingMessage = '';
  readonly stageNames = ['Vocabulary', 'Comprehension', 'Recall'];
  
  // Vocabulary stage
  vocabularyEntries: VocabularyEntry[] = [];
  randomizedEntries: VocabularyEntry[] = [];
  selectedAudio: string | null = null;
  selectedText: VocabularyEntry | null = null;
  matchedPairs = new Set<string>();

  // Comprehension stage
  comprehensionAnswer: boolean | null = null;
  comprehensionAnswerSubmitted = false;
  comprehensionFeedback: { message: string; isCorrect: boolean } | null = null;

  // Recall stage
  correctRecalls = new Set<string>();

  // Study session
  studySession: StudySession | null = null;

  groupId: number = 0;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private studySessionsService: StudySessionsService,
    private reviewService: ReviewService,
    private http: HttpClient
  ) {
    console.log('DuoRadioGameComponent: Constructor called');
  }

  ngOnInit() {
    console.log('DuoRadioGameComponent: ngOnInit called');
    this.route.params.subscribe(params => {
      this.groupId = +params['groupId'];
      this.startNewSession();
    });
  }

  async startNewSession() {
    try {
      this.isLoading = true;
      this.loadingMessage = 'Starting a new study session...';

      // Start a core study session
      const studySession = await this.studySessionsService.startSession(this.groupId, 'duoradio').toPromise();
      if (!studySession) {
        throw new Error('Failed to create study session');
      }
      this.studySession = studySession;
      console.log('DuoRadioGameComponent: Study session started', this.studySession);

      this.loadingMessage = 'Preparing your personalized listening exercise...';
      const response = await firstValueFrom(
        this.http.post<QuizSession>(
          `http://localhost:8003/api/session/?session_id=${this.studySession.id}`,
          {}
        )
      );
      
      this.session = response;
      this.currentStage = 0;
      this.initializeVocabularyStage();
      this.playAudio(this.session.en_intro_audio);
    } catch (error) {
      console.error('Error starting session:', error);
    } finally {
      this.isLoading = false;
    }
  }

  private initializeVocabularyStage() {
    if (!this.session) return;
    
    this.vocabularyEntries = this.session.vocabulary_stage.entries;
    this.randomizedEntries = [...this.vocabularyEntries].sort(() => Math.random() - 0.5);
    this.matchedPairs.clear();
    this.selectedAudio = null;
    this.selectedText = null;
  }

  async playAudio(cacheKey: string) {
    const audio = new Audio(`http://localhost:8003/api/audio/${cacheKey}`);
    await audio.play();
  }

  toggleAudioSelection(audioKey: string) {
    this.selectedAudio = this.selectedAudio === audioKey ? null : audioKey;
    this.checkMatch();
  }

  toggleTextSelection(entry: VocabularyEntry) {
    this.selectedText = this.selectedText === entry ? null : entry;
    this.checkMatch();
  }

  private checkMatch() {
    if (!this.selectedAudio || !this.selectedText) return;

    if (this.selectedAudio === this.selectedText.jp_audio) {
      this.matchedPairs.add(this.selectedAudio);
    }

    this.selectedAudio = null;
    this.selectedText = null;
  }

  submitComprehensionAnswer() {
    if (!this.session || this.comprehensionAnswer === null) return;

    const isCorrect = this.comprehensionAnswer === this.session.comprehension_stage.correct_answer;
    this.comprehensionAnswerSubmitted = true;
    this.comprehensionFeedback = {
      message: isCorrect ? 'Correct! Well done!' : 'Not quite right. Keep practicing!',
      isCorrect
    };
  }

  selectRecallWord(word: string) {
    if (!this.session) return;

    if (word === this.session.recall_stage.incorrect_option) {
      this.correctRecalls.clear();
    } else {
      this.correctRecalls.add(word);
    }
  }

  nextStage() {
    if (!this.session) return;
    
    this.currentStage++;
    this.comprehensionAnswer = null;
    this.comprehensionAnswerSubmitted = false;
    this.comprehensionFeedback = null;
    this.correctRecalls.clear();
  }

  finishSession() {
    if (!this.session) return;
    
    this.currentStage = 3;
    this.playAudio(this.session.en_outro_audio);

    // End the study session
    if (this.studySession?.id) {
      this.studySessionsService.endSession(this.studySession.id).subscribe();
    }
  }

  backToStart() {
    // Navigate back to the main DuoRadio component using absolute path
    // Component will be destroyed and recreated when revisited
    this.router.navigate(['']);
  }

  playAgain() {
    // Clear only the essential state that might affect starting a new session
    this.session = null;
    this.studySession = null;
    this.isLoading = false;  // Reset loading state in case previous session had errors
    
    // Start a new session
    this.startNewSession();
  }
}
