import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl } from '@angular/forms';
import { StudySessionsService, StudySession } from '../../../services/study-sessions.service';
import { ReviewService } from '../../../services/review.service';

interface GameSession {
  id: number;
  groupId: number;
  startTime: Date;
  correctCount: number;
  incorrectCount: number;
}

@Component({
  selector: 'app-flashcard-game',
  standalone: false,
  templateUrl: './flashcard-game.component.html',
  styleUrls: ['./flashcard-game.component.scss']
})
export class FlashcardGameComponent implements OnInit {
  groupId!: number;
  studySession: StudySession | null = null;
  session: GameSession | null = null;
  showAnswer = false;
  lastAnswerCorrect = false;
  isSessionComplete = false;
  answerControl = new FormControl('');

  get correctCount() {
    return this.session?.correctCount ?? 0;
  }

  get incorrectCount() {
    return this.session?.incorrectCount ?? 0;
  }

  get totalAnswered() {
    return (this.correctCount + this.incorrectCount);
  }

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private studySessionsService: StudySessionsService,
    private reviewService: ReviewService
  ) {
    console.log('FlashcardGameComponent: Constructor called');
  }

  ngOnInit() {
    console.log('FlashcardGameComponent: ngOnInit called');
    this.route.params.subscribe(params => {
      this.groupId = +params['groupId'];
      this.startNewSession();
    });
  }

  private async startNewSession() {
    console.log('FlashcardGameComponent: Starting new session for group', this.groupId);
    try {
      // Start a study session
      const studySession = await this.studySessionsService.startSession(this.groupId, 'flashcards').toPromise();
      if (!studySession) {
        throw new Error('Failed to create study session');
      }
      this.studySession = studySession;
      console.log('FlashcardGameComponent: Study session started', this.studySession);

      this.isSessionComplete = false;
      console.log('FlashcardGameComponent: Game session started', this.session);
    } catch (error) {
      console.error('FlashcardGameComponent: Error starting session:', error);
      // TODO: Show error message to user
    }
  }

  async submitAnswer() {
    if (!this.session || !this.studySession) return;

    const userAnswer = this.answerControl.value?.trim().toLowerCase() ?? '';
    const correctAnswer = this.currentItem.answer.toLowerCase();
    this.lastAnswerCorrect = userAnswer === correctAnswer;

    // Update session stats
    if (this.lastAnswerCorrect) {
      this.session.correctCount++;
    } else {
      this.session.incorrectCount++;
    }

    // Send review to backend
    try {
      await this.reviewService.createReview({
        item_type: this.currentItem.type,
        item_id: this.currentItem.id,
        study_session_id: this.studySession.id,
        correct: this.lastAnswerCorrect
      }).toPromise();
    } catch (error) {
      console.error('Error creating review:', error);
    }

    this.answerControl.reset();
  }

  nextCard() {
    if (!this.session) return;

    this.session.currentIndex++;
    if (this.session.currentIndex >= this.session.items.length) {
      this.completeSession();
    }
  }

  async completeSession() {
    if (!this.studySession) return;

    try {
      await this.studySessionsService.endSession(this.studySession.id).toPromise();
      this.isSessionComplete = true;
    } catch (error) {
      console.error('Error ending session:', error);
      // TODO: Show error message to user
    }
  }

  async endSession() {
    if (this.studySession) {
      try {
        await this.studySessionsService.endSession(this.studySession.id).toPromise();
      } catch (error) {
        console.error('Error ending session:', error);
      }
    }
    this.router.navigate(['../../'], { relativeTo: this.route });
  }

  restartSession() {
    this.startNewSession();
  }
}
