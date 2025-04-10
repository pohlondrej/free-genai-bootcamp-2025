import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl } from '@angular/forms';
import { GroupsService } from '../../../services/groups.service';
import { StudySessionsService, StudySession } from '../../../services/study-sessions.service';
import { ReviewService } from '../../../services/review.service';

interface FlashcardItem {
  id: number;
  type: string;
  question: string;
  answer: string;
}

interface GameSession {
  id: number;
  groupId: number;
  startTime: Date;
  items: FlashcardItem[];
  currentIndex: number;
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
  currentItem: FlashcardItem | null = null;
  showAnswer = false;
  lastAnswerCorrect = false;
  isSessionComplete = false;
  answerControl = new FormControl('');

  get totalItems() {
    return this.session?.items.length ?? 0;
  }

  get currentIndex() {
    return this.session?.currentIndex ?? 0;
  }

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
    private groupsService: GroupsService,
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

      // Get the group items
      const response = await this.groupsService.getGroupItems(this.groupId);
      if (!response || !response.items) {
        throw new Error('Failed to get group items');
      }
      console.log('FlashcardGameComponent: Got group items', response);

      // Initialize the game session
      this.session = {
        id: this.studySession.id,
        groupId: this.groupId,
        startTime: new Date(),
        items: response.items.map((item: any) => ({
          id: item.id,
          type: item.item_type,
          question: item.name,
          answer: item.level
        })),
        currentIndex: 0,
        correctCount: 0,
        incorrectCount: 0
      };
      this.currentItem = this.session.items[0];
      this.showAnswer = false;
      this.isSessionComplete = false;
      console.log('FlashcardGameComponent: Game session started', this.session);
    } catch (error) {
      console.error('FlashcardGameComponent: Error starting session:', error);
      // TODO: Show error message to user
    }
  }

  async submitAnswer() {
    if (!this.session || !this.currentItem || !this.studySession) return;

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

    this.showAnswer = true;
    this.answerControl.reset();
  }

  nextCard() {
    if (!this.session) return;

    this.session.currentIndex++;
    if (this.session.currentIndex >= this.session.items.length) {
      this.completeSession();
    } else {
      this.currentItem = this.session.items[this.session.currentIndex];
      this.showAnswer = false;
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
