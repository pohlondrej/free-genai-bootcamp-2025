import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl } from '@angular/forms';
import { GroupsService, GroupItem } from '../../../services/groups.service';

interface FlashcardItem {
  id: number;
  type: 'word' | 'kanji';
  question: string;
  answer: string;
}

interface StudySession {
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
export class FlashcardGameComponent implements OnInit, OnDestroy {
  groupId!: number;
  session: StudySession | null = null;
  currentItem: FlashcardItem | null = null;
  showAnswer = false;
  answerControl = new FormControl('');
  lastAnswerCorrect = false;

  get totalItems(): number {
    return this.session?.items.length || 0;
  }

  get currentIndex(): number {
    return this.session?.currentIndex || 0;
  }

  get correctCount(): number {
    return this.session?.correctCount || 0;
  }

  get incorrectCount(): number {
    return this.session?.incorrectCount || 0;
  }

  get totalAnswered(): number {
    return this.correctCount + this.incorrectCount;
  }

  get isSessionComplete(): boolean {
    return this.session !== null && this.currentIndex >= this.totalItems;
  }

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private groupsService: GroupsService
  ) {
    console.log('FlashcardGameComponent: Constructor');
  }

  ngOnInit() {
    console.log('FlashcardGameComponent: OnInit');
    this.route.params.subscribe(params => {
      this.groupId = +params['groupId'];
      this.startNewSession();
    });
  }

  ngOnDestroy() {
    // TODO: Save session progress to backend
  }

  private async startNewSession() {
    console.log('FlashcardGameComponent: Starting new session for group', this.groupId);
    try {
      const response = await this.groupsService.getGroupItems(this.groupId);
      console.log('FlashcardGameComponent: Got group items', response);
      this.session = {
        id: Date.now(),
        groupId: this.groupId,
        startTime: new Date(),
        items: response.items.map((item: GroupItem) => ({
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
      console.log('FlashcardGameComponent: Session started', this.session);
    } catch (error) {
      console.error('FlashcardGameComponent: Error starting session:', error);
      // TODO: Show error message to user
    }
  }

  submitAnswer() {
    if (!this.session || !this.currentItem || this.showAnswer) return;

    const userAnswer = this.answerControl.value?.trim().toLowerCase() || '';
    const correctAnswer = this.currentItem.answer.toLowerCase();
    this.lastAnswerCorrect = userAnswer === correctAnswer;

    if (this.lastAnswerCorrect) {
      this.session.correctCount++;
    } else {
      this.session.incorrectCount++;
    }

    this.showAnswer = true;
    this.answerControl.disable();
  }

  nextCard() {
    if (!this.session) return;

    this.session.currentIndex++;
    this.showAnswer = false;
    this.answerControl.enable();
    this.answerControl.reset();

    if (this.session.currentIndex < this.session.items.length) {
      this.currentItem = this.session.items[this.session.currentIndex];
    }
  }

  restartSession() {
    this.startNewSession();
  }

  endSession() {
    this.router.navigate(['/games/flashcards']);
  }
}
